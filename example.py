"""
Example script demonstrating the Dynamic Question Router
Shows how to use the system programmatically
"""

from main import DynamicQuestionRouter


def run_examples():
    """Run example questions through the system"""
    
    # Initialize the router
    print("Initializing Dynamic Question Router...\n")
    router = DynamicQuestionRouter()
    
    # Get system statistics
    stats = router.get_statistics()
    print(f"Available chatbots: {', '.join(stats['available_chatbots'])}")
    print(f"Feedback stats: {stats['feedback_stats']}\n")
    
    if not stats['available_chatbots']:
        print("WARNING: No chatbot APIs configured. Please add API keys to .env file.")
        print("The system will still classify questions but cannot generate answers.\n")
    
    # Example questions covering different domains and difficulties
    example_questions = [
        {
            "question": "What is 2 + 2?",
            "expected_domain": "Math",
            "expected_difficulty": "Easy"
        },
        {
            "question": "Write a Python function to calculate the Fibonacci sequence",
            "expected_domain": "Coding",
            "expected_difficulty": "Medium"
        },
        {
            "question": "Explain quantum entanglement and its implications",
            "expected_domain": "Science",
            "expected_difficulty": "Hard"
        },
        {
            "question": "If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly?",
            "expected_domain": "Reasoning",
            "expected_difficulty": "Medium"
        },
        {
            "question": "Create a plan to automate my daily email workflow",
            "expected_domain": "Agentic",
            "expected_difficulty": "Medium"
        }
    ]
    
    print("=" * 80)
    print("Running Example Questions")
    print("=" * 80)
    
    for i, example in enumerate(example_questions, 1):
        question = example["question"]
        
        print(f"\n[Example {i}]")
        print(f"Question: {question}")
        print(f"Expected - Domain: {example['expected_domain']}, Difficulty: {example['expected_difficulty']}")
        
        # Process the question
        result = router.process_question(question)
        
        # Display results
        print(f"Classified - Domain: {result['domain']}, Difficulty: {result['difficulty']}")
        
        if result['success']:
            print(f"Chatbot: {result['chatbot']}")
            print(f"Answer: {result['answer'][:200]}...")  # Show first 200 chars
            
            # Simulate positive feedback for demonstration
            router.submit_feedback(
                result['question'],
                result['domain'],
                result['difficulty'],
                result['answer'],
                result['chatbot'],
                is_positive=True
            )
            print("✓ Positive feedback recorded")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
        
        print("-" * 80)
    
    # Show updated statistics
    print("\n")
    print("=" * 80)
    print("Final Statistics")
    print("=" * 80)
    stats = router.get_statistics()
    print(f"Available chatbots: {stats['available_chatbots']}")
    print(f"Feedback stats: {stats['feedback_stats']}")


if __name__ == "__main__":
    run_examples()
