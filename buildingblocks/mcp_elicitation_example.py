"""
MCP Elicitation Example

This example demonstrates how to work with MCP elicitation including different
elicitation types, user interaction patterns, form-based elicitation, and
elicitation management.

Requirements:
- pip install mcp
"""

import asyncio
import json
import uuid
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    TextContent,
    ElicitationRequest,
    ElicitationResponse,
    ElicitationForm,
    ElicitationField,
    ElicitationValidation,
    ElicitationResult
)


# ============================================================================
# Elicitation Management
# ============================================================================

class ElicitationManager:
    """Manages different types of elicitation patterns and user interactions."""
    
    def __init__(self):
        self.elicitation_sessions = {}
        self.elicitation_templates = {}
        self.user_responses = {}
        self.setup_sample_elicitation()
        
    def setup_sample_elicitation(self):
        """Set up sample elicitation patterns for demonstration."""
        
        # Form-based elicitation templates
        self.elicitation_templates["user_registration"] = {
            "type": "form",
            "title": "User Registration",
            "description": "Please provide your information to create an account",
            "fields": [
                {
                    "id": "username",
                    "type": "text",
                    "label": "Username",
                    "required": True,
                    "validation": {
                        "min_length": 3,
                        "max_length": 20,
                        "pattern": "^[a-zA-Z0-9_]+$"
                    },
                    "placeholder": "Enter your username"
                },
                {
                    "id": "email",
                    "type": "email",
                    "label": "Email Address",
                    "required": True,
                    "validation": {
                        "pattern": "^[^@]+@[^@]+\\.[^@]+$"
                    },
                    "placeholder": "Enter your email"
                },
                {
                    "id": "password",
                    "type": "password",
                    "label": "Password",
                    "required": True,
                    "validation": {
                        "min_length": 8,
                        "pattern": "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)"
                    },
                    "placeholder": "Enter your password"
                },
                {
                    "id": "confirm_password",
                    "type": "password",
                    "label": "Confirm Password",
                    "required": True,
                    "validation": {
                        "matches": "password"
                    },
                    "placeholder": "Confirm your password"
                },
                {
                    "id": "age",
                    "type": "number",
                    "label": "Age",
                    "required": False,
                    "validation": {
                        "min": 13,
                        "max": 120
                    },
                    "placeholder": "Enter your age"
                },
                {
                    "id": "interests",
                    "type": "multiselect",
                    "label": "Interests",
                    "required": False,
                    "options": [
                        {"value": "technology", "label": "Technology"},
                        {"value": "sports", "label": "Sports"},
                        {"value": "music", "label": "Music"},
                        {"value": "reading", "label": "Reading"},
                        {"value": "travel", "label": "Travel"}
                    ],
                    "placeholder": "Select your interests"
                },
                {
                    "id": "newsletter",
                    "type": "checkbox",
                    "label": "Subscribe to newsletter",
                    "required": False,
                    "default": False
                }
            ],
            "submit_text": "Create Account",
            "cancel_text": "Cancel"
        }
        
        # Conversational elicitation templates
        self.elicitation_templates["conversational_survey"] = {
            "type": "conversational",
            "title": "Customer Satisfaction Survey",
            "description": "Let's have a quick conversation about your experience",
            "flow": [
                {
                    "step": 1,
                    "question": "How would you rate your overall experience with our service?",
                    "type": "rating",
                    "options": ["1 - Poor", "2 - Fair", "3 - Good", "4 - Very Good", "5 - Excellent"],
                    "required": True
                },
                {
                    "step": 2,
                    "question": "What aspects of our service did you find most valuable?",
                    "type": "multiselect",
                    "options": [
                        "Customer Support",
                        "Product Quality",
                        "Pricing",
                        "Ease of Use",
                        "Features"
                    ],
                    "required": False
                },
                {
                    "step": 3,
                    "question": "Is there anything specific you'd like us to improve?",
                    "type": "text",
                    "required": False,
                    "placeholder": "Share your suggestions..."
                },
                {
                    "step": 4,
                    "question": "Would you recommend our service to others?",
                    "type": "yes_no",
                    "required": True
                }
            ]
        }
        
        # Multi-step elicitation templates
        self.elicitation_templates["project_requirements"] = {
            "type": "multi_step",
            "title": "Project Requirements Gathering",
            "description": "Let's gather information about your project requirements",
            "steps": [
                {
                    "step": 1,
                    "title": "Project Overview",
                    "questions": [
                        {
                            "id": "project_name",
                            "question": "What is the name of your project?",
                            "type": "text",
                            "required": True
                        },
                        {
                            "id": "project_type",
                            "question": "What type of project is this?",
                            "type": "select",
                            "options": [
                                {"value": "web_app", "label": "Web Application"},
                                {"value": "mobile_app", "label": "Mobile Application"},
                                {"value": "desktop_app", "label": "Desktop Application"},
                                {"value": "api", "label": "API/Backend Service"},
                                {"value": "other", "label": "Other"}
                            ],
                            "required": True
                        }
                    ]
                },
                {
                    "step": 2,
                    "title": "Technical Requirements",
                    "questions": [
                        {
                            "id": "technologies",
                            "question": "What technologies would you prefer?",
                            "type": "multiselect",
                            "options": [
                                {"value": "python", "label": "Python"},
                                {"value": "javascript", "label": "JavaScript"},
                                {"value": "java", "label": "Java"},
                                {"value": "csharp", "label": "C#"},
                                {"value": "go", "label": "Go"},
                                {"value": "rust", "label": "Rust"}
                            ],
                            "required": False
                        },
                        {
                            "id": "timeline",
                            "question": "What is your expected timeline?",
                            "type": "select",
                            "options": [
                                {"value": "1_month", "label": "1 Month"},
                                {"value": "3_months", "label": "3 Months"},
                                {"value": "6_months", "label": "6 Months"},
                                {"value": "1_year", "label": "1 Year"},
                                {"value": "flexible", "label": "Flexible"}
                            ],
                            "required": True
                        }
                    ]
                },
                {
                    "step": 3,
                    "title": "Budget and Resources",
                    "questions": [
                        {
                            "id": "budget_range",
                            "question": "What is your budget range?",
                            "type": "select",
                            "options": [
                                {"value": "under_10k", "label": "Under $10,000"},
                                {"value": "10k_50k", "label": "$10,000 - $50,000"},
                                {"value": "50k_100k", "label": "$50,000 - $100,000"},
                                {"value": "over_100k", "label": "Over $100,000"}
                            ],
                            "required": True
                        },
                        {
                            "id": "team_size",
                            "question": "How many people will be working on this project?",
                            "type": "number",
                            "required": False,
                            "validation": {"min": 1, "max": 50}
                        }
                    ]
                }
            ]
        }
        
        # Adaptive elicitation templates
        self.elicitation_templates["adaptive_consultation"] = {
            "type": "adaptive",
            "title": "Adaptive Consultation",
            "description": "This consultation adapts based on your responses",
            "rules": [
                {
                    "condition": "experience_level == 'beginner'",
                    "questions": [
                        {
                            "id": "basic_needs",
                            "question": "What are your basic requirements?",
                            "type": "text",
                            "required": True
                        }
                    ]
                },
                {
                    "condition": "experience_level == 'intermediate'",
                    "questions": [
                        {
                            "id": "technical_details",
                            "question": "What technical specifications do you need?",
                            "type": "multiselect",
                            "options": [
                                {"value": "scalability", "label": "Scalability"},
                                {"value": "security", "label": "Security"},
                                {"value": "performance", "label": "Performance"},
                                {"value": "integration", "label": "Third-party Integration"}
                            ],
                            "required": False
                        }
                    ]
                },
                {
                    "condition": "experience_level == 'expert'",
                    "questions": [
                        {
                            "id": "advanced_features",
                            "question": "What advanced features do you require?",
                            "type": "text",
                            "required": False,
                            "placeholder": "Describe advanced requirements..."
                        }
                    ]
                }
            ],
            "initial_question": {
                "id": "experience_level",
                "question": "What is your experience level?",
                "type": "select",
                "options": [
                    {"value": "beginner", "label": "Beginner"},
                    {"value": "intermediate", "label": "Intermediate"},
                    {"value": "expert", "label": "Expert"}
                ],
                "required": True
            }
        }
    
    def create_elicitation_session(self, template_id: str, session_id: str = None) -> Dict[str, Any]:
        """Create a new elicitation session."""
        if template_id not in self.elicitation_templates:
            return {"status": "error", "message": "Template not found"}
        
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        template = self.elicitation_templates[template_id]
        session = {
            "session_id": session_id,
            "template_id": template_id,
            "template": template,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "responses": {},
            "current_step": 1,
            "completed": False
        }
        
        self.elicitation_sessions[session_id] = session
        return {"status": "success", "session_id": session_id, "session": session}
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get an elicitation session by ID."""
        return self.elicitation_sessions.get(session_id)
    
    def submit_response(self, session_id: str, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Submit responses for an elicitation session."""
        session = self.get_session(session_id)
        if not session:
            return {"status": "error", "message": "Session not found"}
        
        # Validate responses based on template type
        validation_result = self.validate_responses(session, responses)
        if not validation_result["valid"]:
            return validation_result
        
        # Update session with responses
        session["responses"].update(responses)
        
        # Handle different template types
        template = session["template"]
        if template["type"] == "form":
            # Form is complete after one submission
            session["completed"] = True
            session["status"] = "completed"
        elif template["type"] == "conversational":
            # Move to next step in conversational flow
            current_step = session["current_step"]
            flow = template["flow"]
            if current_step < len(flow):
                session["current_step"] = current_step + 1
            else:
                session["completed"] = True
                session["status"] = "completed"
        elif template["type"] == "multi_step":
            # Handle multi-step progression
            current_step = session["current_step"]
            steps = template["steps"]
            if current_step < len(steps):
                session["current_step"] = current_step + 1
            else:
                session["completed"] = True
                session["status"] = "completed"
        elif template["type"] == "adaptive":
            # Handle adaptive flow based on responses
            session["completed"] = True
            session["status"] = "completed"
        
        return {
            "status": "success",
            "session_id": session_id,
            "responses": session["responses"],
            "completed": session["completed"],
            "next_step": session["current_step"] if not session["completed"] else None
        }
    
    def validate_responses(self, session: Dict[str, Any], responses: Dict[str, Any]) -> Dict[str, Any]:
        """Validate responses against the template requirements."""
        template = session["template"]
        validation_errors = []
        
        if template["type"] == "form":
            for field in template["fields"]:
                field_id = field["id"]
                if field["required"] and field_id not in responses:
                    validation_errors.append(f"Required field '{field['label']}' is missing")
                elif field_id in responses:
                    # Validate field value
                    field_validation = self.validate_field(field, responses[field_id])
                    if not field_validation["valid"]:
                        validation_errors.append(f"Field '{field['label']}': {field_validation['error']}")
        
        elif template["type"] == "conversational":
            current_step = session["current_step"]
            flow = template["flow"]
            if current_step <= len(flow):
                step = flow[current_step - 1]
                if step["required"] and "response" not in responses:
                    validation_errors.append(f"Required response for step {current_step} is missing")
        
        elif template["type"] == "multi_step":
            current_step = session["current_step"]
            steps = template["steps"]
            if current_step <= len(steps):
                step = steps[current_step - 1]
                for question in step["questions"]:
                    question_id = question["id"]
                    if question["required"] and question_id not in responses:
                        validation_errors.append(f"Required question '{question['question']}' is missing")
                    elif question_id in responses:
                        # Validate question response
                        question_validation = self.validate_field(question, responses[question_id])
                        if not question_validation["valid"]:
                            validation_errors.append(f"Question '{question['question']}': {question_validation['error']}")
        
        if validation_errors:
            return {
                "valid": False,
                "errors": validation_errors
            }
        
        return {"valid": True}
    
    def validate_field(self, field: Dict[str, Any], value: Any) -> Dict[str, Any]:
        """Validate a single field value."""
        validation = field.get("validation", {})
        
        # Check required
        if field.get("required", False) and (value is None or value == ""):
            return {"valid": False, "error": "Field is required"}
        
        # Check min/max length for text fields
        if field["type"] in ["text", "email", "password"]:
            if "min_length" in validation and len(str(value)) < validation["min_length"]:
                return {"valid": False, "error": f"Minimum length is {validation['min_length']} characters"}
            if "max_length" in validation and len(str(value)) > validation["max_length"]:
                return {"valid": False, "error": f"Maximum length is {validation['max_length']} characters"}
            
            # Check pattern for text fields
            if "pattern" in validation:
                import re
                if not re.match(validation["pattern"], str(value)):
                    return {"valid": False, "error": "Value does not match required pattern"}
        
        # Check min/max for number fields
        if field["type"] == "number":
            try:
                num_value = float(value)
                if "min" in validation and num_value < validation["min"]:
                    return {"valid": False, "error": f"Minimum value is {validation['min']}"}
                if "max" in validation and num_value > validation["max"]:
                    return {"valid": False, "error": f"Maximum value is {validation['max']}"}
            except (ValueError, TypeError):
                return {"valid": False, "error": "Value must be a number"}
        
        # Check email pattern
        if field["type"] == "email":
            import re
            email_pattern = r"^[^@]+@[^@]+\.[^@]+$"
            if not re.match(email_pattern, str(value)):
                return {"valid": False, "error": "Invalid email format"}
        
        # Check password confirmation
        if "matches" in validation:
            if value != validation["matches"]:
                return {"valid": False, "error": "Values do not match"}
        
        return {"valid": True}
    
    def get_current_questions(self, session_id: str) -> Dict[str, Any]:
        """Get current questions for an active session."""
        session = self.get_session(session_id)
        if not session:
            return {"status": "error", "message": "Session not found"}
        
        template = session["template"]
        current_step = session["current_step"]
        
        if template["type"] == "form":
            return {
                "status": "success",
                "type": "form",
                "title": template["title"],
                "description": template["description"],
                "fields": template["fields"],
                "submit_text": template["submit_text"],
                "cancel_text": template["cancel_text"]
            }
        
        elif template["type"] == "conversational":
            flow = template["flow"]
            if current_step <= len(flow):
                current_question = flow[current_step - 1]
                return {
                    "status": "success",
                    "type": "conversational",
                    "title": template["title"],
                    "description": template["description"],
                    "current_step": current_step,
                    "total_steps": len(flow),
                    "question": current_question
                }
            else:
                return {"status": "error", "message": "Session completed"}
        
        elif template["type"] == "multi_step":
            steps = template["steps"]
            if current_step <= len(steps):
                current_step_data = steps[current_step - 1]
                return {
                    "status": "success",
                    "type": "multi_step",
                    "title": template["title"],
                    "description": template["description"],
                    "current_step": current_step,
                    "total_steps": len(steps),
                    "step_title": current_step_data["title"],
                    "questions": current_step_data["questions"]
                }
            else:
                return {"status": "error", "message": "Session completed"}
        
        elif template["type"] == "adaptive":
            # For adaptive, return the initial question
            return {
                "status": "success",
                "type": "adaptive",
                "title": template["title"],
                "description": template["description"],
                "question": template["initial_question"]
            }
        
        return {"status": "error", "message": "Unknown template type"}
    
    def list_sessions(self, status: str = None) -> List[Dict[str, Any]]:
        """List elicitation sessions."""
        sessions = []
        
        for session_id, session in self.elicitation_sessions.items():
            if status and session["status"] != status:
                continue
            
            sessions.append({
                "session_id": session_id,
                "template_id": session["template_id"],
                "status": session["status"],
                "created_at": session["created_at"],
                "completed": session["completed"],
                "current_step": session["current_step"]
            })
        
        return sessions
    
    def get_session_results(self, session_id: str) -> Dict[str, Any]:
        """Get results from a completed session."""
        session = self.get_session(session_id)
        if not session:
            return {"status": "error", "message": "Session not found"}
        
        if not session["completed"]:
            return {"status": "error", "message": "Session not completed"}
        
        return {
            "status": "success",
            "session_id": session_id,
            "template_id": session["template_id"],
            "responses": session["responses"],
            "completed_at": session.get("completed_at"),
            "total_responses": len(session["responses"])
        }
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """List available elicitation templates."""
        templates = []
        
        for template_id, template in self.elicitation_templates.items():
            templates.append({
                "id": template_id,
                "type": template["type"],
                "title": template["title"],
                "description": template["description"]
            })
        
        return templates


