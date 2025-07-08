"""Shared layout utilities for Streamlit pages."""

import streamlit as st
from ui import SidebarComponents, SessionStateManager
from styles import MAIN_CSS

def setup_page(title: str, icon: str, page_title: str) -> None:
    """
    Setup the page with standard configuration including sidebar.
    
    Args:
        title: Main title to display at the top of the page
        icon: Icon emoji for the page
        page_title: Title for the browser tab
    """
    # Page configuration
    st.set_page_config(
        page_title=page_title,
        page_icon=icon,
        layout="wide"
    )
    
    # Initialize session state
    SessionStateManager.initialize()
    
    # Render sidebar - consistent across all pages
    sidebar = SidebarComponents()
    sidebar.render_all()
    
    # Apply custom CSS
    st.markdown(MAIN_CSS, unsafe_allow_html=True)
    
    # Page header
    st.markdown(f'<h1 class="main-header">{icon} {title}</h1>', unsafe_allow_html=True)
