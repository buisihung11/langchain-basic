"""Core chatbot functionality using LangChain."""

from typing import Generator, Optional, Dict, Any
from pydantic import SecretStr
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.callbacks.base import BaseCallbackHandler

from config import lmstudio_config, app_config
from utils import format_error_message, ConnectionManager
import logging

logger = logging.getLogger(__name__)


class StreamingCallbackHandler(BaseCallbackHandler):
    """Callback handler for streaming tokens to Streamlit."""
    
    def __init__(self, container):
        """Initialize with a Streamlit container for updates."""
        self.container = container
        self.text = ""
    
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Handle new token from LLM streaming."""
        self.text += token
        self.container.markdown(
            f'<div class="chat-message assistant-message">{self.text}</div>', 
            unsafe_allow_html=True
        )


class ChatbotCore:
    """Core chatbot functionality with LangChain integration."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the chatbot.
        
        Args:
            config: Optional configuration overrides
        """
        self.config = config or {}
        self.llm = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        self.chain = None
        self.connection_manager = ConnectionManager()
        
        self._setup_llm()
        self._setup_memory()
        self._setup_chain()
    
    def _setup_llm(self) -> None:
        """Initialize the ChatOpenAI model pointing to LMStudio."""
        base_url = self.config.get("base_url", st.session_state.get("base_url", lmstudio_config.base_url))
        model = self.config.get("model", st.session_state.get("model", lmstudio_config.model))
        temperature = self.config.get("temperature", st.session_state.get("temperature", lmstudio_config.temperature))
        
        try:
            self.llm = ChatOpenAI(
                base_url=f"{base_url}/v1",
                api_key=SecretStr(lmstudio_config.api_key),
                model=str(model),
                temperature=temperature,
                streaming=st.session_state.get("enable_streaming", True),
                timeout=lmstudio_config.timeout
            )
            logger.info(f"LLM initialized with model: {model}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise
    
    def _setup_memory(self) -> None:
        """Initialize conversation memory."""
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Load existing messages from session state into memory
        if hasattr(st.session_state, 'messages'):
            for message in st.session_state.messages:
                if message["role"] == "user":
                    self.memory.chat_memory.add_user_message(message["content"])
                elif message["role"] == "assistant":
                    self.memory.chat_memory.add_ai_message(message["content"])
        
        logger.info("Memory initialized and loaded from session state")
    
    def _setup_chain(self) -> None:
        """Setup the conversation chain with prompt template."""
        system_message = self.config.get(
            "system_message", 
            st.session_state.get("system_message", app_config.default_system_message)
        ) or "I am a helpful AI assistant."
        
        # Create chat prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}")
        ])
        
        # Create the chain
        if not self.llm:
            raise ValueError("LLM must be initialized before creating the chain")
            
        self.chain = (
            {
                "input": RunnablePassthrough(),
                "chat_history": lambda x: self.memory.chat_memory.messages,
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
        logger.info("Conversation chain initialized")
    
    def get_response(self, user_input: str) -> str:
        """
        Get response from the chatbot using LangChain.
        
        Args:
            user_input: User's message
            
        Returns:
            AI response text
        """
        try:
            # Use the chain to get response
            response = self.chain.invoke(user_input)
            
            # Update memory with the conversation
            self.memory.chat_memory.add_user_message(user_input)
            self.memory.chat_memory.add_ai_message(response)
            
            logger.info(f"Generated response for input: {user_input[:50]}...")
            return response
            
        except Exception as e:
            error_msg = format_error_message(e)
            logger.error(f"Error generating response: {e}")
            return error_msg
    
    def get_streaming_response(self, user_input: str, container=None) -> str:
        """
        Get streaming response from the chatbot.
        
        Args:
            user_input: User's message
            container: Optional Streamlit container for streaming updates
            
        Returns:
            Complete AI response text
        """
        try:
            full_response = ""
            
            if container:
                # For streaming with UI updates
                callback_handler = StreamingCallbackHandler(container)
                
                # Stream the response
                for chunk in self.chain.stream(user_input, {"callbacks": [callback_handler]}):
                    if isinstance(chunk, str):
                        full_response += chunk
            else:
                # For non-UI streaming
                for chunk in self.chain.stream(user_input):
                    if isinstance(chunk, str):
                        full_response += chunk
            
            # Update memory with the conversation
            self.memory.chat_memory.add_user_message(user_input)
            self.memory.chat_memory.add_ai_message(full_response)
            
            logger.info(f"Generated streaming response for input: {user_input[:50]}...")
            return full_response
            
        except Exception as e:
            error_msg = format_error_message(e)
            logger.error(f"Error generating streaming response: {e}")
            return error_msg
    
    def clear_memory(self) -> None:
        """Clear conversation memory."""
        self.memory.clear()
        logger.info("Conversation memory cleared")
    
    def update_config(self, new_config: Dict[str, Any]) -> None:
        """
        Update configuration and reinitialize components.
        
        Args:
            new_config: New configuration values
        """
        self.config.update(new_config)
        self._setup_llm()
        self._setup_chain()
        logger.info("Configuration updated and components reinitialized")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about current memory usage."""
        messages = self.memory.chat_memory.messages
        return {
            "total_messages": len(messages),
            "user_messages": len([m for m in messages if isinstance(m, HumanMessage)]),
            "assistant_messages": len([m for m in messages if isinstance(m, AIMessage)]),
            "total_tokens": sum(len(m.content.split()) for m in messages)
        }
    
    def is_connected(self) -> bool:
        """Check if connection to LMStudio is working."""
        return self.connection_manager.is_connected()
