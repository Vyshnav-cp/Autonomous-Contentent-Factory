# CopywriterAgent

An AI-powered agent that generates professional marketing content from product factsheets. Creates diverse, value-focused content across multiple formats.

## Features

The `CopywriterAgent` generates three types of marketing content:

### 1. **Blog Post** (500 words, professional tone)
- Compelling introduction with value proposition hook
- Detailed feature explanations with use cases
- Target audience alignment
- Professional, authoritative tone
- Clear call-to-action

### 2. **Tweet Thread** (5 tweets, engaging tone)
- Hook with problem statement or surprising fact
- Value proposition emphasis
- Feature highlights with benefits
- Direct call-to-action
- Strategic emoji usage
- Under 280 characters per tweet

### 3. **Email Teaser** (1 paragraph, persuasive)
- Curiosity-driven copy
- Emphasized value proposition
- Benefit-focused messaging
- Direct audience address
- Implied call-to-action

All content formats consistently highlight the product's value proposition.

## Installation

Ensure dependencies are installed:

```bash
pip install -r ../requirements.txt
```

Required packages:
- `openai>=2.0.0`
- `python-dotenv`

## Configuration

Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or create a `.env` file:

```
OPENAI_API_KEY=your-api-key-here
```

## Usage

### Basic Usage

```python
from copywriter_agent import CopywriterAgent

# Initialize the agent
agent = CopywriterAgent()

# Prepare factsheet
factsheet = {
    "product_name": "CloudVault Pro",
    "key_features": [
        "Unlimited cloud storage",
        "Military-grade encryption",
        "Real-time team collaboration",
        "AI-powered file organization",
        "Advanced analytics"
    ],
    "technical_specs": {
        "storage": "Unlimited",
        "encryption": "AES-256",
        "team_members": "Up to 1000",
        "integrations": "50+",
        "uptime_sla": "99.99%"
    },
    "target_audience": "Enterprise teams seeking secure cloud storage",
    "value_proposition": "Secure, scalable cloud storage enabling seamless collaboration"
}

# Generate content
result = agent.generate_content(factsheet)

# Access individual content pieces
blog = result["content"]["blog_post"]
tweets = result["content"]["tweet_thread"]
email = result["content"]["email_teaser"]
```

### Batch Generation

```python
factsheets = [factsheet1, factsheet2, factsheet3]
results = agent.generate_batch(factsheets)

for result in results:
    if result["status"] == "success":
        print(f"Generated content for {result['product_name']}")
    else:
        print(f"Error: {result['error']}")
```

### Output Structure

```json
{
  "status": "success",
  "timestamp": "2026-04-09T10:30:45.123456",
  "product_name": "CloudVault Pro",
  "content": {
    "blog_post": "Compelling 500-word blog post...",
    "tweet_thread": [
      "1/ Hook tweet with problem statement",
      "2/ Value proposition tweet",
      "3/ Features and benefits tweet",
      "4/ Audience alignment tweet",
      "5/ Call-to-action tweet"
    ],
    "email_teaser": "Compelling one-paragraph email teaser..."
  },
  "metadata": {
    "model_used": "gpt-4o-mini",
    "blog_word_count": 487,
    "tweet_count": 5,
    "value_proposition": "Secure, scalable cloud storage enabling seamless collaboration"
  }
}
```

## Factsheet Format

Required fields for the input factsheet:

| Field | Type | Description |
|-------|------|-------------|
| `product_name` | string | Name of the product (required) |
| `key_features` | array | List of main features (required) |
| `target_audience` | string | Description of intended audience (required) |
| `value_proposition` | string | Core value offered to customers (required) |
| `technical_specs` | object | Optional technical specifications |
| `ambiguous_statements` | array | Optional statements to avoid in marketing |

### Example Factsheet

```python
factsheet = {
    "product_name": "TaskMaster 360",
    "key_features": [
        "Intelligent task prioritization",
        "Real-time team communication",
        "Gantt charts and timelines",
        "Automated workflows",
        "Performance analytics"
    ],
    "technical_specs": {
        "projects": "Unlimited",
        "team_size": "1-10,000 members",
        "integrations": "Slack, GitHub, Jira",
        "api_rate": "10,000 req/hour"
    },
    "target_audience": "Project managers and development teams",
    "value_proposition": "Deliver projects on time with intelligent automation"
}
```

## API Reference

### Methods

#### `generate_content(factsheet: Dict) -> Dict`

Generate all marketing content from a factsheet.

**Parameters:**
- `factsheet`: Dictionary with product information

**Returns:**
- Dictionary with generated blog, tweets, email teaser, and metadata

