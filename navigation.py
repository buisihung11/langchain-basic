"""Navigation and routing system for the multi-page LangChain application."""

import streamlit as st
from typing import Dict, Callable, Any
from dataclasses import dataclass
from enum import Enum


class PageID(Enum):
    """Enumeration of all available pages."""
    CHATBOT = "chatbot"
    SEQUENTIAL_CHAIN = "sequential_chain"
    RAG_CHATBOT = "rag_chatbot"
    AGENT_TOOLS = "agent_tools"


@dataclass
class Page:
    """Represents a page in the application."""
    id: PageID
    title: str
    icon: str
    description: str
    render_function: Callable[[], None]
    order: int = 0  # Add order field for sorting


class NavigationManager:
    """Manages page navigation and routing."""
    
    def __init__(self):
        self.pages: Dict[PageID, Page] = {}
        self._current_page = None
    
    def register_page(self, page: Page) -> None:
        """Register a new page."""
        self.pages[page.id] = page
    
    def get_page(self, page_id: PageID) -> Page:
        """Get a page by ID."""
        return self.pages.get(page_id)
    
    def get_all_pages(self) -> Dict[PageID, Page]:
        """Get all registered pages."""
        return self.pages
    
    def render_sidebar_navigation(self) -> PageID:
        """Render the sidebar navigation and return selected page ID."""
        st.sidebar.title("🦜 LangChain Learning Hub")
        st.sidebar.markdown("---")
        
        # Sort pages by order and create options
        sorted_pages = sorted(self.pages.values(), key=lambda p: p.order)
        page_options = {
            f"{page.icon} Mini Project {page.order}: {page.title}": page.id 
            for page in sorted_pages
        }
        
        # Get current selection from session state or default to chatbot
        if "current_page" not in st.session_state:
            st.session_state.current_page = PageID.CHATBOT
        
        # Find current page display name
        current_display_name = next(
            (display_name for display_name, page_id in page_options.items() 
             if page_id == st.session_state.current_page),
            list(page_options.keys())[0]
        )
        
        selected_display_name = st.sidebar.selectbox(
            "Select Mini Project:",
            options=list(page_options.keys()),
            index=list(page_options.keys()).index(current_display_name),
            key="page_selector"
        )
        
        selected_page_id = page_options[selected_display_name]
        st.session_state.current_page = selected_page_id
        
        # Show page description
        selected_page = self.get_page(selected_page_id)
        if selected_page:
            st.sidebar.markdown(f"**Description:**")
            st.sidebar.markdown(selected_page.description)
        
        st.sidebar.markdown("---")
        
        return selected_page_id
    
    def render_page_header(self, page_id: PageID) -> None:
        """Render the main page header."""
        page = self.get_page(page_id)
        if page:
            # Include project number in header
            header_title = f"{page.icon} Mini Project {page.order}: {page.title}"
            st.markdown(
                f'<h1 class="main-header">{header_title}</h1>', 
                unsafe_allow_html=True
            )
            st.markdown(f"*{page.description}*")
            st.markdown("---")
    
    def render_current_page(self) -> None:
        """Render the currently selected page."""
        current_page_id = self.render_sidebar_navigation()
        self.render_page_header(current_page_id)
        
        page = self.get_page(current_page_id)
        if page and page.render_function:
            page.render_function()
        else:
            st.error(f"Page {current_page_id.value} not found or has no render function!")


# Global navigation manager instance
nav_manager = NavigationManager()
