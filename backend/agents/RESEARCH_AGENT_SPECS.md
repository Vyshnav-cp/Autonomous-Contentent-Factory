# ResearchAgent Specifications

## Overview

The `ResearchAgent` class is a sophisticated AI-powered agent designed to analyze source documents and extract structured product information. It leverages OpenAI's API to intelligently parse and categorize product details into a standardized JSON format.

## Responsibilities

### 1. **Analyze Source Document** ✓
- Accepts raw text input of any length
- Validates input is non-empty
- Tracks input metadata (length, timestamp)
- Returns input length in response

### 2. **Extract Product Name** ✓
- Identifies explicit product name/title
- Infers product name from context if not directly stated
- Returns "Unknown" if name cannot be determined
- Field: `analysis.product_name`

### 3. **Extract Key Features** ✓
- Identifies and lists main features and capabilities
- Returns as array of strings
- Captures the most important characteristics
- Prioritizes features by relevance
- Field: `analysis.key_features`

### 4. **Extract Technical Specs** ✓
- Captures technical specifications and metrics
- Returns as structured object/dictionary
- Includes measurements, dimensions, performance metrics
- Examples: storage capacity, response time, user limits, compatibility
- Field: `analysis.technical_specs`

### 5. **Extract Target Audience** ✓
- Identifies intended customer segments
- Describes demographics and use cases
- Captures business context (SMB, Enterprise, etc.)
- Field: `analysis.target_audience`

### 6. **Extract Value Proposition** ✓
- Determines core value and main benefits
- Identifies problems solved or needs fulfilled
- Distinguishes benefits from features
- Field: `analysis.value_proposition`

### 7. **Identify Ambiguous Statements** ✓
- Flags unclear, vague, or unsubstantiated claims
- Identifies marketing hype without backing evidence
- Highlights undefined terms or metrics
- Returns as array of strings
- Field: `analysis.ambiguous_statements`

### 8. **Return Structured JSON** ✓
- Formats all extracted data as valid JSON
- Includes metadata (status, timestamp)
- Provides consistent schema
- Serializable to string via `to_json()` method

## Output Schema

```json
{
  "status": "success|error",
  "timestamp": "ISO-8601 timestamp",
  "raw_input_length": 1234,
  "analysis": {
    "product_name": "Product Name",
    "key_features": [
      "Feature 1",
      "Feature 2",
      "Feature 3"
    ],
    "technical_specs": {
      "spec_key_1": "value",
      "spec_key_2": "value"
    },
    "target_audience": "Description of target audience",
    "value_proposition": "Core value and benefits",
    "ambiguous_statements": [
      "Vague claim 1",
      "Unsubstantiated claim 2"
    ]
  }
}
```

## Usage

### Basic Analysis
```python
from research_agent import ResearchAgent

agent = ResearchAgent()
result = agent.analyze("Product description text...")
print(agent.to_json(result))
```

### Batch Processing
```python
texts = ["Product 1...", "Product 2...", "Product 3..."]
results = agent.analyze_batch(texts)
```

### Error Handling
```python
try:
    result = agent.analyze("")  # Empty input raises ValueError
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Processing error: {e}")
```

## Configuration

### Model Selection
- Default: `gpt-4` (better quality extraction)
- Alternative: `gpt-3.5-turbo` (faster, cost-effective)

```python
agent = ResearchAgent(model="gpt-3.5-turbo")
```

### API Key
```python
# Via environment variable
export OPENAI_API_KEY="your-key"

# Via constructor
agent = ResearchAgent(api_key="your-key")
```

## Extraction Quality

### Temperature Setting
- Temperature: 0.3 (low)
- Effect: Consistent, focused extraction
- Minimizes creative interpretation
- Ideal for structured data extraction

### Response Format
- Uses OpenAI's `json_object` response format
- Ensures valid JSON output
- Eliminates parsing ambiguity

### Extraction Confidence
- System prompt: "Expert product analyst"
- Detailed field descriptions
- Clear instructions for ambiguous cases
- Validation and error handling

## Performance

### Latency
- Single document: 1-3 seconds (API dependent)
- Batch processing: Sequential (linear time)
- Network latency dominates processing time

### Token Usage
- Average document: 500-2000 tokens
- Response: 200-500 tokens
- Cost-effective at scale

### Recommended Constraints
- Input size: 50-5000 characters
- Batch size: 1-100 documents
- Concurrent requests: Sequential recommended

## Error Handling

| Error | Cause | Resolution |
|-------|-------|-----------|
| `ValueError: Input text cannot be empty` | Empty or whitespace-only input | Provide non-empty document |
| `ValueError: OpenAI API key not provided` | Missing API key | Set OPENAI_API_KEY env var |
| `ValueError: Failed to parse API response as JSON` | Invalid JSON from API | Retry or check API status |
| `Exception: Error during API call` | Network or API error | Check connectivity and API status |

## Validation

### Input Validation
- Non-empty text required
- Whitespace-only rejected
- No size limits enforced (but API has token limits)

### Output Validation
- JSON parsing validation
- Schema consistency check
- Metadata completeness

## Testing

### Test Suite
- `test_research_agent.py`: Basic functionality
- `validate_research_agent.py`: Comprehensive validation

### Test Coverage
- Single document analysis
- Batch processing
- Error handling
- Output validation
- All 8 responsibilities

## Dependencies

- `openai>=2.0.0`: OpenAI API client
- `python-dotenv`: Environment variable management
- Python standard library: `json`, `datetime`, `typing`

## Integration

### With FastAPI
```python
from fastapi import FastAPI
from research_agent import ResearchAgent

app = FastAPI()
agent = ResearchAgent()

@app.post("/analyze")
async def analyze_product(text: str):
    result = agent.analyze(text)
    return result
```

### With Other Modules
```python
from agents import ResearchAgent

# Import from package
agent = ResearchAgent()
```

## Future Enhancements

- Async API support for parallel processing
- Streaming responses for large documents
- Custom extraction templates
- Multi-language support
- Advanced NLP validation
- Confidence scoring per extraction

## Compliance

- Respects OpenAI API terms of service
- No PII extraction without consent
- Rate limiting based on API quotas
- Audit trail via timestamps

## Support

For issues or questions:
1. Check API key configuration
2. Verify OpenAI account status
3. Review error messages
4. Consult test examples
5. Check documentation
