"""
MCP Roots Example

This example demonstrates how to work with MCP roots including different
types of roots, root management, root validation, and root operations.

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
    Root,
    RootUri,
    RootType,
    RootValidation,
    RootResult
)


# ============================================================================
# Root Management
# ============================================================================

class RootManager:
    """Manages different types of roots and their operations."""
    
    def __init__(self):
        self.roots = {}
        self.root_types = {}
        self.root_operations = {}
        self.setup_sample_roots()
        
    def setup_sample_roots(self):
        """Set up sample roots for demonstration."""
        # File system roots
        self.roots["file_system"] = {
            "type": "file_system",
            "uri": "file:///",
            "description": "File system root for file operations",
            "capabilities": ["read", "write", "list", "delete"],
            "validation": {
                "required": ["path"],
                "constraints": {
                    "path": "valid_file_path"
                }
            }
        }
        
        # Database roots
        self.roots["database"] = {
            "type": "database",
            "uri": "db://localhost:5432",
            "description": "Database root for database operations",
            "capabilities": ["query", "insert", "update", "delete"],
            "validation": {
                "required": ["table", "query"],
                "constraints": {
                    "table": "valid_table_name",
                    "query": "valid_sql_query"
                }
            }
        }
        
        # API roots
        self.roots["api"] = {
            "type": "api",
            "uri": "https://api.example.com",
            "description": "API root for external service operations",
            "capabilities": ["get", "post", "put", "delete"],
            "validation": {
                "required": ["endpoint", "method"],
                "constraints": {
                    "endpoint": "valid_api_endpoint",
                    "method": "valid_http_method"
                }
            }
        }
        
        # Memory roots
        self.roots["memory"] = {
            "type": "memory",
            "uri": "memory://",
            "description": "In-memory root for temporary data",
            "capabilities": ["store", "retrieve", "delete", "list"],
            "validation": {
                "required": ["key"],
                "constraints": {
                    "key": "valid_memory_key"
                }
            }
        }
        
        # Network roots
        self.roots["network"] = {
            "type": "network",
            "uri": "network://",
            "description": "Network root for network operations",
            "capabilities": ["ping", "scan", "connect", "monitor"],
            "validation": {
                "required": ["host"],
                "constraints": {
                    "host": "valid_host_address",
                    "port": "valid_port_number"
                }
            }
        }
        
        # Cloud storage roots
        self.roots["cloud_storage"] = {
            "type": "cloud_storage",
            "uri": "s3://bucket-name",
            "description": "Cloud storage root for cloud operations",
            "capabilities": ["upload", "download", "list", "delete"],
            "validation": {
                "required": ["bucket", "object_key"],
                "constraints": {
                    "bucket": "valid_bucket_name",
                    "object_key": "valid_object_key"
                }
            }
        }
        
        # Configuration roots
        self.roots["config"] = {
            "type": "config",
            "uri": "config://",
            "description": "Configuration root for settings management",
            "capabilities": ["read", "write", "validate", "backup"],
            "validation": {
                "required": ["section", "key"],
                "constraints": {
                    "section": "valid_config_section",
                    "key": "valid_config_key"
                }
            }
        }
        
        # Log roots
        self.roots["log"] = {
            "type": "log",
            "uri": "log://",
            "description": "Log root for logging operations",
            "capabilities": ["write", "read", "rotate", "archive"],
            "validation": {
                "required": ["level", "message"],
                "constraints": {
                    "level": "valid_log_level",
                    "message": "non_empty_string"
                }
            }
        }
    
    def get_root(self, root_id: str) -> Optional[Dict[str, Any]]:
        """Get a root by ID."""
        return self.roots.get(root_id)
    
    def list_roots(self, root_type: str = None) -> List[Dict[str, Any]]:
        """List available roots."""
        results = []
        
        for root_id, root in self.roots.items():
            if root_type and root.get("type") != root_type:
                continue
            
            results.append({
                "id": root_id,
                "type": root["type"],
                "uri": root["uri"],
                "description": root["description"],
                "capabilities": root["capabilities"],
                "validation": root.get("validation", {})
            })
        
        return results
    
    def validate_root_operation(self, root_id: str, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a root operation."""
        root = self.get_root(root_id)
        if not root:
            return {"valid": False, "error": "Root not found"}
        
        # Check if operation is supported
        if operation not in root["capabilities"]:
            return {
                "valid": False,
                "error": f"Operation '{operation}' not supported by root '{root_id}'",
                "supported_operations": root["capabilities"]
            }
        
        # Validate parameters based on root type
        validation_rules = root.get("validation", {})
        required_params = validation_rules.get("required", [])
        constraints = validation_rules.get("constraints", {})
        
        # Check required parameters
        missing_params = [param for param in required_params if param not in parameters]
        if missing_params:
            return {
                "valid": False,
                "error": f"Missing required parameters: {missing_params}",
                "missing_parameters": missing_params
            }
        
        # Check parameter constraints
        for param_name, constraint in constraints.items():
            if param_name in parameters:
                param_value = parameters[param_name]
                
                if constraint == "valid_file_path":
                    if not isinstance(param_value, str) or not param_value.strip():
                        return {
                            "valid": False,
                            "error": f"Parameter {param_name} must be a valid file path",
                            "invalid_parameter": param_name,
                            "expected": "valid_file_path"
                        }
                
                elif constraint == "valid_table_name":
                    if not isinstance(param_value, str) or not param_value.strip():
                        return {
                            "valid": False,
                            "error": f"Parameter {param_name} must be a valid table name",
                            "invalid_parameter": param_name,
                            "expected": "valid_table_name"
                        }
                
                elif constraint == "valid_sql_query":
                    if not isinstance(param_value, str) or not param_value.strip():
                        return {
                            "valid": False,
                            "error": f"Parameter {param_name} must be a valid SQL query",
                            "invalid_parameter": param_name,
                            "expected": "valid_sql_query"
                        }
                
                elif constraint == "valid_api_endpoint":
                    if not isinstance(param_value, str) or not param_value.strip():
                        return {
                            "valid": False,
                            "error": f"Parameter {param_name} must be a valid API endpoint",
                            "invalid_parameter": param_name,
                            "expected": "valid_api_endpoint"
                        }
                
                elif constraint == "valid_http_method":
                    valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
                    if param_value not in valid_methods:
                        return {
                            "valid": False,
                            "error": f"Parameter {param_name} must be a valid HTTP method",
                            "invalid_parameter": param_name,
                            "expected": "valid_http_method",
                            "valid_methods": valid_methods
                        }
                
                elif constraint == "valid_memory_key":
                    if not isinstance(param_value, str) or not param_value.strip():
                        return {
                            "valid": False,
                            "error": f"Parameter {param_name} must be a valid memory key",
                            "invalid_parameter": param_name,
                            "expected": "valid_memory_key"
                        }
                
                elif constraint == "valid_host_address":
                    if not isinstance(param_value, str) or not param_value.strip():
                        return {
                            "valid": False,
                            "error": f"Parameter {param_name} must be a valid host address",
                            "invalid_parameter": param_name,
                            "expected": "valid_host_address"
                        }
                
                elif constraint == "valid_port_number":
                    if not isinstance(param_value, int) or param_value < 1 or param_value > 65535:
                        return {
                            "valid": False,
                            "error": f"Parameter {param_name} must be a valid port number (1-65535)",
                            "invalid_parameter": param_name,
                            "expected": "valid_port_number"
                        }
                
                elif constraint == "valid_bucket_name":
                    if not isinstance(param_value, str) or not param_value.strip():
                        return {
                            "valid": False,
                            "error": f"Parameter {param_name} must be a valid bucket name",
                            "invalid_parameter": param_name,
                            "expected": "valid_bucket_name"
                        }
                
                elif constraint == "valid_object_key":
                    if not isinstance(param_value, str) or not param_value.strip():
                        return {
                            "valid": False,
                            "error": f"Parameter {param_name} must be a valid object key",
                            "invalid_parameter": param_name,
                            "expected": "valid_object_key"
                        }
                
                elif constraint == "valid_config_section":
                    if not isinstance(param_value, str) or not param_value.strip():
                        return {
                            "valid": False,
                            "error": f"Parameter {param_name} must be a valid config section",
                            "invalid_parameter": param_name,
                            "expected": "valid_config_section"
                        }
                
                elif constraint == "valid_config_key":
                    if not isinstance(param_value, str) or not param_value.strip():
                        return {
                            "valid": False,
                            "error": f"Parameter {param_name} must be a valid config key",
                            "invalid_parameter": param_name,
                            "expected": "valid_config_key"
                        }
                
                elif constraint == "valid_log_level":
                    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
                    if param_value not in valid_levels:
                        return {
                            "valid": False,
                            "error": f"Parameter {param_name} must be a valid log level",
                            "invalid_parameter": param_name,
                            "expected": "valid_log_level",
                            "valid_levels": valid_levels
                        }
                
                elif constraint == "non_empty_string":
                    if not isinstance(param_value, str) or not param_value.strip():
                        return {
                            "valid": False,
                            "error": f"Parameter {param_name} must be a non-empty string",
                            "invalid_parameter": param_name,
                            "expected": "non_empty_string"
                        }
        
        return {"valid": True}
    
    def execute_root_operation(self, root_id: str, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an operation on a root."""
        root = self.get_root(root_id)
        if not root:
            return {"status": "error", "message": "Root not found"}
        
        # Validate operation
        validation = self.validate_root_operation(root_id, operation, parameters)
        if not validation["valid"]:
            return {"status": "error", "validation": validation}
        
        try:
            if root_id == "file_system":
                return self._execute_file_system_operation(operation, parameters)
            elif root_id == "database":
                return self._execute_database_operation(operation, parameters)
            elif root_id == "api":
                return self._execute_api_operation(operation, parameters)
            elif root_id == "memory":
                return self._execute_memory_operation(operation, parameters)
            elif root_id == "network":
                return self._execute_network_operation(operation, parameters)
            elif root_id == "cloud_storage":
                return self._execute_cloud_storage_operation(operation, parameters)
            elif root_id == "config":
                return self._execute_config_operation(operation, parameters)
            elif root_id == "log":
                return self._execute_log_operation(operation, parameters)
            else:
                return {"status": "error", "message": "Unknown root type"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _execute_file_system_operation(self, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute file system operations."""
        path = parameters.get("path", "")
        
        if operation == "read":
            try:
                with open(path, 'r') as f:
                    content = f.read()
                return {
                    "status": "success",
                    "operation": "read",
                    "path": path,
                    "content": content,
                    "size": len(content)
                }
            except Exception as e:
                return {"status": "error", "message": f"Error reading file: {e}"}
        
        elif operation == "write":
            content = parameters.get("content", "")
            try:
                with open(path, 'w') as f:
                    f.write(content)
                return {
                    "status": "success",
                    "operation": "write",
                    "path": path,
                    "size": len(content)
                }
            except Exception as e:
                return {"status": "error", "message": f"Error writing file: {e}"}
        
        elif operation == "list":
            try:
                items = os.listdir(path)
                return {
                    "status": "success",
                    "operation": "list",
                    "path": path,
                    "items": items,
                    "count": len(items)
                }
            except Exception as e:
                return {"status": "error", "message": f"Error listing directory: {e}"}
        
        elif operation == "delete":
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    import shutil
                    shutil.rmtree(path)
                return {
                    "status": "success",
                    "operation": "delete",
                    "path": path
                }
            except Exception as e:
                return {"status": "error", "message": f"Error deleting: {e}"}
        
        return {"status": "error", "message": f"Unknown operation: {operation}"}
    
    def _execute_database_operation(self, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute database operations."""
        table = parameters.get("table", "")
        query = parameters.get("query", "")
        
        # Simulate database operations
        if operation == "query":
            return {
                "status": "success",
                "operation": "query",
                "table": table,
                "query": query,
                "result": f"Simulated query result from {table}",
                "rows_affected": 5
            }
        
        elif operation == "insert":
            return {
                "status": "success",
                "operation": "insert",
                "table": table,
                "data": parameters.get("data", {}),
                "rows_affected": 1
            }
        
        elif operation == "update":
            return {
                "status": "success",
                "operation": "update",
                "table": table,
                "query": query,
                "rows_affected": 3
            }
        
        elif operation == "delete":
            return {
                "status": "success",
                "operation": "delete",
                "table": table,
                "query": query,
                "rows_affected": 2
            }
        
        return {"status": "error", "message": f"Unknown operation: {operation}"}
    
    def _execute_api_operation(self, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute API operations."""
        endpoint = parameters.get("endpoint", "")
        method = parameters.get("method", "GET")
        data = parameters.get("data", {})
        
        # Simulate API operations
        return {
            "status": "success",
            "operation": operation,
            "endpoint": endpoint,
            "method": method,
            "data": data,
            "response": f"Simulated {method} response from {endpoint}",
            "status_code": 200
        }
    
    def _execute_memory_operation(self, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute memory operations."""
        key = parameters.get("key", "")
        
        if operation == "store":
            value = parameters.get("value", "")
            # Simulate storing in memory
            return {
                "status": "success",
                "operation": "store",
                "key": key,
                "value": value
            }
        
        elif operation == "retrieve":
            # Simulate retrieving from memory
            return {
                "status": "success",
                "operation": "retrieve",
                "key": key,
                "value": f"Simulated value for key: {key}"
            }
        
        elif operation == "delete":
            return {
                "status": "success",
                "operation": "delete",
                "key": key
            }
        
        elif operation == "list":
            # Simulate listing memory keys
            return {
                "status": "success",
                "operation": "list",
                "keys": ["key1", "key2", "key3"]
            }
        
        return {"status": "error", "message": f"Unknown operation: {operation}"}
    
    def _execute_network_operation(self, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute network operations."""
        host = parameters.get("host", "")
        port = parameters.get("port", 80)
        
        if operation == "ping":
            return {
                "status": "success",
                "operation": "ping",
                "host": host,
                "response_time": 15.5,
                "status": "reachable"
            }
        
        elif operation == "scan":
            return {
                "status": "success",
                "operation": "scan",
                "host": host,
                "open_ports": [22, 80, 443],
                "scan_time": 2.3
            }
        
        elif operation == "connect":
            return {
                "status": "success",
                "operation": "connect",
                "host": host,
                "port": port,
                "connection_status": "established"
            }
        
        elif operation == "monitor":
            return {
                "status": "success",
                "operation": "monitor",
                "host": host,
                "uptime": 99.8,
                "response_time": 12.3
            }
        
        return {"status": "error", "message": f"Unknown operation: {operation}"}
    
    def _execute_cloud_storage_operation(self, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute cloud storage operations."""
        bucket = parameters.get("bucket", "")
        object_key = parameters.get("object_key", "")
        
        if operation == "upload":
            return {
                "status": "success",
                "operation": "upload",
                "bucket": bucket,
                "object_key": object_key,
                "size": parameters.get("size", 1024)
            }
        
        elif operation == "download":
            return {
                "status": "success",
                "operation": "download",
                "bucket": bucket,
                "object_key": object_key,
                "content": f"Simulated content from {bucket}/{object_key}"
            }
        
        elif operation == "list":
            return {
                "status": "success",
                "operation": "list",
                "bucket": bucket,
                "objects": ["file1.txt", "file2.jpg", "file3.pdf"]
            }
        
        elif operation == "delete":
            return {
                "status": "success",
                "operation": "delete",
                "bucket": bucket,
                "object_key": object_key
            }
        
        return {"status": "error", "message": f"Unknown operation: {operation}"}
    
    def _execute_config_operation(self, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute configuration operations."""
        section = parameters.get("section", "")
        key = parameters.get("key", "")
        
        if operation == "read":
            return {
                "status": "success",
                "operation": "read",
                "section": section,
                "key": key,
                "value": f"Simulated config value for {section}.{key}"
            }
        
        elif operation == "write":
            value = parameters.get("value", "")
            return {
                "status": "success",
                "operation": "write",
                "section": section,
                "key": key,
                "value": value
            }
        
        elif operation == "validate":
            return {
                "status": "success",
                "operation": "validate",
                "section": section,
                "valid": True,
                "errors": []
            }
        
        elif operation == "backup":
            return {
                "status": "success",
                "operation": "backup",
                "backup_path": f"/backup/config_{datetime.now().isoformat()}.json"
            }
        
        return {"status": "error", "message": f"Unknown operation: {operation}"}
    
    def _execute_log_operation(self, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute logging operations."""
        level = parameters.get("level", "INFO")
        message = parameters.get("message", "")
        
        if operation == "write":
            return {
                "status": "success",
                "operation": "write",
                "level": level,
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
        
        elif operation == "read":
            return {
                "status": "success",
                "operation": "read",
                "level": level,
                "entries": [
                    {"timestamp": "2024-01-01T10:00:00", "level": "INFO", "message": "System started"},
                    {"timestamp": "2024-01-01T10:01:00", "level": "WARNING", "message": "High memory usage"}
                ]
            }
        
        elif operation == "rotate":
            return {
                "status": "success",
                "operation": "rotate",
                "rotated_files": ["log.2024-01-01.gz", "log.2024-01-02.gz"]
            }
        
        elif operation == "archive":
            return {
                "status": "success",
                "operation": "archive",
                "archive_path": "/archive/logs_2024-01-01.tar.gz"
            }
        
        return {"status": "error", "message": f"Unknown operation: {operation}"}
    
    def create_root(self, root_id: str, root_type: str, uri: str, description: str,
                   capabilities: List[str], validation: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new root."""
        self.roots[root_id] = {
            "type": root_type,
            "uri": uri,
            "description": description,
            "capabilities": capabilities,
            "validation": validation or {}
        }
        
        return {"status": "success", "root_id": root_id}
    
    def update_root(self, root_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing root."""
        if root_id not in self.roots:
            return {"status": "error", "message": "Root not found"}
        
        self.roots[root_id].update(updates)
        return {"status": "success", "root_id": root_id}
    
    def delete_root(self, root_id: str) -> Dict[str, Any]:
        """Delete a root."""
        if root_id not in self.roots:
            return {"status": "error", "message": "Root not found"}
        
        del self.roots[root_id]
        return {"status": "success", "root_id": root_id}


# ============================================================================
# MCP Root Tools
# ============================================================================

root_manager = RootManager()


@tool("list_roots")
async def list_roots_tool(root_type: str = None) -> Dict[str, Any]:
    """
    List available roots.
    
    Args:
        root_type: Optional root type filter
        
    Returns:
        Dictionary containing list of roots
    """
    try:
        roots = root_manager.list_roots(root_type)
        return {
            "status": "success",
            "roots": roots,
            "count": len(roots),
            "root_type": root_type
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("get_root")
async def get_root_tool(root_id: str) -> Dict[str, Any]:
    """
    Get a specific root by ID.
    
    Args:
        root_id: ID of the root to retrieve
        
    Returns:
        Dictionary containing root details
    """
    try:
        root = root_manager.get_root(root_id)
        if root:
            return {
                "status": "success",
                "root": root
            }
        else:
            return {"status": "error", "message": "Root not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("validate_root_operation")
async def validate_root_operation_tool(root_id: str, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a root operation.
    
    Args:
        root_id: ID of the root to validate for
        operation: Operation to validate
        parameters: Dictionary of parameters to validate
        
    Returns:
        Dictionary containing validation result
    """
    try:
        validation_result = root_manager.validate_root_operation(root_id, operation, parameters)
        return {
            "status": "success",
            "root_id": root_id,
            "operation": operation,
            "validation": validation_result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("execute_root_operation")
async def execute_root_operation_tool(root_id: str, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute an operation on a root.
    
    Args:
        root_id: ID of the root to operate on
        operation: Operation to execute
        parameters: Dictionary of parameters for the operation
        
    Returns:
        Dictionary containing operation result
    """
    try:
        result = root_manager.execute_root_operation(root_id, operation, parameters)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("create_root")
async def create_root_tool(root_id: str, root_type: str, uri: str, description: str,
                          capabilities: List[str], validation: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Create a new root.
    
    Args:
        root_id: Unique ID for the root
        root_type: Type of the root
        uri: URI for the root
        description: Description of the root
        capabilities: List of capabilities for the root
        validation: Optional validation rules
        
    Returns:
        Dictionary containing operation result
    """
    try:
        result = root_manager.create_root(root_id, root_type, uri, description, capabilities, validation)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("update_root")
async def update_root_tool(root_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an existing root.
    
    Args:
        root_id: ID of the root to update
        updates: Dictionary of updates to apply
        
    Returns:
        Dictionary containing operation result
    """
    try:
        result = root_manager.update_root(root_id, updates)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("delete_root")
async def delete_root_tool(root_id: str) -> Dict[str, Any]:
    """
    Delete a root.
    
    Args:
        root_id: ID of the root to delete
        
    Returns:
        Dictionary containing operation result
    """
    try:
        result = root_manager.delete_root(root_id)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("root_info")
async def root_info_tool() -> Dict[str, Any]:
    """
    Get information about the root system.
    
    Returns:
        Dictionary containing system information
    """
    try:
        return {
            "status": "success",
            "total_roots": len(root_manager.roots),
            "root_types": list(set(root["type"] for root in root_manager.roots.values())),
            "available_roots": list(root_manager.roots.keys()),
            "supported_operations": ["read", "write", "list", "delete", "query", "insert", "update", 
                                   "get", "post", "put", "store", "retrieve", "ping", "scan", "connect", 
                                   "monitor", "upload", "download", "validate", "backup", "rotate", "archive"]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============================================================================
# MCP Server Implementation
# ============================================================================

@server("mcp-roots-server")
class MCPRootsServer:
    """MCP Server for root management."""
    
    def __init__(self):
        self.server = Server("mcp-roots-server")
        
    async def initialize(self, options: InitializationOptions) -> None:
        """Initialize the server."""
        print(f"Initializing MCP Roots server: {options.server_name} v{options.server_version}")
        print(f"Available roots: {len(root_manager.roots)}")
        
    async def shutdown(self) -> None:
        """Shutdown the server."""
        print("Shutting down MCP Roots server")


async def main():
    """Main function to run the MCP roots server."""
    server = MCPRootsServer()
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-roots-server",
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
