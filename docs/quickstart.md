# Quick Start

Get your Firefly III MCP server running in minutes!

## Prerequisites

- ✅ Python 3.12+
- ✅ Running Firefly III instance
- ✅ Firefly III Personal Access Token
- ✅ Claude Desktop or Cursor IDE

## 5-Minute Setup

### 1. Choose Your Setup Method

=== "Direct from GitHub (Easiest)"

    No local setup required! Skip to step 3 and use this configuration:
    
    ```json
    {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/horsfallnathan/firefly-iii-mcp-server.git", "firefly-mcp"]
    }
    ```

=== "Local Development"

    ```bash
    # Clone and setup
    git clone https://github.com/horsfallnathan/firefly-iii-mcp-server.git
    cd firefly-mcp
    uv sync
    ```

### 2. Configure Your Connection

=== "Direct from GitHub"

    Configuration is done directly in your MCP client config (step 4). No `.env` file needed!

=== "Local Development"

    Create `.env` file:

    ```bash
    # Copy the example
    cp .env.example .env

    # Edit with your details
    FIREFLY_API_URL=https://your-firefly-instance.com/api/v1
    FIREFLY_API_TOKEN=your_token_here
    FIREFLY_ENABLED_ENTITIES=all
    ```

### 3. Test the Server (Optional)

=== "Direct from GitHub"

    ```bash
    # Test with MCP Inspector
    npx @modelcontextprotocol/inspector uvx --from git+https://github.com/horsfallnathan/firefly-iii-mcp-server.git firefly-mcp
    ```

=== "Local Development"

    ```bash
    # Quick test
    uv run firefly-mcp --help

    # Interactive test with MCP Inspector
    npx @modelcontextprotocol/inspector uv run firefly-mcp
    ```

### 4. Configure Your MCP Client

=== "Claude Desktop"

    Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

    === "Direct from GitHub"

        ```json
        {
          "mcpServers": {
            "firefly-mcp": {
              "command": "uvx",
              "args": ["--from", "git+https://github.com/horsfallnathan/firefly-iii-mcp-server.git", "firefly-mcp"],
              "env": {
                "FIREFLY_API_URL": "https://your-firefly-instance.com/api/v1",
                "FIREFLY_API_TOKEN": "your_token_here",
                "FIREFLY_ENABLED_ENTITIES": "all"
              }
            }
          }
        }
        ```

    === "Local Development"

        ```json
        {
          "mcpServers": {
            "firefly-mcp": {
              "command": "uv",
              "args": ["--directory", "/absolute/path/to/firefly-mcp", "run", "firefly-mcp"],
              "env": {
                "FIREFLY_API_URL": "https://your-firefly-instance.com/api/v1",
                "FIREFLY_API_TOKEN": "your_token_here",
                "FIREFLY_ENABLED_ENTITIES": "all"
              }
            }
          }
        }
        ```

=== "Cursor IDE"

    Add to workspace/global settings:

    === "Direct from GitHub"

        ```json
        {
          "mcp.servers": {
            "firefly-mcp": {
              "command": "uvx",
              "args": ["--from", "git+https://github.com/horsfallnathan/firefly-iii-mcp-server.git", "firefly-mcp"],
              "env": {
                "FIREFLY_API_URL": "https://your-firefly-instance.com/api/v1",
                "FIREFLY_API_TOKEN": "your_token_here",
                "FIREFLY_ENABLED_ENTITIES": "all"
              }
            }
          }
        }
        ```

    === "Local Development"

        ```json
        {
          "mcp.servers": {
            "firefly-mcp": {
              "command": "uv",
              "args": ["--directory", "/absolute/path/to/firefly-mcp", "run", "firefly-mcp"],
              "env": {
                "FIREFLY_API_URL": "https://your-firefly-instance.com/api/v1",
                "FIREFLY_API_TOKEN": "your_token_here",
                "FIREFLY_ENABLED_ENTITIES": "all"
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

- 📚 [Complete Setup Guide](setup.md)
- 🔧 [Configuration Guide](configuration.md)
- 🎯 [Available Operations Reference](api/operations.md)
