"""
FastMCP Client Test Example

This example demonstrates how to create a client that connects to a FastMCP server
and uses its tools. This shows the modern FastMCP approach.

Requirements:
- pip install fastmcp
- Run the FastMCP server first: python fastmcp_server_example.py
"""

import asyncio
import json
from typing import Any, Dict, List
from fastmcp import FastMCPClient


class FastMCPClientTest:
    """FastMCP Client for testing the server."""
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        self.server_url = server_url
        self.client = None
        
    async def connect(self):
        """Connect to the FastMCP server."""
        self.client = FastMCPClient(self.server_url)
        await self.client.connect()
        print("Connected to FastMCP server successfully!")
        
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools from the server."""
        if not self.client:
            raise RuntimeError("Not connected to server")
            
        tools = await self.client.list_tools()
        return tools
        
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call a specific tool on the server."""
        if not self.client:
            raise RuntimeError("Not connected to server")
            
        result = await self.client.call_tool(tool_name, arguments)
        return json.dumps(result, indent=2)
        
    async def close(self):
        """Close the connection to the server."""
        if self.client:
            await self.client.close()


async def test_fastmcp_client():
    """Test the FastMCP client with various operations."""
    
    # Create client
    client = FastMCPClientTest()
    
    try:
        # Connect to the server
        await client.connect()
        
        # List available tools
        print("\n=== Available Tools ===")
        tools = await client.list_tools()
        for tool in tools:
            print(f"- {tool['name']}: {tool['description']}")
            print(f"  Schema: {tool['inputSchema']}")
            
        # Test calculator tool
        print("\n=== Testing Calculator Tool ===")
        calc_operations = [
            {"operation": "add", "a": 10, "b": 5},
            {"operation": "multiply", "a": 7, "b": 8},
            {"operation": "subtract", "a": 20, "b": 3},
            {"operation": "divide", "a": 100, "b": 4}
        ]
        
        for op in calc_operations:
            result = await client.call_tool("calculator", op)
            print(f"{op['operation']} result: {result}")
            
        # Test weather tool
        print("\n=== Testing Weather Tool ===")
        locations = ["New York", "London", "Tokyo"]
        for location in locations:
            result = await client.call_tool("weather", {"location": location})
            print(f"Weather for {location}: {result}")
            
        # Test file operations tool
        print("\n=== Testing File Operations Tool ===")
        
        # Write a file
        write_args = {
            "operation": "write",
            "filename": "test_file.txt",
            "content": "Hello from FastMCP server!"
        }
        result = await client.call_tool("file_operations", write_args)
        print(f"Write result: {result}")
        
        # Read the file
        read_args = {
            "operation": "read",
            "filename": "test_file.txt"
        }
        result = await client.call_tool("file_operations", read_args)
        print(f"Read result: {result}")
        
        # Delete the file
        delete_args = {
            "operation": "delete",
            "filename": "test_file.txt"
        }
        result = await client.call_tool("file_operations", delete_args)
        print(f"Delete result: {result}")
        
        # Test system info tool
        print("\n=== Testing System Info Tool ===")
        result = await client.call_tool("system_info", {})
        print(f"System info: {result}")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the FastMCP server is running first!")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(test_fastmcp_client())
