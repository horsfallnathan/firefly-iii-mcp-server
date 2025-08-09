# Configuration

## Environment Variables

Create a `.env` file in the project root with your Firefly III configuration:

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

## Getting a Firefly III API Token

1. Log into your Firefly III instance
2. Go to **Options** → **Profile** → **OAuth**
3. Click **Create New Token**
4. Give it a descriptive name (e.g., "MCP Server")
5. Copy the generated token to your `.env` file

!!! warning "Security"
    Never commit your `.env` file or API tokens to version control. The `.env` file is already included in `.gitignore`.

## Configuration Options

### API Connection

| Variable | Default | Description |
|----------|---------|-------------|
| `FIREFLY_API_URL` | `https://firefly.dev.nlocal/api/v1` | Your Firefly III API base URL |
| `FIREFLY_API_TOKEN` | *(required)* | Personal Access Token from Firefly III |
| `FIREFLY_DISABLE_SSL_VERIFY` | `false` | Disable SSL verification for development |

### Operation Mode

| Variable | Default | Description |
|----------|---------|-------------|
| `FIREFLY_DIRECT_MODE` | `false` | Enable individual tools for each operation vs consolidated tools |

#### Consolidated Mode (Default)
- Provides 3 meta-tools: `firefly_execute`, `firefly_list_operations`, `firefly_get_schema`
- More flexible for AI assistants
- Easier to manage

#### Direct Mode
- Creates individual tools for each operation (e.g., `account_list`, `transaction_create`)
- More explicit tool names
- Better for specific automations

### Entity Filtering

| Variable | Default | Description |
|----------|---------|-------------|
| `FIREFLY_ENABLED_ENTITIES` | `account` | Which Firefly III entities to enable |

Available entities:
- `account` - Asset, expense, revenue, and liability accounts
- `transaction` - Financial transactions and transfers
- `budget` - Budget management and spending limits
- `category` - Transaction categorization
- `tag` - Transaction tagging
- `bill` - Recurring bills and payments
- `piggy_bank` - Savings goals and targets
- `rule` - Transaction automation rules
- `rule_group` - Rule organization and management

Examples:
```bash
# Enable only accounts and transactions
FIREFLY_ENABLED_ENTITIES=account,transaction

# Enable everything
FIREFLY_ENABLED_ENTITIES=all

# Enable budgeting features only
FIREFLY_ENABLED_ENTITIES=account,budget,category,tag
```

### Logging

| Variable | Default | Description |
|----------|---------|-------------|
| `FIREFLY_LOG_LEVEL` | `INFO` | Logging verbosity |

Available levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`

## Validation

Test your configuration:

```bash
# Test API connectivity
uv run python -c "
from firefly_mcp.lib.http_client import client
response = client.get('/about')
print('✅ Connected to Firefly III' if response.status_code == 200 else '❌ Connection failed')
"

# Test with MCP Inspector
npx @modelcontextprotocol/inspector uv run firefly-mcp
```

## Environment-Specific Configuration

### Development

Create `.env.dev`:
```bash
FIREFLY_API_URL=http://localhost:8080/api/v1
FIREFLY_API_TOKEN=your_dev_token
FIREFLY_DISABLE_SSL_VERIFY=true
FIREFLY_LOG_LEVEL=DEBUG
FIREFLY_ENABLED_ENTITIES=all
```

### Production

Create `.env.prod`:
```bash
FIREFLY_API_URL=https://firefly.example.com/api/v1
FIREFLY_API_TOKEN=your_prod_token
FIREFLY_DISABLE_SSL_VERIFY=false
FIREFLY_LOG_LEVEL=INFO
FIREFLY_ENABLED_ENTITIES=account,transaction,budget,category
```

## Next Steps

1. **[Quick Start](quickstart.md)** - Test your configuration
2. **[MCP Integration](integrations.md)** - Set up with your preferred client
