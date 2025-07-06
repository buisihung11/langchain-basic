"""UI components and session state management for the chatbot."""

import streamlit as st
from typing import Dict, Any, List, Tuple
from config import app_config, ui_config, lmstudio_config
from utils import ConnectionManager, get_example_prompts, validate_temperature
from chatbot import ChatbotCore
import logging

logger = logging.getLogger(__name__)


class SessionStateManager:
    """Manages Streamlit session state variables."""
    
    @staticmethod
    def initialize() -> None:
        """Initialize all session state variables with defaults."""
        defaults = {
            "messages": [],
            "model": lmstudio_config.model,
            "temperature": lmstudio_config.temperature,
            "system_message": app_config.default_system_message,
            "base_url": lmstudio_config.base_url,
            "available_models": app_config.default_models.copy(),
            "connection_status": "❓ Not checked",
            "enable_streaming": ui_config.enable_streaming,
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
        
        logger.info("Session state initialized")
    
    @staticmethod
    def clear_chat() -> None:
        """Clear chat messages from session state."""
        st.session_state.messages = []
        logger.info("Chat history cleared from session state")
    
    @staticmethod
    def get_config() -> Dict[str, Any]:
        """Get current configuration from session state."""
        return {
            "base_url": st.session_state.base_url,
            "model": st.session_state.model,
            "temperature": st.session_state.temperature,
            "system_message": st.session_state.system_message,
        }


class ChatDisplay:
    """Handles chat message display."""
    
    @staticmethod
    def render_message(message: Dict[str, str]) -> None:
        """
        Render a single chat message.
        
        Args:
            message: Message dictionary with 'role' and 'content' keys
        """
        if message["role"] == "user":
            with st.chat_message("user", avatar=ui_config.chat_avatar_user):
                st.markdown(
                    f'<div class="{ui_config.css_user_message}">{message["content"]}</div>', 
                    unsafe_allow_html=True
                )
        else:
            with st.chat_message("assistant", avatar=ui_config.chat_avatar_assistant):
                st.markdown(
                    f'<div class="{ui_config.css_assistant_message}">{message["content"]}</div>', 
                    unsafe_allow_html=True
                )
    
    @staticmethod
    def render_chat_history() -> None:
        """Render all messages in chat history."""
        for message in st.session_state.messages:
            ChatDisplay.render_message(message)


class SidebarComponents:
    """Sidebar UI components."""
    
    def __init__(self):
        self.connection_manager = ConnectionManager()
    
    def render_connection_status(self) -> None:
        """Render connection status section."""
        st.sidebar.header("⚙️ LMStudio Settings")
        
        # Display connection status with appropriate styling
        status = st.session_state.connection_status
        if "✅" in status:
            st.sidebar.success(status)
        elif "⚠️" in status:
            st.sidebar.warning(status)
        elif "❌" in status:
            st.sidebar.error(status)
        else:
            st.sidebar.info(status)
    
    def render_connection_settings(self) -> None:
        """Render connection configuration settings."""
        # Base URL input
        st.session_state.base_url = st.sidebar.text_input(
            "LMStudio Base URL",
            value=st.session_state.base_url,
            help="The base URL where LMStudio is running"
        )
        
        # Test connection button
        if st.sidebar.button("🔄 Test Connection"):
            self._test_connection()
    
    def render_model_settings(self) -> None:
        """Render model configuration settings."""
        # Model selection
        model_options = st.session_state.available_models
        current_model = st.session_state.model if st.session_state.model in model_options else model_options[0]
        
        st.session_state.model = st.sidebar.selectbox(
            "Select Model",
            options=model_options,
            index=model_options.index(current_model) if current_model in model_options else 0,
            help="Available models from LMStudio"
        )
        
        # Temperature slider
        st.session_state.temperature = st.sidebar.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=validate_temperature(st.session_state.temperature),
            step=0.1,
            help="Higher values make output more random, lower values make it more focused"
        )
    
    def render_system_settings(self) -> None:
        """Render system message and other settings."""
        # System message
        st.session_state.system_message = st.sidebar.text_area(
            "System Message",
            value=st.session_state.system_message,
            height=100,
            help="Instructions for the AI assistant"
        )
        
        # Streaming toggle
        st.session_state.enable_streaming = st.sidebar.checkbox(
            "Enable Streaming",
            value=st.session_state.enable_streaming,
            help="Stream responses as they are generated"
        )
    
    def render_actions(self) -> None:
        """Render action buttons."""
        # Clear chat button
        if st.sidebar.button("🧹 Clear Chat"):
            SessionStateManager.clear_chat()
            st.rerun()
    
    def render_info_sections(self) -> None:
        """Render informational sections."""
        # LMStudio Instructions
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📋 LMStudio Setup")
        st.sidebar.markdown("""
        1. Open LMStudio
        2. Load a model
        3. Start the server
        4. Test connection above
        """)
        
        # About section
        st.sidebar.markdown("---")
        st.sidebar.markdown("### About")
        st.sidebar.markdown("""
        This chatbot is built with:
        - 🦜 LangChain
        - 🎈 Streamlit  
        - 🖥️ LMStudio Local API
        """)
        
        # Memory stats if available
        if hasattr(st.session_state, 'chatbot_instance'):
            try:
                stats = st.session_state.chatbot_instance.get_memory_stats()
                st.sidebar.markdown("---")
                st.sidebar.markdown("### 💾 Memory Stats")
                st.sidebar.markdown(f"**Messages:** {stats['total_messages']}")
                st.sidebar.markdown(f"**Tokens:** {stats['total_tokens']}")
            except:
                pass
    
    def _test_connection(self) -> None:
        """Test connection to LMStudio and update session state."""
        self.connection_manager.base_url = st.session_state.base_url
        status, models = self.connection_manager.test_connection()
        st.session_state.connection_status = status
        st.session_state.available_models = models
        st.rerun()
    
    def render_all(self) -> None:
        """Render all sidebar components."""
        self.render_connection_status()
        self.render_connection_settings()
        self.render_model_settings()
        self.render_system_settings()
        self.render_actions()
        self.render_info_sections()


