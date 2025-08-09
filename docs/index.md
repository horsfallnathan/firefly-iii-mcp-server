# Firefly III MCP Server

A Model Context Protocol (MCP) server that provides programmatic access to [Firefly III](https://www.firefly-iii.org/) personal finance management through Claude Desktop, Cursor IDE, and other MCP-compatible AI assistants.

## What is MCP?

The Model Context Protocol (MCP) is an open standard for connecting AI assistants to external data sources and tools. This server makes your Firefly III financial data accessible to AI assistants for natural language financial management.

## Key Features

- **🤖 AI Integration**: Works seamlessly with Claude Desktop, Cursor IDE, and other MCP clients
- **💰 Comprehensive Finance**: Supports accounts, transactions, budgets, categories, tags, bills, and savings goals
- **🔒 Type-Safe**: Full Pydantic model validation for all requests and responses
- **⚡ Flexible**: Choose between consolidated tools or direct API access
- **🎯 Configurable**: Enable only the Firefly III entities you need

## Quick Example

Once set up, you can interact with your finances naturally:

!!! example "Natural Language Finance Management"

    === "Querying Information"

        ```
        "Show me my account balances"
        "Create a new expense for $25.50 at Coffee Shop from my Checking Account"
        "Show me a summary of my spending by category for the last 30 days"
        "What's my budget status for this month?"
        "List all my transactions from last week"
        ```

    === "Creating Entries"

        ```
        "Help me create a transaction rule that automatically categorizes Starbucks purchases as 'Coffee'"
        "Create a new budget category for 'Home Improvement' with a $500 monthly limit"
        ```

## Getting Started

1. **[Quickstart](quickstart.md)** the MCP server
2. **[Configure](configuration.md)** your Firefly III connection
3. **[Integrate](integrations.md)** with your preferred MCP client
4. Start managing your finances with AI!

## Available Operations

| Entity | Description | Operations |
|--------|-------------|------------|
| **Accounts** | Asset, expense, revenue, and liability accounts | list, get, create, update, delete, list_transactions, list_attachments, list_piggy_banks |
| **Transactions** | Financial transactions and transfers | list, get, create, update, delete, list_attachments |
| **Budgets** | Budget management and spending limits | list, get, create, update, delete, list_limits, create_limit, get_limit, update_limit, delete_limit, list_transactions, list_attachments |
| **Categories** | Transaction categorization | list, get, create, update, delete, list_transactions, list_attachments |
| **Tags** | Transaction tagging | list, get, create, update, delete, list_transactions, list_attachments |
| **Bills** | Recurring bills and payments | list, get, create, update, delete, list_transactions, list_attachments, list_rules |
| **Piggy Banks** | Savings goals and targets | list, get, create, update, delete, list_events, list_attachments |
| **Rules** | Transaction automation rules | list, get, create, update, delete, test, trigger |
| **Rule Groups** | Rule organization and management | list, get, create, update, delete, list_rules, test, trigger |

## Requirements

- Python 3.12+
- A running Firefly III instance
- Firefly III API token (Personal Access Token)
- MCP-compatible client (Claude Desktop, Cursor IDE, etc.)

## Support

- 📖 [Documentation](https://horsfallnathan.github.io/firefly-iii-mcp-server/)
- 🐛 [Issues](https://github.com/horsfallnathan/firefly-iii-mcp-server/issues)
- 💬 Use github issues for discussion and support
