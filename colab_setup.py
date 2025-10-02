"""
Google Colab setup script for the Dynamic Question Router.
Run this in a Colab notebook to set up the environment.
"""

# Installation commands for Colab
COLAB_SETUP = """
# Install required packages
!pip install -q fastapi uvicorn[standard] pydantic python-multipart
!pip install -q transformers torch accelerate
!pip install -q openai anthropic requests pandas aiofiles python-dotenv

# Clone the repository (if needed)
# !git clone https://github.com/VARUNVARSHAN-RN/DYNAMIC-QUESTION-ROUTER.git
# %cd DYNAMIC-QUESTION-ROUTER

# Start the server in the background using pyngrok for public URL
!pip install -q pyngrok

from pyngrok import ngrok
import uvicorn
import threading
import time

# Set up ngrok tunnel
public_url = ngrok.connect(8000)
print(f"Public URL: {public_url}")

# Start FastAPI server in background thread
def run_server():
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Wait for server to start
time.sleep(5)
print("Server started! You can now make requests to the API.")
"""

# Sample usage in Colab
COLAB_USAGE = """
import requests
import json

# Get the public URL from ngrok
# public_url should be set from the setup above

# Example 1: Ask a math question
response = requests.post(
    f"{public_url}/ask",
    json={"question": "What is the derivative of x^2 + 3x + 5?"}
)
print("Math Question Response:")
print(json.dumps(response.json(), indent=2))

# Example 2: Ask a coding question
response = requests.post(
    f"{public_url}/ask",
    json={"question": "How do I implement a binary search algorithm in Python?"}
)
print("\\nCoding Question Response:")
print(json.dumps(response.json(), indent=2))

# Example 3: Submit positive feedback
feedback_response = requests.post(
    f"{public_url}/feedback",
    json={
        "question": "What is the derivative of x^2?",
        "predicted_domain": "Math",
        "predicted_difficulty": "Easy",
        "chatbot_used": "openai",
        "response": "The derivative is 2x",
        "feedback_positive": True
    }
)
print("\\nFeedback Response:")
print(json.dumps(feedback_response.json(), indent=2))

# Example 4: Get statistics
stats_response = requests.get(f"{public_url}/stats")
print("\\nStatistics:")
print(json.dumps(stats_response.json(), indent=2))
"""


def print_colab_instructions():
    """Print instructions for using in Google Colab."""
    print("=" * 80)
    print("GOOGLE COLAB SETUP INSTRUCTIONS")
    print("=" * 80)
    print("\n1. SETUP - Run this in a Colab cell:")
    print("-" * 80)
    print(COLAB_SETUP)
    print("\n2. USAGE - Test the API with these examples:")
    print("-" * 80)
    print(COLAB_USAGE)
    print("\n3. CONFIGURATION:")
    print("-" * 80)
    print("Create a .env file or set environment variables with your API keys:")
    print("  OPENAI_API_KEY=your_key")
    print("  DEEPSEEK_API_KEY=your_key")
    print("  ANTHROPIC_API_KEY=your_key")
    print("  HUGGINGFACE_API_KEY=your_key")
    print("\n4. For Colab, you can also set variables directly in Python:")
    print("  import os")
    print("  os.environ['OPENAI_API_KEY'] = 'your_key_here'")
    print("=" * 80)


if __name__ == "__main__":
    print_colab_instructions()
