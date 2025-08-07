"""
MCP Roots Client Test

This example demonstrates how to use the MCP roots server with various
root types and operations.

Requirements:
- pip install mcp
"""

import asyncio
import json
import tempfile
import os
from typing import Dict, Any, List
from mcp.client import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_roots_server():
    """Test the MCP roots server with various root types and operations."""
    
    # Connect to the roots server
    server_params = StdioServerParameters(
        command="python",
        args=["buildingblocks/mcp_roots_example.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, "mcp-roots-client") as session:
            print("Connected to MCP Roots Server")
            
            # Test 1: List all roots
            print("\n=== Test 1: List All Roots ===")
            result = await session.call_tool("list_roots", {})
            print(f"Available roots: {json.dumps(result, indent=2)}")
            
            # Test 2: Get specific root details
            print("\n=== Test 2: Get Root Details ===")
            result = await session.call_tool("get_root", {"root_id": "file_system"})
            print(f"File system root: {json.dumps(result, indent=2)}")
            
            # Test 3: Validate root operation
            print("\n=== Test 3: Validate Root Operation ===")
            result = await session.call_tool("validate_root_operation", {
                "root_id": "file_system",
                "operation": "read",
                "parameters": {"path": "/tmp/test.txt"}
            })
            print(f"Validation result: {json.dumps(result, indent=2)}")
            
            # Test 4: File system operations
            print("\n=== Test 4: File System Operations ===")
            
            # Create a temporary file for testing
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
            temp_file.write("Hello MCP Roots!")
            temp_file.close()
            
            # Test file read
            result = await session.call_tool("execute_root_operation", {
                "root_id": "file_system",
                "operation": "read",
                "parameters": {"path": temp_file.name}
            })
            print(f"File read result: {json.dumps(result, indent=2)}")
            
            # Test file write
            result = await session.call_tool("execute_root_operation", {
                "root_id": "file_system",
                "operation": "write",
                "parameters": {"path": temp_file.name, "content": "Updated content!"}
            })
            print(f"File write result: {json.dumps(result, indent=2)}")
            
            # Test directory listing
            result = await session.call_tool("execute_root_operation", {
                "root_id": "file_system",
                "operation": "list",
                "parameters": {"path": "/tmp"}
            })
            print(f"Directory list result: {json.dumps(result, indent=2)}")
            
            # Clean up
            os.unlink(temp_file.name)
            
            # Test 5: Database operations
            print("\n=== Test 5: Database Operations ===")
            result = await session.call_tool("execute_root_operation", {
                "root_id": "database",
                "operation": "query",
                "parameters": {"table": "users", "query": "SELECT * FROM users"}
            })
            print(f"Database query result: {json.dumps(result, indent=2)}")
            
            # Test 6: API operations
            print("\n=== Test 6: API Operations ===")
            result = await session.call_tool("execute_root_operation", {
                "root_id": "api",
                "operation": "get",
                "parameters": {"endpoint": "/users", "method": "GET"}
            })
            print(f"API GET result: {json.dumps(result, indent=2)}")
            
            # Test 7: Memory operations
            print("\n=== Test 7: Memory Operations ===")
            result = await session.call_tool("execute_root_operation", {
                "root_id": "memory",
                "operation": "store",
                "parameters": {"key": "test_key", "value": "test_value"}
            })
            print(f"Memory store result: {json.dumps(result, indent=2)}")
            
            result = await session.call_tool("execute_root_operation", {
                "root_id": "memory",
                "operation": "retrieve",
                "parameters": {"key": "test_key"}
            })
            print(f"Memory retrieve result: {json.dumps(result, indent=2)}")
            
            # Test 8: Network operations
            print("\n=== Test 8: Network Operations ===")
            result = await session.call_tool("execute_root_operation", {
                "root_id": "network",
                "operation": "ping",
                "parameters": {"host": "google.com"}
            })
            print(f"Network ping result: {json.dumps(result, indent=2)}")
            
            # Test 9: Cloud storage operations
            print("\n=== Test 9: Cloud Storage Operations ===")
            result = await session.call_tool("execute_root_operation", {
                "root_id": "cloud_storage",
                "operation": "upload",
                "parameters": {"bucket": "my-bucket", "object_key": "test.txt", "size": 1024}
            })
            print(f"Cloud storage upload result: {json.dumps(result, indent=2)}")
            
            # Test 10: Configuration operations
            print("\n=== Test 10: Configuration Operations ===")
            result = await session.call_tool("execute_root_operation", {
                "root_id": "config",
                "operation": "read",
                "parameters": {"section": "database", "key": "host"}
            })
            print(f"Config read result: {json.dumps(result, indent=2)}")
            
            # Test 11: Log operations
            print("\n=== Test 11: Log Operations ===")
            result = await session.call_tool("execute_root_operation", {
                "root_id": "log",
                "operation": "write",
                "parameters": {"level": "INFO", "message": "Test log message"}
            })
            print(f"Log write result: {json.dumps(result, indent=2)}")
            
            # Test 12: Create custom root
            print("\n=== Test 12: Create Custom Root ===")
            result = await session.call_tool("create_root", {
                "root_id": "custom_cache",
                "root_type": "cache",
                "uri": "cache://",
                "description": "Custom cache root for caching operations",
                "capabilities": ["get", "set", "delete", "clear"],
                "validation": {
                    "required": ["key"],
                    "constraints": {
                        "key": "valid_cache_key"
                    }
                }
            })
            print(f"Create root result: {json.dumps(result, indent=2)}")
            
            # Test 13: Get root system info
            print("\n=== Test 13: Get System Info ===")
            result = await session.call_tool("root_info", {})
            print(f"System info: {json.dumps(result, indent=2)}")
            
            print("\n=== All Tests Completed ===")


async def test_root_validation():
    """Test root operation validation with invalid parameters."""
    
    server_params = StdioServerParameters(
        command="python",
        args=["buildingblocks/mcp_roots_example.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, "mcp-roots-validation-client") as session:
            print("\n=== Testing Root Operation Validation ===")
            
            # Test invalid operations
            test_cases = [
                {
                    "name": "Invalid operation for file system",
                    "root_id": "file_system",
                    "operation": "invalid_op",
                    "parameters": {"path": "/tmp/test.txt"}
                },
                {
                    "name": "Missing required parameter",
                    "root_id": "file_system",
                    "operation": "read",
                    "parameters": {}
                },
                {
                    "name": "Invalid HTTP method",
                    "root_id": "api",
                    "operation": "get",
                    "parameters": {"endpoint": "/test", "method": "INVALID"}
                },
                {
                    "name": "Invalid log level",
                    "root_id": "log",
                    "operation": "write",
                    "parameters": {"level": "INVALID", "message": "test"}
                },
                {
                    "name": "Invalid port number",
                    "root_id": "network",
                    "operation": "ping",
                    "parameters": {"host": "test.com", "port": 99999}
                }
            ]
            
            for test_case in test_cases:
                print(f"\n--- {test_case['name']} ---")
                result = await session.call_tool("validate_root_operation", {
                    "root_id": test_case["root_id"],
                    "operation": test_case["operation"],
                    "parameters": test_case["parameters"]
                })
                print(f"Validation result: {json.dumps(result, indent=2)}")


async def test_root_operations():
    """Test various root operations across different root types."""
    
    server_params = StdioServerParameters(
        command="python",
        args=["buildingblocks/mcp_roots_example.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, "mcp-roots-operations-client") as session:
            print("\n=== Testing Root Operations ===")
            
            # Test operations for each root type
            root_operations = [
                {
                    "name": "File System - List Directory",
                    "root_id": "file_system",
                    "operation": "list",
                    "parameters": {"path": "."}
                },
                {
                    "name": "Database - Insert Data",
                    "root_id": "database",
                    "operation": "insert",
                    "parameters": {"table": "users", "data": {"name": "John", "age": 30}}
                },
                {
                    "name": "API - POST Request",
                    "root_id": "api",
                    "operation": "post",
                    "parameters": {"endpoint": "/users", "method": "POST", "data": {"name": "Jane"}}
                },
                {
                    "name": "Memory - List Keys",
                    "root_id": "memory",
                    "operation": "list",
                    "parameters": {}
                },
                {
                    "name": "Network - Scan Ports",
                    "root_id": "network",
                    "operation": "scan",
                    "parameters": {"host": "localhost"}
                },
                {
                    "name": "Cloud Storage - List Objects",
                    "root_id": "cloud_storage",
                    "operation": "list",
                    "parameters": {"bucket": "my-bucket"}
                },
                {
                    "name": "Config - Write Value",
                    "root_id": "config",
                    "operation": "write",
                    "parameters": {"section": "app", "key": "debug", "value": "true"}
                },
                {
                    "name": "Log - Read Entries",
                    "root_id": "log",
                    "operation": "read",
                    "parameters": {"level": "INFO"}
                }
            ]
            
            for operation in root_operations:
                print(f"\n--- {operation['name']} ---")
                result = await session.call_tool("execute_root_operation", {
                    "root_id": operation["root_id"],
                    "operation": operation["operation"],
                    "parameters": operation["parameters"]
                })
                
                if result["status"] == "success":
                    print(f"Success: {result['operation']}")
                    if "result" in result:
                        print(f"Result: {result['result']}")
                    elif "response" in result:
                        print(f"Response: {result['response']}")
                else:
                    print(f"Error: {result['message']}")


async def test_root_management():
    """Test root management operations (create, update, delete)."""
    
    server_params = StdioServerParameters(
        command="python",
        args=["buildingblocks/mcp_roots_example.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, "mcp-roots-management-client") as session:
            print("\n=== Testing Root Management ===")
            
            # Test 1: Create a new root
            print("\n--- Creating Custom Root ---")
            result = await session.call_tool("create_root", {
                "root_id": "test_cache",
                "root_type": "cache",
                "uri": "cache://test",
                "description": "Test cache root",
                "capabilities": ["get", "set", "delete"],
                "validation": {
                    "required": ["key"],
                    "constraints": {
                        "key": "non_empty_string"
                    }
                }
            })
            print(f"Create result: {json.dumps(result, indent=2)}")
            
            # Test 2: List roots to see the new one
            print("\n--- Listing Roots After Creation ---")
            result = await session.call_tool("list_roots", {})
            print(f"Roots after creation: {json.dumps(result, indent=2)}")
            
            # Test 3: Update the root
            print("\n--- Updating Root ---")
            result = await session.call_tool("update_root", {
                "root_id": "test_cache",
                "updates": {
                    "description": "Updated test cache root",
                    "capabilities": ["get", "set", "delete", "clear"]
                }
            })
            print(f"Update result: {json.dumps(result, indent=2)}")
            
            # Test 4: Get the updated root
            print("\n--- Getting Updated Root ---")
            result = await session.call_tool("get_root", {"root_id": "test_cache"})
            print(f"Updated root: {json.dumps(result, indent=2)}")
            
            # Test 5: Delete the root
            print("\n--- Deleting Root ---")
            result = await session.call_tool("delete_root", {"root_id": "test_cache"})
            print(f"Delete result: {json.dumps(result, indent=2)}")
            
            # Test 6: Verify deletion
            print("\n--- Verifying Deletion ---")
            result = await session.call_tool("list_roots", {})
            print(f"Roots after deletion: {json.dumps(result, indent=2)}")


async def main():
    """Main function to run all roots tests."""
    print("Starting MCP Roots Client Tests")
    
    try:
        # Run basic tests
        await test_roots_server()
        
        # Run validation tests
        await test_root_validation()
        
        # Run operation tests
        await test_root_operations()
        
        # Run management tests
        await test_root_management()
        
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {e}")


if __name__ == "__main__":
    asyncio.run(main())
