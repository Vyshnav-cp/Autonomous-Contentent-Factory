# ResearchAgent Quick Reference

## What It Does

Analyzes product descriptions and extracts structured information into JSON.

## 8 Key Responsibilities

| # | Responsibility | Output Field | Type |
|---|---|---|---|
| 1 | Analyze source document | `raw_input_length` | int |
| 2 | Extract product name | `analysis.product_name` | string |
| 3 | Extract key features | `analysis.key_features` | array |
| 4 | Extract technical specs | `analysis.technical_specs` | object |
| 5 | Extract target audience | `analysis.target_audience` | string |
| 6 | Extract value proposition | `analysis.value_proposition` | string |
| 7 | Identify ambiguous statements | `analysis.ambiguous_statements` | array |
| 8 | Return structured JSON | Full result | JSON |

## Quick Start

### Setup
```bash
# Set API key
export OPENAI_API_KEY="your-key-here"

# Navigate to agents directory
cd backend/agents
```

### Single Analysis
```python
from research_agent import ResearchAgent

agent = ResearchAgent()
result = agent.analyze("Your product description here...")
print(agent.to_json(result))
```

### Batch Analysis
```python
texts = [
    "Product 1 description...",
    "Product 2 description...",
    "Product 3 description..."
]
results = agent.analyze_batch(texts)
```

### Validation
```python
# Run comprehensive test
python validate_research_agent.py

# Run basic test
python test_research_agent.py
```

## Output Structure

```json
{
  "status": "success",
  "timestamp": "2026-04-09T10:30:45.123456",
  "raw_input_length": 450,
  "analysis": {
    "product_name": "CloudVault Pro",
    "key_features": [
      "Feature 1",
      "Feature 2",
      "Feature 3"
    ],
    "technical_specs": {
      "spec_key": "value"
    },
    "target_audience": "Enterprises and teams",
    "value_proposition": "Core benefits and value",
    "ambiguous_statements": [
      "Vague claim 1",
      "Unsubstantiated claim 2"
    ]
  }
}
```

## Configuration Options

```python
# Use different model
agent = ResearchAgent(model="gpt-3.5-turbo")

# Provide API key directly
agent = ResearchAgent(api_key="sk-...")

# Both together
agent = ResearchAgent(
    api_key="sk-...",
    model="gpt-4"
)
```

## Common Patterns

### Extract Features Only
```python
result = agent.analyze(text)
features = result['analysis']['key_features']
```

### Get JSON String
```python
json_string = agent.to_json(result)
```

### Handle Errors
```python
try:
    result = agent.analyze(text)
except ValueError as e:
    print(f"Input error: {e}")
except Exception as e:
    print(f"Processing error: {e}")
```

### Batch with Error Handling
```python
results = agent.analyze_batch(texts)
for result in results:
    if result['status'] == 'error':
        print(f"Error at index {result['index']}: {result['error']}")
    else:
        print(f"Product: {result['analysis']['product_name']}")
```

## Key Parameters

| Parameter | Default | Options |
|-----------|---------|---------|
| `model` | `gpt-4` | `gpt-4`, `gpt-3.5-turbo` |
| `api_key` | `OPENAI_API_KEY` env var | Any valid OpenAI key |
| `temperature` | `0.3` | (internal, not changeable) |
| `response_format` | `json_object` | (internal, always JSON) |

## Field Explanations

### product_name
- Explicit name from document
- Inferred from context
- "Unknown" if not found

### key_features
- Array of 3-10 main features
- Ranked by importance
- Clear, concise descriptions

### technical_specs
- Dictionary of metrics and measurements
- Examples: capacity, speed, users, integrations
- Numeric values with units

### target_audience
- Who the product is for
- Business type and size
- Use case/industry

### value_proposition
- Core problem solved
- Main customer benefit
- Why customers should care

### ambiguous_statements
- Vague marketing claims
- Unsupported assertions
- Undefined metrics or terms

## Performance Notes

- Single analysis: 1-3 seconds
- Batch processing: Sequential
- Temperature: 0.3 (consistent results)
- Supports documents: 50-5000 characters

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API key error | Set `OPENAI_API_KEY` environment variable |
| Empty input error | Provide non-empty text |
| JSON parse error | Retry or check OpenAI API status |
| Timeout | Check network and API status |

## Files

| File | Purpose |
|------|---------|
| `research_agent.py` | Main implementation |
| `test_research_agent.py` | Basic tests |
| `validate_research_agent.py` | Comprehensive validation |
| `RESEARCH_AGENT_SPECS.md` | Detailed specifications |
| `README.md` | Full documentation |

## Next Steps

1. Set up OpenAI API key
2. Import `ResearchAgent`
3. Create agent instance
4. Call `analyze()` with text
5. Process results

See `RESEARCH_AGENT_SPECS.md` for detailed documentation.
