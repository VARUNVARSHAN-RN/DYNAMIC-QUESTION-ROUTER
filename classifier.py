"""
Domain and Difficulty Classifier using DeBERTaV3
Classifies questions into domains (Math, Coding, Science, Reasoning, Agentic)
and difficulty levels (Easy, Medium, Hard)
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import Tuple, Dict
import logging

logger = logging.getLogger(__name__)


class QuestionClassifier:
    """Classifier for question domain and difficulty using DeBERTaV3"""
    
    DOMAINS = ["Math", "Coding", "Science", "Reasoning", "Agentic"]
    DIFFICULTIES = ["Easy", "Medium", "Hard"]
    
    def __init__(self, model_name: str = "microsoft/deberta-v3-base", use_pretrained: bool = True):
        """
        Initialize the classifier with DeBERTaV3 model
        
        Args:
            model_name: Hugging Face model name for DeBERTaV3
            use_pretrained: Whether to load the pretrained model (requires internet)
        """
        self.use_pretrained = use_pretrained
        self.tokenizer = None
        self.model = None
        self.device = None
        
        if use_pretrained:
            try:
                logger.info(f"Loading classifier model: {model_name}")
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModelForSequenceClassification.from_pretrained(
                    model_name,
                    num_labels=len(self.DOMAINS) + len(self.DIFFICULTIES)
                )
                self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                self.model.to(self.device)
                logger.info(f"Classifier loaded on device: {self.device}")
            except Exception as e:
                logger.warning(f"Could not load pretrained model: {e}")
                logger.info("Falling back to rule-based classification")
                self.use_pretrained = False
        else:
            logger.info("Using rule-based classification (pretrained model disabled)")
    
    def classify(self, question: str) -> Tuple[str, str]:
        """
        Classify a question into domain and difficulty
        
        Args:
            question: Input question text
            
        Returns:
            Tuple of (domain, difficulty)
        """
        # For initial implementation, use rule-based classification
        # This can be fine-tuned later with user feedback
        domain = self._classify_domain(question)
        difficulty = self._classify_difficulty(question)
        
        logger.info(f"Question classified - Domain: {domain}, Difficulty: {difficulty}")
        return domain, difficulty
    
    def _classify_domain(self, question: str) -> str:
        """Rule-based domain classification (to be replaced with fine-tuned model)"""
        question_lower = question.lower()
        
        # Simple keyword-based classification with better patterns
        math_keywords = [
            'calculate', 'equation', 'solve', 'math', 'number', 'algebra',
            'geometry', 'trigonometry', 'integral', 'derivative', 'sum',
            'multiply', 'divide', 'add', 'subtract', '+', '-', '*', '/',
            'coefficient', 'polynomial', 'factorial', 'prime'
        ]
        coding_keywords = [
            'code', 'program', 'function', 'algorithm', 'debug', 'python',
            'java', 'javascript', 'class', 'method', 'variable', 'loop',
            'array', 'list', 'dict', 'string', 'implement', 'write a',
            'recursive', 'iteration', 'compile', 'syntax', 'script'
        ]
        science_keywords = [
            'science', 'physics', 'chemistry', 'biology', 'molecule',
            'atom', 'cell', 'experiment', 'hypothesis', 'theory',
            'photosynthesis', 'evolution', 'dna', 'rna', 'protein',
            'energy', 'force', 'reaction', 'element', 'compound'
        ]
        agentic_keywords = [
            'agent', 'task', 'execute', 'workflow', 'automation',
            'orchestrate', 'plan', 'multi-step', 'automate', 'schedule',
            'coordinate', 'organize', 'manage', 'control flow'
        ]
        
        # Count keyword matches
        math_count = sum(1 for kw in math_keywords if kw in question_lower)
        coding_count = sum(1 for kw in coding_keywords if kw in question_lower)
        science_count = sum(1 for kw in science_keywords if kw in question_lower)
        agentic_count = sum(1 for kw in agentic_keywords if kw in question_lower)
        
        # Determine domain based on highest count
        counts = {
            "Math": math_count,
            "Coding": coding_count,
            "Science": science_count,
            "Agentic": agentic_count
        }
        
        max_count = max(counts.values())
        if max_count > 0:
            # Return domain with highest count
            for domain, count in counts.items():
                if count == max_count:
                    return domain
        
        # Default to Reasoning if no strong match
        return "Reasoning"
    
    def _classify_difficulty(self, question: str) -> str:
        """Rule-based difficulty classification (to be replaced with fine-tuned model)"""
        question_lower = question.lower()
        word_count = len(question.split())
        
        # Simple heuristic based on question length and complexity indicators
        if any(keyword in question_lower for keyword in [
            'advanced', 'complex', 'prove', 'derive', 'optimize', 'analyze deeply'
        ]) or word_count > 30:
            return "Hard"
        elif any(keyword in question_lower for keyword in [
            'basic', 'simple', 'what is', 'define', 'list'
        ]) or word_count < 10:
            return "Easy"
        else:
            return "Medium"
    
    def fine_tune(self, training_data: list):
        """
        Fine-tune the classifier with feedback data
        
        Args:
            training_data: List of tuples (question, domain, difficulty)
        """
        logger.info(f"Fine-tuning classifier with {len(training_data)} examples")
        # Implementation for fine-tuning would go here
        # This is a placeholder for future enhancement
        pass
