"""Mini Project 1: Basic Chatbot - Original Implementation."""

import streamlit as st
from ui import ChatInterface


def render_chatbot_page() -> None:
    """Render the basic chatbot page (original implementation)."""
    
    # Just use the existing ChatInterface
    chat_interface = ChatInterface()
    chat_interface.render()


if __name__ == "__main__":
    render_chatbot_page()
