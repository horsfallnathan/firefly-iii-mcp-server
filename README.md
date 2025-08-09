# Firefly III MCP Server

A Model Context Protocol (MCP) server that provides programmatic access to [Firefly III](https://www.firefly-iii.org/) personal finance management through Claude Desktop, Cursor IDE, and other MCP-compatible AI assistants.

## Overview

This MCP server enables AI assistants to interact with your Firefly III instance, allowing you to manage your personal finances through natural language conversations. You can:

- **Manage accounts**: List, create, update, and delete asset, expense, revenue, and liability accounts
- **Handle transactions**: Create, retrieve, update, and delete financial transactions
- **Budget management**: Work with budgets, budget limits, and track spending
- **Categorization**: Manage transaction categories and tags
- **Bill tracking**: Handle recurring bills and payment monitoring
- **Piggy banks**: Manage savings goals and track progress
- **Rules & automation**: Configure transaction rules and rule groups

## Features

- **MCP Integration**: Works seamlessly with Claude Desktop, Cursor IDE, and other MCP clients
- **Comprehensive API coverage**: Supports most Firefly III v1 API endpoints
- **Flexible operation modes**: Choose between consolidated tools or direct API access
- **Type-safe operations**: Full Pydantic model validation for all requests/responses
- **Entity filtering**: Enable only the Firefly III entities you need

## Requirements

- Python 3.12+
- A running Firefly III instance
- Firefly III API token (Personal Access Token)

## Installation

### Using UV (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd firefly-mcp

# Install dependencies
uv sync

# Install in development mode
uv pip install -e .
```

### Using Pip

```bash
# Clone the repository
git clone <repository-url>
cd firefly-mcp

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Configuration

Create a `.env` file in the project root:

```bash
# Required: Your Firefly III API URL
FIREFLY_API_URL=https://your-firefly-instance.com/api/v1

# Required: Your Personal Access Token from Firefly III
FIREFLY_API_TOKEN=your_token_here

# Optional: Disable SSL verification for development (default: false)
FIREFLY_DISABLE_SSL_VERIFY=false

# Optional: Enable direct mode for individual tools (default: false)
FIREFLY_DIRECT_MODE=false

# Optional: Comma-separated list of entities to enable (default: account)
# Available: account,transaction,budget,category,tag,rule,rule_group,bill,piggy_bank
# Use "all" to enable everything
FIREFLY_ENABLED_ENTITIES=all

# Optional: Logging level (default: INFO)
FIREFLY_LOG_LEVEL=INFO
```

### Getting a Firefly III API Token

1. Log into your Firefly III instance
2. Go to **Options** → **Profile** → **OAuth**
3. Click **Create New Token**
4. Give it a descriptive name (e.g., "MCP Server")
5. Copy the generated token to your `.env` file

## Usage
### Integrating with MCP Clients

#### Claude Desktop

Add the server to your Claude Desktop configuration file:

**On macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**On Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "firefly-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/firefly-mcp",
        "run",
        "firefly-mcp"
      ],
      "env": {
        "FIREFLY_API_URL": "https://your-firefly-instance.com/api/v1",
        "FIREFLY_API_TOKEN": "your_token_here",
        "FIREFLY_ENABLED_ENTITIES": "all"
      }
    }
  }
}
```

#### VSCode/ Cursor IDE

For IDEs, add the MCP server configuration to your workspace or global settings:

```json
{
  "mcp.servers": {
    "firefly-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/firefly-mcp", 
        "run",
        "firefly-mcp"
      ],
      "env": {
        "FIREFLY_API_URL": "https://your-firefly-instance.com/api/v1",
        "FIREFLY_API_TOKEN": "your_token_here",
        "FIREFLY_ENABLED_ENTITIES": "all"
      }
    }
  }
}
```

#### Other MCP Clients

For other MCP-compatible clients, configure them to run the server with:
- **Command**: `uv run firefly-mcp` (or your preferred execution method)
- **Working Directory**: Path to this project
- **Environment Variables**: Your Firefly III configuration

### Operation Modes

#### Consolidated Mode (Default)

Provides three meta-tools for dynamic operation:

- `firefly_execute(entity, operation, params)` - Execute any Firefly III operation
- `firefly_list_operations(entity?)` - List available operations
- `firefly_get_schema(entity, operation)` - Get parameter schema for operations

#### Direct Mode

Set `FIREFLY_DIRECT_MODE=true` to register individual tools for each operation:

- `account_list(limit?, page?)` - List accounts
- `account_get(id)` - Get account details
- `transaction_create(transactions)` - Create transactions
- And many more...

### Using with AI Assistants

Once configured, you can interact with your Firefly III data through natural language in your MCP client:

#### Examples with Claude Desktop

```
"Show me my account balances"
"Create a new expense for $25.50 at Coffee Shop from my Checking Account"
"What's my budget status for this month?"
"List all my transactions from last week"
"Create a new savings goal for a vacation with a target of $2000"
"Show me all bills that are due this month"
```

#### Examples with Cursor IDE

In Cursor, you can ask the AI assistant to help manage your finances:

```
"Help me create a transaction rule that automatically categorizes Starbucks purchases as 'Coffee'"
"Show me a summary of my spending by category for the last 30 days"
"Create a new budget category for 'Home Improvement' with a $500 monthly limit"
```

### Technical Usage (Direct API calls)

For direct programmatic access, you can also use the underlying operations:

```python
# List all accounts
firefly_execute("account", "list", {"limit": 10})

