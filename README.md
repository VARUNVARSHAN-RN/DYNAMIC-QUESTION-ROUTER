# Dynamic Question Router

A multi-task question classifier with intelligent chatbot routing system. This system uses DeBERTaV3 for question classification and routes questions to specialized chatbot APIs (OpenAI GPT-4o-mini, DeepSeek R1, Anthropic Claude, HuggingFace Mistral-7B) based on domain and difficulty.

## Features

- **Intelligent Classification**: Automatically classifies questions by domain (Math, Coding, Science, Reasoning, Agentic) and difficulty (Easy, Medium, Hard)
- **Smart Routing**: Routes questions to the most appropriate chatbot based on classification
- **Fallback Mechanism**: Automatically falls back to OpenAI GPT if primary chatbot fails
- **Feedback System**: Collects user feedback for continuous improvement
- **Multiple API Support**: Integrates with OpenAI, DeepSeek, Anthropic Claude, and HuggingFace
- **Colab Support**: Easy setup for Google Colab runtime

## Architecture

```
User Question → Classification (DeBERTaV3) → Rule-based Routing → Chatbot API → Response
                                                   ↓
                                            Fallback (OpenAI)
                                                   ↓
                                            Feedback Collection
```

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/VARUNVARSHAN-RN/DYNAMIC-QUESTION-ROUTER.git
cd DYNAMIC-QUESTION-ROUTER
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure API keys:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. Start the server:
```bash
python main.py
# Or using uvicorn directly:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Google Colab Setup

1. Run the setup script:
```python
!git clone https://github.com/VARUNVARSHAN-RN/DYNAMIC-QUESTION-ROUTER.git
%cd DYNAMIC-QUESTION-ROUTER
!pip install -r requirements.txt

# Set your API keys
import os
os.environ['OPENAI_API_KEY'] = 'your_key_here'
os.environ['DEEPSEEK_API_KEY'] = 'your_key_here'
os.environ['ANTHROPIC_API_KEY'] = 'your_key_here'
os.environ['HUGGINGFACE_API_KEY'] = 'your_key_here'

# Run the setup script for detailed instructions
!python colab_setup.py
```

## API Endpoints

### POST /ask
Submit a question for classification and answering.

**Request:**
```json
{
  "question": "What is the derivative of x^2 + 3x?"
}
```

**Response:**
```json
{
  "question": "What is the derivative of x^2 + 3x?",
  "domain": "Math",
  "difficulty": "Easy",
  "confidence": {
    "domain": 0.85,
    "difficulty": 0.75
  },
  "chatbot_used": "openai",
  "answer": "The derivative is 2x + 3",
  "success": true
}
```

### POST /feedback
Submit feedback for a previous answer.

**Request:**
```json
{
  "question": "What is the derivative of x^2?",
  "predicted_domain": "Math",
  "predicted_difficulty": "Easy",
  "chatbot_used": "openai",
  "response": "The derivative is 2x",
  "feedback_positive": true,
  "corrected_domain": null,
  "corrected_difficulty": null
}
```

**Response:**
```json
{
  "message": "Thank you for your positive feedback!",
  "success": true
}
```

### GET /health
Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "classifier_loaded": true,
  "chatbots_available": ["openai", "deepseek", "claude", "huggingface"]
}
```

### GET /stats
Get feedback statistics.

**Response:**
```json
{
  "total_feedback": 10,
  "positive_feedback": 8,
  "negative_feedback": 2,
  "positive_rate": 0.8,
  "negative_feedback_items": [...]
}
```

## Routing Rules

The system uses the following routing rules:

| Domain | Difficulty | Chatbot |
|--------|------------|---------|
| Math | Easy/Medium | OpenAI GPT-4o-mini |
| Math | Hard | DeepSeek R1 |
| Coding | Easy | OpenAI GPT-4o-mini |
| Coding | Medium/Hard | DeepSeek R1 |
| Science | Easy | OpenAI GPT-4o-mini |
| Science | Medium/Hard | Anthropic Claude |
| Reasoning | Easy | OpenAI GPT-4o-mini |
| Reasoning | Medium/Hard | DeepSeek R1 |
| Agentic | Easy | OpenAI GPT-4o-mini |
| Agentic | Medium | Anthropic Claude |
| Agentic | Hard | HuggingFace Mistral-7B |

## Testing

Run the test suite:
```bash
# Start the server first
python main.py

# In another terminal, run tests
python test_api.py
```

## Project Structure

```
DYNAMIC-QUESTION-ROUTER/
├── main.py                 # FastAPI application
├── classifier.py           # Question classification logic
├── chatbots.py            # Chatbot API connectors
├── feedback_storage.py    # Feedback logging system
├── config.py              # Configuration management
├── colab_setup.py         # Google Colab setup script
├── test_api.py            # API test suite
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment variables
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Configuration

Edit `config.py` or set environment variables to customize:

- **API Keys**: Set your API keys for OpenAI, DeepSeek, Claude, and HuggingFace
- **Routing Rules**: Modify `ROUTING_RULES` dictionary to change chatbot assignment
- **Fallback Chatbot**: Set `FALLBACK_CHATBOT` to change the default fallback
- **Model**: Change `CLASSIFICATION_MODEL` to use a different classification model

## Feedback System

The system stores feedback in two formats:
- **JSON** (`feedback_data.json`): Structured format for programmatic access
- **CSV** (`feedback_data.csv`): Tabular format for analysis in spreadsheets

Negative feedback includes corrected labels for future model fine-tuning.

## Development

### Adding a New Chatbot

1. Create a new chatbot class in `chatbots.py` inheriting from `ChatbotConnector`
2. Implement the `get_response()` method
3. Register the chatbot in `ChatbotRouter.__init__()`
4. Update routing rules in `config.py`

### Customizing Classification

The current implementation uses keyword-based classification. To use a fine-tuned DeBERTaV3 model:

1. Train your model on labeled question data
2. Update `QuestionClassifier` in `classifier.py` to load your model
3. Implement `classify()` to use the model's predictions

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.