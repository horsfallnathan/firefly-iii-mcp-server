from pydantic import BaseModel, Field
from firefly_mcp.models.model import AccountUpdate, TransactionUpdate, BudgetUpdate, BudgetLimit, BudgetLimitStore, CategoryUpdate, TagModelUpdate, RuleUpdate, RuleGroupUpdate, BillUpdate, PiggyBankUpdate
from typing import List, Literal


class AccountListRequest(BaseModel):
    """Request model for listing accounts."""
    type: Literal['all', 'asset', 'cash', 'expense', 'revenue', 'special', 'hidden', 'liability', 'liabilities', 'Default account', 'Cash account', 'Asset account', 'Expense account', 'Revenue account', 'Initial balance account', 'Beneficiary account', 'Import account', 'Reconciliation account', 'Loan', 'Debt', 'Mortgage'] = Field(default='all', description="Filter by account type")
    limit: int | None = Field(default=None, description="Pagination limit")
    page: int | None = Field(default=None, description="Page number")
    date: str | None = Field(default=None, description="Balance date (ISO format)")


class AccountGetRequest(BaseModel):
    """Request model for getting a single account"""
    id: str = Field(..., description="Id of the account")
    date: str | None = Field(None, description="A date formatted YYYY-MM-DD. When added to the request, Firefly III will show the account's balance on that day.")

class AccountUpdateRequest(BaseModel):
    """Request model for updating an account"""
    id: str = Field(..., description="The ID of the account.")
    account_update: AccountUpdate = Field(..., description="The updated account data.")

class AccountTransactionsRequest(BaseModel):
    """Request model for listing transactions for an account"""
    id: str = Field(..., description="The ID of the account")
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")
    start: str | None = Field(None, description="Start date formatted YYYY-MM-DD")
    end: str | None = Field(None, description="End date formatted YYYY-MM-DD")
    type: Literal['all', 'withdrawal', 'withdrawals', 'expense', 'deposit', 'deposits', 'income', 'transfer', 'transfers', 'opening_balance', 'reconciliation', 'special', 'specials', 'default'] | None = Field(None, description="Optional filter on the transaction type(s) returned")

class AccountAttachmentsRequest(BaseModel):
    """Request model for listing attachments for an account"""
    id: str = Field(..., description="The ID of the account")
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")

class AccountPiggyBanksRequest(BaseModel):
    """Request model for listing piggy banks for an account"""
    id: str = Field(..., description="The ID of the account")
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")

class AccountDeleteRequest(BaseModel):
    """Request model for deleting an account"""
    id: str = Field(..., description="The ID of the account to delete")

class AccountDeleteResponse(BaseModel):
    """Response model for account deletion"""
    message: str = Field(..., description="Success message")


# Transaction-related request models
class TransactionListRequest(BaseModel):
    """Request model for listing transactions."""
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")
    start: str | None = Field(None, description="Start date formatted YYYY-MM-DD")
    end: str | None = Field(None, description="End date formatted YYYY-MM-DD")
    type: Literal['all', 'withdrawal', 'withdrawals', 'expense', 'deposit', 'deposits', 'income', 'transfer', 'transfers', 'opening_balance', 'reconciliation', 'special', 'specials', 'default'] | None = Field(None, description="Optional filter on the transaction type(s) returned")


class TransactionGetRequest(BaseModel):
    """Request model for getting a single transaction"""
    id: str = Field(..., description="The ID of the transaction")


class TransactionUpdateRequest(BaseModel):
    """Request model for updating a transaction"""
    id: str = Field(..., description="The ID of the transaction")
    transaction_update: TransactionUpdate = Field(..., description="The updated transaction data")


class TransactionAttachmentsRequest(BaseModel):
    """Request model for listing attachments for a transaction"""
    id: str = Field(..., description="The ID of the transaction")
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")


class TransactionPiggyBankEventsRequest(BaseModel):
    """Request model for listing piggy bank events for a transaction"""
    id: str = Field(..., description="The ID of the transaction")
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")


class TransactionDeleteRequest(BaseModel):
    """Request model for deleting a transaction"""
    id: str = Field(..., description="The ID of the transaction to delete")


class TransactionDeleteResponse(BaseModel):
    """Response model for transaction deletion"""
    message: str = Field(..., description="Success message")


class BulkCategorizeRequest(BaseModel):
    """Request model for bulk categorizing transactions"""
    transaction_ids: List[int] = Field(..., description="List of transaction IDs to categorize")
    category_name: str = Field(..., description="Name of the category to assign")


