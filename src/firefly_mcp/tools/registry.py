"""Plugin-based tool registry for Firefly III MCP operations."""

import logging
import os
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache
from typing import Any, Callable, Dict, List, Optional, Set, Type

from fastmcp import FastMCP
from pydantic import BaseModel, ValidationError as PydanticValidationError

from firefly_mcp.lib.exceptions import EntityNotAvailableError, OperationNotFoundError, RegistryError, ValidationError

logger = logging.getLogger(__name__)


class EntityType(str, Enum):
    """Available entity types in Firefly III."""
    ACCOUNT = "account"
    TRANSACTION = "transaction"
    BUDGET = "budget"
    CATEGORY = "category"
    TAG = "tag"
    RULE = "rule"
    RULE_GROUP = "rule_group"
    BILL = "bill"
    PIGGY_BANK = "piggy_bank"


@dataclass(frozen=True)
class OperationConfig:
    """Configuration for a single operation."""
    name: str
    description: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[Any]]
    core_function: Callable[..., Any]
    tags: Set[str] = field(default_factory=set)
    
    @property
    def tool_name(self) -> str:
        """Generate MCP tool name."""
        return f"{self.name}"


@dataclass(frozen=True)
class RegistryConfig:
    """Configuration for the registry system."""
    direct_mode: bool = False
    enabled_entities: Set[EntityType] = field(default_factory=set)
    log_level: str = "INFO"
    
    @classmethod
    def from_environment(cls) -> "RegistryConfig":
        """Create configuration from environment variables."""
        return cls(
            direct_mode=_parse_bool_env("FIREFLY_DIRECT_MODE"),
            enabled_entities=_parse_entity_set_env("FIREFLY_ENABLED_ENTITIES"),
            log_level=os.getenv("FIREFLY_LOG_LEVEL", "INFO")
        )


class EntityProvider:
    """Entity provider for a single entity type."""
    
    def __init__(self, entity_type: EntityType, operations_config: Dict[str, Dict[str, Any]]):
        self.entity_type = entity_type
        self._operations: Dict[str, OperationConfig] = {}
        
        # Convert dict config to OperationConfig objects
        for name, config in operations_config.items():
            self._operations[name] = OperationConfig(
                name=name,
                description=config["description"],
                request_model=config["request_model"],
                response_model=config["response_model"],
                core_function=config["core_function"],
                tags=set(config.get("tags", []))
            )
    
    def get_operation(self, name: str) -> OperationConfig:
        """Get operation configuration by name."""
        if name not in self._operations:
            raise OperationNotFoundError(f"Operation '{name}' not found for {self.entity_type}")
        return self._operations[name]
    
    def list_operations(self) -> List[OperationConfig]:
        """List all operation configurations."""
        return list(self._operations.values())
    
    def is_available(self) -> bool:
        """Check if this provider is available/enabled."""
        return True


class SchemaConverter:
    """Converts Pydantic models to JSON schemas for MCP tools."""
    
    @staticmethod
    def to_json_schema(model: Optional[Type[Any]]) -> Dict[str, Any]:
        """Convert Pydantic model to JSON schema."""
        if model is None:
            return {"type": "object", "properties": {}}
        
        # Handle BaseModel subclasses directly
        if hasattr(model, 'model_json_schema'):
            return model.model_json_schema()
        
        # Handle generic types using TypeAdapter
        try:
            from pydantic import TypeAdapter
            adapter = TypeAdapter(model)
            return adapter.json_schema()
        except Exception as e:
            logger.warning(f"Failed to generate schema for {model}: {e}")
            return {"type": "object", "properties": {}}
    
    @staticmethod
    def validate_request(data: Any, model: Optional[Type[Any]]) -> Any:
        """Validate request data against model."""
        if model is None:
            return None
        
        try:
            # Handle BaseModel subclasses directly
            if hasattr(model, 'model_validate'):
                if isinstance(data, str):
                    return model.model_validate_json(data)
                elif isinstance(data, dict):
                    return model.model_validate(data)
                elif data is None:
                    return model()
                else:
                    return data if isinstance(data, model) else model()
            
            # Handle generic types using TypeAdapter
            else:
                from pydantic import TypeAdapter
                adapter = TypeAdapter(model)
                if isinstance(data, str):
                    return adapter.validate_json(data)
                else:
                    return adapter.validate_python(data)
                    
        except PydanticValidationError as e:
            raise ValidationError(f"Request validation failed: {e}") from e


