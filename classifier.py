"""
Question Classifier using DeBERTaV3 model for domain and difficulty classification.
"""
from typing import Tuple, Dict
import logging

from config import config

# Optional imports for future deep learning classification
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuestionClassifier:
    """Classifier for question domain and difficulty using DeBERTaV3."""
    
    def __init__(self):
        """Initialize the classifier with DeBERTaV3 model."""
        self.model_name = config.CLASSIFICATION_MODEL
        
        if HAS_TRANSFORMERS:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"Using device: {self.device}")
            # Future: Load tokenizer and model for deep learning classification
            # self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        else:
            logger.info("Using keyword-based classification (transformers not installed)")
        
        # For this implementation, we use a rule-based approach with keyword matching
        # In production, you would fine-tune DeBERTaV3 on labeled data
        # Here we classify based on keywords and patterns
        
        self.domain_keywords = {
            "Math": ["calculate", "solve", "equation", "math", "algebra", "geometry", "calculus", 
                    "integrate", "derivative", "sum", "multiply", "divide", "subtract", "add",
                    "number", "integer", "fraction", "percentage"],
            "Coding": ["code", "program", "function", "algorithm", "debug", "python", "java",
                      "javascript", "implement", "api", "class", "method", "variable", "loop",
                      "recursion", "data structure", "array", "list", "dictionary"],
            "Science": ["explain", "why", "how does", "biology", "chemistry", "physics",
                       "molecule", "atom", "cell", "experiment", "theory", "hypothesis",
                       "energy", "force", "reaction", "evolution", "organism"],
            "Reasoning": ["analyze", "compare", "evaluate", "deduce", "infer", "logic",
                         "reasoning", "conclude", "argument", "premise", "therefore",
                         "because", "if then", "cause", "effect"],
            "Agentic": ["plan", "schedule", "organize", "task", "agent", "decision",
                       "strategy", "optimize", "coordinate", "manage", "workflow"]
        }
        
        self.difficulty_indicators = {
            "Easy": ["simple", "basic", "easy", "beginner", "introduction", "what is"],
            "Medium": ["explain", "describe", "how", "why", "moderate"],
            "Hard": ["complex", "advanced", "difficult", "prove", "derive", "optimize",
                    "analyze deeply", "comprehensive"]
        }
    
    def classify(self, question: str) -> Tuple[str, str, Dict[str, float]]:
        """
        Classify the question into domain and difficulty.
        
        Args:
            question: The input question text
            
        Returns:
            Tuple of (domain, difficulty, confidence_scores)
        """
        question_lower = question.lower()
        
        # Classify domain
        domain_scores = {}
        for domain, keywords in self.domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in question_lower)
            domain_scores[domain] = score
        
        # Get domain with highest score
        domain = max(domain_scores, key=domain_scores.get)
        if domain_scores[domain] == 0:
            domain = "Reasoning"  # Default domain
        
        # Classify difficulty
        difficulty_scores = {
            "Easy": 0,
            "Medium": 0,
            "Hard": 0
        }
        
        # Check for difficulty indicators
        for difficulty, indicators in self.difficulty_indicators.items():
            score = sum(1 for indicator in indicators if indicator in question_lower)
            difficulty_scores[difficulty] = score
        
        # Consider question length and complexity
        word_count = len(question.split())
        if word_count < 10:
            difficulty_scores["Easy"] += 2
        elif word_count < 20:
            difficulty_scores["Medium"] += 2
        else:
            difficulty_scores["Hard"] += 2
        
        # Check for technical complexity
        if any(char in question for char in ["∫", "∑", "∂", "≈", "√"]):
            difficulty_scores["Hard"] += 3
        
        difficulty = max(difficulty_scores, key=difficulty_scores.get)
        if all(score == 0 for score in difficulty_scores.values()):
            difficulty = "Medium"  # Default difficulty
        
        # Normalize scores for confidence
        total_domain = sum(domain_scores.values()) or 1
        total_difficulty = sum(difficulty_scores.values()) or 1
        
        confidence = {
            "domain": domain_scores[domain] / total_domain,
            "difficulty": difficulty_scores[difficulty] / total_difficulty
        }
        
        logger.info(f"Classified question - Domain: {domain}, Difficulty: {difficulty}")
        return domain, difficulty, confidence


# Singleton instance
classifier = QuestionClassifier()
