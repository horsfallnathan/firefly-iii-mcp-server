from __future__ import annotations

from typing import Any, Dict, cast

import httpx


class FireflyAPIError(Exception):
    """Exception raised for HTTP responses returned by the Firefly API.

    This error surfaces the *actual* message returned by Firefly so that it can
    be consumed further up the stack (e.g. by an LLM).
    """

    status_code: int
    errors: Dict[str, Any] | None

    def __init__(self, status_code: int, message: str, errors: Dict[str, Any] | None = None) -> None:
        self.status_code = status_code
        self.errors = errors or {}
        super().__init__(f"{status_code} – {message}")

    @classmethod
    def from_response(cls, response: httpx.Response) -> "FireflyAPIError":
        """Create an instance from an *error* ``httpx.Response`` object."""
        try:
            raw_payload = response.json()
            payload = cast(Dict[str, Any], raw_payload) if isinstance(raw_payload, dict) else {}
        except ValueError:
            payload = {}

        message: str = "Unknown error"
        errors: Dict[str, Any] | None = None
        
        if payload:
            message_value = payload.get("message")
            if message_value is not None:
                message = str(message_value)
            
            errors_value = payload.get("errors")
            if isinstance(errors_value, dict):
                errors = cast(Dict[str, Any], errors_value)
        
        if message == "Unknown error" and response.text:
            message = str(response.text)
            
        return cls(response.status_code, message, errors)

class MissingOperationSchemaError(KeyError):
    """Exception raised when a requested operation schema is missing."""
    pass

def raise_api_error_if_any(response: httpx.Response) -> httpx.Response:
    """Mimic ``response.raise_for_status`` but surface Firefly error messages.

    On success simply returns the *response* unchanged so callers can chain
    operations like ``raise_api_error_if_any(response).json()``.
    """
    if response.is_error:
        raise FireflyAPIError.from_response(response)
    return response 

class FireflyMCPServerError(Exception):
    """Base exception for registry errors."""
    pass

class RegistryError(FireflyMCPServerError):
    """Raised when there is an error in the registry."""
    pass


class EntityNotAvailableError(FireflyMCPServerError):
    """Raised when an entity provider is not available."""
    pass


class OperationNotFoundError(FireflyMCPServerError):
    """Raised when an operation is not found."""
    pass


class ValidationError(FireflyMCPServerError):
    """Raised when parameter validation fails."""
    pass
    