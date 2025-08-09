# Firefly III MCP Server

A Model Context Protocol (MCP) server that provides programmatic access to [Firefly III](https://www.firefly-iii.org/) personal finance management through Claude Desktop, Cursor IDE, and other MCP-compatible AI assistants.

## 📚 Documentation

**📖 [Full Documentation](https://horsfallnathan.github.io/firefly-iii-mcp-server/)**

## Overview

This MCP server enables AI assistants to interact with your Firefly III instance, allowing you to manage your personal finances through natural language conversations. You can:

- **💰 Manage accounts**: List, create, update, and delete asset, expense, revenue, and liability accounts
- **📊 Handle transactions**: Create, retrieve, update, and delete financial transactions
- **💳 Budget management**: Work with budgets, budget limits, and track spending
- **🏷️ Categorization**: Manage transaction categories and tags
- **💸 Bill tracking**: Handle recurring bills and payment monitoring
- **🐷 Piggy banks**: Manage savings goals and track progress
- **⚙️ Rules & automation**: Configure transaction rules and rule groups

## Key Features

- **🤖 AI Integration**: Works seamlessly with Claude Desktop, Cursor IDE, and other MCP clients
- **💡 Comprehensive API**: Supports most Firefly III v1 API endpoints
- **⚡ Flexible modes**: Choose between consolidated tools or direct API access
- **🔒 Type-safe**: Full Pydantic model validation for all requests/responses
- **🎯 Configurable**: Enable only the Firefly III entities you need

## Quick Example

Once set up, you can interact with your finances naturally:

```
"Show me my account balances"
"Create a new expense for $25.50 at Coffee Shop from my Checking Account"
"What's my budget status for this month?"
"List all my transactions from last week"
"Create a new savings goal for a vacation with a target of $2000"
"Show me all bills that are due this month"
"Help me create a transaction rule that automatically categorizes Starbucks purchases as 'Coffee'"
"Create a new budget category for 'Home Improvement' with a $500 monthly limit"
```

## Requirements

- Python 3.12+
- A running Firefly III instance
- Firefly III API token (Personal Access Token)

## 🚀 Quick Setup

### Local Installation

Clone and set up the project locally:

```bash
# Clone the repository
git clone https://github.com/horsfallnathan/firefly-iii-mcp-server.git firefly-mcp
cd firefly-mcp

# Install with UV (recommended)
uv sync

# Or with pip
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### Configuration

Create a `.env` file in the project root:

```bash
# Required: Your Firefly III API URL and token
FIREFLY_API_URL=https://your-firefly-instance.com/api/v1
FIREFLY_API_TOKEN=your_token_here

# Optional: Enable all entities (default: just accounts). Requires `FIREFLY_DIRECT_MODE=true`
# Enabling all entities would lead to about 76 tools being registered and most clients suggest a maximum of 40 tools
FIREFLY_ENABLED_ENTITIES=all

# When false, the server will register consolidated tools for dynamic operation. When true, it will register individual tools for each operation
FIREFLY_DIRECT_MODE=false

FIREFLY_LOG_LEVEL=INFO
```

**🔑 Getting a Firefly III API Token:**
1. Log into your Firefly III instance
2. Go to **Options** → **Profile** → **OAuth**
3. Click **Create New Token**
4. Give it a descriptive name (e.g., "MCP Server")
5. Copy the generated token to your `.env` file

**📖 [See full configuration guide](https://horsfallnathan.github.io/firefly-iii-mcp-server/configuration/)**

## 🔌 MCP Client Integration

### Cursor IDE

Add to your workspace or global settings:

```json
{
  "mcp.servers": {
    "firefly-mcp": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/firefly-mcp", "run", "firefly-mcp"],
      "env": {
        "FIREFLY_API_URL": "https://your-firefly-instance.com/api/v1",
        "FIREFLY_API_TOKEN": "your_token_here",
        "FIREFLY_ENABLED_ENTITIES": "all",
        "FIREFLY_DIRECT_MODE": "false"
      }
    }
  }
}
```

### VSCode

Create an `mcp.json` file in your project root or workspace:

```json
{
  "servers": {
    "firefly-mcp": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/firefly-mcp", "run", "firefly-mcp"],
      "env": {
        "FIREFLY_API_URL": "https://your-firefly-instance.com/api/v1",
        "FIREFLY_API_TOKEN": "your_token_here",
        "FIREFLY_ENABLED_ENTITIES": "all",
        "FIREFLY_DIRECT_MODE": "false"
      }
    }
  }
}
```
## Operation Modes

### Consolidated Mode (Default)
Provides three meta-tools for dynamic operation:
- `firefly_execute(entity, operation, params)` - Execute any Firefly III operation
- `firefly_list_operations(entity?)` - List available operations  
- `firefly_get_schema(entity, operation)` - Get parameter schema for operations

### Direct Mode
Set `FIREFLY_DIRECT_MODE=true` to register individual tools for each operation:
- `account_list(limit?, page?)` - List accounts
- `account_get(id)` - Get account details
- `transaction_create(transactions)` - Create transactions
- And many more...

## 🛠️ Development & Testing

### Using MCP Inspector

For development and debugging, use the [MCP Inspector](https://github.com/modelcontextprotocol/inspector):

```bash
# Install and run MCP Inspector
npx @modelcontextprotocol/inspector uv run firefly-mcp
```

The MCP Inspector provides a web interface where you can:
- 🧪 Test all available tools and operations
- 🔍 Inspect request/response schemas  
- 🐛 Debug server connectivity and authentication
- ✅ Validate your Firefly III configuration

**📖 [See full development guide](https://horsfallnathan.github.io/firefly-iii-mcp-server/development/mcp-inspector/)**

### Running Tests

```bash
# Run all tests
make test-all

# Run with coverage
make coverage

# Run specific test types
make test-unit
make test-integration
```

### Local Development

```bash
# Development with .env file
make dev

# Direct execution
uv run firefly-mcp
python -m firefly_mcp.main
```

## 📋 Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `FIREFLY_API_URL` | `https://firefly.dev.nlocal/api/v1` | Your Firefly III API base URL |
| `FIREFLY_API_TOKEN` | *(required)* | Personal Access Token from Firefly III |
| `FIREFLY_DISABLE_SSL_VERIFY` | `false` | Disable SSL verification for development |
| `FIREFLY_DIRECT_MODE` | `false` | Enable individual tools for each operation |
| `FIREFLY_ENABLED_ENTITIES` | `account` | Comma-separated list of entities to enable |
| `FIREFLY_LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |


## 🎯 API Compatibility

This MCP server is compatible with Firefly III API v1. It has been tested with:
- ✅ Firefly III v6.x

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). See the [LICENSE](LICENSE) file for details.