class BulkTagRequest(BaseModel):
    """Request model for bulk tagging transactions"""
    transaction_ids: List[int] = Field(..., description="List of transaction IDs to tag")
    tag_names: List[str] = Field(..., description="List of tag names to assign")


# Budget-related request models
class BudgetListRequest(BaseModel):
    """Request model for listing budgets."""
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")
    start: str | None = Field(None, description="Start date (YYYY-MM-DD) to get spending info")
    end: str | None = Field(None, description="End date (YYYY-MM-DD) to get spending info")


class BudgetGetRequest(BaseModel):
    """Request model for getting a single budget"""
    id: str = Field(..., description="The ID of the budget")
    start: str | None = Field(None, description="Start date (YYYY-MM-DD) to get spending info")
    end: str | None = Field(None, description="End date (YYYY-MM-DD) to get spending info")


class BudgetUpdateRequest(BaseModel):
    """Request model for updating a budget"""
    id: str = Field(..., description="The ID of the budget")
    budget_update: BudgetUpdate = Field(..., description="The updated budget data")


class BudgetLimitsRequest(BaseModel):
    """Request model for listing budget limits for a budget"""
    id: str = Field(..., description="The ID of the budget")
    start: str | None = Field(None, description="Start date (YYYY-MM-DD)")
    end: str | None = Field(None, description="End date (YYYY-MM-DD)")


class BudgetLimitGetRequest(BaseModel):
    """Request model for getting a single budget limit"""
    budget_id: str = Field(..., description="The ID of the budget")
    limit_id: str = Field(..., description="The ID of the budget limit")


class BudgetLimitCreateRequest(BaseModel):
    """Request model for creating a budget limit"""
    budget_id: str = Field(..., description="The ID of the budget")
    budget_limit_store: BudgetLimitStore = Field(..., description="The budget limit data to create")


class BudgetLimitUpdateRequest(BaseModel):
    """Request model for updating a budget limit"""
    budget_id: str = Field(..., description="The ID of the budget")
    limit_id: str = Field(..., description="The ID of the budget limit")
    budget_limit: BudgetLimit = Field(..., description="The updated budget limit data")


class BudgetTransactionsRequest(BaseModel):
    """Request model for listing transactions for a budget"""
    id: str = Field(..., description="The ID of the budget")
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")
    start: str | None = Field(None, description="Start date (YYYY-MM-DD)")
    end: str | None = Field(None, description="End date (YYYY-MM-DD)")
    type: str | None = Field(None, description="Transaction type filter")


class BudgetAttachmentsRequest(BaseModel):
    """Request model for listing attachments for a budget"""
    id: str = Field(..., description="The ID of the budget")
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")


class BudgetTransactionsWithoutBudgetRequest(BaseModel):
    """Request model for listing transactions without budget"""
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")
    start: str | None = Field(None, description="Start date (YYYY-MM-DD)")
    end: str | None = Field(None, description="End date (YYYY-MM-DD)")


class BudgetDeleteRequest(BaseModel):
    """Request model for deleting a budget"""
    id: str = Field(..., description="The ID of the budget to delete")


class BudgetDeleteResponse(BaseModel):
    """Response model for budget deletion"""
    message: str = Field(..., description="Success message")


class BudgetLimitDeleteRequest(BaseModel):
    """Request model for deleting a budget limit"""
    budget_id: str = Field(..., description="The ID of the budget")
    limit_id: str = Field(..., description="The ID of the budget limit to delete")


class BudgetLimitDeleteResponse(BaseModel):
    """Response model for budget limit deletion"""
    message: str = Field(..., description="Success message")


# Category-related request models
class CategoryListRequest(BaseModel):
    """Request model for listing categories."""
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")


class CategoryGetRequest(BaseModel):
    """Request model for getting a single category"""
    id: str = Field(..., description="The ID of the category")
    start: str | None = Field(None, description="Start date formatted YYYY-MM-DD, to show spent and earned info")
    end: str | None = Field(None, description="End date formatted YYYY-MM-DD, to show spent and earned info")


class CategoryUpdateRequest(BaseModel):
    """Request model for updating a category"""
    id: str = Field(..., description="The ID of the category")
    category_update: CategoryUpdate = Field(..., description="The updated category data")


class CategoryTransactionsRequest(BaseModel):
    """Request model for listing transactions for a category"""
    id: str = Field(..., description="The ID of the category")
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")
    start: str | None = Field(None, description="Start date formatted YYYY-MM-DD")
    end: str | None = Field(None, description="End date formatted YYYY-MM-DD")
    type: Literal['all', 'withdrawal', 'withdrawals', 'expense', 'deposit', 'deposits', 'income', 'transfer', 'transfers', 'opening_balance', 'reconciliation', 'special', 'specials', 'default'] | None = Field(None, description="Optional filter on the transaction type(s) returned")


