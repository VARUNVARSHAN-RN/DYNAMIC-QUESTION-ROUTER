"""
Main application for Dynamic Question Router
Integrates classifier, router, chatbots, and feedback system
"""

import os
import logging
from typing import Dict, Optional
from dotenv import load_dotenv

from classifier import QuestionClassifier
from router import QuestionRouter
from feedback import FeedbackManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DynamicQuestionRouter:
    """Main application class for the dynamic question routing system"""
    
    def __init__(self, use_pretrained_classifier: bool = False):
        """
        Initialize the question routing system
        
        Args:
            use_pretrained_classifier: Whether to use the pretrained DeBERTaV3 model
                                      (requires internet connection)
        """
        logger.info("Initializing Dynamic Question Router")
        
        # Load environment variables
        load_dotenv()
        
        # Initialize components
        self.classifier = QuestionClassifier(use_pretrained=use_pretrained_classifier)
        self.router = QuestionRouter()
        self.feedback_manager = FeedbackManager()
        
        logger.info("Dynamic Question Router initialized successfully")
    
    def process_question(self, question: str) -> Dict:
        """
        Process a question through the complete pipeline
        
        Args:
            question: User's question
            
        Returns:
            Dictionary with results including answer, domain, difficulty, and chatbot
        """
        logger.info(f"Processing question: {question[:50]}...")
        
        # Step 1: Classify domain and difficulty
        domain, difficulty = self.classifier.classify(question)
        
        # Step 2: Route to appropriate chatbot
        answer, chatbot = self.router.route_question(question, domain, difficulty)
        
        # Prepare result
        result = {
            "question": question,
            "domain": domain,
            "difficulty": difficulty,
            "answer": answer,
            "chatbot": chatbot,
            "success": answer is not None
        }
        
        if not result["success"]:
            logger.error("Failed to generate answer")
            result["error"] = "All chatbots failed to generate an answer"
        
        return result
    
    def submit_feedback(
        self,
        question: str,
        domain: str,
        difficulty: str,
        answer: str,
        chatbot: str,
        is_positive: bool,
        correction: Optional[str] = None,
        correct_domain: Optional[str] = None,
        correct_difficulty: Optional[str] = None
    ) -> None:
        """
        Submit user feedback for an answer
        
        Args:
            question: The original question
            domain: Classified domain
            difficulty: Classified difficulty
            answer: The generated answer
            chatbot: Chatbot that generated the answer
            is_positive: Whether feedback is positive
            correction: Optional corrected answer (for negative feedback)
            correct_domain: Optional correct domain (for negative feedback)
            correct_difficulty: Optional correct difficulty (for negative feedback)
        """
        if is_positive:
            self.feedback_manager.log_positive_feedback(
                question, domain, difficulty, answer, chatbot
            )
            logger.info("Positive feedback recorded")
        else:
            self.feedback_manager.log_negative_feedback(
                question, domain, difficulty, answer, chatbot,
                correction, correct_domain, correct_difficulty
            )
            logger.info("Negative feedback recorded with corrections")
    
    def fine_tune_classifier(self) -> None:
        """Fine-tune the classifier using collected feedback"""
        training_data = self.feedback_manager.get_training_data()
        
        if len(training_data) > 0:
            logger.info(f"Fine-tuning classifier with {len(training_data)} examples")
            self.classifier.fine_tune(training_data)
        else:
            logger.info("No training data available for fine-tuning")
    
    def get_statistics(self) -> Dict:
        """Get system statistics"""
        return {
            "available_chatbots": self.router.get_available_chatbots(),
            "feedback_stats": self.feedback_manager.get_feedback_stats()
        }


def main():
    """Main entry point for the application"""
    print("=" * 60)
    print("Dynamic Question Router")
    print("=" * 60)
    
    # Initialize the system
    router = DynamicQuestionRouter()
    
    # Show available chatbots
    stats = router.get_statistics()
    print(f"\nAvailable chatbots: {', '.join(stats['available_chatbots'])}")
    
    if not stats['available_chatbots']:
        print("\nWARNING: No chatbot APIs are configured!")
        print("Please set API keys in .env file (see .env.example)")
        print("\nRunning in demo mode with mock responses...")
    
    print("\n" + "=" * 60)
    print("Enter your questions (type 'quit' to exit, 'stats' for statistics)")
    print("=" * 60)
    
    while True:
        print("\n")
        question = input("Question: ").strip()
        
        if question.lower() == 'quit':
            break
        elif question.lower() == 'stats':
            stats = router.get_statistics()
            print("\nSystem Statistics:")
            print(f"Available chatbots: {stats['available_chatbots']}")
            print(f"Feedback: {stats['feedback_stats']}")
            continue
        elif not question:
            continue
        
        # Process the question
        result = router.process_question(question)
        
        # Display results
        print(f"\nDomain: {result['domain']}")
        print(f"Difficulty: {result['difficulty']}")
        print(f"Chatbot: {result['chatbot']}")
        print(f"\nAnswer: {result['answer']}")
        
        if result['success']:
            # Ask for feedback
            feedback = input("\nWas this answer helpful? (y/n): ").strip().lower()
            
            if feedback == 'y':
                router.submit_feedback(
                    result['question'],
                    result['domain'],
                    result['difficulty'],
                    result['answer'],
                    result['chatbot'],
                    is_positive=True
                )
                print("Thank you for your feedback!")
            elif feedback == 'n':
                correction = input("Provide correct answer (optional): ").strip()
                correct_domain = input(f"Correct domain (current: {result['domain']}, optional): ").strip()
                correct_difficulty = input(f"Correct difficulty (current: {result['difficulty']}, optional): ").strip()
                
                router.submit_feedback(
                    result['question'],
                    result['domain'],
                    result['difficulty'],
                    result['answer'],
                    result['chatbot'],
                    is_positive=False,
                    correction=correction if correction else None,
                    correct_domain=correct_domain if correct_domain else None,
                    correct_difficulty=correct_difficulty if correct_difficulty else None
                )
                print("Thank you for your feedback!")
    
    print("\nGoodbye!")


if __name__ == "__main__":
    main()
