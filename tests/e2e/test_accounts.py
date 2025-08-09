"""End-to-end tests for account MCP tools.

This module tests the complete account functionality through the MCP server,
ensuring that tools are called with correct parameters, parse responses properly,
and return expected results.
"""

import pytest
from typing import Any, Dict, List, Optional
from fastmcp import Client
from mcp.types import TextContent


class TestAccountListE2E:
    """End-to-end tests for account listing functionality."""

    @pytest.mark.parametrize("account_type,expected_count", [
        ("asset", 2),
        ("cash", 0),
        ("expense", 0),
    ])
    async def test_account_list_basic_success(self, account_type: str, expected_count: int, 
                                            mcp_server_direct_mode: Any, mock_http_client: Any, 
                                            sample_account_array_data: Any) -> None:
        """Test basic account listing through MCP tool."""
        # Adjust mock data based on account type
        mock_data: Dict[str, Any]
        if expected_count == 0:
            mock_data = {"data": [], "meta": {"pagination": {"total": 0}}}
        else:
            mock_data = sample_account_array_data
            
        # Setup mock response using the proper httpx.Response mock
        mock_response = mock_http_client.create_response(json_data=mock_data, is_error=False)
        mock_http_client.get.return_value = mock_response
        
        async with Client(mcp_server_direct_mode) as client:
            # Call the account_list tool
            result = await client.call_tool("account_list", {
                "type": account_type,
                "limit": 10,
                "page": 1
            })
            
            # Verify the tool call was successful
            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)
            
            # Parse the response
            import json
            text_content = result.content[0]
            assert isinstance(text_content, TextContent)
            response_data = json.loads(text_content.text)
            
            # Verify response structure
            assert "data" in response_data
            assert "meta" in response_data
            assert len(response_data["data"]) == expected_count
            
            if expected_count > 0:
                # Verify account data
                first_account = response_data["data"][0]
                assert first_account["id"] == "1"
                assert first_account["attributes"]["name"] == "Test Checking Account"
                assert first_account["attributes"]["type"] == "asset"
                assert first_account["attributes"]["current_balance"] == "1500.00"
            
            # Verify HTTP client was called correctly
            mock_http_client.get.assert_called_once_with(
                "/accounts", 
                params={
                    "type": account_type,
                    "limit": 10, 
                    "page": 1
                }
            )

    @pytest.mark.parametrize("filters,expected_params", [
        ({"date": "2023-12-01", "limit": 5, "page": 2}, 
         {"type": "all", "date": "2023-12-01", "limit": 5, "page": 2}),
        ({"limit": 20}, {"type": "all", "limit": 20}),
        ({}, {"type": "all"}),
    ])
    async def test_account_list_with_filters(self, filters: Dict[str, Any], expected_params: Dict[str, Any],
                                           mcp_server_direct_mode: Any, mock_http_client: Any, 
                                           sample_account_array_data: Any) -> None:
        """Test account listing with various filters and pagination."""
        # Setup mock response using the proper httpx.Response mock
        mock_response = mock_http_client.create_response(json_data=sample_account_array_data, is_error=False)
        mock_http_client.get.return_value = mock_response
        
        # Prepare request parameters
        request_params: Dict[str, Any] = {"type": "all", **filters}
        
        async with Client(mcp_server_direct_mode) as client:
            # Call with filters
            result = await client.call_tool("account_list", request_params)
            
            # Verify successful response
            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)
            
            # Verify HTTP client received correct parameters
            mock_http_client.get.assert_called_once_with(
                "/accounts",
                params=expected_params
            )


class TestAccountGetE2E:
    """End-to-end tests for getting individual accounts."""

    @pytest.mark.parametrize("date_param,expected_params", [
        ("2023-12-01", {"date": "2023-12-01"}),
        (None, {}),
    ])
    async def test_account_get_success(self, date_param: Optional[str], expected_params: Dict[str, Any],
                                     mcp_server_direct_mode: Any, mock_http_client: Any, 
                                     sample_account_data: Any) -> None:
        """Test getting a specific account by ID."""
        # Setup mock response using the proper httpx.Response mock
        mock_response = mock_http_client.create_response(json_data=sample_account_data, is_error=False)
        mock_http_client.get.return_value = mock_response
        
        # Prepare request parameters
        request_params = {"id": "1"}
        if date_param:
            request_params["date"] = date_param
        
        async with Client(mcp_server_direct_mode) as client:
            # Call the account_get tool
            result = await client.call_tool("account_get", request_params)
            
            # Verify the tool call was successful
            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)
            
            # Parse the response
            import json
            text_content = result.content[0]
            assert isinstance(text_content, TextContent)
            response_data = json.loads(text_content.text)
            
            # Verify response structure
            assert "data" in response_data
            account_data = response_data["data"]
            assert account_data["id"] == "1"
            assert account_data["attributes"]["name"] == "Test Checking Account"
            assert account_data["attributes"]["current_balance"] == "1500.00"
            assert account_data["attributes"]["account_number"] == "123456789"
            
            # Verify HTTP client was called correctly
            mock_http_client.get.assert_called_once_with(
                "/accounts/1", 
                params=expected_params
            )