# ============================================================================
# MCP Elicitation Tools
# ============================================================================

elicitation_manager = ElicitationManager()


@tool("list_elicitation_templates")
async def list_elicitation_templates_tool() -> Dict[str, Any]:
    """
    List available elicitation templates.
    
    Returns:
        Dictionary containing list of templates
    """
    try:
        templates = elicitation_manager.list_templates()
        return {
            "status": "success",
            "templates": templates,
            "count": len(templates)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("create_elicitation_session")
async def create_elicitation_session_tool(template_id: str, session_id: str = None) -> Dict[str, Any]:
    """
    Create a new elicitation session.
    
    Args:
        template_id: ID of the template to use
        session_id: Optional custom session ID
        
    Returns:
        Dictionary containing session information
    """
    try:
        result = elicitation_manager.create_elicitation_session(template_id, session_id)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("get_current_questions")
async def get_current_questions_tool(session_id: str) -> Dict[str, Any]:
    """
    Get current questions for an active session.
    
    Args:
        session_id: ID of the session
        
    Returns:
        Dictionary containing current questions
    """
    try:
        result = elicitation_manager.get_current_questions(session_id)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("submit_elicitation_response")
async def submit_elicitation_response_tool(session_id: str, responses: Dict[str, Any]) -> Dict[str, Any]:
    """
    Submit responses for an elicitation session.
    
    Args:
        session_id: ID of the session
        responses: Dictionary of responses
        
    Returns:
        Dictionary containing operation result
    """
    try:
        result = elicitation_manager.submit_response(session_id, responses)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("get_session_results")
async def get_session_results_tool(session_id: str) -> Dict[str, Any]:
    """
    Get results from a completed session.
    
    Args:
        session_id: ID of the session
        
    Returns:
        Dictionary containing session results
    """
    try:
        result = elicitation_manager.get_session_results(session_id)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("list_elicitation_sessions")
async def list_elicitation_sessions_tool(status: str = None) -> Dict[str, Any]:
    """
    List elicitation sessions.
    
    Args:
        status: Optional status filter
        
    Returns:
        Dictionary containing list of sessions
    """
    try:
        sessions = elicitation_manager.list_sessions(status)
        return {
            "status": "success",
            "sessions": sessions,
            "count": len(sessions),
            "status_filter": status
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("get_session_info")
async def get_session_info_tool(session_id: str) -> Dict[str, Any]:
    """
    Get information about a session.
    
    Args:
        session_id: ID of the session
        
    Returns:
        Dictionary containing session information
    """
    try:
        session = elicitation_manager.get_session(session_id)
        if session:
            return {
                "status": "success",
                "session": session
            }
        else:
            return {"status": "error", "message": "Session not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool("elicitation_info")
async def elicitation_info_tool() -> Dict[str, Any]:
    """
    Get information about the elicitation system.
    
    Returns:
        Dictionary containing system information
    """
    try:
        return {
            "status": "success",
            "total_templates": len(elicitation_manager.elicitation_templates),
            "total_sessions": len(elicitation_manager.elicitation_sessions),
            "active_sessions": len([s for s in elicitation_manager.elicitation_sessions.values() if s["status"] == "active"]),
            "completed_sessions": len([s for s in elicitation_manager.elicitation_sessions.values() if s["status"] == "completed"]),
            "template_types": list(set(t["type"] for t in elicitation_manager.elicitation_templates.values())),
            "available_templates": list(elicitation_manager.elicitation_templates.keys())
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============================================================================
# MCP Server Implementation
# ============================================================================

@server("mcp-elicitation-server")
class MCPElicitationServer:
    """MCP Server for elicitation management."""
    
    def __init__(self):
        self.server = Server("mcp-elicitation-server")
        
    async def initialize(self, options: InitializationOptions) -> None:
        """Initialize the server."""
        print(f"Initializing MCP Elicitation server: {options.server_name} v{options.server_version}")
        print(f"Available templates: {len(elicitation_manager.elicitation_templates)}")
        
    async def shutdown(self) -> None:
        """Shutdown the server."""
        print("Shutting down MCP Elicitation server")


async def main():
    """Main function to run the MCP elicitation server."""
    server = MCPElicitationServer()
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-elicitation-server",
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
