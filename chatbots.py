"""
Chatbot API integrations for OpenAI, DeepSeek, Claude (Anthropic), and Hugging Face
"""

import os
import logging
from typing import Optional, Dict
from abc import ABC, abstractmethod
import requests

logger = logging.getLogger(__name__)


class ChatbotAPI(ABC):
    """Abstract base class for chatbot APIs"""
    
    @abstractmethod
    def generate_answer(self, question: str, context: Dict = None) -> Optional[str]:
        """Generate answer for a given question"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the API is available"""
        pass


class OpenAIChatbot(ChatbotAPI):
    """OpenAI GPT API integration"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = "gpt-3.5-turbo"
    
    def generate_answer(self, question: str, context: Dict = None) -> Optional[str]:
        """Generate answer using OpenAI API"""
        if not self.is_available():
            logger.error("OpenAI API key not configured")
            return None
        
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": question}
                ],
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            logger.info("OpenAI generated answer successfully")
            return answer
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return None
    
    def is_available(self) -> bool:
        return bool(self.api_key and self.api_key != "your_openai_api_key_here")


class DeepSeekChatbot(ChatbotAPI):
    """DeepSeek API integration"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.base_url = "https://api.deepseek.com/v1"
    
    def generate_answer(self, question: str, context: Dict = None) -> Optional[str]:
        """Generate answer using DeepSeek API"""
        if not self.is_available():
            logger.error("DeepSeek API key not configured")
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "user", "content": question}
                ],
                "max_tokens": 500
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                answer = response.json()["choices"][0]["message"]["content"]
                logger.info("DeepSeek generated answer successfully")
                return answer
            else:
                logger.error(f"DeepSeek API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"DeepSeek API error: {str(e)}")
            return None
    
    def is_available(self) -> bool:
        return bool(self.api_key and self.api_key != "your_deepseek_api_key_here")


class ClaudeChatbot(ChatbotAPI):
    """Anthropic Claude API integration"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = "claude-3-sonnet-20240229"
    
    def generate_answer(self, question: str, context: Dict = None) -> Optional[str]:
        """Generate answer using Claude API"""
        if not self.is_available():
            logger.error("Anthropic API key not configured")
            return None
        
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            
            message = client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            
            answer = message.content[0].text
            logger.info("Claude generated answer successfully")
            return answer
            
        except Exception as e:
            logger.error(f"Claude API error: {str(e)}")
            return None
    
    def is_available(self) -> bool:
        return bool(self.api_key and self.api_key != "your_anthropic_api_key_here")


class HuggingFaceChatbot(ChatbotAPI):
    """Hugging Face Inference API integration"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        self.model = "mistralai/Mistral-7B-Instruct-v0.1"
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
    
    def generate_answer(self, question: str, context: Dict = None) -> Optional[str]:
        """Generate answer using Hugging Face API"""
        if not self.is_available():
            logger.error("Hugging Face API key not configured")
            return None
        
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            payload = {
                "inputs": question,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "")
                logger.info("Hugging Face generated answer successfully")
                return answer
            else:
                logger.error(f"Hugging Face API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Hugging Face API error: {str(e)}")
            return None
    
    def is_available(self) -> bool:
        return bool(self.api_key and self.api_key != "your_huggingface_api_key_here")
