# Quick Start

Get your Firefly III MCP server running in minutes!

## Prerequisites

- ✅ Python 3.12+
- ✅ Running Firefly III instance
- ✅ Firefly III Personal Access Token
- ✅ MCP Client, eg. Claude Desktop or AI-configured IDE

## 5-Minute Setup

### 1. Local Installation

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

### 2. Configuration

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

### 3. Test the Server (Optional)

    ```bash
    # Quick test
    uv run firefly-mcp --help

    # Interactive test with MCP Inspector
    npx @modelcontextprotocol/inspector uv run firefly-mcp
    ```

### 4. Configure Your MCP Client

=== "Cursor IDE"

    Add to workspace or global settings:

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

=== "VSCode"

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

### 5. Start Using It!

Restart your MCP client and try:

```
"Show me all my Firefly III accounts"
"What's my budget status this month?"
"Create a new expense for $50 lunch from my checking account"
```

## First Commands to Try

### Account Information
- "List all my accounts"
- "Show me my checking account balance"
- "What are my asset accounts?"

### Recent Activity
- "Show me my last 10 transactions"
- "What did I spend money on yesterday?"
- "List all income from this month"

### Budget Overview
- "What's my budget status?"
- "How much have I spent on groceries this month?"
- "Show me my budget categories"

### Quick Entry
- "Create a new expense for $25 at Starbucks from my checking account"
- "Add a $500 income from salary to my checking account"

## Troubleshooting Quick Fixes

### ❌ "Connection failed"
```bash
# Check your API URL and token
curl -H "Authorization: Bearer YOUR_TOKEN" \
     "https://your-firefly-instance.com/api/v1/about"
```

### ❌ "No tools available"
1. Restart your MCP client
2. Check JSON configuration syntax
3. Verify file paths are absolute

### ❌ "Server not starting"
```bash
# Check dependencies
uv sync

# Check Python version
python --version  # Should be 3.12+

# Test directly
uv run python -m firefly_mcp.main
```

### ❌ "SSL/Certificate errors"
Add to your `.env`:
```bash
FIREFLY_DISABLE_SSL_VERIFY=true
```

## What's Next?

- 🔧 [Configuration Guide](configuration.md)
- 🎯 [Available Operations Reference](api/operations.md)
