"""
LangGraph Gmail Agent Example

This example demonstrates how to create a LangGraph agent that integrates with Gmail
for email processing, sending, and workflow automation.

Requirements:
- pip install langgraph langchain openai google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
- Set OPENAI_API_KEY environment variable
- Set up Gmail API credentials
"""

import os
import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from langgraph.graph import StateGraph, END
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import email


class GmailAgent:
    """LangGraph agent for Gmail operations."""
    
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=openai_api_key
        )
        self.gmail_service = None
        self.setup_gmail_service()
        
    def setup_gmail_service(self):
        """Set up Gmail API service."""
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
                  'https://www.googleapis.com/auth/gmail.send']
        
        creds = None
        # The file token.json stores the user's access and refresh tokens
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        try:
            self.gmail_service = build('gmail', 'v1', credentials=creds)
            print("Gmail service initialized successfully!")
        except Exception as e:
            print(f"Error setting up Gmail service: {e}")
            self.gmail_service = None
    
    def read_emails(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Read recent emails from Gmail."""
        if not self.gmail_service:
            state["error"] = "Gmail service not available"
            return state
        
        try:
            # Get recent emails
            results = self.gmail_service.users().messages().list(
                userId='me', maxResults=5).execute()
            
            messages = results.get('messages', [])
            email_data = []
            
            for message in messages:
                msg = self.gmail_service.users().messages().get(
                    userId='me', id=message['id']).execute()
                
                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
                date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')
                
                # Get email body
                body = ""
                if 'parts' in msg['payload']:
                    for part in msg['payload']['parts']:
                        if part['mimeType'] == 'text/plain':
                            body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                            break
                elif 'body' in msg['payload']:
                    body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
                
                email_data.append({
                    'id': message['id'],
                    'subject': subject,
                    'sender': sender,
                    'date': date,
                    'body': body[:500] + "..." if len(body) > 500 else body
                })
            
            state["emails"] = email_data
            state["email_count"] = len(email_data)
            print(f"Read {len(email_data)} emails")
            
        except HttpError as error:
            state["error"] = f"Gmail API error: {error}"
            print(f"Gmail API error: {error}")
        
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
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            state["analysis"] = response.content
            print("Email analysis completed")
        except Exception as e:
            state["error"] = f"Analysis error: {e}"
            print(f"Analysis error: {e}")
        
        return state
    
    def send_email(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Send an email using Gmail API."""
        if not self.gmail_service:
            state["error"] = "Gmail service not available"
            return state
        
        # Check if we need to send an email based on analysis
        if "analysis" in state and "urgent" in state["analysis"].lower():
            try:
                # Create email message
                message = email.mime.text.MIMEText(
                    "This is an automated response to urgent emails.",
                    'plain'
                )
                message['to'] = 'your-email@gmail.com'  # Replace with actual email
                message['subject'] = 'Urgent Email Alert'
                
                # Encode the message
                raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
                
                # Send the email
                self.gmail_service.users().messages().send(
                    userId='me', body={'raw': raw_message}).execute()
                
                state["email_sent"] = True
                state["sent_message"] = "Alert email sent for urgent emails"
                print("Alert email sent")
                
            except HttpError as error:
                state["error"] = f"Error sending email: {error}"
                print(f"Error sending email: {error}")
        
        return state
    
    def create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow."""
        workflow = StateGraph(StateType=Dict[str, Any])
        
        # Add nodes
        workflow.add_node("read_emails", self.read_emails)
        workflow.add_node("analyze_emails", self.analyze_emails)
        workflow.add_node("send_email", self.send_email)
        
        # Define the workflow
        workflow.set_entry_point("read_emails")
        workflow.add_edge("read_emails", "analyze_emails")
        workflow.add_edge("analyze_emails", "send_email")
        workflow.add_edge("send_email", END)
        
        return workflow.compile()
    
    def run_workflow(self) -> Dict[str, Any]:
        """Run the Gmail workflow."""
        workflow = self.create_workflow()
        
        # Initial state
        initial_state = {
            "user_query": "Process my recent emails",
            "timestamp": datetime.now().isoformat()
        }
        
        # Run the workflow
        final_state = workflow.invoke(initial_state)
        
        return final_state


def test_gmail_agent():
    """Test the Gmail agent workflow."""
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: Please set your OPENAI_API_KEY environment variable")
        return
    
    # Check if Gmail credentials are available
    if not os.path.exists('credentials.json'):
        print("Error: Please download credentials.json from Google Cloud Console")
        print("1. Go to Google Cloud Console")
        print("2. Enable Gmail API")
        print("3. Create credentials (OAuth 2.0 Client ID)")
        print("4. Download as credentials.json")
        return
    
    # Create and run the agent
    agent = GmailAgent(os.getenv("OPENAI_API_KEY"))
    
    print("=== Gmail Agent Workflow Test ===\n")
    
    try:
        final_state = agent.run_workflow()
        
        print("=== Workflow Results ===\n")
        
        if "emails" in final_state:
            print(f"Emails processed: {final_state['email_count']}")
            
        if "analysis" in final_state:
            print("\nEmail Analysis:")
            print("-" * 50)
            print(final_state["analysis"])
            
        if "email_sent" in final_state:
            print(f"\nEmail Action: {final_state['sent_message']}")
            
        if "error" in final_state:
            print(f"\nError: {final_state['error']}")
            
    except Exception as e:
        print(f"Error running workflow: {e}")


if __name__ == "__main__":
    test_gmail_agent()
