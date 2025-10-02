"""
Chatbot API connectors for OpenAI, DeepSeek, Claude, and HuggingFace.
"""
import openai
import anthropic
import requests
from typing import Optional
import logging

from config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatbotConnector:
    """Base class for chatbot connectors."""
    
    def __init__(self):
        """Initialize the connector."""
        pass
    
    def get_response(self, question: str) -> Optional[str]:
        """
        Get response from the chatbot.
        
        Args:
            question: The question to ask
            
        Returns:
            The chatbot's response or None if failed
        """
        raise NotImplementedError


class OpenAIChatbot(ChatbotConnector):
    """OpenAI GPT-4o-mini connector."""
    
    def __init__(self):
        super().__init__()
        self.api_key = config.OPENAI_API_KEY
        if self.api_key:
            openai.api_key = self.api_key
    
    def get_response(self, question: str) -> Optional[str]:
        """Get response from OpenAI GPT-4o-mini."""
        try:
            if not self.api_key:
                logger.warning("OpenAI API key not configured")
                return None
            
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides clear and accurate answers."},
                    {"role": "user", "content": question}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content
            logger.info("Successfully got response from OpenAI")
            return answer
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return None


class DeepSeekChatbot(ChatbotConnector):
    """DeepSeek R1 connector."""
    
    def __init__(self):
        super().__init__()
        self.api_key = config.DEEPSEEK_API_KEY
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
    
    def get_response(self, question: str) -> Optional[str]:
        """Get response from DeepSeek R1."""
        try:
            if not self.api_key:
                logger.warning("DeepSeek API key not configured")
                return None
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that provides clear and accurate answers."},
                    {"role": "user", "content": question}
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            answer = response.json()["choices"][0]["message"]["content"]
            logger.info("Successfully got response from DeepSeek")
            return answer
            
        except Exception as e:
            logger.error(f"DeepSeek API error: {str(e)}")
            return None


class ClaudeChatbot(ChatbotConnector):
    """Anthropic Claude connector."""
    
    def __init__(self):
        super().__init__()
        self.api_key = config.ANTHROPIC_API_KEY
        if self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def get_response(self, question: str) -> Optional[str]:
        """Get response from Anthropic Claude."""
        try:
            if not self.api_key:
                logger.warning("Anthropic API key not configured")
                return None
            
            message = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            
            answer = message.content[0].text
            logger.info("Successfully got response from Claude")
            return answer
            
        except Exception as e:
            logger.error(f"Claude API error: {str(e)}")
            return None


class HuggingFaceChatbot(ChatbotConnector):
    """HuggingFace Mistral-7B connector."""
    
    def __init__(self):
        super().__init__()
        self.api_key = config.HUGGINGFACE_API_KEY
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    
    def get_response(self, question: str) -> Optional[str]:
        """Get response from HuggingFace Mistral-7B."""
        try:
            if not self.api_key:
                logger.warning("HuggingFace API key not configured")
                return None
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": f"<s>[INST] {question} [/INST]",
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
            
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                answer = result[0].get("generated_text", "")
            else:
                answer = result.get("generated_text", "")
            
            logger.info("Successfully got response from HuggingFace")
            return answer
            
        except Exception as e:
            logger.error(f"HuggingFace API error: {str(e)}")
            return None


class ChatbotRouter:
    """Router to manage multiple chatbot connectors with fallback."""
    
    def __init__(self):
        """Initialize all chatbot connectors."""
        self.chatbots = {
            "openai": OpenAIChatbot(),
            "deepseek": DeepSeekChatbot(),
            "claude": ClaudeChatbot(),
            "huggingface": HuggingFaceChatbot()
        }
        self.fallback = config.FALLBACK_CHATBOT
    
    def route_question(self, question: str, chatbot_name: str) -> tuple[Optional[str], str]:
        """
        Route question to specified chatbot with fallback.
        
        Args:
            question: The question to ask
            chatbot_name: Name of the primary chatbot to use
            
        Returns:
            Tuple of (response, actual_chatbot_used)
        """
        # Try primary chatbot
        if chatbot_name in self.chatbots:
            logger.info(f"Routing to primary chatbot: {chatbot_name}")
            response = self.chatbots[chatbot_name].get_response(question)
            
            if response:
                return response, chatbot_name
            
            logger.warning(f"Primary chatbot {chatbot_name} failed, falling back to {self.fallback}")
        
        # Fallback to OpenAI
        if self.fallback in self.chatbots:
            response = self.chatbots[self.fallback].get_response(question)
            if response:
                return response, f"{self.fallback} (fallback)"
        
        return None, "none"


# Singleton instance
router = ChatbotRouter()
