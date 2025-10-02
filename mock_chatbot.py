"""
Mock chatbot for testing purposes (no API keys required).
"""
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MockChatbot:
    """Mock chatbot that generates simple responses for testing."""
    
    def __init__(self, name: str = "mock"):
        self.name = name
    
    def get_response(self, question: str) -> Optional[str]:
        """Generate a mock response based on question keywords."""
        question_lower = question.lower()
        
        # Math questions
        if any(word in question_lower for word in ["derivative", "integrate", "calculate", "solve", "math"]):
            return f"[Mock {self.name}] This is a mathematical problem. In a real scenario, I would provide a detailed solution using mathematical principles and formulas."
        
        # Coding questions
        elif any(word in question_lower for word in ["code", "program", "function", "algorithm", "python", "java"]):
            return f"[Mock {self.name}] This is a coding question. Here's how you would approach it: 1) Define your requirements, 2) Design the algorithm, 3) Implement the solution, 4) Test thoroughly."
        
        # Science questions
        elif any(word in question_lower for word in ["science", "biology", "chemistry", "physics", "explain", "photosynthesis"]):
            return f"[Mock {self.name}] This is a scientific question. I would explain the underlying principles, mechanisms, and real-world applications of this concept."
        
        # Reasoning questions
        elif any(word in question_lower for word in ["if", "then", "logic", "reasoning", "conclude", "infer"]):
            return f"[Mock {self.name}] This requires logical reasoning. Based on the premises provided, I would analyze the logical relationship and provide a valid conclusion."
        
        # Agentic questions
        elif any(word in question_lower for word in ["plan", "schedule", "organize", "workflow", "agent", "task"]):
            return f"[Mock {self.name}] This involves planning and organization. I would break down the task into steps, prioritize actions, and create a structured approach."
        
        # Default response
        else:
            return f"[Mock {self.name}] I understand your question. In a production environment with proper API keys, I would provide a detailed and accurate response based on my specialized capabilities."
