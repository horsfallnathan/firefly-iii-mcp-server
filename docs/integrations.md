# MCP Client Integrations

This page shows how to configure the Firefly III MCP server with popular MCP clients.

## Claude Desktop

**Configuration file location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

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

## VSCode

Create an `mcp.json` file in your project root or workspace:

```json
{
  "servers": {
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
        "FIREFLY_ENABLED_ENTITIES": "all",
        "FIREFLY_DIRECT_MODE": "false"
      }
    }
  }
}
```

## Cursor IDE

Add to your workspace or global settings:

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
        "FIREFLY_ENABLED_ENTITIES": "all",
        "FIREFLY_DIRECT_MODE": "false"
      }
    }
  }
}
```

## Generic MCP Clients

Most MCP clients follow a similar pattern. Configure with:

- **Command**: `uv run firefly-mcp` (or `python -m firefly_mcp.main`)
- **Working Directory**: Path to your firefly-mcp project
- **Environment Variables**: Your Firefly III configuration

## Alternative: Direct Python

If you prefer not to use UV:

```json
{
  "command": "python",
  "args": ["-m", "firefly_mcp.main"],
  "cwd": "/path/to/firefly-mcp",
  "env": {
    "FIREFLY_API_URL": "https://your-firefly-instance.com/api/v1",
    "FIREFLY_API_TOKEN": "your_token_here",
    "FIREFLY_ENABLED_ENTITIES": "all",
    "FIREFLY_DIRECT_MODE": "false"
  }
}
```

## Common Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `FIREFLY_API_URL` | Your Firefly III API URL | `https://firefly.example.com/api/v1` |
| `FIREFLY_API_TOKEN` | Personal Access Token | `your_token_here` |
| `FIREFLY_ENABLED_ENTITIES` | Which entities to enable | `all` or `account,transaction,budget` |
| `FIREFLY_DIRECT_MODE` | Use individual tools vs consolidated | `false` (default) |
| `FIREFLY_LOG_LEVEL` | Logging verbosity | `INFO` (default) |

## Verification

After configuration:

1. Restart your MCP client
2. Look for the 🔌 icon (Claude) or MCP tools availability
3. Test with: "Show me my Firefly III accounts"

## Troubleshooting

- **Server not found**: Check the path is absolute and correct
- **No tools available**: Verify JSON syntax and restart client
- **Connection errors**: Validate API URL and token with `curl`
- **SSL issues**: Add `"FIREFLY_DISABLE_SSL_VERIFY": "true"` for development
