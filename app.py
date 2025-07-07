"""Main application entry point for the LangChain Learning Hub."""

import streamlit as st
from ui import ChatInterface
from styles import MAIN_CSS

# Page configuration
st.set_page_config(
    page_title="LangChain Learning Hub",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(MAIN_CSS, unsafe_allow_html=True)

# Page header
st.markdown('<h1 class="main-header">🔗 LangChain Learning Hub</h1>', unsafe_allow_html=True)
st.markdown("*A collection of mini-projects to learn LangChain concepts and implementations.*")
st.markdown("---")

# Main content
st.markdown("## Welcome to the LangChain Learning Hub!")

st.markdown("""
This application contains a series of mini-projects to help you learn various LangChain concepts and implementations:

1. **🤖 Basic Chatbot** - A simple chatbot with conversation memory and streaming responses
2. **🔗 Sequential Chain Pipeline** - Chain multiple LLM operations for complex workflows
3. **📚 RAG Chatbot** - Chat with your documents using Retrieval-Augmented Generation
4. **🛠️ Agent with Tools** - Build AI agents that can use tools to complete complex tasks
""")

st.info("""
**How to navigate:** Use the sidebar to switch between mini-projects.

Each mini-project includes:
- Working implementation
- Explanation of key concepts
- Code annotations
- Learning resources
""")

# Footer
st.markdown("---")
st.markdown("*Made with Streamlit and LangChain*")
