# Research Agent

A Python AI agent that analyzes raw text input to extract structured product information using OpenAI's API.

## Features

The `ResearchAgent` extracts and structures the following information from product descriptions:

- **Product Name**: Identifies the product name or title
- **Key Features**: Extracts main features and capabilities
- **Technical Specs**: Captures technical specifications and metrics
- **Target Audience**: Identifies the intended audience/customer segments
- **Value Proposition**: Determines the core value and main benefits
- **Ambiguous Statements**: Flags vague, unclear, or unsubstantiated claims

## Installation

Ensure the required dependencies are installed:

```bash
pip install -r ../requirements.txt
```

Required packages:
- `openai>=2.0.0`
- `python-dotenv`

## Configuration

Set up your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or create a `.env` file in the backend directory:

```
OPENAI_API_KEY=your-api-key-here
```

## Usage

### Basic Usage

```python
from research_agent import ResearchAgent

# Initialize the agent
agent = ResearchAgent()

# Analyze a product description
raw_text = """
The CloudVault Pro is a cloud storage solution offering unlimited storage 
with military-grade encryption. Supports real-time team collaboration for 
up to 1000 members and integrates with popular tools.
"""

result = agent.analyze(raw_text)
print(agent.to_json(result))
```

### Batch Analysis

```python
texts = [
    "Product description 1...",
    "Product description 2...",
    "Product description 3..."
]

results = agent.analyze_batch(texts)
for result in results:
    print(result)
```

### API Response Structure

```json
{
  "status": "success",
  "timestamp": "2026-04-09T10:30:45.123456",
  "raw_input_length": 450,
  "analysis": {
    "product_name": "CloudVault Pro",
    "key_features": [
      "Unlimited storage capacity",
      "Military-grade encryption",
      "Real-time team collaboration",
      "Tool integrations"
    ],
    "technical_specs": {
      "storage_capacity": "Unlimited",
      "encryption": "Military-grade",
      "max_team_members": 1000,
      "integrations": "50+"
    },
    "target_audience": "Enterprise businesses and large teams",
    "value_proposition": "Secure, collaborative cloud storage for enterprises",
    "ambiguous_statements": [
      "AI-powered automatic file organization - no details provided",
      "Unprecedented insights - vague marketing claim",
      "Transform digital infrastructure - unclear benefit"
    ]
  }
}
```

### Error Handling

```python
from research_agent import ResearchAgent

try:
    agent = ResearchAgent()
    result = agent.analyze("")  # Empty input
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Error: {e}")
```

## Testing

Run the test script to verify the agent works correctly:

```bash
cd backend/agents
python test_research_agent.py
```

## Advanced Options

### Using a Different Model

```python
# Use GPT-3.5 Turbo instead of GPT-4
agent = ResearchAgent(model="gpt-3.5-turbo")
```

### Custom API Key

```python
agent = ResearchAgent(api_key="your-custom-api-key")
```

## Architecture

The `ResearchAgent` class includes:

- **`__init__`**: Initialize with OpenAI client and model selection
- **`analyze`**: Main method to analyze a single product description
- **`analyze_batch`**: Process multiple descriptions sequentially
- **`to_json`**: Format results as pretty-printed JSON
- **`_build_extraction_prompt`**: Create the extraction prompt for OpenAI
- **`_format_result`**: Format and validate extracted data

## Error Handling

The agent handles various error scenarios:

- Missing or invalid API key
- Empty input text
- JSON parsing errors
- OpenAI API errors
- Batch processing errors (returns error for individual items)

## Performance Notes

- API calls are made sequentially for batch processing
- Response time depends on OpenAI API availability
- Temperature is set to 0.3 for consistent, focused extraction
- Recommended for products with descriptions of 50-5000 characters

## Requirements

- Python 3.8+
- OpenAI API key with access to GPT-4 or GPT-3.5-turbo
- Active internet connection for API calls

## License

Part of the Autonomous Content Factory project.
