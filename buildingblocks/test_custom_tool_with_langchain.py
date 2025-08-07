"""
Test: Using CustomCalculatorTool with LangChain Agent and ChatGPT LLM

Requirements:
- pip install langchain openai
- Set your OpenAI API key in the environment: export OPENAI_API_KEY=sk-...

This script demonstrates how to register a custom tool with a LangChain agent and use ChatGPT as the LLM.
"""

from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
import os

# Import the custom tool
from buildingblocks.custom_tool_example import CustomCalculatorTool

def main():
    # Initialize the custom calculator tool
    calc = CustomCalculatorTool()

    # Define the tool for LangChain
    calculator_tool = Tool(
        name="Calculator",
        func=lambda x: str(eval(x)),  # For demo: use eval for simple math expressions
        description="Useful for simple math operations. Input should be a valid Python math expression, e.g., '2 + 2' or '10 / 5'."
    )

    # (Optional) If you want to use the actual methods, you can define more granular tools:
    # add_tool = Tool(name="Add", func=lambda x: str(calc.add(*map(float, x.split()))), description="Add two numbers. Input: 'a b'")
    # ...

    # Set up the LLM
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # Initialize the agent with the tool
    agent = initialize_agent(
        tools=[calculator_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    # Test: Ask the agent a math question
    question = "What is 7 times 8 plus 10?"
    print("Agent response:")
    response = agent.run(question)
    print(response)

if __name__ == "__main__":
    main()
