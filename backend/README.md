# Backend - Autonomous Content Factory

Intelligent backend services for content analysis, generation, and research using AI agents powered by OpenAI's API.

## 📁 Project Structure

```
backend/
├── openai_client.py                    # ⭐ OpenAI client wrapper (main utility)
├── test_openai_client.py              # Unit tests for client wrapper
├── integration_examples.py             # Usage examples and patterns
├── QUICK_REFERENCE.md                 # Quick reference guide
├── OPENAI_CLIENT_README.md            # Full client documentation
├── IMPLEMENTATION_SUMMARY.md          # Implementation details
├── ARCHITECTURE.md                    # System design & architecture
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
└── agents/
    ├── research_agent.py              # 🤖 ResearchAgent - Product analysis
    ├── test_research_agent.py        # ResearchAgent tests
    ├── __init__.py                   # Package initialization
    └── README.md                     # Agent documentation
```

## 🚀 Quick Start

### 1. Setup

```bash
# Set API key
export OPENAI_API_KEY="sk-your-api-key-here"

# Install dependencies
pip install -r requirements.txt
```

### 2. Basic Usage

```python
from openai_client import generate_response

# One-liner
response = generate_response("What is artificial intelligence?")
print(response)
```

### 3. Run Tests

```bash
# Test the client wrapper
python test_openai_client.py

# See integration examples
python integration_examples.py

# Test the ResearchAgent
cd agents
python test_research_agent.py
```

## 📦 Core Components

### OpenAI Client Wrapper (`openai_client.py`)

A lightweight, production-ready wrapper for the OpenAI API.

**Features:**
- Simple `generate_response()` function for quick usage
- Flexible `OpenAIClientWrapper` class for advanced control
- Configurable temperature, max_tokens, system prompts
- Comprehensive error handling
- Default model: `gpt-4o-mini` (fast & economical)

**Usage:**
```python
from openai_client import generate_response, OpenAIClientWrapper

# Quick usage
response = generate_response("Your question")

# Advanced usage
client = OpenAIClientWrapper(model="gpt-4")
response = client.generate_response(
    prompt="Your question",
    system_prompt="Expert role context",
    temperature=0.5,
    max_tokens=500
)
```

### Research Agent (`agents/research_agent.py`)

Analyzes product descriptions to extract structured information.

**Extracts:**
- Product name
- Key features
- Technical specifications
- Target audience
- Value proposition
- Ambiguous/vague statements

**Usage:**
```python
from agents.research_agent import ResearchAgent

agent = ResearchAgent()
result = agent.analyze("Product description text here...")

# Result includes analysis, timestamps, metadata
print(result)
```

## 📚 Documentation

### Quick Start
- **QUICK_REFERENCE.md** - One-page cheat sheet
- **Getting started**: 5 minutes to first API call

### Comprehensive Guides
- **OPENAI_CLIENT_README.md** - Full API documentation
- **ARCHITECTURE.md** - System design & technical details
- **IMPLEMENTATION_SUMMARY.md** - Implementation overview

### Examples
- **integration_examples.py** - 7 complete usage examples
- **test_openai_client.py** - Unit tests with examples
- **agents/test_research_agent.py** - Agent usage examples

## 🔧 Configuration

### Required
```bash
export OPENAI_API_KEY="sk-your-key"
```

### Optional
```bash
export OPENAI_MODEL="gpt-4o-mini"  # Default model
```

### In Code
```python
# Custom configuration
client = OpenAIClientWrapper(
    api_key="sk-custom-key",
    model="gpt-4"
)
```

## 🎯 Use Cases

### 1. Product Analysis
```python
from agents.research_agent import ResearchAgent

agent = ResearchAgent()
result = agent.analyze("Your product description")
```

### 2. Content Generation
```python
from openai_client import generate_response

# Creative
tagline = generate_response(
    "Create a marketing tagline",
    temperature=1.2
)

# Factual
summary = generate_response(
    "Summarize quantum computing",
    temperature=0.3
)
```

### 3. Data Extraction
```python
from openai_client import generate_response

response = generate_response(
    prompt="Extract features from this product: ...",
    system_prompt="You are a data extraction expert",
    temperature=0.2
)
```

### 4. Batch Processing
```python
from openai_client import generate_response

products = ["Product 1", "Product 2", "Product 3"]
results = [generate_response(f"Analyze: {p}") for p in products]
```

## 📊 API Reference

### `generate_response()`
Main convenience function.

```python
response = generate_response(
    prompt: str,                    # Required: Your question/prompt
    temperature: float = 0.7,       # Optional: 0.0-2.0
    max_tokens: Optional[int] = None,  # Optional: Response length limit
    system_prompt: Optional[str] = None  # Optional: Context/role
) -> str
```

### `OpenAIClientWrapper` Class

