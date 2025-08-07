"""
Simple MCP-LangChain Integration Example

This example demonstrates how to integrate MCP tools with LangChain agents
and ChatGPT LLM for dynamic tool discovery and usage.

Requirements:
- pip install langchain openai mcp
- Set OPENAI_API_KEY environment variable
- Run an MCP server (e.g., fastmcp_server_example.py)
"""

import os
import asyncio
import json
from typing import Any, Dict, List
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from mcp.client import ClientSession, StdioServerParameters
from mcp.types import CallToolRequest, ListToolsRequest


class MCPToolAdapter:
    """Adapter to convert MCP tools to LangChain tools."""
    
    def __init__(self, mcp_session: ClientSession, tool_name: str, tool_description: str):
        self.mcp_session = mcp_session
        self.tool_name = tool_name
        self.tool_description = tool_description
        
    def __call__(self, *args, **kwargs) -> str:
        """Execute the MCP tool and return the result."""
        try:
            # Convert arguments to the format expected by MCP
            arguments = kwargs if kwargs else {}
            
            # Create the tool call request
            request = CallToolRequest(name=self.tool_name, arguments=arguments)
            
            # Execute the tool
            result = asyncio.run(self.mcp_session.call_tool(request))
            
            # Extract text content from the result
            if result.content and len(result.content) > 0:
                return result.content[0].text
            return "No response"
            
        except Exception as e:
            return f"Error executing MCP tool {self.tool_name}: {str(e)}"


async def main():
    """Main function to demonstrate MCP-LangChain integration."""
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: Please set your OPENAI_API_KEY environment variable")
        return
    
    print("Setting up MCP-LangChain integration...")
    
    # Connect to MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["buildingblocks/fastmcp_server_example.py"]
    )
    
    mcp_session = ClientSession(server_params)
    await mcp_session.initialize()
    print("Connected to MCP server")
    
    # Discover available tools
    print("\n=== Discovering MCP Tools ===")
    request = ListToolsRequest()
    result = await mcp_session.list_tools(request)
    
    mcp_tools = []
    for tool in result.tools:
        mcp_tools.append({
            "name": tool.name,
            "description": tool.description,
            "inputSchema": tool.inputSchema
        })
        print(f"- {tool.name}: {tool.description}")
    
    # Convert MCP tools to LangChain tools
    print("\n=== Converting to LangChain Tools ===")
    langchain_tools = []
    
    for mcp_tool in mcp_tools:
        tool_name = mcp_tool["name"]
        tool_description = mcp_tool["description"]
        
        # Create adapter for the MCP tool
        adapter = MCPToolAdapter(mcp_session, tool_name, tool_description)
        
        # Create LangChain tool
        langchain_tool = Tool(
            name=tool_name,
            func=adapter,
            description=tool_description
        )
        
        langchain_tools.append(langchain_tool)
    
    print(f"Created {len(langchain_tools)} LangChain tools")
    
    # Create LangChain agent
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    agent = initialize_agent(
        tools=langchain_tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )
    
    print("Agent created successfully!")
    
    # Test the agent
    test_queries = [
        "What is 15 plus 7?",
        "What is the weather like in Paris?",
        "What is the current system information?"
    ]
    
    print("\n=== Testing MCP-LangChain Integration ===\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"Test {i}: {query}")
        print("-" * 50)
        
        try:
            response = agent.run(query)
            print(f"Response: {response}\n")
        except Exception as e:
            print(f"Error: {e}\n")
        
        print("=" * 50 + "\n")
    
    # Close the MCP session
    await mcp_session.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