class ExamplePrompts:
    """Handles example prompt buttons."""
    
    @staticmethod
    def render(chatbot: ChatbotCore) -> None:
        """
        Render example prompt buttons.
        
        Args:
            chatbot: ChatbotCore instance for generating responses
        """
        if len(st.session_state.messages) == 0:
            st.info("👋 Welcome! Start a conversation by typing a message below.")
            
            # Example prompts
            st.markdown("### 💡 Try these example prompts:")
            cols = st.columns(3)
            
            examples = get_example_prompts()
            
            for i, (button_text, prompt) in enumerate(examples):
                with cols[i]:
                    if st.button(button_text):
                        ExamplePrompts._handle_example_prompt(prompt, chatbot)
    
    @staticmethod
    def _handle_example_prompt(prompt: str, chatbot: ChatbotCore) -> None:
        """
        Handle example prompt button click.
        
        Args:
            prompt: The prompt text
            chatbot: ChatbotCore instance
        """
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get and add assistant response
        if st.session_state.enable_streaming:
            response_container = st.empty()
            response = chatbot.get_streaming_response(prompt, response_container)
        else:
            with st.spinner("Thinking..."):
                response = chatbot.get_response(prompt)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()


class ChatInterface:
    """Main chat interface manager."""
    
    def __init__(self):
        self.chatbot = None
        self.sidebar = SidebarComponents()
    
    def initialize_chatbot(self) -> None:
        """Initialize or update the chatbot instance."""
        config = SessionStateManager.get_config()
        
        if 'chatbot_instance' not in st.session_state:
            self.chatbot = ChatbotCore(config)
            st.session_state.chatbot_instance = self.chatbot
        else:
            self.chatbot = st.session_state.chatbot_instance
            # Update config if changed
            if config != getattr(self.chatbot, 'last_config', {}):
                self.chatbot.update_config(config)
                self.chatbot.last_config = config
    
    def handle_user_input(self, prompt: str) -> None:
        """
        Handle user input and generate response.
        
        Args:
            prompt: User's input message
        """
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user", avatar=ui_config.chat_avatar_user):
            st.markdown(
                f'<div class="{ui_config.css_user_message}">{prompt}</div>', 
                unsafe_allow_html=True
            )
        
        # Get and display assistant response
        with st.chat_message("assistant", avatar=ui_config.chat_avatar_assistant):
            if st.session_state.enable_streaming:
                # Streaming response
                response_container = st.empty()
                response = self.chatbot.get_streaming_response(prompt, response_container)
            else:
                # Non-streaming response
                with st.spinner("Thinking..."):
                    response = self.chatbot.get_response(prompt)
                st.markdown(
                    f'<div class="{ui_config.css_assistant_message}">{response}</div>', 
                    unsafe_allow_html=True
                )
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    def render(self) -> None:
        """Render the complete chat interface."""
        # Initialize session state
        SessionStateManager.initialize()
        
        # Render sidebar
        self.sidebar.render_all()
        
        # Initialize chatbot
        self.initialize_chatbot()
        
        # Display chat history
        ChatDisplay.render_chat_history()
        
        # Handle chat input
        if prompt := st.chat_input("What would you like to know?"):
            self.handle_user_input(prompt)
        
        # Show example prompts for new users
        ExamplePrompts.render(self.chatbot)
