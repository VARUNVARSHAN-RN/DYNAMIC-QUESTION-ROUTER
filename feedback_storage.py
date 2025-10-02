"""
Feedback storage system for logging user feedback.
"""
import json
import csv
import os
from datetime import datetime
from typing import Dict, List
import logging

from config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeedbackStorage:
    """Storage system for user feedback."""
    
    def __init__(self):
        """Initialize feedback storage."""
        self.json_path = config.FEEDBACK_JSON_PATH
        self.csv_path = config.FEEDBACK_CSV_PATH
        
        # Initialize files if they don't exist
        self._initialize_storage()
    
    def _initialize_storage(self):
        """Initialize storage files if they don't exist."""
        # Initialize JSON file
        if not os.path.exists(self.json_path):
            with open(self.json_path, 'w') as f:
                json.dump([], f)
            logger.info(f"Created feedback JSON file: {self.json_path}")
        
        # Initialize CSV file
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'question', 'predicted_domain', 'predicted_difficulty',
                    'chatbot_used', 'response', 'feedback_positive', 'corrected_domain',
                    'corrected_difficulty'
                ])
            logger.info(f"Created feedback CSV file: {self.csv_path}")
    
    def save_feedback(self, feedback_data: Dict):
        """
        Save feedback to both JSON and CSV files.
        
        Args:
            feedback_data: Dictionary containing feedback information
        """
        # Add timestamp
        feedback_data['timestamp'] = datetime.now().isoformat()
        
        # Save to JSON
        try:
            with open(self.json_path, 'r') as f:
                data = json.load(f)
            
            data.append(feedback_data)
            
            with open(self.json_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info("Feedback saved to JSON")
        except Exception as e:
            logger.error(f"Error saving to JSON: {str(e)}")
        
        # Save to CSV
        try:
            with open(self.csv_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    feedback_data.get('timestamp', ''),
                    feedback_data.get('question', ''),
                    feedback_data.get('predicted_domain', ''),
                    feedback_data.get('predicted_difficulty', ''),
                    feedback_data.get('chatbot_used', ''),
                    feedback_data.get('response', ''),
                    feedback_data.get('feedback_positive', ''),
                    feedback_data.get('corrected_domain', ''),
                    feedback_data.get('corrected_difficulty', '')
                ])
            
            logger.info("Feedback saved to CSV")
        except Exception as e:
            logger.error(f"Error saving to CSV: {str(e)}")
    
    def get_all_feedback(self) -> List[Dict]:
        """
        Get all stored feedback.
        
        Returns:
            List of feedback dictionaries
        """
        try:
            with open(self.json_path, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            logger.error(f"Error reading feedback: {str(e)}")
            return []
    
    def get_negative_feedback(self) -> List[Dict]:
        """
        Get all negative feedback for fine-tuning.
        
        Returns:
            List of feedback dictionaries with negative feedback
        """
        all_feedback = self.get_all_feedback()
        return [fb for fb in all_feedback if not fb.get('feedback_positive', True)]


# Singleton instance
storage = FeedbackStorage()
