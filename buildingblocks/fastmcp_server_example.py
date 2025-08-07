"""
FastMCP Server Example

This example demonstrates how to create an MCP server using FastMCP,
a modern, fast implementation of the Model Context Protocol.

Requirements:
- pip install fastmcp
"""

import asyncio
import json
import os
from typing import Dict, Any, List
from fastmcp import FastMCP, tool, server


@tool("calculator")
async def calculator_tool(operation: str, a: float, b: float) -> Dict[str, Any]:
    """
    Perform basic mathematical operations.
    
    Args:
        operation: The operation to perform (add, subtract, multiply, divide)
        a: First number
        b: Second number
        
    Returns:
        Dictionary containing the result
    """
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
    else:
        raise ValueError(f"Unknown operation: {operation}")
        
    return {"result": result}


@tool("weather")
async def weather_tool(location: str) -> Dict[str, Any]:
    """
    Get weather information for a location.
    
    Args:
        location: The location to get weather for
        
    Returns:
        Dictionary containing weather information
    """
    # Mock weather data
    weather_data = {
        "location": location,
        "temperature": "22°C",
        "condition": "Sunny",
        "humidity": "65%",
        "wind": "10 km/h"
    }
    
    return weather_data


@tool("file_operations")
async def file_operations_tool(operation: str, filename: str, content: str = "") -> Dict[str, Any]:
    """
    Perform file operations (read, write, delete).
    
    Args:
        operation: The operation to perform (read, write, delete)
        filename: The name of the file
        content: Content to write (for write operation)
        
    Returns:
        Dictionary containing the result
    """
    if operation == "read":
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                content = f.read()
            return {"status": "success", "content": content}
        else:
            return {"status": "error", "message": "File not found"}
            
    elif operation == "write":
        try:
            with open(filename, 'w') as f:
                f.write(content)
            return {"status": "success", "message": f"File {filename} written successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
            
    elif operation == "delete":
        try:
            if os.path.exists(filename):
                os.remove(filename)
                return {"status": "success", "message": f"File {filename} deleted successfully"}
            else:
                return {"status": "error", "message": "File not found"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
            
    else:
        return {"status": "error", "message": f"Unknown operation: {operation}"}


@tool("system_info")
async def system_info_tool() -> Dict[str, Any]:
    """
    Get system information.
    
    Returns:
        Dictionary containing system information
    """
    import platform
    import psutil
    
    try:
        system_info = {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "cpu_count": psutil.cpu_count(),
            "memory_total": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            "memory_available": f"{psutil.virtual_memory().available / (1024**3):.2f} GB",
            "disk_usage": f"{psutil.disk_usage('/').percent:.1f}%"
        }
        return system_info
    except ImportError:
        return {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "note": "psutil not available for detailed system info"
        }


@server("fastmcp-example-server")
class FastMCPServer:
    """FastMCP Server implementation."""
    
    def __init__(self):
        self.name = "fastmcp-example-server"
        self.version = "1.0.0"
        
    async def initialize(self) -> None:
        """Initialize the server."""
        print(f"Initializing FastMCP server: {self.name} v{self.version}")
        
    async def shutdown(self) -> None:
        """Shutdown the server."""
        print("Shutting down FastMCP server")


async def main():
    """Main function to run the FastMCP server."""
    
    # Create FastMCP instance
    fastmcp = FastMCP()
    
    # Register the server
    server_instance = FastMCPServer()
    fastmcp.register_server(server_instance)
    
    # Run the server
    await fastmcp.run()


if __name__ == "__main__":
    asyncio.run(main())