class Registry:
    """Registry for Firefly III MCP operations."""
    
    def __init__(self, config: RegistryConfig):
        self._config = config
        self._providers: Dict[EntityType, EntityProvider] = {}
        self._converter = SchemaConverter()
        
        # Configure logging
        logging.getLogger().setLevel(self._config.log_level)
    
    @property
    def config(self) -> RegistryConfig:
        """Public access to configuration."""
        return self._config
    
    @property
    def providers(self) -> Dict[EntityType, EntityProvider]:
        """Public access to providers."""
        return self._providers.copy()
    
    @property 
    def converter(self) -> SchemaConverter:
        """Public access to schema converter."""
        return self._converter
    
    def register_provider(self, provider: EntityProvider) -> None:
        """Register an entity provider."""
        if provider.entity_type not in self._config.enabled_entities:
            logger.debug(f"Provider {provider.entity_type} not enabled, skipping")
            return
        
        if not provider.is_available():
            logger.warning(f"Provider {provider.entity_type} not available")
            return
        
        self._providers[provider.entity_type] = provider
        logger.info(f"Registered provider: {provider.entity_type}")
    
    def get_provider(self, entity_type: EntityType) -> EntityProvider:
        """Get provider for entity type."""
        if entity_type not in self._providers:
            raise EntityNotAvailableError(f"No provider for: {entity_type}")
        return self._providers[entity_type]
    
    def execute_operation(self, entity: str, operation: str, params: Any = None) -> Any:
        """Direct operation execution with validation."""
        try:
            entity_type = EntityType(entity)
            provider = self.get_provider(entity_type)
            op_config = provider.get_operation(operation)
            
            # Validate parameters
            validated_params = self._converter.validate_request(params, op_config.request_model)
            
            # Execute operation
            result: Any = op_config.core_function(validated_params)
            
            # Convert result for serialization
            return self._serialize_result(result)
            
        except (ValueError, OperationNotFoundError, EntityNotAvailableError, ValidationError):
            raise
        except Exception as e:
            logger.exception(f"Operation execution failed: {entity}.{operation}")
            raise RegistryError(f"Execution error: {e}") from e
    
    def list_operations(self, entity_type: Optional[EntityType] = None) -> List[Dict[str, Any]]:
        """List all operations, optionally filtered by entity type."""
        operations: List[Dict[str, Any]] = []
        
        providers = [self._providers[entity_type]] if entity_type else self._providers.values()
        
        for provider in providers:
            for op_config in provider.list_operations():
                operation_info: Dict[str, Any] = {
                    "name": f"{provider.entity_type.value}.{op_config.name}",
                    "entity": provider.entity_type.value,
                    "operation": op_config.name,
                    "description": op_config.description,
                    "tags": list(op_config.tags)
                }
                operations.append(operation_info)
        
        return sorted(operations, key=lambda op: str(op.get("name", "")))
    
    def get_operation_schema(self, entity: str, operation: str) -> Dict[str, Any]:
        """Get schema for a specific operation."""
        entity_type = EntityType(entity)
        provider = self.get_provider(entity_type)
        op_config = provider.get_operation(operation)
        return self._converter.to_json_schema(op_config.request_model)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        total_operations = sum(len(p.list_operations()) for p in self._providers.values())
        return {
            "providers": len(self._providers),
            "operations": total_operations,
            "entities": [entity.value for entity in self._providers.keys()],
            "config": {
                "direct_mode": self._config.direct_mode,
                "enabled_entities": [e.value for e in self._config.enabled_entities]
            }
        }
    
    def _serialize_result(self, result: Any) -> Any:
        """Convert result to serializable format."""
        if isinstance(result, BaseModel):
            return result.model_dump()
        elif hasattr(result, 'to_dict'):
            return result.to_dict()
        return result


def setup_firefly_tools(
    mcp: FastMCP,
    providers: List[EntityProvider],
    config: Optional[RegistryConfig] = None
) -> None:
    """Setup Firefly III tools with MCP server.

    
    Args:
        mcp: FastMCP server instance
        providers: List of entity providers to register
        config: Optional configuration (uses environment defaults if None)
    """
    if config is None:
        config = RegistryConfig.from_environment()
    
    # Create registry
    registry = Registry(config)
    
    # Register providers
    registered_count = 0
    for provider in providers:
        try:
            registry.register_provider(provider)
            registered_count += 1
        except Exception as e:
            logger.error(f"Failed to register provider {provider.entity_type}: {e}")
    
    logger.info(f"Successfully registered {registered_count}/{len(providers)} providers")
    
    # Register tools based on mode
    if config.direct_mode:
        _register_direct_mode_tools(mcp, registry)
        logger.info("Direct mode: registered individual tools for all operations")
    else:
        _register_consolidated_tools(mcp, registry)
        logger.info("Consolidated mode: registered meta-tools")
    
    # Log final stats
    stats = registry.get_stats()
    logger.info(f"Firefly tools setup complete: {stats}")


