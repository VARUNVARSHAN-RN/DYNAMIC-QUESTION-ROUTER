# Quick Start Guide

Get the Dynamic Question Router up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

## Installation

### Method 1: Clone from GitHub

```bash
git clone https://github.com/VARUNVARSHAN-RN/DYNAMIC-QUESTION-ROUTER.git
cd DYNAMIC-QUESTION-ROUTER
pip install -r requirements.txt
```

### Method 2: Download ZIP

1. Download the repository as ZIP
2. Extract to a folder
3. Open terminal in that folder
4. Run: `pip install -r requirements.txt`

## Quick Test (No API Keys Required)

The system includes mock chatbots for testing without API keys!

### Step 1: Start the Server

```bash
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Test the API

Open a new terminal and try:

```bash
# Test health check
curl http://localhost:8000/health

# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the derivative of x^2?"}'
```

### Step 3: Run the Interactive Demo

```bash
python demo_example.py
```

This will showcase all features with 5 different question types!

## Using Real AI APIs (Optional)

To use actual AI services instead of mock responses:

### Step 1: Get API Keys

- OpenAI: https://platform.openai.com/api-keys
- DeepSeek: https://platform.deepseek.com/
- Anthropic: https://console.anthropic.com/
- HuggingFace: https://huggingface.co/settings/tokens

### Step 2: Configure Keys

```bash
cp .env.example .env
# Edit .env and add your API keys
```

### Step 3: Restart Server

```bash
python main.py
```

Now the system will use real AI responses!

## Using in Google Colab

### Option 1: Notebook

1. Open `colab_demo.ipynb` in Google Colab
2. Run all cells sequentially
3. Follow the interactive examples

### Option 2: Manual Setup

```python
# In a Colab cell
!git clone https://github.com/VARUNVARSHAN-RN/DYNAMIC-QUESTION-ROUTER.git
%cd DYNAMIC-QUESTION-ROUTER
!pip install -r requirements.txt

# Set API keys
import os
os.environ['OPENAI_API_KEY'] = 'your_key_here'

# Run setup
!python colab_setup.py
```

## API Endpoints

Once the server is running, you can access:

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Ask Question**: POST http://localhost:8000/ask
- **Submit Feedback**: POST http://localhost:8000/feedback
- **Get Statistics**: http://localhost:8000/stats

## Example Questions to Try

```bash
# Math
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" \
  -d '{"question": "Calculate the integral of 2x"}'

# Coding
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" \
  -d '{"question": "How do I sort a list in Python?"}'

# Science
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" \
  -d '{"question": "Explain how DNA replication works"}'

# Reasoning
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" \
  -d '{"question": "If A is true and B is false, what is A AND B?"}'

# Agentic
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" \
  -d '{"question": "Plan a task workflow for multiple agents"}'
```

## Troubleshooting

### Port Already in Use

If port 8000 is busy:
```bash
uvicorn main:app --port 8080
```

### Module Not Found

Install dependencies:
```bash
pip install -r requirements.txt
```

### API Key Errors

- Using mock mode? Ignore API key warnings
- Using real APIs? Check your .env file has correct keys

## Next Steps

1. Read the [README.md](README.md) for detailed documentation
2. Check [DEMO.md](DEMO.md) for system architecture
3. Review [SUMMARY.md](SUMMARY.md) for project overview
4. Run `python test_api.py` for automated tests
5. Explore the code in the Python files

## Getting Help

- Check the documentation files
- Review the code comments
- Open an issue on GitHub
- Read the API docs at /docs endpoint

Enjoy using the Dynamic Question Router! 🚀
