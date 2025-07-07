"""Mini Project 3: ConversationalRetrievalChain (RAG Chatbot) - Placeholder Page."""

import streamlit as st
from styles import MAIN_CSS
import logging

logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Mini Project 3: RAG Chatbot",
    page_icon="📚",
    layout="wide"
)

# Apply custom CSS
st.markdown(MAIN_CSS, unsafe_allow_html=True)

# Page header
st.markdown('<h1 class="main-header">📚 Mini Project 3: RAG Chatbot</h1>', unsafe_allow_html=True)
st.markdown("*Building a chatbot that can answer questions based on your documents using RAG (Retrieval-Augmented Generation).*")
st.markdown("---")

# Main content
st.markdown("## 📚 RAG Chatbot with Document Retrieval")

st.info("""
**What we'll build:** A chatbot that can answer questions based on your documents using RAG (Retrieval-Augmented Generation).

Upload PDFs, text files, or web content and chat with your data!
""")

st.markdown("### Key Features:")
st.markdown("- Upload and process documents")
st.markdown("- Vector embeddings and similarity search")
st.markdown("- Context-aware responses")
st.markdown("- Conversation memory with document context")

st.warning("🚧 **Coming Soon!** This page will be implemented in a future lesson.")
