# Agent Exploration Project

This repository is dedicated to exploring the world of agents—autonomous systems or entities capable of making decisions and taking actions in their environment.

## Purpose

The project serves as a sandbox for experimenting with agent concepts, architectures, implementations, and applications. Exploration is organized around the following key questions:

- **What are agents?**  
  Defining agents, their properties, and their roles in various domains.

- **Why study agents?**  
  Understanding the significance of agents in AI, automation, robotics, distributed systems, and beyond.

- **How do agents work?**  
  Investigating agent architectures, decision-making processes, learning strategies, and interaction mechanisms.

- **Who uses agents?**  
  Exploring applications and industries where agents play a critical role.

- **When are agents relevant?**  
  Analyzing scenarios and problems where agent-based approaches are beneficial.

## Topics Covered

- **[Understanding Agents](knowledgebase/understanding-agents.md):**  
  Comprehensive overview of agent concepts, types, architectures, and applications.

- **[Agent Research Frontier](knowledgebase/agent-frontier-issues.md):**  
  Current challenges and research directions in agent development and deployment.

- **Building Blocks of Agents:**  
  Fundamental components and principles that make up agent systems.

- **System Design:**  
  Architectures and design patterns for various agent types.

- **Agent Implementations:**  
  Example implementations and prototypes of selected agents.

- **Current Issues:**  
  Challenges and open problems in agent research and application.

## Building Blocks Examples

The `buildingblocks/` directory contains comprehensive examples and tests demonstrating various agent capabilities and integrations:

### **Custom Tools and LangChain Integration**
- `custom_tool_example.py` - Simple custom calculator tool implementation
- `test_custom_tool_with_langchain.py` - Testing custom tools with LangChain agents and ChatGPT LLM
- `test_custom_tool_with_langchain_colab.ipynb` - Google Colab notebook version of the custom tool test

### **Web Search and Information Retrieval**
- `web_search_agent_example.py` - Web search capabilities using DuckDuckGo with LangChain agents and ChatGPT LLM

### **RAG (Retrieval-Augmented Generation) Systems**
- `rag_agent_example.py` - Comprehensive RAG system with LangChain and OpenAI LLM
- `rag_agent_simple.py` - Simplified RAG agent example
- `rag_agent_colab.ipynb` - Google Colab notebook version of the RAG agent

### **MCP (Model Context Protocol) Integration**
- `mcp_langchain_integration.py` - Integration of MCP tools with LangChain agents and ChatGPT LLM
- `mcp_langchain_simple.py` - Simplified MCP-LangChain integration
- `mcp_langchain_integration_colab.ipynb` - Google Colab notebook version of MCP-LangChain integration

### **FastMCP Framework**
- `fastmcp_server_example.py` - FastMCP server implementation with various tools
- `fastmcp_client_test.py` - Client to test FastMCP server functionality

### **LangGraph Workflow Automation**
- `langgraph_gmail_agent.py` - LangGraph agent integrated with Gmail API for email processing
- `langgraph_gmail_simple.py` - Simplified LangGraph Gmail agent using mock data

### **MCP Core Features**

#### **Resources Management**
- `mcp_resources_example.py` - MCP resources usage including file, directory, and data resources
- `mcp_resources_client_test.py` - Client to test MCP resources functionality

#### **Prompts Management**
- `mcp_prompts_example.py` - MCP prompts usage including templates, variables, and validation
- `mcp_prompts_client_test.py` - Client to test MCP prompts functionality

#### **Sampling Strategies**
- `mcp_sampling_example.py` - MCP sampling usage including random, stratified, systematic, and Monte Carlo sampling
- `mcp_sampling_client_test.py` - Client to test MCP sampling functionality

#### **Roots Management**
- `mcp_roots_example.py` - MCP roots usage including file system, database, API, and network roots
- `mcp_roots_client_test.py` - Client to test MCP roots functionality

#### **Tool Types**
- `mcp_tool_types_example.py` - MCP tool types usage including simple, complex, file, network, and ML tools
- `mcp_tool_types_client_test.py` - Client to test MCP tool types functionality

#### **Elicitation**
- `mcp_elicitation_example.py` - MCP elicitation usage for gathering information and preferences

### **Example Categories**

#### **Basic Agent Capabilities**
- Custom tool creation and integration
- Web search and information retrieval
- RAG systems for knowledge augmentation

#### **Advanced Integrations**
- MCP protocol for tool discovery and usage
- LangGraph for workflow automation
- FastMCP for modern MCP implementations

#### **MCP Core Features**
- **Resources**: File, directory, and data management
- **Prompts**: Template management and variable substitution
- **Sampling**: Statistical sampling strategies
- **Roots**: System resource management
- **Tool Types**: Various tool categories and capabilities
- **Elicitation**: Information gathering and preference elicitation

#### **Testing and Validation**
Each example includes comprehensive client tests demonstrating:
- Parameter validation
- Error handling
- Integration testing
- Performance testing
- Real-world usage scenarios

## How to Use this Repository

- Browse code samples and prototypes in the `buildingblocks/` directory
- Run examples to understand agent capabilities
- Use client tests to validate functionality
- Read documentation and notes about various agent approaches
- Contribute your own experiments or references
- Suggest new ideas or features via issues

## Getting Started

1. **Install Dependencies**: Most examples require `langchain`, `openai`, `mcp`, and other Python packages
2. **Set Up API Keys**: Configure OpenAI API keys for LLM-based examples
3. **Run Examples**: Start with simple examples like `custom_tool_example.py`
4. **Test Functionality**: Use corresponding client test files to validate
5. **Explore Integrations**: Try MCP and LangGraph examples for advanced features

## Contributions

Feel free to add anything agent-related—code, papers, links, or notes—that you think is worth sharing!

---

*This README will expand as the project grows and new directions are explored.*