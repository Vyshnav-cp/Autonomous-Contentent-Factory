# Quick Reference - OpenAI Client Wrapper

## One-Liner (Fastest)
```python
from openai_client import generate_response
print(generate_response("Your question here"))
```

## Setup (One-time)
```bash
export OPENAI_API_KEY="sk-your-key"
```

## Common Patterns

### Pattern 1: Simple Q&A
```python
from openai_client import generate_response

response = generate_response("What is machine learning?")
```

### Pattern 2: Controlled Output
```python
response = generate_response(
    "Summarize AI trends",
    temperature=0.3,      # More focused
    max_tokens=200        # Limit response length
)
```

### Pattern 3: Specialized Behavior
```python
response = generate_response(
    prompt="How do I learn Python?",
    system_prompt="You are an expert programmer. Give practical advice.",
    temperature=0.6
)
```

### Pattern 4: Custom Client
```python
from openai_client import OpenAIClientWrapper

client = OpenAIClientWrapper(model="gpt-4")
response = client.generate_response("Your prompt")
```

### Pattern 5: Batch Processing
```python
from openai_client import generate_response

questions = ["What is AI?", "What is ML?", "What is DL?"]
for q in questions:
    print(generate_response(q))
```

## Parameter Quick Guide

| Parameter | Default | Range | Use Case |
|-----------|---------|-------|----------|
| `temperature` | 0.7 | 0.0-2.0 | 0.2=focused, 0.7=balanced, 1.5=creative |
| `max_tokens` | None | 1-4096 | Limit response length, control costs |
| `model` | gpt-4o-mini | - | Switch to gpt-4, gpt-3.5-turbo, etc. |
| `system_prompt` | None | - | Define role/context for the AI |

## Temperature Presets

```python
# Deterministic - for analysis/extraction
response = generate_response(prompt, temperature=0.2)

# Balanced - default, good for most tasks
response = generate_response(prompt, temperature=0.7)

# Creative - for brainstorming/content
response = generate_response(prompt, temperature=1.2)
```

## Error Handling Template

```python
from openai_client import generate_response

try:
    response = generate_response("Your prompt")
    print(response)
except ValueError as e:
    print(f"Input error: {e}")  # Empty prompt, missing API key
except Exception as e:
    print(f"API error: {e}")    # OpenAI API error
```

## Integration Points

### With ResearchAgent
```python
from agents.research_agent import ResearchAgent

agent = ResearchAgent()
result = agent.analyze("Product description...")
```

### In a FastAPI endpoint
```python
from fastapi import FastAPI
from openai_client import generate_response

app = FastAPI()

@app.post("/generate")
async def generate(prompt: str):
    response = generate_response(prompt)
    return {"response": response}
```

### In a data pipeline
```python
from openai_client import OpenAIClientWrapper

client = OpenAIClientWrapper()

for item in data:
    analysis = client.generate_response(
        f"Analyze: {item}",
        temperature=0.3
    )
    results.append(analysis)
```

## Testing Your Setup

```bash
# Verify installation
python -c "from openai_client import generate_response; print('✓ Import OK')"

# Test API connectivity
python test_openai_client.py

# See examples
python integration_examples.py
```

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| `ValueError: API key not provided` | `export OPENAI_API_KEY="sk-..."` |
| `ValueError: Prompt cannot be empty` | Ensure `prompt` is not empty/whitespace |
| Import error | `pip install openai` |
| Timeout | Response takes >5s, may need retry |
| Rate limited | Wait 60s or upgrade API plan |

## Files Location

```
backend/
├── openai_client.py              ← Main module
├── test_openai_client.py         ← Unit tests
├── integration_examples.py        ← Usage examples
├── OPENAI_CLIENT_README.md       ← Full docs
└── IMPLEMENTATION_SUMMARY.md     ← Overview
```

## Model Choices

```python
# Fast & Cheap (default)
client = OpenAIClientWrapper(model="gpt-4o-mini")

# More capable
client = OpenAIClientWrapper(model="gpt-4")

# Fast & Cheaper
client = OpenAIClientWrapper(model="gpt-3.5-turbo")

# Change on the fly
client.set_model("gpt-4")
```

## Cost Tips

1. Use `max_tokens` to limit response length
2. Use lower `temperature` when possible (more deterministic = fewer retries)
3. Use `gpt-4o-mini` for most tasks (cheapest)
4. Monitor token usage in OpenAI dashboard

## Next Steps

1. Set `OPENAI_API_KEY` environment variable
2. Run `python test_openai_client.py` to verify
3. Check `integration_examples.py` for patterns
4. Use `generate_response()` in your code

## Additional Resources

- **Full Docs**: `OPENAI_CLIENT_README.md`
- **Implementation**: `IMPLEMENTATION_SUMMARY.md`
- **Examples**: `integration_examples.py`
- **Tests**: `test_openai_client.py`
- **OpenAI Docs**: https://platform.openai.com/docs

---

**Made with ❤️ for the Autonomous Content Factory**
