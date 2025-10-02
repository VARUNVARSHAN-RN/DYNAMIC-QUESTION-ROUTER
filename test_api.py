"""
Test script for the Dynamic Question Router API.
Can be used for local testing without API keys.
"""
import requests
import json
from typing import Dict, Any


class APITester:
    """Tester for the Dynamic Question Router API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize tester with base URL."""
        self.base_url = base_url
    
    def test_health(self) -> Dict[str, Any]:
        """Test health check endpoint."""
        print("\n" + "=" * 80)
        print("Testing Health Check Endpoint")
        print("=" * 80)
        
        try:
            response = requests.get(f"{self.base_url}/health")
            response.raise_for_status()
            result = response.json()
            print(json.dumps(result, indent=2))
            return result
        except Exception as e:
            print(f"Error: {str(e)}")
            return {}
    
    def test_ask(self, question: str) -> Dict[str, Any]:
        """Test ask endpoint."""
        print("\n" + "=" * 80)
        print(f"Testing Ask Endpoint")
        print(f"Question: {question}")
        print("=" * 80)
        
        try:
            response = requests.post(
                f"{self.base_url}/ask",
                json={"question": question}
            )
            response.raise_for_status()
            result = response.json()
            print(json.dumps(result, indent=2))
            return result
        except Exception as e:
            print(f"Error: {str(e)}")
            return {}
    
    def test_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Test feedback endpoint."""
        print("\n" + "=" * 80)
        print("Testing Feedback Endpoint")
        print("=" * 80)
        
        try:
            response = requests.post(
                f"{self.base_url}/feedback",
                json=feedback_data
            )
            response.raise_for_status()
            result = response.json()
            print(json.dumps(result, indent=2))
            return result
        except Exception as e:
            print(f"Error: {str(e)}")
            return {}
    
    def test_stats(self) -> Dict[str, Any]:
        """Test stats endpoint."""
        print("\n" + "=" * 80)
        print("Testing Stats Endpoint")
        print("=" * 80)
        
        try:
            response = requests.get(f"{self.base_url}/stats")
            response.raise_for_status()
            result = response.json()
            print(json.dumps(result, indent=2))
            return result
        except Exception as e:
            print(f"Error: {str(e)}")
            return {}
    
    def run_all_tests(self):
        """Run all test cases."""
        print("\n" + "=" * 80)
        print("DYNAMIC QUESTION ROUTER - API TEST SUITE")
        print("=" * 80)
        
        # Test 1: Health check
        self.test_health()
        
        # Test 2: Math question - Easy
        math_result = self.test_ask("What is 5 + 3?")
        
        # Test 3: Coding question - Medium
        coding_result = self.test_ask("How do I implement a binary search algorithm in Python?")
        
        # Test 4: Science question - Hard
        science_result = self.test_ask("Explain the complex mechanism of photosynthesis at the molecular level")
        
        # Test 5: Reasoning question
        reasoning_result = self.test_ask("If all mammals are animals and all dogs are mammals, are dogs animals?")
        
        # Test 6: Positive feedback
        if math_result:
            self.test_feedback({
                "question": "What is 5 + 3?",
                "predicted_domain": math_result.get("domain", "Math"),
                "predicted_difficulty": math_result.get("difficulty", "Easy"),
                "chatbot_used": math_result.get("chatbot_used", "openai"),
                "response": math_result.get("answer", ""),
                "feedback_positive": True
            })
        
        # Test 7: Negative feedback with corrections
        if coding_result:
            self.test_feedback({
                "question": "How do I implement a binary search?",
                "predicted_domain": coding_result.get("domain", "Coding"),
                "predicted_difficulty": coding_result.get("difficulty", "Medium"),
                "chatbot_used": coding_result.get("chatbot_used", "deepseek"),
                "response": coding_result.get("answer", ""),
                "feedback_positive": False,
                "corrected_domain": "Coding",
                "corrected_difficulty": "Hard"
            })
        
        # Test 8: Get statistics
        self.test_stats()
        
        print("\n" + "=" * 80)
        print("ALL TESTS COMPLETED")
        print("=" * 80)


if __name__ == "__main__":
    import sys
    
    base_url = "http://localhost:8000"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    tester = APITester(base_url)
    tester.run_all_tests()
