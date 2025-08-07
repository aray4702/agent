"""
Simple RAG Agent Example with LangChain and OpenAI LLM

This example demonstrates how to build a RAG system that can be used by agents
to access knowledge bases and provide more accurate, contextual responses.

Requirements:
- pip install langchain openai chromadb sentence-transformers
- Set OPENAI_API_KEY environment variable
"""

import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA


def create_sample_documents() -> List[str]:
    """Create sample documents for demonstration."""
    return [
        """
        Artificial Intelligence (AI) is a branch of computer science that aims to create 
        intelligent machines that can perform tasks that typically require human intelligence. 
        These tasks include learning, reasoning, problem-solving, perception, and language understanding.
        
        Key areas of AI include:
        - Machine Learning: Algorithms that can learn from data
        - Natural Language Processing: Understanding and generating human language
        - Computer Vision: Interpreting visual information
        - Robotics: Physical systems that can interact with the environment
        """,
        
        """
        Machine Learning is a subset of AI that focuses on developing algorithms and 
        statistical models that enable computers to improve their performance on a specific 
        task through experience. There are three main types of machine learning:
        
        1. Supervised Learning: Learning from labeled training data
        2. Unsupervised Learning: Finding patterns in unlabeled data
        3. Reinforcement Learning: Learning through interaction with an environment
        """,
        
        """
        Large Language Models (LLMs) are a type of neural network that can understand 
        and generate human language. They are trained on vast amounts of text data and 
        can perform various natural language processing tasks.
        
        Popular LLMs include:
        - GPT (Generative Pre-trained Transformer) series by OpenAI
        - BERT (Bidirectional Encoder Representations from Transformers) by Google
        - T5 (Text-To-Text Transfer Transformer) by Google
        - LLaMA (Large Language Model Meta AI) by Meta
        """,
        
        """
        Retrieval-Augmented Generation (RAG) is a technique that combines information 
        retrieval with text generation. It works by:
        
        1. Retrieving relevant documents from a knowledge base
        2. Using the retrieved information to generate more accurate responses
        3. Providing citations and sources for the generated content
        
        RAG systems are particularly useful for:
        - Question answering with up-to-date information
        - Reducing hallucinations in language models
        - Providing factual, sourced responses
        """
    ]


def main():
    """Main function to demonstrate RAG agent."""
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: Please set your OPENAI_API_KEY environment variable")
        return
    
    print("Building RAG system...")
    
    # Create embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create sample documents
    documents = create_sample_documents()
    
    # Create text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    # Split documents into chunks
    texts = []
    for doc in documents:
        chunks = text_splitter.split_text(doc)
        texts.extend(chunks)
    
    print(f"Created {len(texts)} text chunks from {len(documents)} documents")
    
    # Create vector store
    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    
    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        ),
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
    )
    
    print("Knowledge base built successfully!")
    
    # Create RAG tool
    def rag_query(query: str) -> str:
        """Query the RAG system."""
        try:
            result = qa_chain.run(query)
            return result
        except Exception as e:
            return f"Error querying RAG system: {str(e)}"
    
    rag_tool = Tool(
        name="rag_knowledge_base",
        func=rag_query,
        description="Useful for answering questions about AI, machine learning, LLMs, and RAG systems."
    )
    
    # Create agent
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    agent = initialize_agent(
        tools=[rag_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )
    
    print("RAG Agent created successfully!")
    
    # Test the agent
    test_query = "What is artificial intelligence and what are its key areas?"
    print(f"\nTesting query: {test_query}")
    print("-" * 50)
    
    try:
        response = agent.run(test_query)
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
