"""
Router logic to map domain/difficulty classifications to appropriate chatbot APIs
Includes fallback mechanism for chatbot failures
"""

import logging
from typing import Tuple, List, Optional
from chatbots import ChatbotAPI, OpenAIChatbot, DeepSeekChatbot, ClaudeChatbot, HuggingFaceChatbot

logger = logging.getLogger(__name__)


class QuestionRouter:
    """Routes questions to appropriate chatbot based on domain and difficulty"""
    
    # Routing map: (domain, difficulty) -> [primary_chatbot, fallback_chatbots]
    ROUTING_MAP = {
        # Math questions
        ("Math", "Easy"): ["OpenAI", "HuggingFace", "Claude", "DeepSeek"],
        ("Math", "Medium"): ["Claude", "OpenAI", "DeepSeek", "HuggingFace"],
        ("Math", "Hard"): ["Claude", "DeepSeek", "OpenAI", "HuggingFace"],
        
        # Coding questions
        ("Coding", "Easy"): ["DeepSeek", "OpenAI", "Claude", "HuggingFace"],
        ("Coding", "Medium"): ["DeepSeek", "Claude", "OpenAI", "HuggingFace"],
        ("Coding", "Hard"): ["DeepSeek", "Claude", "OpenAI", "HuggingFace"],
        
        # Science questions
        ("Science", "Easy"): ["OpenAI", "Claude", "HuggingFace", "DeepSeek"],
        ("Science", "Medium"): ["Claude", "OpenAI", "DeepSeek", "HuggingFace"],
        ("Science", "Hard"): ["Claude", "DeepSeek", "OpenAI", "HuggingFace"],
        
        # Reasoning questions
        ("Reasoning", "Easy"): ["OpenAI", "Claude", "HuggingFace", "DeepSeek"],
        ("Reasoning", "Medium"): ["Claude", "OpenAI", "DeepSeek", "HuggingFace"],
        ("Reasoning", "Hard"): ["Claude", "DeepSeek", "OpenAI", "HuggingFace"],
        
        # Agentic questions
        ("Agentic", "Easy"): ["OpenAI", "Claude", "DeepSeek", "HuggingFace"],
        ("Agentic", "Medium"): ["Claude", "OpenAI", "DeepSeek", "HuggingFace"],
        ("Agentic", "Hard"): ["Claude", "OpenAI", "DeepSeek", "HuggingFace"],
    }
    
    def __init__(self):
        """Initialize router with all available chatbots"""
        self.chatbots = {
            "OpenAI": OpenAIChatbot(),
            "DeepSeek": DeepSeekChatbot(),
            "Claude": ClaudeChatbot(),
            "HuggingFace": HuggingFaceChatbot()
        }
        logger.info("Router initialized with chatbots")
    
    def route_question(
        self,
        question: str,
        domain: str,
        difficulty: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Route question to appropriate chatbot with fallback
        
        Args:
            question: The question to answer
            domain: Classified domain
            difficulty: Classified difficulty
            
        Returns:
            Tuple of (answer, chatbot_name) or (None, None) if all fail
        """
        routing_key = (domain, difficulty)
        chatbot_priority = self.ROUTING_MAP.get(
            routing_key,
            ["OpenAI", "Claude", "DeepSeek", "HuggingFace"]  # Default fallback
        )
        
        logger.info(f"Routing {domain}/{difficulty} question to chatbots: {chatbot_priority}")
        
        # Try each chatbot in priority order
        for chatbot_name in chatbot_priority:
            chatbot = self.chatbots.get(chatbot_name)
            
            if chatbot and chatbot.is_available():
                logger.info(f"Attempting to use {chatbot_name}")
                answer = chatbot.generate_answer(question)
                
                if answer:
                    logger.info(f"Successfully got answer from {chatbot_name}")
                    return answer, chatbot_name
                else:
                    logger.warning(f"{chatbot_name} failed, trying fallback")
            else:
                logger.warning(f"{chatbot_name} not available, trying fallback")
        
        logger.error("All chatbots failed to generate an answer")
        return None, None
    
    def get_available_chatbots(self) -> List[str]:
        """Get list of currently available chatbots"""
        return [
            name for name, chatbot in self.chatbots.items()
            if chatbot.is_available()
        ]
