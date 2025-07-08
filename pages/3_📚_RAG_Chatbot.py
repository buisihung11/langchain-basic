"""Mini Project 3: ConversationalRetrievalChain (RAG Chatbot) - Placeholder Page."""

import streamlit as st
import logging
from layout_utils import setup_page  # Import the shared layout utility

logger = logging.getLogger(__name__)

# Setup page with shared layout utility
setup_page(
    title="Mini Project 3: RAG Chatbot",
    icon="📚",
    page_title="Mini Project 3: RAG Chatbot"
)

# Subtitle
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
