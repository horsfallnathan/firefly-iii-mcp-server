# MCP Inspector

The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) is an essential tool for developing and debugging MCP servers. It provides a web interface to test your Firefly III MCP server interactively.

## Installation

The MCP Inspector requires Node.js and can be run with npx:

```bash
# No installation required - run directly with npx
npx @modelcontextprotocol/inspector
```

## Usage with Firefly MCP

### Basic Usage

```bash
# Start the inspector with your Firefly MCP server
npx @modelcontextprotocol/inspector uv run firefly-mcp
```

This will:
1. Start your Firefly MCP server
2. Connect the inspector to it
3. Open a web interface (usually at `http://localhost:5173`)

### With Custom Environment

```bash
# Use specific environment file
FIREFLY_API_URL=https://dev.firefly.com/api/v1 \
FIREFLY_API_TOKEN=dev_token \
npx @modelcontextprotocol/inspector uv run firefly-mcp
```

### Using Python Directly

```bash
# If you prefer not to use UV
npx @modelcontextprotocol/inspector python -m firefly_mcp.main
```

## Inspector Interface

The web interface provides several key sections:

### 🔧 Tools Tab
- **Available Tools**: Lists all MCP tools provided by your server
- **Tool Schemas**: Shows parameter requirements for each tool
- **Execute Tools**: Test tools with custom parameters

### 📊 Resources Tab  
- **Available Resources**: Shows any resources your server provides
- **Resource Content**: View resource data

### 🏠 Server Info Tab
- **Capabilities**: Server capabilities and supported features
- **Connection Status**: Real-time connection information
- **Logs**: Server communication logs

## Testing Firefly Operations

### 1. List Operations

In the Tools tab, look for:
- `firefly_list_operations` - Shows all available operations
- `firefly_get_schema` - Get parameter schema for specific operations

### 2. Test Account Operations

```json
// Tool: firefly_execute
// Parameters:
{
  "entity": "account",
  "operation": "list",
  "params": {
    "limit": 5
  }
}
```

### 3. Test Transaction Creation

```json
// Tool: firefly_execute  
// Parameters:
{
  "entity": "transaction", 
  "operation": "create",
  "params": {
    "transactions": [{
      "type": "withdrawal",
      "date": "2024-01-01T00:00:00+00:00",
      "amount": "25.50",
      "description": "Test Coffee Purchase",
      "source_name": "Checking Account",
      "destination_name": "Coffee Shop"
    }]
  }
}
```

### 4. Validate Schemas

```json
// Tool: firefly_get_schema
// Parameters:
{
  "entity": "budget",
  "operation": "create"
}
```

## Debugging Common Issues

### Connection Problems

If the inspector can't connect to your server:

1. **Check Server Startup**
   ```bash
   # Test server independently
   uv run firefly-mcp
   # Should not error immediately
   ```

2. **Verify Environment Variables**
   ```bash
   # Test API connectivity
   curl -H "Authorization: Bearer $FIREFLY_API_TOKEN" \
        "$FIREFLY_API_URL/about"
   ```

3. **Check Logs**
   - Enable debug logging: `FIREFLY_LOG_LEVEL=DEBUG`
   - Watch inspector console for error messages

### Schema Validation Errors

If tools show parameter errors:

1. **Check Required Fields**
   - Use `firefly_get_schema` to see required parameters
   - Ensure all required fields are provided

2. **Validate Data Types**
   - Strings should be quoted
   - Numbers should be unquoted
   - Arrays and objects use proper JSON syntax

3. **Test Minimal Examples**
   - Start with simple operations (like `account list`)
   - Add complexity gradually

### Performance Issues

If the inspector is slow:

1. **Limit Entity Scope**
   ```bash
   FIREFLY_ENABLED_ENTITIES=account,transaction \
   npx @modelcontextprotocol/inspector uv run firefly-mcp
   ```

2. **Reduce Data Volume**
   - Use pagination (limit/page parameters)
   - Filter by date ranges where applicable

3. **Check Network Latency**
   - Test API response times directly
   - Consider local Firefly III instance for development

## Development Workflow

### 1. Test-Driven Development

```bash
# 1. Start inspector
npx @modelcontextprotocol/inspector uv run firefly-mcp

# 2. Test operation in browser
# 3. Implement/fix code
# 4. Restart server (Ctrl+C, then restart)
# 5. Test again
```

### 2. Schema Validation

Before implementing operations:
1. Check available operations with `firefly_list_operations`
2. Get parameter schema with `firefly_get_schema`
3. Test with minimal valid parameters
4. Add complexity incrementally

### 3. Error Testing

Test error conditions:
- Invalid authentication tokens
- Missing required parameters  
- Invalid data formats
- Network connectivity issues

## Advanced Features

### Custom Server Arguments

```bash
# Pass arguments to your server
npx @modelcontextprotocol/inspector -- \
  uv run firefly-mcp --custom-arg value
```

### Multiple Server Testing

```bash
# Test with different configurations
FIREFLY_DIRECT_MODE=true \
npx @modelcontextprotocol/inspector uv run firefly-mcp
```

### Automated Testing

While the inspector is primarily interactive, you can script tests:

```bash
# Use curl to test inspector API endpoints
curl -X POST http://localhost:5173/api/tools/execute \
  -H "Content-Type: application/json" \
  -d '{"tool": "firefly_execute", "params": {...}}'
```

## Tips and Best Practices

1. **Start Simple**: Test basic operations before complex ones
2. **Use Real Data**: Test with your actual Firefly III data for realistic scenarios  
3. **Check Schemas**: Always validate parameter schemas before implementation
4. **Monitor Logs**: Watch both inspector and server logs for debugging
5. **Test Edge Cases**: Try invalid inputs, empty responses, network errors
6. **Document Examples**: Save working parameter examples for future reference

## Integration with Development

The MCP Inspector integrates well with your development workflow:

- **Before Code Changes**: Test current functionality
- **During Development**: Validate new features  
- **Before Deployment**: Ensure everything works correctly
- **Debugging**: Isolate issues to server vs client problems

This makes it an essential tool for both initial development and ongoing maintenance of your Firefly III MCP server.
