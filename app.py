"""Main application entry point for the LangChain Learning Hub."""

import streamlit as st
from config import app_config
from styles import MAIN_CSS
from navigation import nav_manager, Page, PageID
from pages import (
    render_chatbot_page,
    render_sequential_chain_page,
    render_rag_chatbot_page,
    render_agent_tools_page
)
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="LangChain Learning Hub",
    page_icon="🦜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(MAIN_CSS, unsafe_allow_html=True)


def register_pages():
    """Register all available pages with the navigation manager."""
    
    # Mini Project 1: Basic Chatbot
    nav_manager.register_page(Page(
        id=PageID.CHATBOT,
        title="Basic Chatbot",
        icon="🤖",
        description="Interactive chatbot using LangChain and LMStudio with conversation memory and streaming.",
        render_function=render_chatbot_page
    ))
    
    # Mini Project 2: Sequential Chain
    nav_manager.register_page(Page(
        id=PageID.SEQUENTIAL_CHAIN,
        title="Sequential Chain Pipeline",
        icon="🔗",
        description="Chain multiple LLM operations together to build complex content generation workflows.",
        render_function=render_sequential_chain_page
    ))
    
    # Mini Project 3: RAG Chatbot
    nav_manager.register_page(Page(
        id=PageID.RAG_CHATBOT,
        title="RAG Chatbot",
        icon="📚",
        description="Retrieval-Augmented Generation chatbot that answers questions based on your documents.",
        render_function=render_rag_chatbot_page
    ))
    
    # Mini Project 4: Agent with Tools
    nav_manager.register_page(Page(
        id=PageID.AGENT_TOOLS,
        title="AI Agent with Tools",
        icon="🛠️",
        description="AI agent that can use various tools to complete complex tasks and solve problems.",
        render_function=render_agent_tools_page
    ))


def main():
    """Main application function."""
    logger.info("Starting LangChain Learning Hub")
    
    # Register all pages
    register_pages()
    
    # Render the current page using navigation manager
    nav_manager.render_current_page()
    
    logger.info("Application rendered successfully")


if __name__ == "__main__":
    main()
