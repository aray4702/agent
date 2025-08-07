"""
MCP Prompts Example

This example demonstrates how to work with MCP prompts including different
prompt types, templates, variables, validation, and management.

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
    Prompt,
    PromptTemplate,
    PromptVariable,
    PromptValidation,
    PromptResult
)


# ============================================================================
# Prompt Management
# ============================================================================

class PromptManager:
    """Manages different types of prompts and templates."""
    
    def __init__(self):
        self.prompts = {}
        self.templates = {}
        self.variables = {}
        self.setup_sample_prompts()
        
    def setup_sample_prompts(self):
        """Set up sample prompts for demonstration."""
        # Simple text prompts
        self.prompts["greeting"] = {
            "type": "text",
            "content": "Hello! How can I help you today?",
            "category": "conversation",
            "tags": ["greeting", "welcome"]
        }
        
        self.prompts["analysis"] = {
            "type": "text",
            "content": "Please analyze the following data and provide insights: {data}",
            "category": "analysis",
            "tags": ["analysis", "data"],
            "variables": ["data"]
        }
        
        # Template prompts
        self.templates["email_template"] = {
            "type": "template",
            "content": """
Subject: {subject}

Dear {recipient},

{body}

Best regards,
{sender}
            """.strip(),
            "category": "communication",
            "tags": ["email", "template"],
            "variables": ["subject", "recipient", "body", "sender"],
            "validation": {
                "required": ["subject", "recipient", "body", "sender"],
                "max_length": 1000
            }
        }
        
        self.templates["code_review"] = {
            "type": "template",
            "content": """
Please review the following code:

```{language}
{code}
```

Focus on:
- Code quality and best practices
- Potential bugs or issues
- Performance considerations
- Security concerns

