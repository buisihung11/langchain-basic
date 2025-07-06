"""Main application entry point for the LangChain Chatbot."""

import streamlit as st
from config import app_config
from styles import MAIN_CSS
from ui import ChatInterface
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title=app_config.page_title,
    page_icon=app_config.page_icon,
    layout='wide',  # Only 'centered' or 'wide' are allowed
    initial_sidebar_state='auto'  # Using 'auto', 'expanded', or 'collapsed'
)

# Apply custom CSS
st.markdown(MAIN_CSS, unsafe_allow_html=True)


def main():
    """Main application function."""
    logger.info("Starting LangChain Chatbot application")
    
    # App header
    st.markdown(
        '<h1 class="main-header">🤖 LangChain Chatbot</h1>', 
        unsafe_allow_html=True
    )
    
    # Initialize and render the chat interface
    chat_interface = ChatInterface()
    chat_interface.render()
    
    logger.info("Application rendered successfully")


if __name__ == "__main__":
    main()
