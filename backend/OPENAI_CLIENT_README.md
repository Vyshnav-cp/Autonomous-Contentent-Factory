# OpenAI Client Wrapper

A reusable, lightweight wrapper around the OpenAI API for generating text responses. Provides a simple interface for consistent API usage across the application.

## Features

- **Simple API**: Single `generate_response()` function for basic usage
- **Flexible**: Class-based interface for advanced customization
- **Context Support**: Add system prompts for specialized behavior
- **Error Handling**: Comprehensive error handling with clear messages
- **Model Switching**: Easily switch between different OpenAI models
- **Global Instance**: Convenient default client instance for quick usage

## Installation

Ensure dependencies are installed:

```bash
pip install -r requirements.txt
```

Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Quick Start

### Basic Usage (Convenience Function)

```python
from openai_client import generate_response

response = generate_response("What is machine learning?")
print(response)
```

### Using the Class

```python
from openai_client import OpenAIClientWrapper

client = OpenAIClientWrapper()
response = client.generate_response(
    prompt="Explain quantum computing",
    temperature=0.5,
    max_tokens=200
)
print(response)
```

## API Reference

### `generate_response()` Function

The main convenience function for generating responses.

**Signature:**
```python
def generate_response(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    system_prompt: Optional[str] = None,
) -> str:
```

**Parameters:**
- `prompt` (str): The user message/question to send to the model
- `temperature` (float, default=0.7): Controls randomness
  - 0.0 = deterministic, focused responses
  - 1.0 = balanced randomness
  - 2.0 = maximum randomness
- `max_tokens` (int, optional): Maximum length of the response
- `system_prompt` (str, optional): System message to set context/behavior

**Returns:**
- `str`: The generated text response

**Examples:**

```python
# Simple question
response = generate_response("What is Python?")

# Controlled output
response = generate_response(
    prompt="List 3 benefits of AI",
    temperature=0.3,
    max_tokens=100
)

# With system prompt
response = generate_response(
    prompt="How do I learn programming?",
    system_prompt="You are an experienced software engineer. Give practical advice.",
    temperature=0.6
)
```

### `OpenAIClientWrapper` Class

For advanced usage and customization.

**Constructor:**
```python
client = OpenAIClientWrapper(
    api_key: Optional[str] = None,
    model: str = "gpt-4o-mini"
)
```

**Methods:**

#### `generate_response()`
Generate a response from the API.

```python
response = client.generate_response(
    prompt="Your question here",
    temperature=0.7,
    max_tokens=None,
    system_prompt=None
)
```

#### `generate_response_with_context()`
Generate a response with additional context.

```python
response = client.generate_response_with_context(
    prompt="How does photosynthesis work?",
    context="The user is a high school biology student",
    temperature=0.6,
    max_tokens=300
)
```

#### `set_model()` / `get_model()`
Switch or check the current model.

```python
client.set_model("gpt-4")
print(client.get_model())  # Output: gpt-4
```

### `get_default_client()` Function

Get the default global client instance.

```python
from openai_client import get_default_client

client = get_default_client()
response = client.generate_response("Hello!")
```

## Usage Examples

### Example 1: Product Description Analysis

```python
from openai_client import generate_response

product = "CloudVault Pro - unlimited cloud storage with encryption"

response = generate_response(
    prompt=f"Extract key features from this product: {product}",
    temperature=0.3,
    system_prompt="You are a product analyst. Extract features as a numbered list."
)
print(response)
```

### Example 2: Content Generation with Temperature Control

```python
from openai_client import OpenAIClientWrapper

client = OpenAIClientWrapper()

# Deterministic (focused) response
focused = client.generate_response(
    prompt="Write a product tagline",
    temperature=0.2,
    max_tokens=50
)

# Creative response
creative = client.generate_response(
    prompt="Write a product tagline",
    temperature=1.5,
    max_tokens=50
)
```

### Example 3: Context-Aware Responses

```python
from openai_client import generate_response

context = """
You are an expert technical writer. 
Always explain complex concepts clearly and concisely.
Use examples when helpful.
"""

response = generate_response(
    prompt="What is REST API?",
    system_prompt=context,
    temperature=0.5,
    max_tokens=300
)
```

## Error Handling

The wrapper includes comprehensive error handling:

```python
from openai_client import generate_response

try:
    response = generate_response("")  # Empty prompt
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"API error: {e}")
```

**Common Errors:**
- `ValueError`: Empty prompt or invalid input
- `ValueError`: Missing API key
- `Exception`: OpenAI API errors (rate limits, quota exceeded, etc.)

## Configuration

### Environment Variables

```bash
# Required
export OPENAI_API_KEY="sk-..."

# Optional - set default model
export OPENAI_MODEL="gpt-4o-mini"
```

### Programmatic Configuration

```python
# Use specific API key
client = OpenAIClientWrapper(api_key="sk-custom-key")

# Use specific model
client = OpenAIClientWrapper(model="gpt-4")

# Switch model later
client.set_model("gpt-3.5-turbo")
```

## Temperature Guide

| Temperature | Use Case | Output |
|-------------|----------|--------|
| 0.0 | Deterministic tasks | Single, consistent answer |
| 0.3 | Analysis, extraction | Focused, logical |
| 0.7 | Balanced (default) | Good balance |
| 1.0 | Creative writing | More varied |
| 1.5+ | Brainstorming | Very creative |

## Testing

Run the test suite:

```bash
python test_openai_client.py
```

Tests include:
- Basic response generation
- Class instantiation
- System prompt handling
- Model switching
- Error handling

## Integration with ResearchAgent

The OpenAI client wrapper is used by the `ResearchAgent`:

```python
from agents.research_agent import ResearchAgent

agent = ResearchAgent()
result = agent.analyze("Product description here...")
```

## Model Support

Currently configured for:
- `gpt-4o-mini` (default - fast and economical)
- `gpt-4` (more capable)
- `gpt-4-turbo` (higher quality)
- `gpt-3.5-turbo` (faster, cheaper)

## Performance Notes

- **Response time**: 0.5-5 seconds typically
- **Cost**: Varies by model (check OpenAI pricing)
- **Rate limits**: Respect OpenAI's rate limits
- **Timeout**: Default 600 seconds

## Troubleshooting

### "API key not provided"
```bash
# Set the environment variable
export OPENAI_API_KEY="your-key"
```

### "Empty prompt"
Ensure your prompt is not empty:
```python
prompt = user_input.strip()
if not prompt:
    print("Prompt cannot be empty")
```

### "Rate limit exceeded"
Add exponential backoff:
```python
import time
try:
    response = generate_response(prompt)
except Exception as e:
    if "rate" in str(e).lower():
        time.sleep(5)
        response = generate_response(prompt)
```

## License

Part of the Autonomous Content Factory project.
