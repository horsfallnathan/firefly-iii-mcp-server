# Installation

## Requirements

- Python 3.12 or higher
- A running Firefly III instance
- Firefly III Personal Access Token

## Installation Methods

### Using UV (Recommended)

[UV](https://docs.astral.sh/uv/) is the fastest way to install and manage Python projects:

```bash
# Clone the repository
git clone https://github.com/yourusername/firefly-mcp.git
cd firefly-mcp

# Install dependencies
uv sync

# Install in development mode
uv pip install -e .
```

### Using Pip

```bash
# Clone the repository
git clone https://github.com/yourusername/firefly-mcp.git
cd firefly-mcp

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

### From PyPI (Future)

!!! note "Coming Soon"
    PyPI package installation will be available in a future release:
    ```bash
    pip install firefly-mcp
    ```

## Verification

Test your installation:

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
