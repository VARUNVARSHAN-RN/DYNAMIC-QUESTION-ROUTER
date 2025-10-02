#!/usr/bin/env python3
"""
Quick example script to demonstrate the Dynamic Question Router.
Run this script to see the system in action with various question types.
"""
import requests
import json
import time


class QuestionRouterDemo:
    """Demo client for the Question Router API."""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.check_server()
    
    def check_server(self):
        """Check if server is running."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server is running and healthy!")
                return True
        except requests.exceptions.ConnectionError:
            print("❌ Server is not running!")
            print("\nPlease start the server first:")
            print("  python main.py")
            print("\nOr run:")
            print("  ./start.sh")
            exit(1)
    
    def ask_question(self, question, description=""):
        """Ask a question and display the response."""
        print(f"\n{'='*80}")
        if description:
            print(f"Demo: {description}")
        print(f"Question: {question}")
        print(f"{'='*80}")
        
        try:
            response = requests.post(
                f"{self.base_url}/ask",
                json={"question": question},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n📊 Classification:")
                print(f"   Domain: {result['domain']}")
                print(f"   Difficulty: {result['difficulty']}")
                print(f"   Confidence: Domain={result['confidence']['domain']:.2f}, Difficulty={result['confidence']['difficulty']:.2f}")
                print(f"\n🤖 Routed to: {result['chatbot_used']}")
                print(f"\n💬 Answer:")
                print(f"   {result['answer']}")
                print(f"\n✅ Success: {result['success']}")
                return result
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"   {response.json()}")
                return None
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return None
    
    def submit_feedback(self, question_data, is_positive, corrections=None):
        """Submit feedback for a question."""
        feedback = {
            "question": question_data["question"],
            "predicted_domain": question_data["domain"],
            "predicted_difficulty": question_data["difficulty"],
            "chatbot_used": question_data["chatbot_used"],
            "response": question_data["answer"],
            "feedback_positive": is_positive
        }
        
        if not is_positive and corrections:
            feedback.update(corrections)
        
        try:
            response = requests.post(
                f"{self.base_url}/feedback",
                json=feedback,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n📝 Feedback submitted: {result['message']}")
                return True
            else:
                print(f"❌ Feedback error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return False
    
    def show_stats(self):
        """Display feedback statistics."""
        print(f"\n{'='*80}")
        print("📊 FEEDBACK STATISTICS")
        print(f"{'='*80}")
        
        try:
            response = requests.get(f"{self.base_url}/stats", timeout=10)
            
            if response.status_code == 200:
                stats = response.json()
                print(f"\nTotal Feedback: {stats['total_feedback']}")
                print(f"Positive: {stats['positive_feedback']} ({stats['positive_rate']*100:.1f}%)")
                print(f"Negative: {stats['negative_feedback']}")
                
                if stats['negative_feedback_items']:
                    print(f"\nRecent Negative Feedback:")
                    for item in stats['negative_feedback_items'][-3:]:
                        print(f"  • {item['question'][:50]}...")
                        if item.get('corrected_domain'):
                            print(f"    Correction: {item['corrected_domain']} / {item['corrected_difficulty']}")
                
                return stats
            else:
                print(f"❌ Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return None
    
    def run_demo(self):
        """Run the complete demo."""
        print("\n" + "="*80)
        print("🚀 DYNAMIC QUESTION ROUTER - INTERACTIVE DEMO")
        print("="*80)
        
        # Demo 1: Math question (Easy)
        result1 = self.ask_question(
            "What is 5 + 3 * 2?",
            "Math Question - Easy"
        )
        if result1:
            time.sleep(1)
            self.submit_feedback(result1, is_positive=True)
        
        time.sleep(1)
        
        # Demo 2: Coding question (Medium)
        result2 = self.ask_question(
            "How do I implement a binary search algorithm in Python?",
            "Coding Question - Medium"
        )
        if result2:
            time.sleep(1)
            self.submit_feedback(result2, is_positive=True)
        
        time.sleep(1)
        
        # Demo 3: Science question (Complex)
        result3 = self.ask_question(
            "Explain the complex mechanism of photosynthesis at the molecular level",
            "Science Question - Complex"
        )
        if result3:
            time.sleep(1)
            # Submit negative feedback with correction
            self.submit_feedback(
                result3,
                is_positive=False,
                corrections={
                    "corrected_domain": "Science",
                    "corrected_difficulty": "Hard"
                }
            )
        
        time.sleep(1)
        
        # Demo 4: Reasoning question
        result4 = self.ask_question(
            "If all mammals are animals and all dogs are mammals, are dogs animals?",
            "Reasoning Question"
        )
        
        time.sleep(1)
        
        # Demo 5: Agentic question
        result5 = self.ask_question(
            "Plan a workflow for coordinating multiple AI agents to solve a complex task",
            "Agentic Question"
        )
        
        time.sleep(1)
        
        # Show final statistics
        self.show_stats()
        
        print("\n" + "="*80)
        print("✅ DEMO COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nTry asking your own questions:")
        print(f"  curl -X POST {self.base_url}/ask \\")
        print("    -H 'Content-Type: application/json' \\")
        print("    -d '{\"question\": \"Your question here\"}'")
        print("\nOr visit the API docs at:")
        print(f"  {self.base_url}/docs")
        print()


if __name__ == "__main__":
    demo = QuestionRouterDemo()
    demo.run_demo()
