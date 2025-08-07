"""
MCP Resources Example

This example demonstrates how to work with MCP resources including files,
directories, data, and resource watching capabilities.

Requirements:
- pip install mcp
"""

import asyncio
import json
import os
import tempfile
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from pathlib import Path
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    TextContent, 
    Resource, 
    ResourceUri, 
    ReadDirectoryRequest, 
    ReadDirectoryResult,
    GetResourceRequest,
    GetResourceResult,
    ListResourcesRequest,
    ListResourcesResult,
    WatchResourcesRequest,
    WatchResourcesResult,
    UnwatchResourcesRequest,
    UnwatchResourcesResult
)


# ============================================================================
# Resource Management
# ============================================================================

class ResourceManager:
    """Manages different types of resources."""
    
    def __init__(self):
        self.resources = {}
        self.watchers = {}
        self.setup_sample_resources()
        
    def setup_sample_resources(self):
        """Set up sample resources for demonstration."""
        # Create temporary directory for resources
        self.resource_dir = tempfile.mkdtemp(prefix="mcp_resources_")
        
        # Create sample files
        sample_files = {
            "config.json": {"name": "config", "version": "1.0", "debug": True},
            "data.csv": "name,age,city\nJohn,30,New York\nAlice,25,Los Angeles\nBob,35,Chicago",
            "log.txt": f"Application log\nStarted at {datetime.now().isoformat()}\nStatus: Running",
            "template.html": "<html><body><h1>Hello MCP Resources</h1></body></html>"
        }
        
        for filename, content in sample_files.items():
            filepath = os.path.join(self.resource_dir, filename)
            if isinstance(content, dict):
                with open(filepath, 'w') as f:
                    json.dump(content, f, indent=2)
            else:
                with open(filepath, 'w') as f:
                    f.write(str(content))
            
            # Register resource
            uri = f"file://{filepath}"
            self.resources[uri] = {
                "type": "file",
                "path": filepath,
                "name": filename,
                "size": os.path.getsize(filepath),
                "modified": datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
            }
    
    def get_resource_uri(self, path: str) -> str:
        """Convert path to resource URI."""
        return f"file://{os.path.abspath(path)}"
    
    def get_path_from_uri(self, uri: str) -> str:
        """Convert resource URI to file path."""
        return uri.replace("file://", "")
    
    def list_resources(self, directory: str = None) -> List[Resource]:
        """List available resources."""
        resources = []
        
        if directory is None:
            directory = self.resource_dir
        
        for uri, info in self.resources.items():
            if directory in info["path"]:
                resources.append(Resource(
                    uri=ResourceUri(uri),
                    name=info["name"],
                    type="file",
                    size=info["size"]
                ))
        
        return resources
    
    def read_resource(self, uri: str) -> Optional[Dict[str, Any]]:
        """Read a resource."""
        if uri not in self.resources:
            return None
        
        path = self.get_path_from_uri(uri)
        try:
            with open(path, 'r') as f:
                content = f.read()
            
            return {
                "content": content,
                "size": len(content),
                "type": "text",
                "uri": uri
            }
        except Exception as e:
            return {"error": str(e)}
    
    def write_resource(self, uri: str, content: str) -> Dict[str, Any]:
        """Write content to a resource."""
        path = self.get_path_from_uri(uri)
        try:
            with open(path, 'w') as f:
                f.write(content)
            
            # Update resource info
            self.resources[uri] = {
                "type": "file",
                "path": path,
                "name": os.path.basename(path),
                "size": len(content),
                "modified": datetime.now().isoformat()
            }
            
            return {"status": "success", "uri": uri, "size": len(content)}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def create_resource(self, name: str, content: str = "") -> Dict[str, Any]:
        """Create a new resource."""
        filepath = os.path.join(self.resource_dir, name)
        uri = self.get_resource_uri(filepath)
        
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            
            # Register new resource
            self.resources[uri] = {
                "type": "file",
                "path": filepath,
                "name": name,
                "size": len(content),
                "modified": datetime.now().isoformat()
            }
            
            return {"status": "success", "uri": uri, "name": name}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def delete_resource(self, uri: str) -> Dict[str, Any]:
        """Delete a resource."""
        if uri not in self.resources:
            return {"status": "error", "message": "Resource not found"}
        
        path = self.get_path_from_uri(uri)
        try:
            os.remove(path)
            del self.resources[uri]
            return {"status": "success", "uri": uri}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def watch_resource(self, uri: str) -> Dict[str, Any]:
        """Start watching a resource for changes."""
        if uri not in self.resources:
            return {"status": "error", "message": "Resource not found"}
        
        self.watchers[uri] = {
            "started_at": datetime.now().isoformat(),
            "last_modified": self.resources[uri]["modified"]
        }
        
        return {"status": "success", "uri": uri, "watching": True}
    
    def unwatch_resource(self, uri: str) -> Dict[str, Any]:
        """Stop watching a resource."""
        if uri in self.watchers:
            del self.watchers[uri]
            return {"status": "success", "uri": uri, "watching": False}
        else:
            return {"status": "error", "message": "Resource not being watched"}


