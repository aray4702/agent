"""
MCP Tools Integration with LangChain Agent and ChatGPT LLM

This example demonstrates how to integrate MCP (Model Context Protocol) tools
with LangChain agents and ChatGPT LLM for dynamic tool discovery and usage.

Requirements:
- pip install langchain openai mcp
- Set OPENAI_API_KEY environment variable
- Run an MCP server (e.g., fastmcp_server_example.py)
"""

import os
import asyncio
import json
from typing import Any, Dict, List, Optional
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


class MCPLangChainAgent:
    """Agent that integrates MCP tools with LangChain and ChatGPT."""
    
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self.mcp_session = None
        self.agent = None
        
    async def connect_to_mcp_server(self, server_command: List[str]):
        """Connect to an MCP server."""
        server_params = StdioServerParameters(
            command=server_command[0],
            args=server_command[1:]
        )
        
        self.mcp_session = ClientSession(server_params)
        await self.mcp_session.initialize()
        print(f"Connected to MCP server: {server_command}")
        
    async def discover_mcp_tools(self) -> List[Dict[str, Any]]:
        """Discover available tools from the MCP server."""
        if not self.mcp_session:
            raise RuntimeError("Not connected to MCP server")
            
        request = ListToolsRequest()
        result = await self.mcp_session.list_tools(request)
        
        tools = []
        for tool in result.tools:
            tools.append({
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.inputSchema
            })
            
        return tools
        
    def create_langchain_tools(self, mcp_tools: List[Dict[str, Any]]) -> List[Tool]:
        """Convert MCP tools to LangChain tools."""
        langchain_tools = []
        
        for mcp_tool in mcp_tools:
            tool_name = mcp_tool["name"]
            tool_description = mcp_tool["description"]
            
            # Create adapter for the MCP tool
            adapter = MCPToolAdapter(self.mcp_session, tool_name, tool_description)
            
            # Create LangChain tool
            langchain_tool = Tool(
                name=tool_name,
                func=adapter,
                description=tool_description
            )
            
            langchain_tools.append(langchain_tool)
            
        return langchain_tools
        
    def create_agent(self, tools: List[Tool]):
        """Create a LangChain agent with the provided tools."""
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=self.openai_api_key
        )
        
        self.agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True
        )
        
    async def run_query(self, query: str) -> str:
        """Run a query using the agent."""
        if not self.agent:
            raise RuntimeError("Agent not initialized")
            
        try:
            result = self.agent.run(query)
            return result
        except Exception as e:
            return f"Error running query: {str(e)}"
            
    async def close(self):
        """Close the MCP session."""
        if self.mcp_session:
            await self.mcp_session.shutdown()


async def test_mcp_langchain_integration():
    """Test the MCP-LangChain integration."""
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: Please set your OPENAI_API_KEY environment variable")
        return
    
    # Create the integrated agent
    agent = MCPLangChainAgent(os.getenv("OPENAI_API_KEY"))
    
    try:
        # Connect to MCP server (assuming FastMCP server is running)
        await agent.connect_to_mcp_server(["python", "buildingblocks/fastmcp_server_example.py"])
        
        # Discover available tools
        print("\n=== Discovering MCP Tools ===")
        mcp_tools = await agent.discover_mcp_tools()
        for tool in mcp_tools:
            print(f"- {tool['name']}: {tool['description']}")
            
        # Convert MCP tools to LangChain tools
        print("\n=== Converting to LangChain Tools ===")
        langchain_tools = agent.create_langchain_tools(mcp_tools)
        print(f"Created {len(langchain_tools)} LangChain tools")
        
        # Create the agent
        agent.create_agent(langchain_tools)
        print("Agent created successfully!")
        
        # Test queries
        test_queries = [
            "What is 15 plus 7?",
            "What is the weather like in Paris?",
            "Can you create a file called test.txt with the content 'Hello from MCP integration'?",
            "What is the current system information?",
            "Can you read the file test.txt and tell me its contents?",
            "What is 25 multiplied by 4?"
        ]
        
        print("\n=== Testing MCP-LangChain Integration ===\n")
        
        for i, query in enumerate(test_queries, 1):
            print(f"Test {i}: {query}")
            print("-" * 50)
            
            try:
                response = await agent.run_query(query)
                print(f"Response: {response}\n")
            except Exception as e:
                print(f"Error: {e}\n")
            
            print("=" * 50 + "\n")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the MCP server is running first!")
    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(test_mcp_langchain_integration())
