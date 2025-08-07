"""
Web Search Agent Example using DuckDuckGo with LangChain and ChatGPT LLM

This example demonstrates how to create an agent that can search the web for real-time information
using DuckDuckGo search tool and ChatGPT as the LLM.

Requirements:
- pip install langchain openai duckduckgo-search
- Set OPENAI_API_KEY environment variable
"""

from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
import os

def create_web_search_agent():
    """Create a LangChain agent with DuckDuckGo search capability."""
    
    # Initialize the search tool
    search_tool = DuckDuckGoSearchRun()
    
    # Set up the LLM (ChatGPT)
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Initialize the agent with the search tool
    agent = initialize_agent(
        tools=[search_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agent

def test_web_search_agent():
    """Test the web search agent with various queries."""
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: Please set your OPENAI_API_KEY environment variable")
        return
    
    # Create the agent
    agent = create_web_search_agent()
    
    # Test queries
    test_queries = [
        "What are the latest developments in AI technology?",
        "What is the current weather in New York?",
        "What are the top news headlines today?",
        "What is the latest version of Python?"
    ]
    
    print("=== Web Search Agent Test ===\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"Test {i}: {query}")
        print("-" * 50)
        
        try:
            response = agent.run(query)
            print(f"Response: {response}\n")
        except Exception as e:
            print(f"Error: {e}\n")
        
        print("=" * 50 + "\n")

if __name__ == "__main__":
    test_web_search_agent()
