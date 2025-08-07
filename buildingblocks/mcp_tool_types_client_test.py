"""
MCP Tool Types Client Test

This example demonstrates how to use the MCP tool types server with various
tool types and operations.

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


async def test_tool_types_server():
    """Test the MCP tool types server with various tool types and operations."""
    
    # Connect to the tool types server
    server_params = StdioServerParameters(
        command="python",
        args=["buildingblocks/mcp_tool_types_example.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, "mcp-tool-types-client") as session:
            print("Connected to MCP Tool Types Server")
            
            # Test 1: List all tools
            print("\n=== Test 1: List All Tools ===")
            result = await session.call_tool("list_tools", {})
            print(f"Available tools: {json.dumps(result, indent=2)}")
            
            # Test 2: Get specific tool details
            print("\n=== Test 2: Get Tool Details ===")
            result = await session.call_tool("get_tool", {"tool_id": "simple_calculator"})
            print(f"Simple calculator tool: {json.dumps(result, indent=2)}")
            
            # Test 3: Validate tool parameters
            print("\n=== Test 3: Validate Tool Parameters ===")
            result = await session.call_tool("validate_tool_parameters", {
                "tool_id": "simple_calculator",
                "parameters": {"operation": "add", "a": 5, "b": 3}
            })
            print(f"Validation result: {json.dumps(result, indent=2)}")
            
            # Test 4: Execute simple calculator
            print("\n=== Test 4: Execute Simple Calculator ===")
            result = await session.call_tool("execute_tool", {
                "tool_id": "simple_calculator",
                "parameters": {"operation": "add", "a": 10, "b": 5}
            })
            print(f"Calculator result: {json.dumps(result, indent=2)}")
            
            # Test 5: Execute data processor
            print("\n=== Test 5: Execute Data Processor ===")
            result = await session.call_tool("execute_tool", {
                "tool_id": "data_processor",
                "parameters": {
                    "data": [1, 2, 3, 4, 5],
                    "operation": "sum"
                }
            })
            print(f"Data processor result: {json.dumps(result, indent=2)}")
            
            # Test 6: Execute file operations
            print("\n=== Test 6: Execute File Operations ===")
            
            # Create a temporary file for testing
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
            temp_file.write("Hello MCP Tool Types!")
            temp_file.close()
            
            # Test file read
            result = await session.call_tool("execute_tool", {
                "tool_id": "file_operations",
                "parameters": {"operation": "read", "path": temp_file.name}
            })
            print(f"File read result: {json.dumps(result, indent=2)}")
            
            # Test file write
            result = await session.call_tool("execute_tool", {
                "tool_id": "file_operations",
                "parameters": {"operation": "write", "path": temp_file.name, "content": "Updated content!"}
            })
            print(f"File write result: {json.dumps(result, indent=2)}")
            
            # Clean up
            os.unlink(temp_file.name)
            
            # Test 7: Execute network scanner
            print("\n=== Test 7: Execute Network Scanner ===")
            result = await session.call_tool("execute_tool", {
                "tool_id": "network_scanner",
                "parameters": {
                    "host": "google.com",
                    "ports": [80, 443, 22, 8080],
                    "timeout": 10
                }
            })
            print(f"Network scanner result: {json.dumps(result, indent=2)}")
            
            # Test 8: Execute database query
            print("\n=== Test 8: Execute Database Query ===")
            result = await session.call_tool("execute_tool", {
                "tool_id": "database_query",
                "parameters": {
                    "query": "SELECT * FROM users WHERE age > 18",
                    "parameters": {"age": 18},
                    "timeout": 30
                }
            })
            print(f"Database query result: {json.dumps(result, indent=2)}")
            
            # Test 9: Execute API client
            print("\n=== Test 9: Execute API Client ===")
            result = await session.call_tool("execute_tool", {
                "tool_id": "api_client",
                "parameters": {
                    "url": "https://api.example.com/users",
                    "method": "GET",
                    "headers": {"Authorization": "Bearer token123"},
                    "data": {}
                }
            })
            print(f"API client result: {json.dumps(result, indent=2)}")
            
            # Test 10: Execute data validator
            print("\n=== Test 10: Execute Data Validator ===")
            result = await session.call_tool("execute_tool", {
                "tool_id": "data_validator",
                "parameters": {
                    "data": {"name": "John", "age": 30, "email": "john@example.com"},
                    "schema": {
                        "name": {"type": "string", "required": True},
                        "age": {"type": "number", "required": True},
                        "email": {"type": "string", "required": True}
                    },
                    "strict": True
                }
            })
            print(f"Data validator result: {json.dumps(result, indent=2)}")
            
            # Test 11: Execute data transformer
            print("\n=== Test 11: Execute Data Transformer ===")
            result = await session.call_tool("execute_tool", {
                "tool_id": "data_transformer",
                "parameters": {
                    "data": {"name": "John", "age": 30},
                    "format": "json",
                    "direction": "to"
                }
            })
            print(f"Data transformer result: {json.dumps(result, indent=2)}")
            
            # Test 12: Execute ML predictor
            print("\n=== Test 12: Execute ML Predictor ===")
            result = await session.call_tool("execute_tool", {
                "tool_id": "ml_predictor",
                "parameters": {
                    "model": "linear_regression",
                    "features": [1.0, 2.0, 3.0, 4.0],
                    "confidence": True
                }
            })
            print(f"ML predictor result: {json.dumps(result, indent=2)}")
            
            # Test 13: Execute security scanner
            print("\n=== Test 13: Execute Security Scanner ===")
            result = await session.call_tool("execute_tool", {
                "tool_id": "security_scanner",
                "parameters": {
                    "target": "example.com",
                    "scan_type": "vulnerability",
                    "options": {"depth": "full", "timeout": 300}
                }
            })
            print(f"Security scanner result: {json.dumps(result, indent=2)}")
            
            # Test 14: Execute system monitor
            print("\n=== Test 14: Execute System Monitor ===")
            result = await session.call_tool("execute_tool", {
                "tool_id": "system_monitor",
                "parameters": {
                    "metric": "cpu",
                    "duration": 60
                }
            })
            print(f"System monitor result: {json.dumps(result, indent=2)}")
            
            # Test 15: Create custom tool
            print("\n=== Test 15: Create Custom Tool ===")
            result = await session.call_tool("create_tool", {
                "tool_id": "custom_string_processor",
                "tool_type": "string",
                "name": "String Processor",
                "description": "Process and manipulate strings",
                "parameters": {
                    "text": {"type": "string", "required": True, "description": "Input text"},
                    "operation": {"type": "string", "required": True, "enum": ["uppercase", "lowercase", "reverse", "length"]}
                },
                "return_type": "string",
                "category": "text_processing"
            })
            print(f"Create tool result: {json.dumps(result, indent=2)}")
            
            # Test 16: Get tool system info
            print("\n=== Test 16: Get System Info ===")
            result = await session.call_tool("tool_info", {})
            print(f"System info: {json.dumps(result, indent=2)}")
            
            print("\n=== All Tests Completed ===")


async def test_tool_validation():
    """Test tool parameter validation with invalid parameters."""
    
    server_params = StdioServerParameters(
        command="python",
        args=["buildingblocks/mcp_tool_types_example.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, "mcp-tool-types-validation-client") as session:
            print("\n=== Testing Tool Parameter Validation ===")
            
            # Test invalid parameters
            test_cases = [
                {
                    "name": "Missing required parameter",
                    "tool_id": "simple_calculator",
                    "parameters": {"operation": "add", "a": 5}
                },
                {
                    "name": "Invalid parameter type",
                    "tool_id": "simple_calculator",
                    "parameters": {"operation": "add", "a": "invalid", "b": 3}
                },
                {
                    "name": "Invalid enum value",
                    "tool_id": "simple_calculator",
                    "parameters": {"operation": "invalid_op", "a": 5, "b": 3}
                },
                {
                    "name": "Invalid data type for array",
                    "tool_id": "data_processor",
                    "parameters": {"data": "not_an_array", "operation": "sum"}
                },
                {
                    "name": "Invalid HTTP method",
                    "tool_id": "api_client",
                    "parameters": {"url": "https://example.com", "method": "INVALID"}
                }
            ]
            
            for test_case in test_cases:
                print(f"\n--- {test_case['name']} ---")
                result = await session.call_tool("validate_tool_parameters", {
                    "tool_id": test_case["tool_id"],
                    "parameters": test_case["parameters"]
                })
                print(f"Validation result: {json.dumps(result, indent=2)}")


async def test_tool_categories():
    """Test tools by category and type."""
    
    server_params = StdioServerParameters(
        command="python",
        args=["buildingblocks/mcp_tool_types_example.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, "mcp-tool-types-categories-client") as session:
            print("\n=== Testing Tool Categories ===")
            
            # Test different categories
            categories = ["mathematics", "data_analysis", "file_system", "networking", "database", "api", "validation", "transformation", "machine_learning", "security", "monitoring"]
            
            for category in categories:
                print(f"\n--- Tools in category: {category} ---")
                result = await session.call_tool("list_tools", {"category": category})
                print(f"Tools: {json.dumps(result, indent=2)}")
            
            # Test different tool types
            tool_types = ["simple", "complex", "file", "network", "database", "api", "validation", "transformation", "machine_learning", "security", "monitoring"]
            
            for tool_type in tool_types:
                print(f"\n--- Tools of type: {tool_type} ---")
                result = await session.call_tool("list_tools", {"tool_type": tool_type})
                print(f"Tools: {json.dumps(result, indent=2)}")


async def test_tool_management():
    """Test tool management operations (create, update, delete)."""
    
    server_params = StdioServerParameters(
        command="python",
        args=["buildingblocks/mcp_tool_types_example.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, "mcp-tool-types-management-client") as session:
            print("\n=== Testing Tool Management ===")
            
            # Test 1: Create a new tool
            print("\n--- Creating Custom Tool ---")
            result = await session.call_tool("create_tool", {
                "tool_id": "test_image_processor",
                "tool_type": "image",
                "name": "Image Processor",
                "description": "Process and manipulate images",
                "parameters": {
                    "image_path": {"type": "string", "required": True, "description": "Path to image file"},
                    "operation": {"type": "string", "required": True, "enum": ["resize", "rotate", "filter", "convert"]},
                    "options": {"type": "object", "required": False, "description": "Processing options"}
                },
                "return_type": "object",
                "category": "image_processing"
            })
            print(f"Create result: {json.dumps(result, indent=2)}")
            
            # Test 2: List tools to see the new one
            print("\n--- Listing Tools After Creation ---")
            result = await session.call_tool("list_tools", {})
            print(f"Tools after creation: {json.dumps(result, indent=2)}")
            
            # Test 3: Update the tool
            print("\n--- Updating Tool ---")
            result = await session.call_tool("update_tool", {
                "tool_id": "test_image_processor",
                "updates": {
                    "description": "Updated image processor tool",
                    "parameters": {
                        "image_path": {"type": "string", "required": True, "description": "Path to image file"},
                        "operation": {"type": "string", "required": True, "enum": ["resize", "rotate", "filter", "convert", "crop"]},
                        "options": {"type": "object", "required": False, "description": "Processing options"},
                        "output_format": {"type": "string", "required": False, "enum": ["jpg", "png", "gif"], "description": "Output format"}
                    }
                }
            })
            print(f"Update result: {json.dumps(result, indent=2)}")
            
            # Test 4: Get the updated tool
            print("\n--- Getting Updated Tool ---")
            result = await session.call_tool("get_tool", {"tool_id": "test_image_processor"})
            print(f"Updated tool: {json.dumps(result, indent=2)}")
            
            # Test 5: Delete the tool
            print("\n--- Deleting Tool ---")
            result = await session.call_tool("delete_tool", {"tool_id": "test_image_processor"})
            print(f"Delete result: {json.dumps(result, indent=2)}")
            
            # Test 6: Verify deletion
            print("\n--- Verifying Deletion ---")
            result = await session.call_tool("list_tools", {})
            print(f"Tools after deletion: {json.dumps(result, indent=2)}")


async def test_tool_execution():
    """Test various tool executions across different tool types."""
    
    server_params = StdioServerParameters(
        command="python",
        args=["buildingblocks/mcp_tool_types_example.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, "mcp-tool-types-execution-client") as session:
            print("\n=== Testing Tool Executions ===")
            
            # Test executions for each tool type
            tool_executions = [
                {
                    "name": "Simple Calculator - Multiplication",
                    "tool_id": "simple_calculator",
                    "parameters": {"operation": "multiply", "a": 6, "b": 7}
                },
                {
                    "name": "Data Processor - Average",
                    "tool_id": "data_processor",
                    "parameters": {"data": [10, 20, 30, 40, 50], "operation": "average"}
                },
                {
                    "name": "Network Scanner - Port Scan",
                    "tool_id": "network_scanner",
                    "parameters": {"host": "localhost", "ports": [22, 80, 443, 3306]}
                },
                {
                    "name": "Database Query - Complex Query",
                    "tool_id": "database_query",
                    "parameters": {"query": "SELECT name, age FROM users WHERE active = true ORDER BY age DESC", "timeout": 60}
                },
                {
                    "name": "API Client - POST Request",
                    "tool_id": "api_client",
                    "parameters": {"url": "https://api.example.com/users", "method": "POST", "data": {"name": "Alice", "email": "alice@example.com"}}
                },
                {
                    "name": "Data Validator - Schema Validation",
                    "tool_id": "data_validator",
                    "parameters": {
                        "data": {"id": 1, "name": "Test", "active": True},
                        "schema": {
                            "id": {"type": "number", "required": True},
                            "name": {"type": "string", "required": True},
                            "active": {"type": "boolean", "required": False}
                        }
                    }
                },
                {
                    "name": "Data Transformer - JSON to XML",
                    "tool_id": "data_transformer",
                    "parameters": {"data": {"user": {"name": "John", "age": 30}}, "format": "xml", "direction": "to"}
                },
                {
                    "name": "ML Predictor - Classification",
                    "tool_id": "ml_predictor",
                    "parameters": {"model": "random_forest", "features": [1.2, 3.4, 5.6, 7.8], "confidence": True}
                },
                {
                    "name": "Security Scanner - Web Scan",
                    "tool_id": "security_scanner",
                    "parameters": {"target": "https://example.com", "scan_type": "web", "options": {"depth": "deep"}}
                },
                {
                    "name": "System Monitor - Memory Usage",
                    "tool_id": "system_monitor",
                    "parameters": {"metric": "memory", "duration": 120}
                }
            ]
            
            for execution in tool_executions:
                print(f"\n--- {execution['name']} ---")
                result = await session.call_tool("execute_tool", {
                    "tool_id": execution["tool_id"],
                    "parameters": execution["parameters"]
                })
                
                if result["status"] == "success":
                    print(f"Success: {result.get('result', result.get('response', 'Operation completed'))}")
                else:
                    print(f"Error: {result['message']}")


async def main():
    """Main function to run all tool types tests."""
    print("Starting MCP Tool Types Client Tests")
    
    try:
        # Run basic tests
        await test_tool_types_server()
        
        # Run validation tests
        await test_tool_validation()
        
        # Run category tests
        await test_tool_categories()
        
        # Run management tests
        await test_tool_management()
        
        # Run execution tests
        await test_tool_execution()
        
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {e}")


if __name__ == "__main__":
    asyncio.run(main())