def _register_consolidated_tools(mcp: FastMCP, registry: Registry) -> None:
    """Register consolidated meta-tools for dynamic operation execution."""
    
    # 1. Main execution tool
    @mcp.tool(name="firefly_execute")
    def execute_firefly_operation(
        entity: str,
        operation: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Execute any Firefly III operation dynamically.
        
        Args:
            entity: Entity type (account, transaction, budget, etc.)
            operation: Operation name (list, get, create, update, delete, etc.)
            params: Operation parameters as dictionary
        """
        try:
            return registry.execute_operation(entity, operation, params)
        except Exception as e:
            logger.warning(f"Operation execution failed: {e}")
            return {"error": str(e)}
    
    # 2. Discovery tools
    @mcp.tool(name="firefly_list_operations")
    def list_available_operations(entity: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all available Firefly III operations.
        
        Args:
            entity: Optional entity filter (account, transaction, etc.)
        """
        try:
            entity_type = EntityType(entity) if entity else None
            return registry.list_operations(entity_type)
        except Exception as e:
            logger.error(f"Failed to list operations: {e}")
            return [{"error": str(e)}]
    
    @mcp.tool(name="firefly_get_schema")
    def get_operation_schema(entity: str, operation: str) -> Dict[str, Any]:
        """Get parameter schema for a specific operation.
        
        Args:
            entity: Entity type (account, transaction, etc.)
            operation: Operation name (list, get, etc.)
        """
        try:
            return registry.get_operation_schema(entity, operation)
        except Exception as e:
            logger.warning(f"Schema request failed: {e}")
            return {"error": str(e)}


def _register_direct_mode_tools(mcp: FastMCP, registry: Registry) -> None:
    """Register individual tools for ALL operations (direct mode)."""
    
    tools_registered = 0
    providers = registry.providers
    
    for provider in providers.values():
        for op_config in provider.list_operations():
            entity = provider.entity_type.value
            operation = op_config.name
            
            try:
                # Create tool name
                tool_name = f"{entity}_{operation}"
                
                # Get parameter schema
                converter = registry.converter
                parameters_schema = converter.to_json_schema(op_config.request_model)
                
                # Create execution wrapper
                def make_wrapper(entity_val: str, operation_val: str):
                    def wrapper(**kwargs: Any) -> Any:
                        return registry.execute_operation(entity_val, operation_val, kwargs if kwargs else None)
                    return wrapper
                
                # Register as function tool
                from fastmcp.tools import FunctionTool
                tool = FunctionTool(
                    name=tool_name,
                    fn=make_wrapper(entity, operation),
                    parameters=parameters_schema,
                    description=op_config.description,
                    tags=op_config.tags
                )
                
                mcp.add_tool(tool)
                logger.debug(f"Registered direct tool: {tool_name}")
                tools_registered += 1
                
            except Exception as e:
                logger.warning(f"Failed to register direct tool {entity}.{operation}: {e}")
    
    logger.info(f"Direct mode: registered {tools_registered} individual tools")


def create_provider_from_config(entity_type: EntityType, operations_config: Dict[str, Dict[str, Any]]) -> EntityProvider:
    """Factory function to create providers from configuration."""
    return EntityProvider(entity_type, operations_config)

# Utility functions
def _parse_bool_env(key: str, default: bool = False) -> bool:
    """Parse boolean from environment variable."""
    value = os.getenv(key, "").lower()
    return value in ("true", "1", "yes", "on") if value else default


@lru_cache(maxsize=1)
def _parse_entity_set_env(key: str) -> Set[EntityType]:
    """Parse set of entities from environment variable."""
    raw_value = os.getenv(key, "").strip()
    
    if not raw_value:
        return {EntityType.ACCOUNT}  # Sensible default
    
    entity_names = [name.strip().lower() for name in raw_value.split(",")]
    
    # Handle special "all" case
    if "all" in entity_names:
        return set(EntityType)
    
    # Parse individual entities
    entities: Set[EntityType] = set()
    for name in entity_names:
        try:
            entities.add(EntityType(name))
        except ValueError:
            logger.warning(f"Unknown entity type '{name}' in {key}, skipping")
    
    return entities or {EntityType.ACCOUNT}
