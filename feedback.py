"""
Feedback collection and logging system
Stores positive feedback and negative feedback with corrections
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class FeedbackManager:
    """Manages user feedback for answers"""
    
    def __init__(self, feedback_dir: str = "feedback_data"):
        """
        Initialize feedback manager
        
        Args:
            feedback_dir: Directory to store feedback data
        """
        self.feedback_dir = feedback_dir
        self.positive_feedback_file = os.path.join(feedback_dir, "positive_feedback.jsonl")
        self.negative_feedback_file = os.path.join(feedback_dir, "negative_feedback.jsonl")
        
        # Create feedback directory if it doesn't exist
        os.makedirs(feedback_dir, exist_ok=True)
        logger.info(f"Feedback manager initialized with directory: {feedback_dir}")
    
    def log_positive_feedback(
        self,
        question: str,
        domain: str,
        difficulty: str,
        answer: str,
        chatbot: str
    ) -> None:
        """
        Log positive feedback
        
        Args:
            question: The original question
            domain: Classified domain
            difficulty: Classified difficulty
            answer: The generated answer
            chatbot: Name of chatbot that generated the answer
        """
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "domain": domain,
            "difficulty": difficulty,
            "answer": answer,
            "chatbot": chatbot,
            "feedback": "positive"
        }
        
        self._append_to_file(self.positive_feedback_file, feedback_entry)
        logger.info(f"Positive feedback logged for {chatbot}")
    
    def log_negative_feedback(
        self,
        question: str,
        domain: str,
        difficulty: str,
        answer: str,
        chatbot: str,
        correction: Optional[str] = None,
        correct_domain: Optional[str] = None,
        correct_difficulty: Optional[str] = None
    ) -> None:
        """
        Log negative feedback with optional corrections
        
        Args:
            question: The original question
            domain: Classified domain
            difficulty: Classified difficulty
            answer: The generated answer
            chatbot: Name of chatbot that generated the answer
            correction: Optional corrected answer
            correct_domain: Optional correct domain classification
            correct_difficulty: Optional correct difficulty classification
        """
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "domain": domain,
            "difficulty": difficulty,
            "answer": answer,
            "chatbot": chatbot,
            "feedback": "negative",
            "correction": correction,
            "correct_domain": correct_domain,
            "correct_difficulty": correct_difficulty
        }
        
        self._append_to_file(self.negative_feedback_file, feedback_entry)
        logger.info(f"Negative feedback logged for {chatbot}")
    
    def get_training_data(self) -> List[Dict]:
        """
        Get training data from negative feedback for classifier fine-tuning
        
        Returns:
            List of training examples with correct classifications
        """
        training_data = []
        
        if os.path.exists(self.negative_feedback_file):
            with open(self.negative_feedback_file, 'r') as f:
                for line in f:
                    entry = json.loads(line)
                    if entry.get("correct_domain") and entry.get("correct_difficulty"):
                        training_data.append({
                            "question": entry["question"],
                            "domain": entry["correct_domain"],
                            "difficulty": entry["correct_difficulty"]
                        })
        
        logger.info(f"Retrieved {len(training_data)} training examples")
        return training_data
    
    def get_feedback_stats(self) -> Dict[str, int]:
        """
        Get statistics about feedback
        
        Returns:
            Dictionary with feedback counts
        """
        stats = {
            "positive": 0,
            "negative": 0,
            "total": 0
        }
        
        if os.path.exists(self.positive_feedback_file):
            with open(self.positive_feedback_file, 'r') as f:
                stats["positive"] = sum(1 for _ in f)
        
        if os.path.exists(self.negative_feedback_file):
            with open(self.negative_feedback_file, 'r') as f:
                stats["negative"] = sum(1 for _ in f)
        
        stats["total"] = stats["positive"] + stats["negative"]
        return stats
    
    def _append_to_file(self, filepath: str, data: Dict) -> None:
        """Append data to a JSONL file"""
        with open(filepath, 'a') as f:
            f.write(json.dumps(data) + '\n')
