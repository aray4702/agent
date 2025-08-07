"""
MCP Tool Types Example

This example demonstrates how to work with MCP tool types including different
tool types, parameters, validation, and management.

Requirements:
- pip install mcp
"""

import asyncio
import json
import re
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    TextContent,
    Tool,
    ToolType,
    ToolParameter,
    ToolValidation,
    ToolResult
)


# ============================================================================
# Tool Type Management
# ============================================================================

class ToolTypeManager:
    """Manages different types of tools and their capabilities."""
    
    def __init__(self):
        self.tool_types = {}
        self.tools = {}
        self.tool_categories = {}
        self.setup_sample_tools()
        
    def setup_sample_tools(self):
        """Set up sample tools for demonstration."""
        # Simple tools
        self.tools["simple_calculator"] = {
            "type": "simple",
            "name": "Simple Calculator",
            "description": "Basic arithmetic operations",
            "parameters": {
                "operation": {"type": "string", "required": True, "enum": ["add", "subtract", "multiply", "divide"]},
                "a": {"type": "number", "required": True, "description": "First number"},
                "b": {"type": "number", "required": True, "description": "Second number"}
            },
            "return_type": "number",
            "category": "mathematics"
        }
        
        # Complex tools
        self.tools["data_processor"] = {
            "type": "complex",
            "name": "Data Processor",
            "description": "Process and analyze data arrays",
            "parameters": {
                "data": {"type": "array", "required": True, "description": "Array of numbers"},
                "operation": {"type": "string", "required": True, "enum": ["sum", "average", "min", "max", "sort"]},
                "filter": {"type": "object", "required": False, "description": "Filter criteria"}
            },
            "return_type": "object",
            "category": "data_analysis"
        }
        
        # File tools
        self.tools["file_operations"] = {
            "type": "file",
            "name": "File Operations",
            "description": "File system operations",
            "parameters": {
                "operation": {"type": "string", "required": True, "enum": ["read", "write", "delete", "list"]},
                "path": {"type": "string", "required": True, "description": "File path"},
                "content": {"type": "string", "required": False, "description": "File content for write operations"}
            },
            "return_type": "object",
            "category": "file_system"
        }
        
        # Network tools
        self.tools["network_scanner"] = {
            "type": "network",
            "name": "Network Scanner",
            "description": "Network scanning and monitoring",
            "parameters": {
                "host": {"type": "string", "required": True, "description": "Target host"},
                "ports": {"type": "array", "required": False, "description": "Ports to scan"},
                "timeout": {"type": "number", "required": False, "default": 5, "description": "Timeout in seconds"}
            },
            "return_type": "object",
            "category": "networking"
        }
        
        # Database tools
        self.tools["database_query"] = {
            "type": "database",
            "name": "Database Query",
            "description": "Execute database queries",
            "parameters": {
                "query": {"type": "string", "required": True, "description": "SQL query"},
                "parameters": {"type": "object", "required": False, "description": "Query parameters"},
                "timeout": {"type": "number", "required": False, "default": 30, "description": "Query timeout"}
            },
            "return_type": "object",
            "category": "database"
        }
        
        # API tools
        self.tools["api_client"] = {
            "type": "api",
            "name": "API Client",
            "description": "Make HTTP API requests",
            "parameters": {
                "url": {"type": "string", "required": True, "description": "API endpoint URL"},
                "method": {"type": "string", "required": True, "enum": ["GET", "POST", "PUT", "DELETE"]},
                "headers": {"type": "object", "required": False, "description": "Request headers"},
                "data": {"type": "object", "required": False, "description": "Request data"}
            },
            "return_type": "object",
            "category": "api"
        }
        
        # Validation tools
        self.tools["data_validator"] = {
            "type": "validation",
            "name": "Data Validator",
            "description": "Validate data against schemas",
            "parameters": {
                "data": {"type": "object", "required": True, "description": "Data to validate"},
                "schema": {"type": "object", "required": True, "description": "Validation schema"},
                "strict": {"type": "boolean", "required": False, "default": False, "description": "Strict validation mode"}
            },
            "return_type": "object",
            "category": "validation"
        }
        
        # Transformation tools
        self.tools["data_transformer"] = {
            "type": "transformation",
            "name": "Data Transformer",
            "description": "Transform data formats",
            "parameters": {
                "data": {"type": "object", "required": True, "description": "Input data"},
                "format": {"type": "string", "required": True, "enum": ["json", "xml", "csv", "yaml"]},
                "direction": {"type": "string", "required": True, "enum": ["to", "from"], "description": "Transformation direction"}
            },
            "return_type": "object",
            "category": "transformation"
        }
        
        # Machine Learning tools
        self.tools["ml_predictor"] = {
            "type": "machine_learning",
            "name": "ML Predictor",
            "description": "Make predictions using ML models",
            "parameters": {
                "model": {"type": "string", "required": True, "description": "Model identifier"},
                "features": {"type": "array", "required": True, "description": "Input features"},
                "confidence": {"type": "boolean", "required": False, "default": False, "description": "Include confidence scores"}
            },
            "return_type": "object",
            "category": "machine_learning"
        }
        
        # Security tools
        self.tools["security_scanner"] = {
            "type": "security",
            "name": "Security Scanner",
            "description": "Security vulnerability scanning",
            "parameters": {
                "target": {"type": "string", "required": True, "description": "Target to scan"},
                "scan_type": {"type": "string", "required": True, "enum": ["vulnerability", "port", "ssl", "web"]},
                "options": {"type": "object", "required": False, "description": "Scan options"}
            },
            "return_type": "object",
            "category": "security"
        }
        
        # Monitoring tools
        self.tools["system_monitor"] = {
            "type": "monitoring",
            "name": "System Monitor",
            "description": "System resource monitoring",
            "parameters": {
                "metric": {"type": "string", "required": True, "enum": ["cpu", "memory", "disk", "network"]},
                "duration": {"type": "number", "required": False, "default": 60, "description": "Monitoring duration in seconds"}
            },
            "return_type": "object",
            "category": "monitoring"
        }
    
    def get_tool(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """Get a tool by ID."""
        return self.tools.get(tool_id)
    
    def list_tools(self, tool_type: str = None, category: str = None) -> List[Dict[str, Any]]:
        """List available tools."""
        results = []
        
        for tool_id, tool in self.tools.items():
            if tool_type and tool.get("type") != tool_type:
                continue
            if category and tool.get("category") != category:
                continue
            
            results.append({
                "id": tool_id,
                "name": tool["name"],
                "type": tool["type"],
                "description": tool["description"],
                "category": tool["category"],
                "parameters": tool["parameters"],
                "return_type": tool["return_type"]
            })
        
        return results
    
    def validate_tool_parameters(self, tool_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate tool parameters."""
        tool = self.get_tool(tool_id)
        if not tool:
            return {"valid": False, "error": "Tool not found"}
        
        tool_params = tool["parameters"]
        missing_params = []
        invalid_params = []
        
        # Check required parameters
        for param_name, param_spec in tool_params.items():
            if param_spec.get("required", False) and param_name not in parameters:
                missing_params.append(param_name)
        
        if missing_params:
            return {
                "valid": False,
                "error": f"Missing required parameters: {missing_params}",
                "missing_parameters": missing_params
            }
        
        # Validate parameter types and values
        for param_name, param_value in parameters.items():
            if param_name in tool_params:
                param_spec = tool_params[param_name]
                param_type = param_spec.get("type")
                
                # Type validation
                if param_type == "string":
                    if not isinstance(param_value, str):
                        invalid_params.append(f"{param_name}: expected string, got {type(param_value).__name__}")
                
                elif param_type == "number":
                    if not isinstance(param_value, (int, float)):
                        invalid_params.append(f"{param_name}: expected number, got {type(param_value).__name__}")
                
                elif param_type == "boolean":
                    if not isinstance(param_value, bool):
                        invalid_params.append(f"{param_name}: expected boolean, got {type(param_value).__name__}")
                
                elif param_type == "array":
                    if not isinstance(param_value, list):
                        invalid_params.append(f"{param_name}: expected array, got {type(param_value).__name__}")
                
                elif param_type == "object":
                    if not isinstance(param_value, dict):
                        invalid_params.append(f"{param_name}: expected object, got {type(param_value).__name__}")
                
                # Enum validation
                if "enum" in param_spec and param_value not in param_spec["enum"]:
                    invalid_params.append(f"{param_name}: value '{param_value}' not in {param_spec['enum']}")
        
        if invalid_params:
            return {
                "valid": False,
                "error": f"Invalid parameters: {invalid_params}",
                "invalid_parameters": invalid_params
            }
        
        return {"valid": True}
    
    def execute_tool(self, tool_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool with parameters."""
        tool = self.get_tool(tool_id)
        if not tool:
            return {"status": "error", "message": "Tool not found"}
        
        # Validate parameters
        validation = self.validate_tool_parameters(tool_id, parameters)
        if not validation["valid"]:
            return {"status": "error", "validation": validation}
        
        try:
            if tool_id == "simple_calculator":
                return self._execute_simple_calculator(parameters)
            elif tool_id == "data_processor":
                return self._execute_data_processor(parameters)
            elif tool_id == "file_operations":
                return self._execute_file_operations(parameters)
            elif tool_id == "network_scanner":
                return self._execute_network_scanner(parameters)
            elif tool_id == "database_query":
                return self._execute_database_query(parameters)
            elif tool_id == "api_client":
                return self._execute_api_client(parameters)
            elif tool_id == "data_validator":
                return self._execute_data_validator(parameters)
            elif tool_id == "data_transformer":
                return self._execute_data_transformer(parameters)
            elif tool_id == "ml_predictor":
                return self._execute_ml_predictor(parameters)
            elif tool_id == "security_scanner":
                return self._execute_security_scanner(parameters)
            elif tool_id == "system_monitor":
                return self._execute_system_monitor(parameters)
            else:
                return {"status": "error", "message": "Unknown tool"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _execute_simple_calculator(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute simple calculator tool."""
        operation = parameters["operation"]
        a = parameters["a"]
        b = parameters["b"]
        
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                return {"status": "error", "message": "Division by zero"}
            result = a / b
        else:
            return {"status": "error", "message": f"Unknown operation: {operation}"}
        
        return {
            "status": "success",
            "result": result,
            "operation": operation,
            "operands": [a, b]
        }
    
    def _execute_data_processor(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute data processor tool."""
        data = parameters["data"]
        operation = parameters["operation"]
        filter_criteria = parameters.get("filter")
        
        if filter_criteria:
            # Apply filter
            data = [x for x in data if all(x.get(k) == v for k, v in filter_criteria.items())]
        
        if operation == "sum":
            result = sum(data)
        elif operation == "average":
            result = sum(data) / len(data) if data else 0
        elif operation == "min":
            result = min(data) if data else None
        elif operation == "max":
            result = max(data) if data else None
        elif operation == "sort":
            result = sorted(data)
        else:
            return {"status": "error", "message": f"Unknown operation: {operation}"}
        
        return {
            "status": "success",
            "result": result,
            "operation": operation,
            "data_length": len(data)
        }
    
    def _execute_file_operations(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute file operations tool."""
        operation = parameters["operation"]
        path = parameters["path"]
        
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
        
        elif operation == "delete":
            try:
                import os
                os.remove(path)
                return {
                    "status": "success",
                    "operation": "delete",
                    "path": path
                }
            except Exception as e:
                return {"status": "error", "message": f"Error deleting file: {e}"}
        
        elif operation == "list":
            try:
                import os
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
        
        return {"status": "error", "message": f"Unknown operation: {operation}"}
    
    def _execute_network_scanner(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute network scanner tool."""
        host = parameters["host"]
        ports = parameters.get("ports", [80, 443, 22])
        timeout = parameters.get("timeout", 5)
        
        # Simulate network scanning
        open_ports = []
        for port in ports:
            if port in [80, 443, 22]:  # Simulate open ports
                open_ports.append(port)
        
        return {
            "status": "success",
            "host": host,
            "scanned_ports": ports,
            "open_ports": open_ports,
            "scan_time": timeout,
            "total_ports": len(ports)
        }
    
    def _execute_database_query(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute database query tool."""
        query = parameters["query"]
        query_params = parameters.get("parameters", {})
        timeout = parameters.get("timeout", 30)
        
        # Simulate database query
        return {
            "status": "success",
            "query": query,
            "parameters": query_params,
            "result": f"Simulated query result for: {query}",
            "rows_affected": 5,
            "execution_time": 0.1
        }
    
    def _execute_api_client(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute API client tool."""
        url = parameters["url"]
        method = parameters["method"]
        headers = parameters.get("headers", {})
        data = parameters.get("data", {})
        
        # Simulate API request
        return {
            "status": "success",
            "url": url,
            "method": method,
            "headers": headers,
            "data": data,
            "response": f"Simulated {method} response from {url}",
            "status_code": 200
        }
    
    def _execute_data_validator(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute data validator tool."""
        data = parameters["data"]
        schema = parameters["schema"]
        strict = parameters.get("strict", False)
        
        # Simple validation simulation
        errors = []
        for field, rules in schema.items():
            if field not in data:
                if strict or rules.get("required", False):
                    errors.append(f"Missing required field: {field}")
            elif "type" in rules:
                expected_type = rules["type"]
                actual_type = type(data[field]).__name__
                if actual_type != expected_type:
                    errors.append(f"Field {field}: expected {expected_type}, got {actual_type}")
        
        return {
            "status": "success",
            "valid": len(errors) == 0,
            "errors": errors,
            "data": data,
            "strict_mode": strict
        }
    
    def _execute_data_transformer(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute data transformer tool."""
        data = parameters["data"]
        format_type = parameters["format"]
        direction = parameters["direction"]
        
        # Simulate data transformation
        if direction == "to":
            if format_type == "json":
                result = json.dumps(data)
            elif format_type == "xml":
                result = f"<data>{str(data)}</data>"
            elif format_type == "csv":
                result = "header1,header2\nvalue1,value2"
            elif format_type == "yaml":
                result = f"data: {str(data)}"
        else:  # from
            if format_type == "json":
                result = json.loads(data) if isinstance(data, str) else data
            else:
                result = {"parsed": data}
        
        return {
            "status": "success",
            "format": format_type,
            "direction": direction,
            "result": result
        }
    
    def _execute_ml_predictor(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute ML predictor tool."""
        model = parameters["model"]
        features = parameters["features"]
        confidence = parameters.get("confidence", False)
        
        # Simulate ML prediction
        prediction = 0.75  # Simulated prediction value
        confidence_score = 0.85 if confidence else None
        
        return {
            "status": "success",
            "model": model,
            "features": features,
            "prediction": prediction,
            "confidence": confidence_score
        }
    
    def _execute_security_scanner(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute security scanner tool."""
        target = parameters["target"]
        scan_type = parameters["scan_type"]
        options = parameters.get("options", {})
        
        # Simulate security scan
        vulnerabilities = []
        if scan_type == "vulnerability":
            vulnerabilities = ["CVE-2023-1234", "CVE-2023-5678"]
        elif scan_type == "port":
            vulnerabilities = ["Open port 22", "Open port 80"]
        elif scan_type == "ssl":
            vulnerabilities = ["Weak cipher suite", "Expired certificate"]
        elif scan_type == "web":
            vulnerabilities = ["SQL injection", "XSS vulnerability"]
        
        return {
            "status": "success",
            "target": target,
            "scan_type": scan_type,
            "vulnerabilities": vulnerabilities,
            "risk_level": "medium" if vulnerabilities else "low"
        }
    
    def _execute_system_monitor(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute system monitor tool."""
        metric = parameters["metric"]
        duration = parameters.get("duration", 60)
        
        # Simulate system monitoring
        metrics = {
            "cpu": {"usage": 45.2, "cores": 8, "temperature": 65},
            "memory": {"used": 8192, "total": 16384, "usage_percent": 50},
            "disk": {"used": 500, "total": 1000, "usage_percent": 50},
            "network": {"bytes_sent": 1024, "bytes_recv": 2048, "packets": 100}
        }
        
        return {
            "status": "success",
            "metric": metric,
            "duration": duration,
            "data": metrics.get(metric, {}),
            "timestamp": datetime.now().isoformat()
        }
    
    def create_tool(self, tool_id: str, tool_type: str, name: str, description: str,
                   parameters: Dict[str, Any], return_type: str, category: str) -> Dict[str, Any]:
        """Create a new tool."""
        self.tools[tool_id] = {
            "type": tool_type,
            "name": name,
            "description": description,
            "parameters": parameters,
            "return_type": return_type,
            "category": category
        }
        
        return {"status": "success", "tool_id": tool_id}
    
    def update_tool(self, tool_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing tool."""
        if tool_id not in self.tools:
            return {"status": "error", "message": "Tool not found"}
        
        self.tools[tool_id].update(updates)
        return {"status": "success", "tool_id": tool_id}
    
    def delete_tool(self, tool_id: str) -> Dict[str, Any]:
        """Delete a tool."""
        if tool_id not in self.tools:
            return {"status": "error", "message": "Tool not found"}
        
        del self.tools[tool_id]
        return {"status": "success", "tool_id": tool_id}


# ============================================================================
# MCP Tool Type Tools
# ============================================================================

tool_manager = ToolTypeManager()


@tool("list_tools")
async def list_tools_tool(tool_type: str = None, category: str = None) -> Dict[str, Any]:
    """
    List available tools.
    
    Args:
        tool_type: Optional tool type filter
        category: Optional category filter
        
    Returns:
        Dictionary containing list of tools
    """
    try:
        tools = tool_manager.list_tools(tool_type, category)
        return {
            "status": "success",
            "tools": tools,
            "count": len(tools),
            "tool_type": tool_type,
            "category": category
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("get_tool")
async def get_tool_tool(tool_id: str) -> Dict[str, Any]:
    """
    Get a specific tool by ID.
    
    Args:
        tool_id: ID of the tool to retrieve
        
    Returns:
        Dictionary containing tool details
    """
    try:
        tool = tool_manager.get_tool(tool_id)
        if tool:
            return {
                "status": "success",
                "tool": tool
            }
        else:
            return {"status": "error", "message": "Tool not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("validate_tool_parameters")
async def validate_tool_parameters_tool(tool_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate tool parameters.
    
    Args:
        tool_id: ID of the tool to validate for
        parameters: Dictionary of parameters to validate
        
    Returns:
        Dictionary containing validation result
    """
    try:
        validation_result = tool_manager.validate_tool_parameters(tool_id, parameters)
        return {
            "status": "success",
            "tool_id": tool_id,
            "validation": validation_result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("execute_tool")
async def execute_tool_tool(tool_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a tool with parameters.
    
    Args:
        tool_id: ID of the tool to execute
        parameters: Dictionary of parameters for the tool
        
    Returns:
        Dictionary containing execution result
    """
    try:
        result = tool_manager.execute_tool(tool_id, parameters)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("create_tool")
async def create_tool_tool(tool_id: str, tool_type: str, name: str, description: str,
                          parameters: Dict[str, Any], return_type: str, category: str) -> Dict[str, Any]:
    """
    Create a new tool.
    
    Args:
        tool_id: Unique ID for the tool
        tool_type: Type of the tool
        name: Name of the tool
        description: Description of the tool
        parameters: Dictionary of tool parameters
        return_type: Return type of the tool
        category: Category of the tool
        
    Returns:
        Dictionary containing operation result
    """
    try:
        result = tool_manager.create_tool(tool_id, tool_type, name, description, parameters, return_type, category)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("update_tool")
async def update_tool_tool(tool_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an existing tool.
    
    Args:
        tool_id: ID of the tool to update
        updates: Dictionary of updates to apply
        
    Returns:
        Dictionary containing operation result
    """
    try:
        result = tool_manager.update_tool(tool_id, updates)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("delete_tool")
async def delete_tool_tool(tool_id: str) -> Dict[str, Any]:
    """
    Delete a tool.
    
    Args:
        tool_id: ID of the tool to delete
        
    Returns:
        Dictionary containing operation result
    """
    try:
        result = tool_manager.delete_tool(tool_id)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("tool_info")
async def tool_info_tool() -> Dict[str, Any]:
    """
    Get information about the tool system.
    
    Returns:
        Dictionary containing system information
    """
    try:
        return {
            "status": "success",
            "total_tools": len(tool_manager.tools),
            "tool_types": list(set(tool["type"] for tool in tool_manager.tools.values())),
            "categories": list(set(tool["category"] for tool in tool_manager.tools.values())),
            "available_tools": list(tool_manager.tools.keys()),
            "supported_parameter_types": ["string", "number", "boolean", "array", "object"],
            "supported_return_types": ["string", "number", "boolean", "array", "object"]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============================================================================
# MCP Server Implementation
# ============================================================================

@server("mcp-tool-types-server")
class MCPToolTypesServer:
    """MCP Server for tool type management."""
    
    def __init__(self):
        self.server = Server("mcp-tool-types-server")
        
    async def initialize(self, options: InitializationOptions) -> None:
        """Initialize the server."""
        print(f"Initializing MCP Tool Types server: {options.server_name} v{options.server_version}")
        print(f"Available tools: {len(tool_manager.tools)}")
        
    async def shutdown(self) -> None:
        """Shutdown the server."""
        print("Shutting down MCP Tool Types server")


async def main():
    """Main function to run the MCP tool types server."""
    server = MCPToolTypesServer()
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-tool-types-server",
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
