# Quick Start Guide

## Setup (5 minutes)

1. **Clone and install:**
   ```bash
   git clone https://github.com/VARUNVARSHAN-RN/DYNAMIC-QUESTION-ROUTER.git
   cd DYNAMIC-QUESTION-ROUTER
   pip install -r requirements.txt
   ```

2. **Configure API keys (optional):**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

3. **Run demo (no API keys needed):**
   ```bash
   python demo.py
   ```

## Usage Scenarios

### Without API Keys
- Run `python demo.py` - See full system demonstration
- Classification and routing logic work without APIs
- Great for understanding the system architecture

### With API Keys
- Run `python main.py` - Interactive CLI
- Run `python example.py` - Process example questions
- Integrate into your own Python code

## Key Files

| File | Purpose |
|------|---------|
| `demo.py` | Demo without API keys |
| `main.py` | Interactive CLI application |
| `example.py` | Batch processing examples |
| `classifier.py` | Domain/difficulty classification |
| `router.py` | Chatbot routing with fallback |
| `chatbots.py` | API integrations |
| `feedback.py` | Feedback collection |

## API Keys

Get your API keys from:
- OpenAI: https://platform.openai.com/api-keys
- Anthropic (Claude): https://console.anthropic.com/
- DeepSeek: https://platform.deepseek.com/
- Hugging Face: https://huggingface.co/settings/tokens

## Architecture at a Glance

```
Question → Classify → Route → Generate → Fallback → Answer → Feedback → Learn
            (DeBERTaV3)  (Priority)  (Primary)  (Backup)
```

## Common Questions

**Q: Do I need all API keys?**
A: No, the system works with any number of configured APIs. It will use available ones.

**Q: How does fallback work?**
A: Each domain/difficulty has a priority list. If primary fails, it tries the next chatbot.

**Q: Can I add my own chatbot?**
A: Yes! Create a class inheriting from `ChatbotAPI` in `chatbots.py` and add to router.

**Q: How is feedback used?**
A: Negative feedback with corrections trains the classifier to improve over time.

**Q: What if no APIs are configured?**
A: Classification and routing still work. Use demo mode to see the system logic.

## Performance Tips

1. **Start with one API**: OpenAI or Claude work well for all domains
2. **Add DeepSeek**: Excellent for coding questions
3. **Use HuggingFace**: Good free fallback option
4. **Collect feedback**: Improves classification accuracy over time

## Troubleshooting

- **Import errors**: Run `pip install -r requirements.txt`
- **API errors**: Check your API keys in `.env`
- **Model download fails**: System falls back to rule-based classification
- **No chatbots available**: Add API keys to `.env` file

## Next Steps

1. Try the demo: `python demo.py`
2. Add your API keys to `.env`
3. Run the interactive CLI: `python main.py`
4. Integrate into your project
5. Collect feedback to improve accuracy