# ============================================================================
# MCP Resource Tools
# ============================================================================

resource_manager = ResourceManager()


@tool("list_resources")
async def list_resources_tool(directory: str = None) -> Dict[str, Any]:
    """
    List available resources.
    
    Args:
        directory: Optional directory to list resources from
        
    Returns:
        Dictionary containing list of resources
    """
    try:
        resources = resource_manager.list_resources(directory)
        resource_list = []
        
        for resource in resources:
            resource_list.append({
                "uri": resource.uri,
                "name": resource.name,
                "type": resource.type,
                "size": resource.size
            })
        
        return {
            "status": "success",
            "resources": resource_list,
            "count": len(resource_list),
            "directory": directory or resource_manager.resource_dir
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("read_resource")
async def read_resource_tool(uri: str) -> Dict[str, Any]:
    """
    Read a resource.
    
    Args:
        uri: Resource URI to read
        
    Returns:
        Dictionary containing resource content
    """
    try:
        result = resource_manager.read_resource(uri)
        if result is None:
            return {"status": "error", "message": "Resource not found"}
        elif "error" in result:
            return {"status": "error", "message": result["error"]}
        else:
            return {
                "status": "success",
                "content": result["content"],
                "size": result["size"],
                "type": result["type"],
                "uri": uri
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("write_resource")
async def write_resource_tool(uri: str, content: str) -> Dict[str, Any]:
    """
    Write content to a resource.
    
    Args:
        uri: Resource URI to write to
        content: Content to write
        
    Returns:
        Dictionary containing operation result
    """
    try:
        result = resource_manager.write_resource(uri, content)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("create_resource")
async def create_resource_tool(name: str, content: str = "") -> Dict[str, Any]:
    """
    Create a new resource.
    
    Args:
        name: Name of the resource to create
        content: Initial content for the resource
        
    Returns:
        Dictionary containing operation result
    """
    try:
        result = resource_manager.create_resource(name, content)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("delete_resource")
async def delete_resource_tool(uri: str) -> Dict[str, Any]:
    """
    Delete a resource.
    
    Args:
        uri: Resource URI to delete
        
    Returns:
        Dictionary containing operation result
    """
    try:
        result = resource_manager.delete_resource(uri)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("watch_resource")
async def watch_resource_tool(uri: str) -> Dict[str, Any]:
    """
    Start watching a resource for changes.
    
    Args:
        uri: Resource URI to watch
        
    Returns:
        Dictionary containing operation result
    """
    try:
        result = resource_manager.watch_resource(uri)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("unwatch_resource")
async def unwatch_resource_tool(uri: str) -> Dict[str, Any]:
    """
    Stop watching a resource.
    
    Args:
        uri: Resource URI to stop watching
        
    Returns:
        Dictionary containing operation result
    """
    try:
        result = resource_manager.unwatch_resource(uri)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("resource_info")
async def resource_info_tool(uri: str = None) -> Dict[str, Any]:
    """
    Get information about resources.
    
    Args:
        uri: Optional specific resource URI
        
    Returns:
        Dictionary containing resource information
    """
    try:
        if uri:
            # Get specific resource info
            if uri in resource_manager.resources:
                info = resource_manager.resources[uri]
                return {
                    "status": "success",
                    "resource": {
                        "uri": uri,
                        "name": info["name"],
                        "type": info["type"],
                        "size": info["size"],
                        "modified": info["modified"],
                        "path": info["path"]
                    }
                }
            else:
                return {"status": "error", "message": "Resource not found"}
        else:
            # Get general resource info
            return {
                "status": "success",
                "resource_directory": resource_manager.resource_dir,
                "total_resources": len(resource_manager.resources),
                "watched_resources": len(resource_manager.watchers),
                "available_resources": list(resource_manager.resources.keys())
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============================================================================
# MCP Server Implementation
# ============================================================================

@server("mcp-resources-server")
class MCPResourcesServer:
    """MCP Server for resource management."""
    
    def __init__(self):
        self.server = Server("mcp-resources-server")
        
    async def initialize(self, options: InitializationOptions) -> None:
        """Initialize the server."""
        print(f"Initializing MCP Resources server: {options.server_name} v{options.server_version}")
        print(f"Resource directory: {resource_manager.resource_dir}")
        
    async def shutdown(self) -> None:
        """Shutdown the server."""
        print("Shutting down MCP Resources server")
        # Clean up temporary directory
        import shutil
        try:
            shutil.rmtree(resource_manager.resource_dir)
            print(f"Cleaned up resource directory: {resource_manager.resource_dir}")
        except Exception as e:
            print(f"Error cleaning up resource directory: {e}")


async def main():
    """Main function to run the MCP resources server."""
    server = MCPResourcesServer()
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-resources-server",
                server_version="1.0.0",
                capabilities=server.server.get_capabilities(
                    notification_options=None,
                    request_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