class CategoryAttachmentsRequest(BaseModel):
    """Request model for listing attachments for a category"""
    id: str = Field(..., description="The ID of the category")
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")


class CategoryDeleteRequest(BaseModel):
    """Request model for deleting a category"""
    id: str = Field(..., description="The ID of the category to delete")


class CategoryDeleteResponse(BaseModel):
    """Response model for category deletion"""
    message: str = Field(..., description="Success message")


# Tag-related request models
class TagListRequest(BaseModel):
    """Request model for listing tags."""
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")


class TagGetRequest(BaseModel):
    """Request model for getting a single tag"""
    id: str = Field(..., description="The ID of the tag")
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")


class TagUpdateRequest(BaseModel):
    """Request model for updating a tag"""
    id: str = Field(..., description="The ID of the tag")
    tag_update: TagModelUpdate = Field(..., description="The updated tag data")


class TagTransactionsRequest(BaseModel):
    """Request model for listing transactions for a tag"""
    id: str = Field(..., description="The ID of the tag")
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")
    start: str | None = Field(None, description="Start date formatted YYYY-MM-DD")
    end: str | None = Field(None, description="End date formatted YYYY-MM-DD")
    type: Literal['all', 'withdrawal', 'withdrawals', 'expense', 'deposit', 'deposits', 'income', 'transfer', 'transfers', 'opening_balance', 'reconciliation', 'special', 'specials', 'default'] | None = Field(None, description="Optional filter on the transaction type(s) returned")


class TagAttachmentsRequest(BaseModel):
    """Request model for listing attachments for a tag"""
    id: str = Field(..., description="The ID of the tag")
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")


class TagDeleteRequest(BaseModel):
    """Request model for deleting a tag"""
    id: str = Field(..., description="The ID of the tag to delete")


class TagDeleteResponse(BaseModel):
    """Response model for tag deletion"""
    message: str = Field(..., description="Success message")


# Rule-related request models
class RuleListRequest(BaseModel):
    """Request model for listing rules."""
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")


class RuleGetRequest(BaseModel):
    """Request model for getting a single rule"""
    id: str = Field(..., description="The ID of the rule")


class RuleUpdateRequest(BaseModel):
    """Request model for updating a rule"""
    id: str = Field(..., description="The ID of the rule")
    rule_update: RuleUpdate = Field(..., description="The updated rule data")


class RuleTestRequest(BaseModel):
    """Request model for testing which transactions would be hit by a rule"""
    id: str = Field(..., description="The ID of the rule")
    start: str | None = Field(None, description="Start date formatted YYYY-MM-DD to limit transactions")
    end: str | None = Field(None, description="End date formatted YYYY-MM-DD to limit transactions")
    accounts: List[int] | None = Field(None, description="Limit testing to these asset accounts or liabilities")


class RuleTriggerRequest(BaseModel):
    """Request model for firing a rule on transactions"""
    id: str = Field(..., description="The ID of the rule")
    start: str | None = Field(None, description="Start date formatted YYYY-MM-DD to limit transactions")
    end: str | None = Field(None, description="End date formatted YYYY-MM-DD to limit transactions")
    accounts: List[int] | None = Field(None, description="Limit triggering to these asset accounts or liabilities")


class RuleDeleteRequest(BaseModel):
    """Request model for deleting a rule"""
    id: str = Field(..., description="The ID of the rule to delete")


class RuleDeleteResponse(BaseModel):
    """Response model for rule deletion"""
    message: str = Field(..., description="Success message")


# Rule Group-related request models
class RuleGroupListRequest(BaseModel):
    """Request model for listing rule groups."""
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")


class RuleGroupGetRequest(BaseModel):
    """Request model for getting a single rule group"""
    id: str = Field(..., description="The ID of the rule group")


class RuleGroupUpdateRequest(BaseModel):
    """Request model for updating a rule group"""
    id: str = Field(..., description="The ID of the rule group")
    rule_group_update: RuleGroupUpdate = Field(..., description="The updated rule group data")


class RuleGroupListRulesRequest(BaseModel):
    """Request model for listing rules in a rule group"""
    id: str = Field(..., description="The ID of the rule group")
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")


