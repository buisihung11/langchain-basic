"""Configuration management for the chatbot application."""

import os
from dataclasses import dataclass, field
from typing import List
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()


@dataclass
class LMStudioConfig:
    """Configuration for LMStudio connection."""
    
    # Try to get values from Streamlit secrets first, then from environment variables, then use defaults
    base_url: str = field(default_factory=lambda: st.secrets.get("lmstudio", {}).get("base_url", os.environ.get("LMSTUDIO_BASE_URL", "http://localhost:1234")))
    model: str = field(default_factory=lambda: st.secrets.get("lmstudio", {}).get("model", os.environ.get("LMSTUDIO_MODEL", "local-model")))
    temperature: float = field(default_factory=lambda: float(st.secrets.get("lmstudio", {}).get("temperature", os.environ.get("LMSTUDIO_TEMPERATURE", 0.7))))
    timeout: int = field(default_factory=lambda: int(st.secrets.get("lmstudio", {}).get("timeout", os.environ.get("LMSTUDIO_TIMEOUT", 60))))
    api_key: str = field(default_factory=lambda: st.secrets.get("lmstudio", {}).get("api_key", os.environ.get("LMSTUDIO_API_KEY", "lm-studio")))
    
    @property
    def api_url(self) -> str:
        """Get the full API URL."""
        return f"{self.base_url}/v1"


@dataclass
class OpenAIConfig:
    """Configuration for OpenAI connection."""
    
    # Try to get values from Streamlit secrets first, then from environment variables
    api_key: str = field(default_factory=lambda: st.secrets.get("openai", {}).get("api_key", os.environ.get("OPENAI_API_KEY", "")))
    model: str = field(default_factory=lambda: st.secrets.get("openai", {}).get("model", os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")))
    temperature: float = field(default_factory=lambda: float(st.secrets.get("openai", {}).get("temperature", os.environ.get("OPENAI_TEMPERATURE", 0.7))))
    timeout: int = field(default_factory=lambda: int(st.secrets.get("openai", {}).get("timeout", os.environ.get("OPENAI_TIMEOUT", 60))))
    
    @property
    def available(self) -> bool:
        """Check if OpenAI API is configured."""
        return bool(self.api_key)


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
    
    # Available models (fallback) - using default_factory for mutable default
    default_models: List[str] = field(default_factory=lambda: ["local-model"])
    
    # OpenAI model options
    openai_model_options: List[str] = field(default_factory=lambda: [
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k",
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4o"
    ])


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
openai_config = OpenAIConfig()
app_config = AppConfig()
ui_config = UIConfig()
