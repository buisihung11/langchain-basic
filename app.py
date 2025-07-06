import streamlit as st
import os
import requests
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.callbacks.manager import CallbackManagerForLLMRun, AsyncCallbackManagerForLLMRun
from langchain_core.prompt_values import PromptValue
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.outputs import LLMResult, Generation
from typing import Any, List, Optional, Dict, Union
from pydantic import Field
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="LangChain Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #1976d2;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left-color: #7b1fa2;
    }
    .stButton > button {
        background-color: #1976d2;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

class LMStudioLLM(BaseLanguageModel):
    """Custom LangChain LLM for LMStudio local API"""
    
    base_url: str = Field(default="http://localhost:1234", description="The base URL for LMStudio API")
    model: str = Field(default="local-model", description="The model name to use")
    temperature: float = Field(default=0.7, description="The temperature for generation")
    
    def __init__(self, base_url: str = "http://localhost:1234", model: str = "local-model", temperature: float = 0.7, **kwargs):
        super().__init__(base_url=base_url, model=model, temperature=temperature, **kwargs)
    
    def _generate(self, prompts: List[str], stop: Optional[List[str]] = None, run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any) -> LLMResult:
        """Generate response from LMStudio API"""
        generations = []
        
        for prompt in prompts:
            try:
                # Format message for LMStudio
                formatted_messages = [{"role": "user", "content": prompt}]
                
                # Make API call to LMStudio
                response = requests.post(
                    f"{self.base_url}/v1/chat/completions",
                    json={
                        "model": self.model,
                        "messages": formatted_messages,
                        "temperature": self.temperature,
                        "stream": False
                    },
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    generations.append([Generation(text=content)])
                else:
                    error_msg = f"Error: API returned status {response.status_code} - {response.text}"
                    generations.append([Generation(text=error_msg)])
                    
            except requests.exceptions.ConnectionError:
                error_msg = "Error: Cannot connect to LMStudio. Please make sure LMStudio is running on localhost:1234"
                generations.append([Generation(text=error_msg)])
            except requests.exceptions.Timeout:
                error_msg = "Error: Request timed out. The model might be taking too long to respond."
                generations.append([Generation(text=error_msg)])
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                generations.append([Generation(text=error_msg)])
        
        return LLMResult(generations=generations)
    
    async def _agenerate(self, prompts: List[str], stop: Optional[List[str]] = None, run_manager: Optional[AsyncCallbackManagerForLLMRun] = None, **kwargs: Any) -> LLMResult:
        """Async version of generate - just calls sync version for simplicity"""
        return self._generate(prompts, stop, None, **kwargs)
    
    def _llm_type(self) -> str:
        return "lmstudio"
    
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {
            "base_url": self.base_url,
            "model": self.model,
            "temperature": self.temperature
        }
    
    def invoke(self, input: Union[str, List[BaseMessage]], config: Optional[Dict] = None, **kwargs: Any) -> AIMessage:
        """Invoke the model with a single input"""
        if isinstance(input, str):
            prompt = input
        elif isinstance(input, list):
            # Convert messages to a single prompt
            prompt = "\n".join([msg.content for msg in input if hasattr(msg, 'content')])
        else:
            prompt = str(input)
        
        result = self._generate([prompt], **kwargs)
        return AIMessage(content=result.generations[0][0].text)
    
    def predict(self, text: str, **kwargs: Any) -> str:
        """Make a prediction with text input"""
        result = self._generate([text], **kwargs)
        return result.generations[0][0].text
    
    def predict_messages(self, messages: List[BaseMessage], **kwargs: Any) -> BaseMessage:
        """Make a prediction with message input"""
        prompt = "\n".join([msg.content for msg in messages if hasattr(msg, 'content')])
        result = self._generate([prompt], **kwargs)
        return AIMessage(content=result.generations[0][0].text)
    
    def generate_prompt(self, prompts: List[PromptValue], **kwargs: Any) -> LLMResult:
        """Generate with PromptValue inputs"""
        prompt_strings = [p.to_string() for p in prompts]
        return self._generate(prompt_strings, **kwargs)
    
    async def apredict(self, text: str, **kwargs: Any) -> str:
        """Async version of predict"""
        result = await self._agenerate([text], **kwargs)
        return result.generations[0][0].text
    
    async def apredict_messages(self, messages: List[BaseMessage], **kwargs: Any) -> BaseMessage:
        """Async version of predict_messages"""
        prompt = "\n".join([msg.content for msg in messages if hasattr(msg, 'content')])
        result = await self._agenerate([prompt], **kwargs)
        return AIMessage(content=result.generations[0][0].text)
    
    async def agenerate_prompt(self, prompts: List[PromptValue], **kwargs: Any) -> LLMResult:
        """Async version of generate_prompt"""
        prompt_strings = [p.to_string() for p in prompts]
        return await self._agenerate(prompt_strings, **kwargs)

class ChatbotApp:
    """Streamlit Chatbot Application using LangChain with LMStudio"""
    
    def __init__(self):
        self.setup_llm()
        self.setup_connection()
    
    def setup_llm(self):
        """Initialize the LMStudio language model"""
        base_url = st.session_state.get("base_url", "http://localhost:1234")
        model = st.session_state.get("model", "local-model")
        temperature = st.session_state.get("temperature", 0.7)
        
        self.llm = LMStudioLLM(
            base_url=base_url,
            model=model,
            temperature=temperature
        )
        
    def get_response(self, user_input: str) -> str:
        """Get response from the chatbot, considering chat history"""
        try:
            # Compile the chat history with system message
            system_message = st.session_state.get("system_message", 
                "You are a helpful AI assistant. Be concise, friendly, and informative.")
            
            # Build conversation history with the input
            conversation_history = system_message + "\n"
            for message in st.session_state.messages:
                conversation_history += message["role"] + ": " + message["content"] + "\n"
            conversation_history += "user: " + user_input + "\n"

            # Create messages for the API call
            messages = [{"role": "system", "content": system_message},
                        {"role": "user", "content": conversation_history}]

            # Make API call to LMStudio
            response = requests.post(
                f"{st.session_state.get('base_url', 'http://localhost:1234')}/v1/chat/completions",
                json={
                    "model": st.session_state.get("model", "local-model"),
                    "messages": messages,
                    "temperature": st.session_state.get("temperature", 0.7),
                    "stream": False
                },
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"Error: API returned status {response.status_code} - {response.text}"
                
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to LMStudio. Please make sure LMStudio is running and the server is started."
        except requests.exceptions.Timeout:
            return "Error: Request timed out. The model might be taking too long to respond."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def setup_connection(self):
        """Test connection to LMStudio"""
        try:
            response = requests.get(f"{st.session_state.get('base_url', 'http://localhost:1234')}/v1/models", timeout=5)
            if response.status_code == 200:
                models = response.json()
                if models.get("data"):
                    st.session_state.available_models = [model["id"] for model in models["data"]]
                    st.session_state.connection_status = "✅ Connected to LMStudio"
                else:
                    st.session_state.available_models = ["local-model"]
                    st.session_state.connection_status = "⚠️ Connected but no models loaded"
            else:
                st.session_state.connection_status = "❌ LMStudio API error"
                st.session_state.available_models = ["local-model"]
        except requests.exceptions.ConnectionError:
            st.session_state.connection_status = "❌ Cannot connect to LMStudio"
            st.session_state.available_models = ["local-model"]
        except Exception as e:
            st.session_state.connection_status = f"❌ Error: {str(e)}"
            st.session_state.available_models = ["local-model"]
    

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "model" not in st.session_state:
        st.session_state.model = "local-model"
    
    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.7
    
    if "system_message" not in st.session_state:
        st.session_state.system_message = "You are a helpful AI assistant. Be concise, friendly, and informative."
    
    if "base_url" not in st.session_state:
        st.session_state.base_url = "http://localhost:1234"
    
    if "available_models" not in st.session_state:
        st.session_state.available_models = ["local-model"]
    
    if "connection_status" not in st.session_state:
        st.session_state.connection_status = "❓ Not checked"

def display_chat_history():
    """Display chat history"""
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', 
                          unsafe_allow_html=True)
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(f'<div class="chat-message assistant-message">{message["content"]}</div>', 
                          unsafe_allow_html=True)

def sidebar_settings():
    """Create sidebar with settings"""
    st.sidebar.header("⚙️ LMStudio Settings")
    
    # Connection status
    st.sidebar.markdown(f"**Status:** {st.session_state.connection_status}")
    
    # Base URL input
    st.session_state.base_url = st.sidebar.text_input(
        "LMStudio Base URL",
        value=st.session_state.base_url,
        help="The base URL where LMStudio is running"
    )
    
    # Test connection button
    if st.sidebar.button("🔄 Test Connection"):
        chatbot_temp = ChatbotApp()
        st.rerun()
    
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
        value=st.session_state.temperature,
        step=0.1,
        help="Higher values make output more random, lower values make it more focused"
    )
    
    # System message
    st.session_state.system_message = st.sidebar.text_area(
        "System Message",
        value=st.session_state.system_message,
        height=100,
        help="Instructions for the AI assistant"
    )
    
    # Clear chat button
    if st.sidebar.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    # LMStudio Instructions
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 LMStudio Setup")
    st.sidebar.markdown("1. Open LMStudio")
    st.sidebar.markdown("2. Load a model")
    st.sidebar.markdown("3. Start the server")
    st.sidebar.markdown("4. Test connection above")
    
    # About section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.markdown("This is a chatbot built with:")
    st.sidebar.markdown("- 🦜 LangChain")
    st.sidebar.markdown("- 🎈 Streamlit")
    st.sidebar.markdown("- 🖥️ LMStudio Local API")

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # App header
    st.markdown('<h1 class="main-header">🤖 LangChain Chatbot</h1>', unsafe_allow_html=True)
    
    # Sidebar
    sidebar_settings()
    
    # Initialize chatbot
    chatbot = ChatbotApp()
    
    # Display chat history
    display_chat_history()
    
    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(f'<div class="chat-message user-message">{prompt}</div>', 
                      unsafe_allow_html=True)
        
        # Get and display assistant response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                response = chatbot.get_response(prompt)
            st.markdown(f'<div class="chat-message assistant-message">{response}</div>', 
                      unsafe_allow_html=True)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Instructions for first-time users
    if len(st.session_state.messages) == 0:
        st.info("👋 Welcome! Start a conversation by typing a message below.")
        
        # Example prompts
        st.markdown("### 💡 Try these example prompts:")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Explain quantum computing"):
                st.session_state.messages.append({"role": "user", "content": "Explain quantum computing"})
                st.rerun()
        
        with col2:
            if st.button("Write a Python function"):
                st.session_state.messages.append({"role": "user", "content": "Write a Python function to calculate factorial"})
                st.rerun()
        
        with col3:
            if st.button("Plan a trip to Japan"):
                st.session_state.messages.append({"role": "user", "content": "Help me plan a 7-day trip to Japan"})
                st.rerun()

if __name__ == "__main__":
    main()