# Get specific account
firefly_execute("account", "get", {"id": "123"})

# Create a new transaction
firefly_execute("transaction", "create", {
    "transactions": [{
        "type": "withdrawal",
        "date": "2024-01-01T00:00:00+00:00",
        "amount": "25.50",
        "description": "Coffee",
        "source_name": "Checking Account",
        "destination_name": "Coffee Shop"
    }]
})
```

## Development
### Using MCP Inspector

For development and debugging, use the [MCP Inspector](https://github.com/modelcontextprotocol/inspector) to test your server interactively:

```bash
# Install MCP Inspector (if not already installed)
npx @modelcontextprotocol/inspector

# Run with your Firefly MCP server
npx @modelcontextprotocol/inspector uv run firefly-mcp
```

The MCP Inspector provides a web interface where you can:
- Test all available tools and operations
- Inspect request/response schemas
- Debug server connectivity and authentication
- Validate your Firefly III configuration

### Direct Python Debugging

For direct Python debugging and development:

```bash
# Using UV (recommended)
uv run firefly-mcp

# Using the Makefile
make app

# Development with .env file
make dev

# Direct Python execution
python -m firefly_mcp.main
```

### Running Tests

```bash
# Run all tests
make test-all

# Run only unit tests
make test-unit

# Run only integration tests
make test-integration

# Run with coverage
make coverage

# Run specific tests with custom args
make test-unit ARGS="--maxfail=1 -v"
```

### Development Server

```bash
# Run with development environment
make dev

# Clean generated files
make clean
```

### Project Structure

```
firefly-mcp/
├── src/firefly_mcp/
│   ├── core/           # Core business logic for each entity
│   ├── lib/            # Shared utilities (HTTP client, exceptions)
│   ├── models/         # Pydantic models and schemas
│   ├── tools/          # MCP tool implementations
│   └── main.py         # Entry point
├── tests/              # Test suite
├── .env.example        # Environment template
└── pyproject.toml      # Project configuration
```

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `FIREFLY_API_URL` | `https://firefly.dev.nlocal/api/v1` | Your Firefly III API base URL |
| `FIREFLY_API_TOKEN` | *(required)* | Personal Access Token from Firefly III |
| `FIREFLY_DISABLE_SSL_VERIFY` | `false` | Disable SSL verification for development |
| `FIREFLY_DIRECT_MODE` | `false` | Enable individual tools for each operation |
| `FIREFLY_ENABLED_ENTITIES` | `account` | Comma-separated list of entities to enable |
| `FIREFLY_LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |

## Troubleshooting

### Connection Issues

- Verify your `FIREFLY_API_URL` is correct and accessible
- Check that your API token is valid and has appropriate permissions
- For development with self-signed certificates, set `FIREFLY_DISABLE_SSL_VERIFY=true`

### Entity Not Available

- Check that the entity is included in `FIREFLY_ENABLED_ENTITIES`
- Verify your Firefly III version supports the required API endpoints

### Operation Failures

- Use `firefly_get_schema(entity, operation)` to check required parameters
- Enable DEBUG logging with `FIREFLY_LOG_LEVEL=DEBUG` for detailed error information

## API Compatibility

This MCP server is compatible with Firefly III API v1. It has been tested with:

- Firefly III v6.x
- Firefly III v5.x (most features)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). See the [LICENSE](LICENSE) file for details.

