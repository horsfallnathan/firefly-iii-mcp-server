# Setup

## Requirements

- Python 3.12 or higher (only for local setup)
- A running Firefly III instance
- Firefly III Personal Access Token
- MCP-compatible client (Claude Desktop, Cursor IDE, etc.)

## Setup Methods

Choose the method that works best for your workflow:

### Option 1: Direct from GitHub (Recommended)

!!! tip "No Local Setup Required"
    Your MCP client can run the server directly from GitHub - no cloning or local Python setup needed!

Configure your MCP client to run the server directly from the repository:

=== "Claude Desktop"

    Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

=== "Cursor IDE"

    Add to workspace/global settings:

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

### Option 2: Local Development Setup

For development, testing, or customization, you can set up the code locally:

=== "Using UV (Recommended)"

    ```bash
    # Clone the repository
    git clone https://github.com/horsfallnathan/firefly-iii-mcp-server.git
    cd firefly-mcp

    # Install dependencies
    uv sync
    ```

    Then configure your MCP client to use the local version:

    ```json
    {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/firefly-mcp", "run", "firefly-mcp"]
    }
    ```

=== "Using Pip"

    ```bash
    # Clone the repository
    git clone https://github.com/horsfallnathan/firefly-iii-mcp-server.git
    cd firefly-mcp

    # Create virtual environment
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate

    # Install dependencies
    pip install -e .
    ```

    Then configure your MCP client to use the local version:

    ```json
    {
      "command": "/absolute/path/to/firefly-mcp/.venv/bin/python",
      "args": ["-m", "firefly_mcp.main"]
    }
    ```

### Option 3: MCP Registry (Future)

!!! note "Coming Soon"
    We plan to publish this server to an MCP registry for even easier installation:
    ```json
    {
      "mcpServers": {
        "firefly-mcp": {
          "source": "registry://firefly-mcp"
        }
      }
    }
    ```

## Verification

=== "Direct from GitHub"

    Test the GitHub setup using MCP Inspector:

    ```bash
    # Test with MCP Inspector (requires Node.js)
    npx @modelcontextprotocol/inspector uvx --from git+https://github.com/horsfallnathan/firefly-iii-mcp-server.git firefly-mcp
    ```

=== "Local Setup"

    Test your local setup:

    ```bash
    # Check if the server can start
    uv run firefly-mcp --help

    # Test with MCP Inspector (requires Node.js)
    npx @modelcontextprotocol/inspector uv run firefly-mcp
    ```

## Next Steps

1. **[Configure](configuration.md)** your Firefly III connection
2. **[Set up MCP integration](integrations.md)** with your preferred client
3. **[Quick start guide](quickstart.md)** to get running immediately

## Troubleshooting

### Python Version Issues

Ensure you're using Python 3.12+:

```bash
python --version
# Should show Python 3.12.x or higher
```

### Dependency Conflicts

If you encounter dependency issues, try:

```bash
# With UV
uv sync --reinstall

# With pip
pip install -e . --force-reinstall
```

### Virtual Environment Issues

Make sure you're in the correct virtual environment:

```bash
# Check which Python you're using
which python

# Should point to your virtual environment
```