class TestAccountErrorHandling:
    """Test error handling in account operations."""

    @pytest.mark.parametrize("status_code,error_message", [
        (400, "Invalid account type"),
        (401, "Unauthorized"),
        (404, "Account not found"),
        (500, "Internal server error"),
    ])
    async def test_account_list_api_errors(self, status_code: int, error_message: str,
                                         mcp_server_direct_mode: Any, mock_http_client: Any) -> None:
        """Test handling of various API errors in account listing."""
        # Setup mock response with error using proper httpx.Response mock
        error_data = {"message": error_message, "errors": [{"detail": error_message}]}
        mock_response = mock_http_client.create_response(
            json_data=error_data, 
            status_code=status_code, 
            is_error=True
        )
        mock_http_client.get.return_value = mock_response
        
        async with Client(mcp_server_direct_mode) as client:
            # This should raise an exception through the MCP layer
            with pytest.raises(Exception):
                await client.call_tool("account_list", {
                    "type": "invalid_type" if status_code == 400 else "asset"
                })

    async def test_account_get_validation_error(self, mcp_server_direct_mode: Any) -> None:
        """Test parameter validation for account get."""
        async with Client(mcp_server_direct_mode) as client:
            # Missing required 'id' parameter should cause validation error
            with pytest.raises(Exception):
                await client.call_tool("account_get", {})


class TestAccountToolsIntegration:
    """Integration tests combining multiple account operations."""

    async def test_list_then_get_account_flow(self, mcp_server_direct_mode: Any, mock_http_client: Any, 
                                             sample_account_array_data: Any, sample_account_data: Any) -> None:
        """Test typical workflow: list accounts, then get specific account details."""
        # Setup mock responses using proper httpx.Response mocks
        mock_response_list = mock_http_client.create_response(json_data=sample_account_array_data, is_error=False)
        mock_response_get = mock_http_client.create_response(json_data=sample_account_data, is_error=False)
        
        # Configure mock to return different responses for different calls
        mock_http_client.get.side_effect = [mock_response_list, mock_response_get]
        
        async with Client(mcp_server_direct_mode) as client:
            # First, list accounts to find available accounts
            list_result = await client.call_tool("account_list", {
                "type": "asset"
            })
            
            # Parse the list response to extract account ID
            import json
            list_text_content = list_result.content[0]
            assert isinstance(list_text_content, TextContent)
            list_data = json.loads(list_text_content.text)
            first_account_id = list_data["data"][0]["id"]
            
            # Then get detailed information for the first account
            get_result = await client.call_tool("account_get", {
                "id": first_account_id
            })
            
            # Verify both calls were successful
            assert len(list_result.content) == 1
            assert len(get_result.content) == 1
            
            # Verify the get result has more detailed information
            get_text_content = get_result.content[0]
            assert isinstance(get_text_content, TextContent)
            get_data = json.loads(get_text_content.text)
            account_attrs = get_data["data"]["attributes"]
            assert "account_number" in account_attrs
            assert "opening_balance" in account_attrs
            assert "notes" in account_attrs
            
            # Verify HTTP client was called twice with correct parameters
            assert mock_http_client.get.call_count == 2
            calls = mock_http_client.get.call_args_list
            
            # First call: list accounts
            assert calls[0][0] == ("/accounts",)
            assert calls[0][1]["params"] == {"type": "asset"}
            
            # Second call: get specific account
            assert calls[1][0] == (f"/accounts/{first_account_id}",)
            assert calls[1][1]["params"] == {}

    @pytest.mark.parametrize("account_type", [
        "asset", "expense", "revenue", "liability", "cash"
    ])
    async def test_different_account_types(self, account_type: str, 
                                         mcp_server_direct_mode: Any, mock_http_client: Any) -> None:
        """Test account listing with different account types."""
        # Setup mock response using proper httpx.Response mock
        empty_data: Dict[str, Any] = {"data": [], "meta": {"pagination": {"total": 0}}}
        mock_response = mock_http_client.create_response(json_data=empty_data, is_error=False)
        mock_http_client.get.return_value = mock_response
        
        async with Client(mcp_server_direct_mode) as client:
            result = await client.call_tool("account_list", {
                "type": account_type
            })
            
            # Verify call succeeded
            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)
            
            # Verify correct account type was passed
            mock_http_client.get.assert_called_once_with(
                "/accounts",
                params={"type": account_type}
            )


