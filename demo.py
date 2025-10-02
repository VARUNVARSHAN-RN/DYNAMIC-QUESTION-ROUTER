"""
Demo script showing the Dynamic Question Router in action
Works without API keys by demonstrating classification and routing logic
"""

from classifier import QuestionClassifier
from router import QuestionRouter
from feedback import FeedbackManager
import os


def print_separator(char="=", length=80):
    """Print a separator line"""
    print(char * length)


def demo_classification():
    """Demonstrate the classification system"""
    print_separator()
    print("DEMO 1: Question Classification")
    print_separator()
    print()
    
    classifier = QuestionClassifier(use_pretrained=False)
    
    test_questions = [
        "What is the integral of x^2 from 0 to 5?",
        "Write a Python function to sort a list using bubble sort",
        "Explain how DNA replication works in cells",
        "If all mammals are warm-blooded and whales are mammals, what can we conclude?",
        "Create an automated workflow to process incoming emails and categorize them"
    ]
    
    for i, question in enumerate(test_questions, 1):
        domain, difficulty = classifier.classify(question)
        print(f"Question {i}:")
        print(f"  {question}")
        print(f"  → Domain: {domain}")
        print(f"  → Difficulty: {difficulty}")
        print()


def demo_routing():
    """Demonstrate the routing system"""
    print_separator()
    print("DEMO 2: Intelligent Routing with Fallback")
    print_separator()
    print()
    
    router = QuestionRouter()
    
    test_cases = [
        ("Math", "Hard"),
        ("Coding", "Medium"),
        ("Science", "Easy"),
        ("Reasoning", "Medium"),
        ("Agentic", "Hard")
    ]
    
    for domain, difficulty in test_cases:
        chatbot_priority = router.ROUTING_MAP.get(
            (domain, difficulty),
            ["OpenAI", "Claude", "DeepSeek", "HuggingFace"]
        )
        print(f"{domain} / {difficulty}:")
        print(f"  Priority: {' → '.join(chatbot_priority)}")
        print(f"  Strategy: Primary is {chatbot_priority[0]}, falls back to {chatbot_priority[1:]} if needed")
        print()


def demo_feedback():
    """Demonstrate the feedback system"""
    print_separator()
    print("DEMO 3: Feedback Collection & Learning")
    print_separator()
    print()
    
    # Use temp directory for demo
    feedback_dir = "/tmp/demo_feedback"
    os.makedirs(feedback_dir, exist_ok=True)
    
    feedback_mgr = FeedbackManager(feedback_dir=feedback_dir)
    
    # Simulate some feedback
    print("Simulating user feedback...")
    print()
    
    # Positive feedback
    feedback_mgr.log_positive_feedback(
        question="What is 2+2?",
        domain="Math",
        difficulty="Easy",
        answer="2+2 equals 4",
        chatbot="OpenAI"
    )
    print("✓ Positive feedback recorded")
    
    # Negative feedback with correction
    feedback_mgr.log_negative_feedback(
        question="What is machine learning?",
        domain="Coding",  # Initially misclassified
        difficulty="Medium",
        answer="Some incorrect answer",
        chatbot="HuggingFace",
        correction="Machine learning is a subset of AI that enables systems to learn from data...",
        correct_domain="Science",  # Correct classification
        correct_difficulty="Hard"
    )
    print("✓ Negative feedback with corrections recorded")
    print()
    
    # Get statistics
    stats = feedback_mgr.get_feedback_stats()
    print(f"Feedback Statistics:")
    print(f"  Positive: {stats['positive']}")
    print(f"  Negative: {stats['negative']}")
    print(f"  Total: {stats['total']}")
    print()
    
    # Get training data
    training_data = feedback_mgr.get_training_data()
    print(f"Training Data Available: {len(training_data)} examples")
    if training_data:
        print("  Sample training example:")
        example = training_data[0]
        print(f"    Question: {example['question']}")
        print(f"    Correct Domain: {example['domain']}")
        print(f"    Correct Difficulty: {example['difficulty']}")
    print()


def demo_complete_flow():
    """Demonstrate the complete flow"""
    print_separator()
    print("DEMO 4: Complete Question Processing Flow")
    print_separator()
    print()
    
    from main import DynamicQuestionRouter
    
    router = DynamicQuestionRouter(use_pretrained_classifier=False)
    
    question = "Write a recursive function to calculate the nth Fibonacci number"
    
    print(f"User Question: {question}")
    print()
    print("Step 1: Classify the question...")
    result = router.process_question(question)
    print(f"  → Domain: {result['domain']}")
    print(f"  → Difficulty: {result['difficulty']}")
    print()
    
    print("Step 2: Route to appropriate chatbot...")
    print(f"  → Primary chatbot: {router.router.ROUTING_MAP.get((result['domain'], result['difficulty']))[0]}")
    print(f"  → Fallback chain: {router.router.ROUTING_MAP.get((result['domain'], result['difficulty']))[1:]}")
    print()
    
    if result['success']:
        print("Step 3: Generate answer...")
        print(f"  → Using: {result['chatbot']}")
        print(f"  → Answer: {result['answer'][:100]}...")
    else:
        print("Step 3: Answer generation...")
        print(f"  → Status: No API keys configured (this is expected in demo mode)")
        print(f"  → Note: In production, the system would try each chatbot in priority order")
    print()
    
    print("Step 4: Collect feedback...")
    print("  → User can provide positive/negative feedback")
    print("  → Negative feedback can include corrections")
    print("  → Data is stored for future classifier fine-tuning")
    print()


def main():
    """Run all demos"""
    print()
    print_separator("=")
    print("DYNAMIC QUESTION ROUTER - SYSTEM DEMONSTRATION")
    print_separator("=")
    print()
    print("This demo showcases the complete system without requiring API keys.")
    print("In production, the system would connect to actual chatbot APIs.")
    print()
    
    try:
        demo_classification()
        demo_routing()
        demo_feedback()
        demo_complete_flow()
        
        print_separator("=")
        print("DEMO COMPLETE")
        print_separator("=")
        print()
        print("To use the system with real chatbot APIs:")
        print("1. Copy .env.example to .env")
        print("2. Add your API keys")
        print("3. Run: python main.py")
        print()
        
    except Exception as e:
        print(f"\nDemo error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
