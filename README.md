# DYNAMIC-QUESTION-ROUTER

A sophisticated question routing system that uses DeBERTaV3 to classify questions by domain and difficulty, then intelligently routes them to the most appropriate chatbot API (OpenAI, DeepSeek, Claude, or Hugging Face) with automatic fallback and feedback learning capabilities.

## 🚀 Features

- **Intelligent Classification**: Uses DeBERTaV3 to classify questions into:
  - **Domains**: Math, Coding, Science, Reasoning, Agentic
  - **Difficulty**: Easy, Medium, Hard

- **Smart Routing**: Routes questions to the best chatbot API based on classification:
  - OpenAI GPT
  - DeepSeek
  - Claude (Anthropic)
  - Hugging Face Inference API

- **Automatic Fallback**: If primary chatbot fails, automatically tries fallback options

- **Feedback System**: 
  - Collects positive and negative feedback
  - Stores corrections for model improvement
  - Enables future classifier fine-tuning

- **Extensible Architecture**: Easy to add new chatbots or modify routing logic

## 📋 Requirements

- Python 3.8+
- API keys for at least one chatbot service (OpenAI, DeepSeek, Claude, or Hugging Face)

## 🔧 Installation

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

## ⚙️ Configuration

Edit the `.env` file with your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

You only need to configure the APIs you want to use. The system will automatically skip unavailable chatbots.

## 🎯 Usage

### Command Line Interface

Run the interactive CLI:

```bash
python main.py
```

Example session:
```
Question: What is the derivative of x^2?

Domain: Math
Difficulty: Medium
Chatbot: Claude

Answer: The derivative of x^2 is 2x...

Was this answer helpful? (y/n): y
```

### Python API

```python
from main import DynamicQuestionRouter

# Initialize the router
router = DynamicQuestionRouter()

# Process a question
result = router.process_question("What is machine learning?")

print(f"Domain: {result['domain']}")
print(f"Difficulty: {result['difficulty']}")
print(f"Answer: {result['answer']}")
print(f"Chatbot: {result['chatbot']}")

# Submit positive feedback
router.submit_feedback(
    question=result['question'],
    domain=result['domain'],
    difficulty=result['difficulty'],
    answer=result['answer'],
    chatbot=result['chatbot'],
    is_positive=True
)

# Submit negative feedback with corrections
router.submit_feedback(
    question=result['question'],
    domain=result['domain'],
    difficulty=result['difficulty'],
    answer=result['answer'],
    chatbot=result['chatbot'],
    is_positive=False,
    correction="The correct answer is...",
    correct_domain="Science",
    correct_difficulty="Easy"
)

# Get system statistics
stats = router.get_statistics()
print(stats)
```

## 🔄 System Flow

1. **User Input**: User enters a question
2. **Classification**: DeBERTaV3 classifies domain and difficulty
3. **Routing**: Router selects optimal chatbot based on classification
4. **Generation**: Selected chatbot generates answer
5. **Fallback**: If primary fails, fallback chatbots are tried
6. **Response**: Answer is displayed to user
7. **Feedback**: User provides feedback (positive/negative)
8. **Learning**: Feedback stored for future classifier fine-tuning

## 📊 Routing Strategy

The system uses an intelligent routing map optimized for each domain and difficulty:

- **Math Questions**: Claude excels at hard problems, OpenAI for easy ones
- **Coding Questions**: DeepSeek prioritized for coding tasks
- **Science Questions**: Claude and OpenAI preferred
- **Reasoning Questions**: Claude for complex reasoning, OpenAI for simpler tasks
- **Agentic Questions**: Claude and OpenAI for multi-step planning

Each classification has a priority-ordered list of chatbots with automatic fallback.

## 📁 Project Structure

```
DYNAMIC-QUESTION-ROUTER/
├── main.py              # Main application entry point
├── classifier.py        # DeBERTaV3-based question classifier
├── router.py           # Routing logic with fallback
├── chatbots.py         # Chatbot API integrations
├── feedback.py         # Feedback collection and storage
├── requirements.txt    # Python dependencies
├── .env.example       # Example environment configuration
├── .gitignore         # Git ignore patterns
└── README.md          # This file
```

## 🔒 Security

- API keys are stored in `.env` file (not committed to git)
- All API communications use secure HTTPS
- Sensitive data is never logged

## 🤝 Contributing

Contributions are welcome! To add a new chatbot:

1. Add the chatbot class to `chatbots.py` (inherit from `ChatbotAPI`)
2. Add the chatbot to the router in `router.py`
3. Update routing map as needed
4. Test thoroughly

## 📝 License

MIT License - feel free to use this project for any purpose.

## 🙏 Acknowledgments

- DeBERTaV3 by Microsoft
- OpenAI, Anthropic, DeepSeek, and Hugging Face for their excellent APIs