class TestAccountCreateE2E:
    """End-to-end tests for account creation functionality."""

    async def test_account_create_success(self, mcp_server_direct_mode: Any, mock_http_client: Any, 
                                        sample_account_store: Any, sample_account_created_data: Any) -> None:
        """Test creating a single account through MCP tool."""
        # Setup mock response for successful creation using proper httpx.Response mock
        mock_response = mock_http_client.create_response(json_data=sample_account_created_data, is_error=False)
        mock_http_client.post.return_value = mock_response
        
        async with Client(mcp_server_direct_mode) as client:
            # Call the account_create tool with a single account
            result = await client.call_tool("account_create", sample_account_store)
            
            # Verify the tool call was successful
            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)
            
            # Parse the response
            import json
            text_content = result.content[0]
            assert isinstance(text_content, TextContent)
            response_data = json.loads(text_content.text)
            
            # Verify account was created
            created_account = response_data["data"]
            assert created_account["type"] == "accounts"
            assert created_account["attributes"]["name"] == "New Test Account"
            
            # Verify HTTP client was called correctly
            mock_http_client.post.assert_called_once()
            call_args = mock_http_client.post.call_args
            assert call_args[0][0] == "/accounts"
            assert call_args[1]["json"]["name"] == sample_account_store["name"]


class TestAccountUpdateE2E:
    """End-to-end tests for account update functionality."""

    async def test_account_update_success(self, mcp_server_direct_mode: Any, mock_http_client: Any,
                                        sample_account_data: Any) -> None:
        """Test updating an account through MCP tool."""
        # Setup mock response using proper httpx.Response mock
        mock_response = mock_http_client.create_response(json_data=sample_account_data, is_error=False)
        mock_http_client.put.return_value = mock_response
        
        # Account update data
        update_data = {
            "id": "1",
            "account_update": {
                "name": "Updated Test Account",
                "notes": "Updated account notes"
            }
        }
        
        async with Client(mcp_server_direct_mode) as client:
            # Call the account_update tool
            result = await client.call_tool("account_update", update_data)
            
            # Verify the tool call was successful
            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)
            
            # Parse the response
            import json
            text_content = result.content[0]
            assert isinstance(text_content, TextContent)
            response_data = json.loads(text_content.text)
            
            # Verify account data is present
            assert "data" in response_data
            assert response_data["data"]["type"] == "accounts"
            
            # Verify HTTP client was called correctly
            mock_http_client.put.assert_called_once()
            call_args = mock_http_client.put.call_args
            assert call_args[0][0] == "/accounts/1"
            assert call_args[1]["json"]["name"] == "Updated Test Account"


class TestAccountDeleteE2E:
    """End-to-end tests for account deletion functionality."""

    async def test_account_delete_success(self, mcp_server_direct_mode: Any, mock_http_client: Any) -> None:
        """Test deleting an account through MCP tool."""
        # Setup mock response for successful deletion using proper httpx.Response mock
        empty_response = {}  # Delete operations typically return empty response
        mock_response = mock_http_client.create_response(json_data=empty_response, is_error=False)
        mock_http_client.delete.return_value = mock_response
        
        async with Client(mcp_server_direct_mode) as client:
            # Call the account_delete tool
            result = await client.call_tool("account_delete", {"id": "1"})
            
            # Verify the tool call was successful
            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)
            
            # Parse the response
            import json
            text_content = result.content[0]
            assert isinstance(text_content, TextContent)
            response_data = json.loads(text_content.text)
            
            # Verify delete response structure
            assert "message" in response_data
            assert "successfully" in response_data["message"].lower()
            
            # Verify HTTP client was called correctly
            mock_http_client.delete.assert_called_once_with("/accounts/1")


