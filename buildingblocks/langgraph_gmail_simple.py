"""
Simple LangGraph Gmail Agent Example

This example demonstrates a simplified LangGraph agent workflow for email processing
without requiring actual Gmail API setup. It shows the workflow structure and concepts.

Requirements:
- pip install langgraph langchain openai
- Set OPENAI_API_KEY environment variable
"""

import os
import json
from typing import Dict, Any, List
from datetime import datetime
from langgraph.graph import StateGraph, END
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


class SimpleGmailAgent:
    """Simplified LangGraph agent for email processing workflow."""
    
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=openai_api_key
        )
        
    def simulate_read_emails(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate reading emails (mock data)."""
        # Mock email data
        mock_emails = [
            {
                'id': '1',
                'subject': 'Meeting Reminder',
                'sender': 'boss@company.com',
                'date': '2024-01-15 10:00',
                'body': 'Please remember the team meeting at 2 PM today.'
            },
            {
                'id': '2',
                'subject': 'Project Update',
                'sender': 'colleague@company.com',
                'date': '2024-01-15 09:30',
                'body': 'The project is progressing well. We need your input on the design.'
            },
            {
                'id': '3',
                'subject': 'URGENT: System Alert',
                'sender': 'system@company.com',
                'date': '2024-01-15 08:45',
                'body': 'Critical system maintenance required. Please respond immediately.'
            }
        ]
        
        state["emails"] = mock_emails
        state["email_count"] = len(mock_emails)
        print(f"Read {len(mock_emails)} emails")
        
        return state
    
    def analyze_emails(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze email content using LLM."""
        if "emails" not in state or not state["emails"]:
            state["analysis"] = "No emails to analyze"
            return state
        
        emails_text = ""
        for i, email in enumerate(state["emails"], 1):
            emails_text += f"Email {i}:\n"
            emails_text += f"Subject: {email['subject']}\n"
            emails_text += f"From: {email['sender']}\n"
            emails_text += f"Date: {email['date']}\n"
            emails_text += f"Body: {email['body']}\n\n"
        
        prompt = f"""
        Analyze the following emails and provide a summary:
        
        {emails_text}
        
        Please provide:
        1. A brief summary of each email
        2. Identify any urgent or important emails
        3. Suggest any actions that might be needed
        4. Rate the urgency level (low/medium/high)
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            state["analysis"] = response.content
            print("Email analysis completed")
        except Exception as e:
            state["error"] = f"Analysis error: {e}"
            print(f"Analysis error: {e}")
        
        return state
    
    def decide_action(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Decide what action to take based on email analysis."""
        if "analysis" not in state:
            state["action"] = "No analysis available"
            return state
        
        prompt = f"""
        Based on this email analysis, what action should be taken?
        
        Analysis: {state["analysis"]}
        
        Choose one of these actions:
        1. "send_alert" - if there are urgent emails
        2. "schedule_meeting" - if meeting-related emails
        3. "follow_up" - if follow-up is needed
        4. "no_action" - if no immediate action needed
        
        Respond with just the action name.
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            action = response.content.strip().lower()
            
            if "alert" in action:
                state["action"] = "send_alert"
                state["action_reason"] = "Urgent emails detected"
            elif "meeting" in action:
                state["action"] = "schedule_meeting"
                state["action_reason"] = "Meeting-related emails found"
            elif "follow" in action:
                state["action"] = "follow_up"
                state["action_reason"] = "Follow-up required"
            else:
                state["action"] = "no_action"
                state["action_reason"] = "No immediate action needed"
                
            print(f"Decided action: {state['action']}")
            
        except Exception as e:
            state["error"] = f"Decision error: {e}"
            print(f"Decision error: {e}")
        
        return state
    
    def execute_action(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the decided action."""
        action = state.get("action", "no_action")
        
        if action == "send_alert":
            state["executed_action"] = "Alert email sent to team"
            state["action_details"] = "Sent urgent email alert to relevant team members"
        elif action == "schedule_meeting":
            state["executed_action"] = "Meeting scheduled"
            state["action_details"] = "Scheduled follow-up meeting based on email content"
        elif action == "follow_up":
            state["executed_action"] = "Follow-up email sent"
            state["action_details"] = "Sent follow-up email to address pending items"
        else:
            state["executed_action"] = "No action taken"
            state["action_details"] = "No immediate action required"
        
        print(f"Executed: {state['executed_action']}")
        return state
    
    def create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow."""
        workflow = StateGraph(StateType=Dict[str, Any])
        
        # Add nodes
        workflow.add_node("read_emails", self.simulate_read_emails)
        workflow.add_node("analyze_emails", self.analyze_emails)
        workflow.add_node("decide_action", self.decide_action)
        workflow.add_node("execute_action", self.execute_action)
        
        # Define the workflow
        workflow.set_entry_point("read_emails")
        workflow.add_edge("read_emails", "analyze_emails")
        workflow.add_edge("analyze_emails", "decide_action")
        workflow.add_edge("decide_action", "execute_action")
        workflow.add_edge("execute_action", END)
        
        return workflow.compile()
    
    def run_workflow(self) -> Dict[str, Any]:
        """Run the email processing workflow."""
        workflow = self.create_workflow()
        
        # Initial state
        initial_state = {
            "user_query": "Process my recent emails",
            "timestamp": datetime.now().isoformat()
        }
        
        # Run the workflow
        final_state = workflow.invoke(initial_state)
        
        return final_state


def test_simple_gmail_agent():
    """Test the simple Gmail agent workflow."""
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: Please set your OPENAI_API_KEY environment variable")
        return
    
    # Create and run the agent
    agent = SimpleGmailAgent(os.getenv("OPENAI_API_KEY"))
    
    print("=== Simple Gmail Agent Workflow Test ===\n")
    
    try:
        final_state = agent.run_workflow()
        
        print("=== Workflow Results ===\n")
        
        if "emails" in final_state:
            print(f"Emails processed: {final_state['email_count']}")
            
        if "analysis" in final_state:
            print("\nEmail Analysis:")
            print("-" * 50)
            print(final_state["analysis"])
            
        if "action" in final_state:
            print(f"\nDecided Action: {final_state['action']}")
            print(f"Reason: {final_state['action_reason']}")
            
        if "executed_action" in final_state:
            print(f"\nExecuted Action: {final_state['executed_action']}")
            print(f"Details: {final_state['action_details']}")
            
        if "error" in final_state:
            print(f"\nError: {final_state['error']}")
            
    except Exception as e:
        print(f"Error running workflow: {e}")


if __name__ == "__main__":
    test_simple_gmail_agent()
