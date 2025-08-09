# Available Operations

This page documents all the operations available through the Firefly III MCP server. These operations allow you to interact with your Firefly III instance through MCP-compatible clients like Claude Desktop and Cursor IDE.

## Account Operations

### List Accounts
**Function:** `mcp_firefly-mcp_account_list`

List all accounts with optional filtering by type and pagination.

**Parameters:**
- `type` (optional): Filter by account type (asset, cash, expense, revenue, etc.)
- `limit` (optional): Number of accounts per page
- `page` (optional): Page number for pagination
- `date` (optional): Balance date in ISO format (YYYY-MM-DD)

**Example Usage:**
```
"Show me all my asset accounts"
"List my checking accounts with current balances"
```

### Get Account Details
**Function:** `mcp_firefly-mcp_account_get`

Get detailed information about a specific account by ID.

**Parameters:**
- `id` (required): Account ID
- `date` (optional): Date for balance calculation

### Create Account
**Function:** `mcp_firefly-mcp_account_create`

Create a new account in Firefly III.

**Parameters:**
- `name` (required): Account name
- `type` (required): Account type (asset, expense, revenue, etc.)
- `account_role` (optional): Role for asset accounts
- `currency_code` (optional): Currency code (e.g., USD, EUR)
- `opening_balance` (optional): Initial balance
- Additional optional parameters for IBAN, notes, etc.

### Update Account
**Function:** `mcp_firefly-mcp_account_update`

Update an existing account's details.

### Delete Account
**Function:** `mcp_firefly-mcp_account_delete`

Delete an account by ID.

### Account Transactions
**Function:** `mcp_firefly-mcp_account_list_transactions`

List all transactions for a specific account.

**Parameters:**
- `id` (required): Account ID
- `start` (optional): Start date (YYYY-MM-DD)
- `end` (optional): End date (YYYY-MM-DD)
- `type` (optional): Transaction type filter
- `limit` (optional): Number of transactions per page
- `page` (optional): Page number

## Budget Operations

### List Budgets
**Function:** `mcp_firefly-mcp_budget_list`

List all budgets with optional spending information.

**Parameters:**
- `start` (optional): Start date for spending info
- `end` (optional): End date for spending info
- `limit` (optional): Number of budgets per page
- `page` (optional): Page number

### Get Budget Details
**Function:** `mcp_firefly-mcp_budget_get`

Get detailed information about a specific budget.

### Create Budget
**Function:** `mcp_firefly-mcp_budget_create`

Create a new budget.

**Parameters:**
- `name` (required): Budget name
- `auto_budget_type` (optional): Auto-budget type (reset, rollover, none)
- `auto_budget_amount` (optional): Auto-budget amount
- `auto_budget_period` (optional): Auto-budget period

### Update Budget
**Function:** `mcp_firefly-mcp_budget_update`

Update an existing budget.

### Delete Budget
**Function:** `mcp_firefly-mcp_budget_delete`

Delete a budget by ID.

### Budget Limits
**Function:** `mcp_firefly-mcp_budget_list_limits`

List budget limits for a specific budget.

### Budget Transactions
**Function:** `mcp_firefly-mcp_budget_list_transactions`

List transactions associated with a budget.

## Bill Operations

### List Bills
**Function:** `mcp_firefly-mcp_bill_list`

List all bills with optional date range for payment calculations.

### Get Bill Details
**Function:** `mcp_firefly-mcp_bill_get`

Get detailed information about a specific bill.

### Create Bill
**Function:** `mcp_firefly-mcp_bill_create`

Create a new recurring bill.

**Parameters:**
- `name` (required): Bill name
- `amount_min` (required): Minimum amount
- `amount_max` (required): Maximum amount
- `date` (required): Bill date
- `repeat_freq` (required): Repeat frequency (weekly, monthly, quarterly, etc.)

### Update Bill
**Function:** `mcp_firefly-mcp_bill_update`

Update an existing bill.

### Delete Bill
**Function:** `mcp_firefly-mcp_bill_delete`

Delete a bill by ID.

## Category Operations

### List Categories
**Function:** `mcp_firefly-mcp_category_list`

List all categories with optional pagination.