**Raises:**
- `ValueError`: If factsheet is missing required fields
- `Exception`: If OpenAI API call fails

#### `generate_batch(factsheets: List) -> List`

Generate content for multiple factsheets.

**Parameters:**
- `factsheets`: List of factsheet dictionaries

**Returns:**
- List of results (includes error status for failed items)

#### `to_json(result: Dict) -> str`

Convert result to formatted JSON.

**Parameters:**
- `result`: Generation result dictionary

**Returns:**
- Pretty-printed JSON string

### Internal Methods

- `_validate_factsheet()`: Validates factsheet structure
- `_generate_blog_post()`: Generates professional blog content
- `_generate_tweet_thread()`: Generates 5-tweet thread
- `_generate_email_teaser()`: Generates email copy
- `_build_blog_prompt()`: Constructs blog generation prompt
- `_build_tweet_prompt()`: Constructs tweet generation prompt
- `_build_email_prompt()`: Constructs email generation prompt
- `_parse_tweets()`: Extracts tweets from API response

## Configuration Options

### Model Selection

```python
# Use GPT-4o Mini (cost-effective, fast)
agent = CopywriterAgent(model="gpt-4o-mini")

# Use GPT-4 (more capable)
agent = CopywriterAgent(model="gpt-4")
```

### Custom API Key

```python
agent = CopywriterAgent(api_key="sk-...")
```

## Content Quality Guidelines

The agent uses specific prompts and temperature settings for each content type:

| Content Type | Temperature | Max Tokens | Tone |
|--------------|-------------|-----------|------|
| Blog Post | 0.7 | 1000 | Professional |
| Tweet Thread | 0.8 | 800 | Engaging |
| Email Teaser | 0.7 | 300 | Persuasive |

## Error Handling

```python
try:
    result = agent.generate_content(factsheet)
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Generation error: {e}")
```

Common errors:

- **Missing required fields**: Ensure all required factsheet fields are present
- **Invalid feature type**: `key_features` must be a list
- **Empty values**: product_name and value_proposition cannot be empty
- **API errors**: Check API key and OpenAI service status

## Testing

Run the test suite:

```bash
cd backend/agents
python test_copywriter_agent.py
```

Tests cover:
- Multi-product generation
- Content validation
- Input validation
- Error handling
- Batch processing

## Best Practices

1. **Clear Value Proposition**: Ensure the value proposition is specific and measurable
2. **Feature Relevance**: Include features most relevant to target audience
3. **Technical Accuracy**: Verify technical specs for accuracy
4. **Consistent Messaging**: The same value proposition flows through all content
5. **Audience Understanding**: Target audience description should be detailed

## Performance Notes

- **API Latency**: Each factsheet generation requires 3 API calls (blog, tweets, email)
- **Cost**: Uses gpt-4o-mini by default for cost-efficiency
- **Batch Processing**: Sequential processing for reliability
- **Token Usage**: ~1000 tokens per factsheet on average

## Limitations

- Tweet parsing may vary based on API response format
- Blog word count is approximate (actual: 400-600 words)
- Batch processing is sequential (not parallel)
- Requires active internet connection for API calls

## Integration Examples

### With ResearchAgent

```python
from research_agent import ResearchAgent
from copywriter_agent import CopywriterAgent

# First, extract product information
researcher = ResearchAgent()
raw_text = "Product description here..."
research_result = researcher.analyze(raw_text)

# Convert research to factsheet format
factsheet = {
    "product_name": research_result["analysis"]["product_name"],
    "key_features": research_result["analysis"]["key_features"],
    "technical_specs": research_result["analysis"]["technical_specs"],
    "target_audience": research_result["analysis"]["target_audience"],
    "value_proposition": research_result["analysis"]["value_proposition"]
}

# Generate marketing content
copywriter = CopywriterAgent()
content = copywriter.generate_content(factsheet)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Import error | Install openai: `pip install openai` |
| API key error | Set OPENAI_API_KEY environment variable |
| Empty tweets | Ensure target_audience is descriptive |
| Low-quality content | Improve value_proposition specificity |
| Slow generation | Normal for 3 API calls; consider batch for multiple |

## Requirements

- Python 3.8+
- OpenAI API key with gpt-4o-mini access
- Active internet connection
- ~1-3 seconds per factsheet

## Version History

- **v0.2.0**: Initial CopywriterAgent release
  - Blog post generation (500 words)
  - Tweet thread generation (5 tweets)
  - Email teaser generation
  - Batch processing support
  - Comprehensive validation

## License

Part of the Autonomous Content Factory project.