class RuleGroupTestRequest(BaseModel):
    """Request model for testing which transactions would be hit by a rule group"""
    id: str = Field(..., description="The ID of the rule group")
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")
    start: str | None = Field(None, description="Start date formatted YYYY-MM-DD to limit transactions")
    end: str | None = Field(None, description="End date formatted YYYY-MM-DD to limit transactions")
    search_limit: int | None = Field(None, description="Maximum number of transactions Firefly III will try")
    triggered_limit: int | None = Field(None, description="Maximum number of transactions the rule group can trigger on")
    accounts: List[int] | None = Field(None, description="Limit testing to these asset accounts or liabilities")


class RuleGroupTriggerRequest(BaseModel):
    """Request model for firing a rule group on transactions"""
    id: str = Field(..., description="The ID of the rule group")
    start: str | None = Field(None, description="Start date formatted YYYY-MM-DD to limit transactions")
    end: str | None = Field(None, description="End date formatted YYYY-MM-DD to limit transactions")
    accounts: List[int] | None = Field(None, description="Limit triggering to these asset accounts or liabilities")


class RuleGroupDeleteRequest(BaseModel):
    """Request model for deleting a rule group"""
    id: str = Field(..., description="The ID of the rule group to delete")


class RuleGroupDeleteResponse(BaseModel):
    """Response model for rule group deletion"""
    message: str = Field(..., description="Success message")


# Bill-related request models
class BillListRequest(BaseModel):
    """Request model for listing bills."""
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")
    start: str | None = Field(None, description="Start date formatted YYYY-MM-DD to calculate payment and paid dates")
    end: str | None = Field(None, description="End date formatted YYYY-MM-DD to calculate payment and paid dates")


class BillGetRequest(BaseModel):
    """Request model for getting a single bill"""
    id: str = Field(..., description="The ID of the bill")
    start: str | None = Field(None, description="Start date formatted YYYY-MM-DD to calculate payment and paid dates")
    end: str | None = Field(None, description="End date formatted YYYY-MM-DD to calculate payment and paid dates")


class BillUpdateRequest(BaseModel):
    """Request model for updating a bill"""
    id: str = Field(..., description="The ID of the bill")
    bill_update: BillUpdate = Field(..., description="The updated bill data")


class BillTransactionsRequest(BaseModel):
    """Request model for listing transactions for a bill"""
    id: str = Field(..., description="The ID of the bill")
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")
    start: str | None = Field(None, description="Start date formatted YYYY-MM-DD")
    end: str | None = Field(None, description="End date formatted YYYY-MM-DD")
    type: Literal['all', 'withdrawal', 'withdrawals', 'expense', 'deposit', 'deposits', 'income', 'transfer', 'transfers', 'opening_balance', 'reconciliation', 'special', 'specials', 'default'] | None = Field(None, description="Optional filter on the transaction type(s) returned")


class BillAttachmentsRequest(BaseModel):
    """Request model for listing attachments for a bill"""
    id: str = Field(..., description="The ID of the bill")
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")


class BillRulesRequest(BaseModel):
    """Request model for listing rules for a bill"""
    id: str = Field(..., description="The ID of the bill")
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")


class BillDeleteRequest(BaseModel):
    """Request model for deleting a bill"""
    id: str = Field(..., description="The ID of the bill to delete")


class BillDeleteResponse(BaseModel):
    """Response model for bill deletion"""
    message: str = Field(..., description="Success message")


class PiggyBankListRequest(BaseModel):
    """Request model for listing piggy banks."""
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")


class PiggyBankGetRequest(BaseModel):
    """Request model for getting a single piggy bank"""
    id: str = Field(..., description="The ID of the piggy bank")


class PiggyBankUpdateRequest(BaseModel):
    """Request model for updating a piggy bank"""
    id: str = Field(..., description="The ID of the piggy bank")
    piggy_bank_update: PiggyBankUpdate = Field(..., description="The updated piggy bank data")


class PiggyBankEventsRequest(BaseModel):
    """Request model for listing events for a piggy bank"""
    id: str = Field(..., description="The ID of the piggy bank")
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")


class PiggyBankAttachmentsRequest(BaseModel):
    """Request model for listing attachments for a piggy bank"""
    id: str = Field(..., description="The ID of the piggy bank")
    limit: int | None = Field(None, description="Number of items per page")
    page: int | None = Field(None, description="Page number")


class PiggyBankDeleteRequest(BaseModel):
    """Request model for deleting a piggy bank"""
    id: str = Field(..., description="The ID of the piggy bank to delete")


class PiggyBankDeleteResponse(BaseModel):
    """Response model for piggy bank deletion"""
    message: str = Field(..., description="Success message")