### Get Category Details
**Function:** `mcp_firefly-mcp_category_get`

Get detailed information about a specific category.

### Create Category
**Function:** `mcp_firefly-mcp_category_create`

Create a new category.

**Parameters:**
- `name` (required): Category name
- `notes` (optional): Category notes

### Update Category
**Function:** `mcp_firefly-mcp_category_update`

Update an existing category.

### Delete Category
**Function:** `mcp_firefly-mcp_category_delete`

Delete a category by ID.

### Category Transactions
**Function:** `mcp_firefly-mcp_category_list_transactions`

List transactions in a specific category.

## Tag Operations

### List Tags
**Function:** `mcp_firefly-mcp_tag_list`

List all tags with optional pagination.

### Get Tag Details
**Function:** `mcp_firefly-mcp_tag_get`

Get detailed information about a specific tag.

### Create Tag
**Function:** `mcp_firefly-mcp_tag_create`

Create a new tag.

**Parameters:**
- `tag` (required): Tag name
- `description` (optional): Tag description
- `date` (optional): Date the tag applies to

### Update Tag
**Function:** `mcp_firefly-mcp_tag_update`

Update an existing tag.

### Delete Tag
**Function:** `mcp_firefly-mcp_tag_delete`

Delete a tag by ID.

## Piggy Bank Operations

### List Piggy Banks
**Function:** `mcp_firefly-mcp_piggy_bank_list`

List all piggy banks (savings goals).

### Get Piggy Bank Details
**Function:** `mcp_firefly-mcp_piggy_bank_get`

Get detailed information about a specific piggy bank.

### Create Piggy Bank
**Function:** `mcp_firefly-mcp_piggy_bank_create`

Create a new piggy bank.

**Parameters:**
- `name` (required): Piggy bank name
- `target_amount` (required): Target savings amount
- `current_amount` (optional): Current saved amount
- `target_date` (optional): Target completion date

### Update Piggy Bank
**Function:** `mcp_firefly-mcp_piggy_bank_update`

Update an existing piggy bank.

### Delete Piggy Bank
**Function:** `mcp_firefly-mcp_piggy_bank_delete`

Delete a piggy bank by ID.

## Rule Operations

### List Rule Groups
**Function:** `mcp_firefly-mcp_rule_group_list`

List all rule groups.

### List Rules
**Function:** `mcp_firefly-mcp_rule_list`

List all rules.

### Test Rule
**Function:** `mcp_firefly-mcp_rule_test`

Test which transactions would be affected by a rule without making changes.

### Trigger Rule
**Function:** `mcp_firefly-mcp_rule_trigger`

Execute a rule on matching transactions.

## Utility Operations

### Get Version
**Function:** `mcp_firefly-mcp_get_version`

Get the version of the Firefly MCP server.

### Echo
**Function:** `mcp_firefly-mcp_echo`

Echo a message back (useful for testing connectivity).

## Common Usage Patterns

### Financial Overview
```
"Show me all my accounts and their current balances"
"What's my net worth?"
"List my recent transactions from the last week"
```

### Budget Management
```
"How much have I spent on groceries this month?"
"What's my budget status for dining out?"
"Create a new budget for travel with $500 monthly limit"
```

### Transaction Analysis
```
"Show me all transactions tagged with 'business'"
"List all income transactions from this year"
"What did I spend at Starbucks last month?"
```

### Bill Management
```
"Show me all my recurring bills"
"When is my next rent payment due?"
"Create a monthly bill for internet at $50"
```

## Error Handling

All operations may return errors for various reasons:

- **Authentication errors**: Invalid API token or expired session
- **Permission errors**: Insufficient permissions for the operation
- **Validation errors**: Invalid parameters or missing required fields
- **Not found errors**: Requested resource doesn't exist
- **Server errors**: Firefly III server issues

The MCP server provides detailed error messages to help diagnose and resolve issues.

## Rate Limiting

The MCP server respects Firefly III's rate limiting. If you encounter rate limit errors, the server will automatically retry with exponential backoff.

## Security Notes

- All operations respect Firefly III's built-in security model
- The MCP server only has access to data that your API token allows
- No personal / query data is cached by the MCP server and the only external calls are to the firefly instance you configure.
