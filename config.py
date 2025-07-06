"""Configuration management for the chatbot application."""

import os
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class LMStudioConfig:
    """Configuration for LMStudio connection."""
    
    base_url: str = "http://localhost:1234"
    model: str = "local-model"
    temperature: float = 0.7
    timeout: int = 60
    api_key: str = "lm-studio"  # LMStudio doesn't require a real API key
    
    @property
    def api_url(self) -> str:
        """Get the full API URL."""
        return f"{self.base_url}/v1"


@dataclass
class AppConfig:
    """General application configuration."""
    
    page_title: str = "LangChain Chatbot"
    page_icon: str = "🤖"
    layout: str = "wide"
    initial_sidebar_state: str = "expanded"
    
    # Default system message
    default_system_message: str = (
        "You are a helpful AI assistant. Be concise, friendly, and informative."
    )
    
    # Available models (fallback)
    default_models: List[str] = None
    
    def __post_init__(self):
        if self.default_models is None:
            self.default_models = ["local-model"]


@dataclass
class UIConfig:
    """UI-specific configuration."""
    
    enable_streaming: bool = True
    chat_avatar_user: str = "👤"
    chat_avatar_assistant: str = "🤖"
    
    # CSS classes
    css_user_message: str = "chat-message user-message"
    css_assistant_message: str = "chat-message assistant-message"


# Global configuration instances
lmstudio_config = LMStudioConfig()
app_config = AppConfig()
ui_config = UIConfig()
