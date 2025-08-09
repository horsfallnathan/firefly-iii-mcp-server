"""Common test fixtures and utilities for Firefly MCP tests."""

import pytest
from unittest.mock import Mock, MagicMock
from typing import Dict, Any, Optional
import httpx

from firefly_mcp.main import get_mcp_server
from firefly_mcp.models.model import AccountTypeFilter
from firefly_mcp.models.requests import AccountGetRequest, AccountListRequest

@pytest.fixture
def mcp_server():
    return get_mcp_server()


@pytest.fixture
def mock_http_response():
    """Create a mock HTTP response."""
    def _create_response(status_code: int = 200, json_data: Optional[Dict[str, Any]] = None):
        response = Mock(spec=httpx.Response)
        response.status_code = status_code
        response.json.return_value = json_data or {}
        response.text = str(json_data or {})
        response.is_error = status_code >= 400
        return response
    return _create_response


@pytest.fixture
def sample_account_data() -> Dict[str, Any]:
    """Sample account data for testing."""
    return {
        "data": {
            "type": "accounts",
            "id": "1",
            "attributes": {
                "name": "Test Checking Account",
                "type": "asset",
                "account_role": "defaultAsset",
                "currency_id": "1",
                "currency_code": "USD",
                "currency_symbol": "$",
                "account_number": "123456789",
                "iban": "US33XXXX1234567890123456",
                "bic": "CHASUS33",
                "virtual_balance": "0.00",
                "opening_balance": "1000.00",
                "opening_balance_date": "2023-01-01T00:00:00+00:00",
                "liability_type": None,
                "liability_direction": None,
                "interest": "0.00",
                "interest_period": None,
                "current_balance": "1500.00",
                "current_balance_date": "2023-12-01T00:00:00+00:00",
                "notes": "Test account notes",
                "monthly_payment_date": None,
                "credit_card_type": None,
                "order": 1,
                "active": True,
                "include_net_worth": True
            }
        }
    }


@pytest.fixture
def sample_account_array_data() -> Dict[str, Any]:
    """Sample account array data for testing."""
    return {
        "data": [
            {
                "type": "accounts",
                "id": "1",
                "attributes": {
                    "name": "Test Checking Account",
                    "type": "asset",
                    "account_role": "defaultAsset",
                    "currency_id": "1",
                    "currency_code": "USD",
                    "currency_symbol": "$",
                    "current_balance": "1500.00",
                    "active": True
                }
            },
            {
                "type": "accounts",
                "id": "2",
                "attributes": {
                    "name": "Test Savings Account",
                    "type": "asset",
                    "account_role": "savingAsset",
                    "currency_id": "1",
                    "currency_code": "USD",
                    "currency_symbol": "$",
                    "current_balance": "5000.00",
                    "active": True
                }
            }
        ],
        "meta": {
            "pagination": {
                "total": 2,
                "count": 2,
                "per_page": 50,
                "current_page": 1,
                "total_pages": 1
            }
        }
    }


@pytest.fixture
def sample_account_get_request():
    """Sample AccountGetRequest for testing."""
    return AccountGetRequest(id="1", date="2023-12-01")


@pytest.fixture
def sample_account_list_request():
    """Sample AccountListRequest for testing."""
    return AccountListRequest(
        type=AccountTypeFilter.asset.value,
        limit=10,
        page=1,
        date="2023-12-01"
    )


@pytest.fixture 
def mock_client(monkeypatch: pytest.MonkeyPatch):
    """Mock the HTTP client."""
    mock = MagicMock()
    monkeypatch.setattr("firefly_mcp.core.accounts.client", mock)
    return mock


@pytest.fixture
def mock_raise_api_error(monkeypatch: pytest.MonkeyPatch):
    """Mock the raise_api_error_if_any function."""
    mock = MagicMock()
    monkeypatch.setattr("firefly_mcp.core.accounts.raise_api_error_if_any", mock)
    return mock


@pytest.fixture
def mock_execute_operations(monkeypatch: pytest.MonkeyPatch):
    """Mock the execute_operations function."""
    mock = MagicMock()
    monkeypatch.setattr("firefly_mcp.core.accounts.execute_operations", mock)
    return mock


# E2E Testing Fixtures

@pytest.fixture
def mcp_server_direct_mode(monkeypatch: pytest.MonkeyPatch):
    """Create MCP server in direct mode for testing individual account tools."""
    # Set environment for direct mode with account tools enabled
    monkeypatch.setenv("FIREFLY_DIRECT_MODE", "true")
    monkeypatch.setenv("FIREFLY_ENABLED_ENTITIES", "account")
    
    # Create a fresh server instance after setting environment variables
    from firefly_mcp.tools.main import create_mcp_server
    return create_mcp_server()


