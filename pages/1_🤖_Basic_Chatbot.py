"""Mini Project 1: Basic Chatbot - Original Implementation."""

import streamlit as st
from ui import ChatInterface
from styles import MAIN_CSS
import logging

logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Mini Project 1: Basic Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Apply custom CSS
st.markdown(MAIN_CSS, unsafe_allow_html=True)

# Page header
st.markdown('<h1 class="main-header">🤖 Mini Project 1: Basic Chatbot</h1>', unsafe_allow_html=True)
st.markdown("*Interactive chatbot using LangChain and LMStudio with conversation memory and streaming.*")
st.markdown("---")

# Render the chat interface
chat_interface = ChatInterface()
chat_interface.render()