Provide a detailed review with suggestions for improvement.
            """.strip(),
            "category": "development",
            "tags": ["code", "review", "development"],
            "variables": ["language", "code"],
            "validation": {
                "required": ["language", "code"],
                "language_options": ["python", "javascript", "java", "cpp", "go"]
            }
        }
        
        # Structured prompts
        self.prompts["structured_qa"] = {
            "type": "structured",
            "content": {
                "question": "What is the capital of {country}?",
                "context": "Geography knowledge",
                "expected_format": "city_name",
                "difficulty": "easy"
            },
            "category": "education",
            "tags": ["geography", "quiz"],
            "variables": ["country"]
        }
        
        # Multi-step prompts
        self.prompts["multi_step_analysis"] = {
            "type": "multi_step",
            "steps": [
                {
                    "step": 1,
                    "prompt": "First, identify the key components in the data: {data}",
                    "output_format": "list"
                },
                {
                    "step": 2,
                    "prompt": "Based on the components identified, analyze their relationships.",
                    "output_format": "analysis"
                },
                {
                    "step": 3,
                    "prompt": "Finally, provide recommendations based on your analysis.",
                    "output_format": "recommendations"
                }
            ],
            "category": "analysis",
            "tags": ["multi_step", "analysis"],
            "variables": ["data"]
        }
        
        # Conditional prompts
        self.prompts["conditional_response"] = {
            "type": "conditional",
            "conditions": [
                {
                    "condition": "user_type == 'expert'",
                    "prompt": "Provide detailed technical analysis: {query}"
                },
                {
                    "condition": "user_type == 'beginner'",
                    "prompt": "Explain in simple terms: {query}"
                },
                {
                    "condition": "default",
                    "prompt": "Provide a balanced explanation: {query}"
                }
            ],
            "category": "adaptive",
            "tags": ["conditional", "adaptive"],
            "variables": ["query", "user_type"]
        }
    
    def get_prompt(self, prompt_id: str) -> Optional[Dict[str, Any]]:
        """Get a prompt by ID."""
        return self.prompts.get(prompt_id)
    
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get a template by ID."""
        return self.templates.get(template_id)
    
    def list_prompts(self, category: str = None, tags: List[str] = None) -> List[Dict[str, Any]]:
        """List available prompts."""
        results = []
        
        for prompt_id, prompt in self.prompts.items():
            if category and prompt.get("category") != category:
                continue
            if tags and not any(tag in prompt.get("tags", []) for tag in tags):
                continue
            
            results.append({
                "id": prompt_id,
                "type": prompt["type"],
                "category": prompt["category"],
                "tags": prompt.get("tags", []),
                "variables": prompt.get("variables", [])
            })
        
        return results
    
    def list_templates(self, category: str = None) -> List[Dict[str, Any]]:
        """List available templates."""
        results = []
        
        for template_id, template in self.templates.items():
            if category and template.get("category") != category:
                continue
            
            results.append({
                "id": template_id,
                "type": template["type"],
                "category": template["category"],
                "tags": template.get("tags", []),
                "variables": template.get("variables", []),
                "validation": template.get("validation", {})
            })
        
        return results
    
    def render_prompt(self, prompt_id: str, variables: Dict[str, Any] = None) -> Optional[str]:
        """Render a prompt with variables."""
        prompt = self.get_prompt(prompt_id)
        if not prompt:
            return None
        
        content = prompt["content"]
        
        if prompt["type"] == "template":
            # Handle template rendering
            if variables:
                for var_name, var_value in variables.items():
                    placeholder = f"{{{var_name}}}"
                    content = content.replace(placeholder, str(var_value))
        
        elif prompt["type"] == "structured":
            # Handle structured prompt rendering
            if isinstance(content, dict) and variables:
                for var_name, var_value in variables.items():
                    placeholder = f"{{{var_name}}}"
                    content["question"] = content["question"].replace(placeholder, str(var_value))
        
        elif prompt["type"] == "multi_step":
            # Handle multi-step prompt rendering
            if variables:
                for step in content["steps"]:
                    for var_name, var_value in variables.items():
                        placeholder = f"{{{var_name}}}"
                        step["prompt"] = step["prompt"].replace(placeholder, str(var_value))
        
        elif prompt["type"] == "conditional":
            # Handle conditional prompt rendering
            user_type = variables.get("user_type", "default") if variables else "default"
            for condition in content["conditions"]:
                if condition["condition"] == f"user_type == '{user_type}'" or condition["condition"] == "default":
                    content = condition["prompt"]
                    if variables:
                        for var_name, var_value in variables.items():
                            placeholder = f"{{{var_name}}}"
                            content = content.replace(placeholder, str(var_value))
                    break
        
        else:
            # Handle simple text prompt
            if variables:
                for var_name, var_value in variables.items():
                    placeholder = f"{{{var_name}}}"
                    content = content.replace(placeholder, str(var_value))
        
        return content
    
    def render_template(self, template_id: str, variables: Dict[str, Any] = None) -> Optional[str]:
        """Render a template with variables."""
        template = self.get_template(template_id)
        if not template:
            return None
        
        content = template["content"]
        
        if variables:
            for var_name, var_value in variables.items():
                placeholder = f"{{{var_name}}}"
                content = content.replace(placeholder, str(var_value))
        
        return content
    
    def validate_prompt(self, prompt_id: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
        """Validate a prompt and its variables."""
        prompt = self.get_prompt(prompt_id)
        if not prompt:
            return {"valid": False, "error": "Prompt not found"}
        
        template = self.get_template(prompt_id)
        validation_rules = template.get("validation", {}) if template else {}
        
        # Check required variables
        required_vars = validation_rules.get("required", [])
        if required_vars:
            missing_vars = [var for var in required_vars if var not in (variables or {})]
            if missing_vars:
                return {
                    "valid": False,
                    "error": f"Missing required variables: {missing_vars}",
                    "missing_variables": missing_vars
                }
        
        # Check variable options (for templates)
        if template:
            for var_name, var_value in (variables or {}).items():
                option_key = f"{var_name}_options"
                if option_key in validation_rules:
                    valid_options = validation_rules[option_key]
                    if var_value not in valid_options:
                        return {
                            "valid": False,
                            "error": f"Invalid value for {var_name}. Must be one of: {valid_options}",
                            "invalid_variable": var_name,
                            "valid_options": valid_options
                        }
        
        # Check content length
        max_length = validation_rules.get("max_length")
        if max_length and variables:
            content = self.render_prompt(prompt_id, variables)
            if content and len(content) > max_length:
                return {
                    "valid": False,
                    "error": f"Content exceeds maximum length of {max_length} characters",
                    "current_length": len(content),
                    "max_length": max_length
                }
        
        return {"valid": True}
    
    def create_prompt(self, prompt_id: str, content: str, prompt_type: str = "text", 
                     category: str = "general", tags: List[str] = None, 
                     variables: List[str] = None) -> Dict[str, Any]:
        """Create a new prompt."""
        self.prompts[prompt_id] = {
            "type": prompt_type,
            "content": content,
            "category": category,
            "tags": tags or [],
            "variables": variables or []
        }
        
        return {"status": "success", "prompt_id": prompt_id}
    
    def update_prompt(self, prompt_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing prompt."""
        if prompt_id not in self.prompts:
            return {"status": "error", "message": "Prompt not found"}
        
        self.prompts[prompt_id].update(updates)
        return {"status": "success", "prompt_id": prompt_id}
    
    def delete_prompt(self, prompt_id: str) -> Dict[str, Any]:
        """Delete a prompt."""
        if prompt_id not in self.prompts:
            return {"status": "error", "message": "Prompt not found"}
        
        del self.prompts[prompt_id]
        return {"status": "success", "prompt_id": prompt_id}


# ============================================================================
# MCP Prompt Tools
# ============================================================================

prompt_manager = PromptManager()


@tool("list_prompts")
async def list_prompts_tool(category: str = None, tags: List[str] = None) -> Dict[str, Any]:
    """
    List available prompts.
    
    Args:
        category: Optional category filter
        tags: Optional list of tags to filter by
        
    Returns:
        Dictionary containing list of prompts
    """
    try:
        prompts = prompt_manager.list_prompts(category, tags)
        return {
            "status": "success",
            "prompts": prompts,
            "count": len(prompts),
            "category": category,
            "tags": tags
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("list_templates")
async def list_templates_tool(category: str = None) -> Dict[str, Any]:
    """
    List available prompt templates.
    
    Args:
        category: Optional category filter
        
    Returns:
        Dictionary containing list of templates
    """
    try:
        templates = prompt_manager.list_templates(category)
        return {
            "status": "success",
            "templates": templates,
            "count": len(templates),
            "category": category
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("get_prompt")
async def get_prompt_tool(prompt_id: str) -> Dict[str, Any]:
    """
    Get a specific prompt by ID.
    
    Args:
        prompt_id: ID of the prompt to retrieve
        
    Returns:
        Dictionary containing prompt details
    """
    try:
        prompt = prompt_manager.get_prompt(prompt_id)
        if prompt:
            return {
                "status": "success",
                "prompt": prompt
            }
        else:
            return {"status": "error", "message": "Prompt not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("get_template")
async def get_template_tool(template_id: str) -> Dict[str, Any]:
    """
    Get a specific template by ID.
    
    Args:
        template_id: ID of the template to retrieve
        
    Returns:
        Dictionary containing template details
    """
    try:
        template = prompt_manager.get_template(template_id)
        if template:
            return {
                "status": "success",
                "template": template
            }
        else:
            return {"status": "error", "message": "Template not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("render_prompt")
async def render_prompt_tool(prompt_id: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Render a prompt with variables.
    
    Args:
        prompt_id: ID of the prompt to render
        variables: Dictionary of variables to substitute
        
    Returns:
        Dictionary containing rendered prompt
    """
    try:
        rendered = prompt_manager.render_prompt(prompt_id, variables or {})
        if rendered:
            return {
                "status": "success",
                "prompt_id": prompt_id,
                "rendered_content": rendered,
                "variables_used": variables or {}
            }
        else:
            return {"status": "error", "message": "Prompt not found or could not be rendered"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("render_template")
async def render_template_tool(template_id: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Render a template with variables.
    
    Args:
        template_id: ID of the template to render
        variables: Dictionary of variables to substitute
        
    Returns:
        Dictionary containing rendered template
    """
    try:
        rendered = prompt_manager.render_template(template_id, variables or {})
        if rendered:
            return {
                "status": "success",
                "template_id": template_id,
                "rendered_content": rendered,
                "variables_used": variables or {}
            }
        else:
            return {"status": "error", "message": "Template not found or could not be rendered"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("validate_prompt")
async def validate_prompt_tool(prompt_id: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Validate a prompt and its variables.
    
    Args:
        prompt_id: ID of the prompt to validate
        variables: Dictionary of variables to validate
        
    Returns:
        Dictionary containing validation result
    """
    try:
        validation_result = prompt_manager.validate_prompt(prompt_id, variables or {})
        return {
            "status": "success",
            "prompt_id": prompt_id,
            "validation": validation_result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("create_prompt")
async def create_prompt_tool(prompt_id: str, content: str, prompt_type: str = "text",
                           category: str = "general", tags: List[str] = None,
                           variables: List[str] = None) -> Dict[str, Any]:
    """
    Create a new prompt.
    
    Args:
        prompt_id: Unique ID for the prompt
        content: Prompt content
        prompt_type: Type of prompt (text, template, structured, etc.)
        category: Category for the prompt
        tags: List of tags for the prompt
        variables: List of variables used in the prompt
        
    Returns:
        Dictionary containing operation result
    """
    try:
        result = prompt_manager.create_prompt(
            prompt_id, content, prompt_type, category, tags, variables
        )
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("update_prompt")
async def update_prompt_tool(prompt_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an existing prompt.
    
    Args:
        prompt_id: ID of the prompt to update
        updates: Dictionary of updates to apply
        
    Returns:
        Dictionary containing operation result
    """
    try:
        result = prompt_manager.update_prompt(prompt_id, updates)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("delete_prompt")
async def delete_prompt_tool(prompt_id: str) -> Dict[str, Any]:
    """
    Delete a prompt.
    
    Args:
        prompt_id: ID of the prompt to delete
        
    Returns:
        Dictionary containing operation result
    """
    try:
        result = prompt_manager.delete_prompt(prompt_id)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("prompt_info")
async def prompt_info_tool() -> Dict[str, Any]:
    """
    Get information about the prompt system.
    
    Returns:
        Dictionary containing system information
    """
    try:
        return {
            "status": "success",
            "total_prompts": len(prompt_manager.prompts),
            "total_templates": len(prompt_manager.templates),
            "categories": list(set(prompt["category"] for prompt in prompt_manager.prompts.values())),
            "prompt_types": list(set(prompt["type"] for prompt in prompt_manager.prompts.values())),
            "available_prompts": list(prompt_manager.prompts.keys()),
            "available_templates": list(prompt_manager.templates.keys())
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============================================================================
# MCP Server Implementation
# ============================================================================

@server("mcp-prompts-server")
class MCPPromptsServer:
    """MCP Server for prompt management."""
    
    def __init__(self):
        self.server = Server("mcp-prompts-server")
        
    async def initialize(self, options: InitializationOptions) -> None:
        """Initialize the server."""
        print(f"Initializing MCP Prompts server: {options.server_name} v{options.server_version}")
        print(f"Available prompts: {len(prompt_manager.prompts)}")
        print(f"Available templates: {len(prompt_manager.templates)}")
        
    async def shutdown(self) -> None:
        """Shutdown the server."""
        print("Shutting down MCP Prompts server")


async def main():
    """Main function to run the MCP prompts server."""
    server = MCPPromptsServer()
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-prompts-server",
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