@pytest.fixture 
def mock_http_client():
    """Mock the HTTP client with sample responses for e2e testing."""
    from unittest.mock import patch, Mock
    import httpx
    
    with patch("firefly_mcp.core.accounts.client") as mock_client:
        # Configure the mock client to return proper httpx.Response objects
        def create_mock_response(json_data: Optional[Dict[str, Any]] = None, status_code: int = 200, is_error: bool = False):
            mock_response = Mock(spec=httpx.Response)
            mock_response.json.return_value = json_data or {}
            mock_response.status_code = status_code
            mock_response.is_error = is_error
            mock_response.text = str(json_data or "")
            return mock_response
        
        # Add helper method to mock client
        mock_client.create_response = create_mock_response
        yield mock_client


@pytest.fixture
def sample_account_created_data():
    """Sample account creation response for testing."""
    return {
        "data": {
            "type": "accounts",
            "id": "1",
            "attributes": {
                "name": "New Test Account",
                "type": "asset",
                "account_role": "defaultAsset",
                "currency_code": "USD",
                "current_balance": "0.00",
                "active": True
            }
        }
    }


@pytest.fixture
def sample_account_store():
    """Sample AccountStore data for create operations."""
    return {
        "name": "Test Account",
        "type": "asset",
        "account_role": "defaultAsset",
        "currency_code": "USD",
        "opening_balance": "1000.00",
        "opening_balance_date": "2023-01-01T00:00:00+00:00",
        "active": True
    }


@pytest.fixture
def sample_transaction_array_data():
    """Sample transaction array data for testing."""
    return {
        "data": [
            {
                "type": "transactions",
                "id": "1",
                "attributes": {
                    "group_title": "Test Transaction",
                    "transactions": [
                        {
                            "transaction_journal_id": "1",
                            "type": "withdrawal",
                            "date": "2023-12-01T00:00:00+00:00",
                            "amount": "25.00",
                            "description": "Test withdrawal",
                            "source_id": "1",
                            "destination_id": "2",
                            "source_name": "Test Checking Account",
                            "destination_name": "Groceries",
                            "category_name": "Food"
                        }
                    ]
                },
                "links": {
                    "self": "https://demo.firefly-iii.org/api/v1/transactions/1"
                }
            }
        ],
        "meta": {
            "pagination": {
                "total": 1,
                "count": 1,
                "per_page": 50,
                "current_page": 1,
                "total_pages": 1
            }
        },
        "links": {
            "self": "https://demo.firefly-iii.org/api/v1/transactions?page=1",
            "first": "https://demo.firefly-iii.org/api/v1/transactions?page=1",
            "last": "https://demo.firefly-iii.org/api/v1/transactions?page=1"
        }
    }


@pytest.fixture
def sample_attachment_array_data():
    """Sample attachment array data for testing."""
    return {
        "data": [
            {
                "type": "attachments",
                "id": "1", 
                "attributes": {
                    "filename": "receipt.pdf",
                    "title": "Grocery Receipt",
                    "notes": "Receipt for grocery shopping",
                    "mime": "application/pdf",
                    "size": 1024,
                    "created_at": "2023-12-01T00:00:00+00:00",
                    "updated_at": "2023-12-01T00:00:00+00:00",
                    "attachable_type": "Account",
                    "attachable_id": "1"
                },
                "links": {
                    "self": "https://demo.firefly-iii.org/api/v1/attachments/1"
                }
            }
        ],
        "meta": {
            "pagination": {
                "total": 1,
                "count": 1,
                "per_page": 50,
                "current_page": 1,
                "total_pages": 1
            }
        }
    }


@pytest.fixture
def sample_piggy_bank_array_data():
    """Sample piggy bank array data for testing."""
    return {
        "data": [
            {
                "type": "piggy_banks",
                "id": "1",
                "attributes": {
                    "name": "Vacation Fund",
                    "target_amount": "5000.00",
                    "current_amount": "1500.00",
                    "start_date": "2023-01-01",
                    "target_date": "2024-06-01",
                    "order": 1,
                    "active": True,
                    "notes": "Saving for summer vacation"
                },
                "links": {
                    "self": "https://demo.firefly-iii.org/api/v1/piggy-banks/1"
                }
            }
        ],
        "meta": {
            "pagination": {
                "total": 1,
                "count": 1,
                "per_page": 50,
                "current_page": 1,
                "total_pages": 1
            }
        },
        "links": {
            "self": "https://demo.firefly-iii.org/api/v1/piggy-banks?page=1",
            "first": "https://demo.firefly-iii.org/api/v1/piggy-banks?page=1",
            "last": "https://demo.firefly-iii.org/api/v1/piggy-banks?page=1"
        }
    }
