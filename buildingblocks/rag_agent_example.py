"""
RAG (Retrieval-Augmented Generation) Agent Example with LangChain and OpenAI LLM

This example demonstrates how to build a RAG system that can be used by agents
to access knowledge bases and provide more accurate, contextual responses.

Requirements:
- pip install langchain openai chromadb sentence-transformers
- Set OPENAI_API_KEY environment variable
"""

import os
from typing import List, Dict, Any
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA


class RAGAgent:
    """RAG Agent that combines knowledge base with LLM for enhanced responses."""
    
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.vectorstore = None
        self.qa_chain = None
        
    def create_sample_documents(self) -> List[str]:
        """Create sample documents for demonstration."""
        documents = [
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
        return documents
    
    def build_knowledge_base(self, documents: List[str], persist_directory: str = "./chroma_db"):
        """Build a knowledge base from documents."""
        print("Building knowledge base...")
        
        # Create text splitter for chunking documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Split documents into chunks
        texts = []
        for i, doc in enumerate(documents):
            chunks = text_splitter.split_text(doc)
            for chunk in chunks:
                texts.append(chunk)
        
        print(f"Created {len(texts)} text chunks from {len(documents)} documents")
        
        # Create vector store
        self.vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings,
            persist_directory=persist_directory
        )
        
        # Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(
                model_name="gpt-3.5-turbo",
                temperature=0,
                openai_api_key=self.openai_api_key
            ),
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3})
        )
        
        print("Knowledge base built successfully!")
        
    def create_rag_tool(self) -> Tool:
        """Create a RAG tool for the agent."""
        def rag_query(query: str) -> str:
            """Query the RAG system."""
            if not self.qa_chain:
                return "RAG system not initialized. Please build the knowledge base first."
            
            try:
                result = self.qa_chain.run(query)
                return result
            except Exception as e:
                return f"Error querying RAG system: {str(e)}"
        
        return Tool(
            name="rag_knowledge_base",
            func=rag_query,
            description="Useful for answering questions about AI, machine learning, LLMs, and RAG systems. Input should be a question about these topics."
        )
    
    def create_agent(self) -> Any:
        """Create a LangChain agent with RAG capabilities."""
        if not self.qa_chain:
            raise ValueError("RAG system not initialized. Please build the knowledge base first.")
        
        # Create the RAG tool
        rag_tool = self.create_rag_tool()
        
        # Set up the LLM
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=self.openai_api_key
        )
        
        # Initialize the agent
        agent = initialize_agent(
            tools=[rag_tool],
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True
        )
        
        return agent


def test_rag_agent():
    """Test the RAG agent with various queries."""
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: Please set your OPENAI_API_KEY environment variable")
        return
    
    # Create RAG agent
    rag_agent = RAGAgent(os.getenv("OPENAI_API_KEY"))
    
    # Create sample documents
    documents = rag_agent.create_sample_documents()
    
    # Build knowledge base
    rag_agent.build_knowledge_base(documents)
    
    # Create agent
    agent = rag_agent.create_agent()
    
    # Test queries
    test_queries = [
        "What is artificial intelligence?",
        "What are the three main types of machine learning?",
        "What are some popular large language models?",
        "How does RAG work and what are its benefits?",
        "What is the difference between supervised and unsupervised learning?",
        "How do LLMs understand and generate human language?"
    ]
    
    print("\n=== RAG Agent Test ===\n")
    
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
    test_rag_agent()