```python
client = OpenAIClientWrapper(
    api_key: Optional[str] = None,  # Uses OPENAI_API_KEY if not provided
    model: str = "gpt-4o-mini"      # Model to use
)

# Methods
client.generate_response(...)           # Core method
client.generate_response_with_context(...)  # With context
client.set_model(model: str)           # Change model
client.get_model() -> str              # Get current model
```

### `ResearchAgent` Class

```python
agent = ResearchAgent(
    api_key: Optional[str] = None,
    model: str = "gpt-4"
)

# Methods
result = agent.analyze(raw_text: str)          # Analyze one text
results = agent.analyze_batch(texts: list)     # Batch analyze
json_str = agent.to_json(result: dict)        # Format as JSON
```

## 🌡️ Temperature Guide

| Value | Behavior | Use Case |
|-------|----------|----------|
| 0.0-0.3 | Deterministic | Analysis, extraction, summarization |
| 0.4-0.8 | Balanced | Default, general purpose |
| 0.9-1.5 | Creative | Brainstorming, content generation |
| 1.6-2.0 | Very creative | Extreme brainstorming, experimentation |

## ⚠️ Error Handling

```python
from openai_client import generate_response

try:
    response = generate_response(prompt)
except ValueError as e:
    # Input validation errors (empty prompt, missing API key)
    print(f"Validation error: {e}")
except Exception as e:
    # API errors (rate limit, quota exceeded, etc.)
    print(f"API error: {e}")
```

## 🧪 Testing

### Unit Tests
```bash
python test_openai_client.py
# Tests: 5 test cases covering all major functionality
```

### Integration Examples
```bash
python integration_examples.py
# Examples: 7 complete usage examples
```

### Agent Tests
```bash
cd agents
python test_research_agent.py
# Tests: ResearchAgent with sample products
```

## 📋 Dependencies

```
openai>=2.0.0           # OpenAI Python SDK
python-dotenv           # .env file support
fastapi>=0.135.3       # Web framework (optional)
uvicorn>=0.44.0        # ASGI server (optional)
pydantic>=2.12.5       # Data validation (optional)
```

See `requirements.txt` for complete list.

## 🔒 Security

### API Key Management
```bash
# ✓ Recommended
export OPENAI_API_KEY="sk-..."

# ✗ Never do this
api_key = "sk-..."  # In code
git commit "api_key = ..."  # In version control
logger.info(f"Key: {api_key}")  # Logging
```

### Input Validation
- All prompts validated before API calls
- API key required at initialization
- Error messages don't expose sensitive data

## 📈 Performance

### Response Times
- Typical: 0.5-5 seconds
- Depends on: prompt complexity, API load, model

### Cost
- Varies by model and token count
- `gpt-4o-mini`: Most economical
- Use `max_tokens` to limit costs

### Concurrency
- Current: Sequential processing
- Future: Async/await support planned

## 🛠️ Troubleshooting

### "API key not provided"
```bash
export OPENAI_API_KEY="sk-your-key"
```

### "Import openai could not be resolved"
```bash
pip install openai
```

### "Empty prompt" error
```python
prompt = user_input.strip()
if not prompt:
    print("Prompt cannot be empty")
else:
    response = generate_response(prompt)
```

### Rate limiting
```python
import time
try:
    response = generate_response(prompt)
except Exception as e:
    if "rate" in str(e).lower():
        time.sleep(5)
        response = generate_response(prompt)
```

## 🚀 Next Steps

1. **Setup**: Set `OPENAI_API_KEY` environment variable
2. **Test**: Run `python test_openai_client.py`
3. **Explore**: Check `integration_examples.py`
4. **Integrate**: Use in your application
5. **Scale**: Monitor performance and costs

## 📖 Related Documentation

- **QUICK_REFERENCE.md** - One-page cheat sheet
- **OPENAI_CLIENT_README.md** - Complete client documentation
- **ARCHITECTURE.md** - Technical architecture
- **IMPLEMENTATION_SUMMARY.md** - Implementation overview
- **agents/README.md** - ResearchAgent documentation

## 🔄 Integration

### With FastAPI
```python
from fastapi import FastAPI
from openai_client import generate_response

app = FastAPI()

@app.post("/generate")
async def generate(prompt: str):
    response = generate_response(prompt)
    return {"response": response}
```

### With ResearchAgent
```python
from agents.research_agent import ResearchAgent

agent = ResearchAgent()
result = agent.analyze("Product text...")
```

### With Data Pipeline
```python
from openai_client import OpenAIClientWrapper

client = OpenAIClientWrapper()
for item in data_stream:
    analysis = client.generate_response(f"Analyze: {item}")
    results.append(analysis)
```

## 📞 Support

For issues or questions:
1. Check **QUICK_REFERENCE.md** for common patterns
2. Review **OPENAI_CLIENT_README.md** for API details
3. Check **ARCHITECTURE.md** for system design
4. See **integration_examples.py** for examples
5. Review test files for working code

## 📝 License

Part of the Autonomous Content Factory project.

---

**Backend v1.0** | OpenAI Client Wrapper + ResearchAgent | Production Ready
