"""Utility functions for the chatbot application."""

import requests
from typing import List, Tuple, Optional
import logging
from config import lmstudio_config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages connection to LMStudio API."""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or lmstudio_config.base_url
    
    def test_connection(self) -> Tuple[str, List[str]]:
        """
        Test connection to LMStudio and fetch available models.
        
        Returns:
            Tuple of (status_message, available_models)
        """
        try:
            response = requests.get(
                f"{self.base_url}/v1/models", 
                timeout=lmstudio_config.timeout
            )
            
            if response.status_code == 200:
                models_data = response.json()
                if models_data.get("data"):
                    available_models = [model["id"] for model in models_data["data"]]
                    status = "✅ Connected to LMStudio"
                    logger.info(f"Connected to LMStudio. Found {len(available_models)} models.")
                    return status, available_models
                else:
                    status = "⚠️ Connected but no models loaded"
                    logger.warning("Connected to LMStudio but no models are loaded.")
                    return status, ["local-model"]
            else:
                status = "❌ LMStudio API error"
                logger.error(f"LMStudio API returned status {response.status_code}")
                return status, ["local-model"]
                
        except requests.exceptions.ConnectionError:
            status = "❌ Cannot connect to LMStudio"
            logger.error("Cannot connect to LMStudio. Is it running?")
            return status, ["local-model"]
        except requests.exceptions.Timeout:
            status = "❌ Connection timeout"
            logger.error("Connection to LMStudio timed out.")
            return status, ["local-model"]
        except Exception as e:
            status = f"❌ Error: {str(e)}"
            logger.error(f"Unexpected error connecting to LMStudio: {e}")
            return status, ["local-model"]
    
    def is_connected(self) -> bool:
        """Check if LMStudio is connected."""
        status, _ = self.test_connection()
        return "✅" in status


def validate_temperature(temperature: float) -> float:
    """Validate and clamp temperature value."""
    return max(0.0, min(2.0, temperature))


def validate_url(url: str) -> bool:
    """Validate if URL format is correct."""
    try:
        result = requests.utils.urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def format_error_message(error: Exception) -> str:
    """Format error messages for user display."""
    error_str = str(error).lower()
    
    if "connection" in error_str:
        return "Error: Cannot connect to LMStudio. Please make sure LMStudio is running and the server is started."
    elif "timeout" in error_str:
        return "Error: Request timed out. The model might be taking too long to respond."
    elif "404" in error_str:
        return "Error: Model not found. Please check your model selection."
    elif "401" in error_str or "403" in error_str:
        return "Error: Authentication failed. Please check your API settings."
    else:
        return f"Error: {str(error)}"


def get_example_prompts() -> List[Tuple[str, str]]:
    """Get example prompts for the UI."""
    return [
        ("Explain quantum computing", "Explain quantum computing in simple terms"),
        ("Write a Python function", "Write a Python function to calculate factorial"),
        ("Plan a trip to Japan", "Help me plan a 7-day trip to Japan"),
    ]