class TestAccountListOperationsE2E:
    """End-to-end tests for account list operations (transactions, attachments, piggy banks)."""

    @pytest.mark.parametrize("operation,endpoint,request_params,expected_params", [
        ("account_list_transactions", "/accounts/1/transactions", 
         {"id": "1", "start": "2023-01-01", "end": "2023-12-31", "type": "withdrawal"},
         {"start": "2023-01-01", "end": "2023-12-31", "type": "withdrawal"}),
        ("account_list_attachments", "/accounts/1/attachments",
         {"id": "1", "page": 1}, {"page": 1}),
        ("account_list_piggy_banks", "/accounts/1/piggy-banks",
         {"id": "1"}, {}),
    ])
    async def test_account_list_operations_success(self, operation: str, endpoint: str, 
                                                 request_params: Dict[str, Any], expected_params: Dict[str, Any],
                                                 mcp_server_direct_mode: Any, mock_http_client: Any,
                                                 sample_transaction_array_data: Any,
                                                 sample_attachment_array_data: Any,
                                                 sample_piggy_bank_array_data: Any) -> None:
        """Test listing operations for accounts through MCP tools."""
        # Choose appropriate sample data based on operation
        if "transaction" in operation:
            sample_data = sample_transaction_array_data
            expected_type = "transactions"
            expected_field = "group_title"
            expected_value = "Test Transaction"
        elif "attachment" in operation:
            sample_data = sample_attachment_array_data
            expected_type = "attachments"
            expected_field = "filename"
            expected_value = "receipt.pdf"
        else:  # piggy_banks
            sample_data = sample_piggy_bank_array_data
            expected_type = "piggy_banks"
            expected_field = "name"
            expected_value = "Vacation Fund"
        
        # Setup mock response using proper httpx.Response mock
        mock_response = mock_http_client.create_response(json_data=sample_data, is_error=False)
        mock_http_client.get.return_value = mock_response
        
        async with Client(mcp_server_direct_mode) as client:
            # Call the operation
            result = await client.call_tool(operation, request_params)
            
            # Verify the tool call was successful
            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)
            
            # Parse the response
            import json
            text_content = result.content[0]
            assert isinstance(text_content, TextContent)
            response_data = json.loads(text_content.text)
            
            # Verify data structure
            assert "data" in response_data
            assert len(response_data["data"]) == 1
            item = response_data["data"][0]
            assert item["type"] == expected_type
            assert item["attributes"][expected_field] == expected_value
            
            # Verify HTTP client was called correctly
            mock_http_client.get.assert_called_once_with(
                endpoint,
                params=expected_params
            )


class TestAccountEdgeCases:
    """Test edge cases and boundary conditions."""

    @pytest.mark.parametrize("page_size,total_items", [
        (1, 100),  # Many pages
        (50, 2),   # Single page
        (10, 0),   # Empty result
    ])
    async def test_pagination_edge_cases(self, page_size: int, total_items: int,
                                       mcp_server_direct_mode: Any, mock_http_client: Any) -> None:
        """Test pagination with various data sizes."""
        # Create mock data based on parameters
        mock_data: Dict[str, Any]
        if total_items == 0:
            mock_data = {"data": [], "meta": {"pagination": {"total": 0}}}
        else:
            mock_accounts: List[Dict[str, Any]] = []
            for i in range(min(page_size, total_items)):
                mock_accounts.append({
                    "type": "accounts",
                    "id": str(i + 1),
                    "attributes": {
                        "name": f"Test Account {i + 1}",
                        "type": "asset",
                        "current_balance": "1000.00"
                    }
                })
            mock_data = {
                "data": mock_accounts,
                "meta": {
                    "pagination": {
                        "total": total_items,
                        "count": len(mock_accounts),
                        "per_page": page_size,
                        "current_page": 1,
                        "total_pages": (total_items + page_size - 1) // page_size if total_items > 0 else 1
                    }
                }
            }
        
        # Setup mock response using proper httpx.Response mock
        mock_response = mock_http_client.create_response(json_data=mock_data, is_error=False)
        mock_http_client.get.return_value = mock_response
        
        async with Client(mcp_server_direct_mode) as client:
            result = await client.call_tool("account_list", {
                "type": "asset",
                "limit": page_size,
                "page": 1
            })
            
            # Verify response structure
            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)
            
            import json
            response_data = json.loads(result.content[0].text)
            assert len(response_data["data"]) == min(page_size, total_items)
            assert response_data["meta"]["pagination"]["total"] == total_items

    @pytest.mark.parametrize("invalid_params", [
        {"id": ""},  # Empty ID
        {"id": "non-numeric"},  # Invalid ID format
        {"date": "invalid-date"},  # Invalid date format
    ])
    async def test_invalid_parameters(self, invalid_params: Dict[str, Any],
                                    mcp_server_direct_mode: Any, mock_http_client: Any) -> None:
        """Test handling of invalid parameters."""
        async with Client(mcp_server_direct_mode) as client:
            # These should either be handled gracefully or raise appropriate exceptions
            try:
                if "id" in invalid_params:
                    await client.call_tool("account_get", invalid_params)
                else:
                    await client.call_tool("account_list", invalid_params)
            except Exception as e:
                # Expect some kind of validation error
                assert "validation" in str(e).lower() or "error" in str(e).lower()