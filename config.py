"""
Configuration management for the Dynamic Question Router application.
"""
import os
from typing import Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration class."""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
    
    # Model Configuration
    CLASSIFICATION_MODEL = os.getenv("CLASSIFICATION_MODEL", "microsoft/deberta-v3-base")
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # Feedback Storage
    FEEDBACK_JSON_PATH = "feedback_data.json"
    FEEDBACK_CSV_PATH = "feedback_data.csv"
    
    # Domain and Difficulty Labels
    DOMAINS = ["Math", "Coding", "Science", "Reasoning", "Agentic"]
    DIFFICULTIES = ["Easy", "Medium", "Hard"]
    
    # Routing Rules: {(domain, difficulty): chatbot}
    ROUTING_RULES: Dict[tuple, str] = {
        # Math routes
        ("Math", "Easy"): "openai",
        ("Math", "Medium"): "openai",
        ("Math", "Hard"): "deepseek",
        
        # Coding routes
        ("Coding", "Easy"): "openai",
        ("Coding", "Medium"): "deepseek",
        ("Coding", "Hard"): "deepseek",
        
        # Science routes
        ("Science", "Easy"): "openai",
        ("Science", "Medium"): "claude",
        ("Science", "Hard"): "claude",
        
        # Reasoning routes
        ("Reasoning", "Easy"): "openai",
        ("Reasoning", "Medium"): "deepseek",
        ("Reasoning", "Hard"): "deepseek",
        
        # Agentic routes
        ("Agentic", "Easy"): "openai",
        ("Agentic", "Medium"): "claude",
        ("Agentic", "Hard"): "huggingface",
    }
    
    # Default fallback chatbot
    FALLBACK_CHATBOT = "openai"


config = Config()
