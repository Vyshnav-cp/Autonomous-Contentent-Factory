# Autonomous Content Factory - Agents Overview

Complete guide to all available AI agents in the Autonomous Content Factory.

## Quick Reference

| Agent | Input | Output | Purpose |
|-------|-------|--------|---------|
| **ResearchAgent** | Raw product text | Structured factsheet JSON | Extract product information |
| **CopywriterAgent** | Factsheet JSON | Marketing content (blog, tweets, email) | Generate diverse marketing content |

## Architecture

```
Raw Product Text
       ↓
   ResearchAgent
   (Analysis Phase)
       ↓
  Factsheet JSON
  (Structured Data)
       ↓
 CopywriterAgent
 (Generation Phase)
       ↓
Marketing Content
 (Blog, Tweets, Email)
```

## ResearchAgent

**Purpose**: Extract structured product information from unstructured text.

**Input**: Raw product description text

**Output**: Structured JSON with:
- Product name
- Key features (list)
- Technical specifications (object)
- Target audience (description)
- Value proposition (string)
- Ambiguous statements (flagged claims)

### Quick Start

```python
from research_agent import ResearchAgent

agent = ResearchAgent()
result = agent.analyze("Product description here...")
print(agent.to_json(result))
```

### Key Features

- ✅ Intelligent extraction of product information
- ✅ Flagging of ambiguous marketing claims
- ✅ Batch processing support
- ✅ Comprehensive validation
- ✅ JSON output with metadata

### Configuration

```python
# Default model: gpt-4
agent = ResearchAgent(model="gpt-4")

# With custom API key
agent = ResearchAgent(api_key="sk-...")
```

[📖 Full ResearchAgent Documentation →](README.md)

---

## CopywriterAgent

**Purpose**: Generate professional marketing content from product factsheets.

**Input**: Structured factsheet JSON

**Output**: Marketing content in three formats:
1. **Blog Post** (500 words, professional tone)
2. **Tweet Thread** (5 tweets, engaging tone)
3. **Email Teaser** (1 paragraph, persuasive)

### Quick Start

```python
from copywriter_agent import CopywriterAgent

agent = CopywriterAgent()
factsheet = {
    "product_name": "CloudVault Pro",
    "key_features": ["Storage", "Encryption", "Collaboration"],
    "technical_specs": {"storage": "Unlimited"},
    "target_audience": "Enterprise teams",
    "value_proposition": "Secure cloud storage for teams"
}
result = agent.generate_content(factsheet)
```

### Key Features

- ✅ Professional blog post generation (500 words)
- ✅ Engaging tweet thread (5 tweets, <280 chars each)
- ✅ Persuasive email teaser (1 paragraph)
- ✅ Consistent value proposition messaging
- ✅ Batch processing support
- ✅ Model flexibility (GPT-4o-mini by default)

### Configuration

```python
# Default model: gpt-4o-mini (cost-effective)
agent = CopywriterAgent(model="gpt-4o-mini")

# With custom API key
agent = CopywriterAgent(api_key="sk-...")
```

[📖 Full CopywriterAgent Documentation →](COPYWRITER_README.md)

---

## Complete Workflow Example

### Research → Copywriting Pipeline

```python
from research_agent import ResearchAgent
from copywriter_agent import CopywriterAgent

# Step 1: Extract product info from raw text
researcher = ResearchAgent()
raw_text = "CloudVault Pro is a secure cloud storage solution..."
research = researcher.analyze(raw_text)

# Step 2: Create factsheet from analysis
factsheet = {
    "product_name": research["analysis"]["product_name"],
    "key_features": research["analysis"]["key_features"],
    "technical_specs": research["analysis"]["technical_specs"],
    "target_audience": research["analysis"]["target_audience"],
    "value_proposition": research["analysis"]["value_proposition"]
}

# Step 3: Generate marketing content
copywriter = CopywriterAgent()
content = copywriter.generate_content(factsheet)

# Step 4: Access generated content
blog = content["content"]["blog_post"]
tweets = content["content"]["tweet_thread"]
email = content["content"]["email_teaser"]
```

[🔗 See Full Integration Example →](integration_example.py)

---

## Common Tasks

### Extract Product Information

```python
from research_agent import ResearchAgent

agent = ResearchAgent()
result = agent.analyze(product_text)

# Access extracted data
product_name = result["analysis"]["product_name"]
features = result["analysis"]["key_features"]
value_prop = result["analysis"]["value_proposition"]
```

### Generate Blog Post

```python
from copywriter_agent import CopywriterAgent

agent = CopywriterAgent()
factsheet = {...}
result = agent.generate_content(factsheet)

blog_post = result["content"]["blog_post"]
```

### Generate Tweet Thread

```python
result = agent.generate_content(factsheet)

tweets = result["content"]["tweet_thread"]
# tweets is a list of 5 tweets, each under 280 chars
for i, tweet in enumerate(tweets, 1):
    print(f"{i}/ {tweet}")
```

### Generate Email Teaser

```python
result = agent.generate_content(factsheet)

email_teaser = result["content"]["email_teaser"]
```

### Batch Processing

#### Research Multiple Products

```python
texts = ["Product 1...", "Product 2...", "Product 3..."]
results = agent.analyze_batch(texts)

for result in results:
    if result["status"] == "success":
        print(result["analysis"]["product_name"])
```

#### Generate Content for Multiple Products

```python
factsheets = [factsheet1, factsheet2, factsheet3]
results = agent.generate_batch(factsheets)

for result in results:
    if result["status"] == "success":
        print(f"Generated: {result['product_name']}")
```

---

## Data Formats

### ResearchAgent Output

```json
{
  "status": "success",
  "timestamp": "2026-04-09T10:30:45.123456",
  "raw_input_length": 450,
  "analysis": {
    "product_name": "CloudVault Pro",
    "key_features": ["Unlimited storage", "Encryption"],
    "technical_specs": {"storage": "Unlimited"},
    "target_audience": "Enterprise teams",
    "value_proposition": "Secure cloud storage",
    "ambiguous_statements": ["AI-powered - vague"]
  }
}
```

### CopywriterAgent Output

```json
{
  "status": "success",
  "timestamp": "2026-04-09T10:30:45.123456",
  "product_name": "CloudVault Pro",
  "content": {
    "blog_post": "Compelling 500-word blog post...",
    "tweet_thread": ["1/ Hook...", "2/ Value...", "3/ Features...", "4/ Audience...", "5/ CTA..."],
    "email_teaser": "Compelling paragraph..."
  },
  "metadata": {
    "model_used": "gpt-4o-mini",
    "blog_word_count": 487,
    "tweet_count": 5,
    "value_proposition": "Secure cloud storage"
  }
}
```

### Factsheet Format

```json
{
  "product_name": "CloudVault Pro",
  "key_features": [
    "Unlimited cloud storage",
    "Military-grade encryption",
    "Real-time collaboration"
  ],
  "technical_specs": {
    "storage": "Unlimited",
    "encryption": "AES-256",
    "team_members": "Up to 1000"
  },
  "target_audience": "Enterprise teams seeking secure cloud storage",
  "value_proposition": "Secure, scalable cloud storage enabling seamless collaboration"
}
```

---

## Configuration & Setup

### Environment Setup

```bash
# 1. Set OpenAI API key
export OPENAI_API_KEY="sk-your-key-here"

# 2. Install dependencies (if not already installed)
pip install -r requirements.txt

# 3. Verify installation
python -c "from research_agent import ResearchAgent; print('✓ Ready')"
```

### Alternative: Using .env File

```bash
# Create backend/.env
echo "OPENAI_API_KEY=sk-your-key-here" > ../.env
```

### Model Selection

| Agent | Recommended Model | Alternative |
|-------|-------------------|-------------|
| ResearchAgent | gpt-4 | gpt-4-turbo |
| CopywriterAgent | gpt-4o-mini | gpt-4-turbo |

---

## Performance & Costs

### ResearchAgent Performance

- **Latency**: 2-5 seconds per analysis
- **Tokens**: ~300-500 tokens per factsheet
- **Cost**: ~$0.01-0.02 per analysis (with gpt-4)

### CopywriterAgent Performance

- **Latency**: 5-10 seconds per factsheet (3 API calls)
- **Tokens**: ~1000-1500 tokens per factsheet
- **Cost**: ~$0.05-0.10 per factsheet (with gpt-4o-mini)

### Optimization Tips

1. **Use gpt-4o-mini** for CopywriterAgent (faster, cheaper)
2. **Batch processing** for multiple items
3. **Cache factsheets** to avoid re-analysis
4. **Use smaller models** if latency is critical

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `API key not provided` | Missing API key | Set `OPENAI_API_KEY` env var |
| `Validation error` | Missing required fields | Check factsheet structure |
| `Input text cannot be empty` | Empty input | Provide non-empty text |
| `Failed to parse JSON` | API response error | Retry or check API status |

### Error Handling Pattern

```python
try:
    result = agent.analyze(text)
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"API error: {e}")
```

---

## Testing

### Run ResearchAgent Tests

```bash
cd backend/agents
python test_research_agent.py
```

### Run CopywriterAgent Tests

```bash
cd backend/agents
python test_copywriter_agent.py
```

### Run Integration Example

```bash
cd backend/agents
python integration_example.py
```

---

## Advanced Usage

### Custom Prompting

#### Modify CopywriterAgent Blog Tone

```python
# Extend CopywriterAgent to customize prompts
class CustomCopywriter(CopywriterAgent):
    def _build_blog_prompt(self, factsheet):
        # Return custom prompt
        return f"Write a technical blog post about {factsheet['product_name']}..."
```

### Combining with External APIs

```python
# Use agents with other services
result = research_agent.analyze(text)
# Send to CRM, content management, etc.
save_to_crm(result["analysis"])
```

### Streaming Results

```python
# Process large batches with progress tracking
import tqdm

texts = [...]
for text in tqdm.tqdm(texts):
    result = agent.analyze(text)
    process_result(result)
```

---

## Best Practices

### 1. Input Quality

- **ResearchAgent**: Provide detailed product descriptions (200+ chars)
- **CopywriterAgent**: Ensure factsheet fields are specific and accurate

### 2. Value Proposition

- Keep it concise (10-20 words)
- Focus on customer benefit, not features
- Make it unique and differentiating

### 3. Features & Specs

- List only relevant features
- Include quantifiable specs where possible
- Prioritize by importance

### 4. Target Audience

- Be specific about who the product is for
- Include use cases or job titles
- Consider business size/type

---

## Troubleshooting

### Issue: Slow Response

**Solution**: 
- Use `gpt-4o-mini` instead of `gpt-4` for CopywriterAgent
- Batch process multiple items together

### Issue: Low-Quality Content

**Solution**:
- Improve value proposition clarity
- Add more specific features
- Provide better technical specifications

### Issue: API Errors

**Solution**:
- Check API key validity
- Verify internet connection
- Check OpenAI service status

---

## Integration Points

### With Flask/FastAPI Backend

```python
from fastapi import FastAPI
from research_agent import ResearchAgent
from copywriter_agent import CopywriterAgent

app = FastAPI()
researcher = ResearchAgent()
copywriter = CopywriterAgent()

@app.post("/analyze")
def analyze_product(text: str):
    return researcher.analyze(text)

@app.post("/generate")
def generate_content(factsheet: dict):
    return copywriter.generate_content(factsheet)
```

### With Frontend

```javascript
// JavaScript/Frontend
const response = await fetch("/analyze", {
  method: "POST",
  body: JSON.stringify({ text: productText })
});
const factsheet = await response.json();
```

---

## File Structure

```
backend/agents/
├── __init__.py                    # Package exports
├── research_agent.py              # ResearchAgent class
├── copywriter_agent.py            # CopywriterAgent class
├── test_research_agent.py         # ResearchAgent tests
├── test_copywriter_agent.py       # CopywriterAgent tests
├── integration_example.py         # End-to-end workflow
├── README.md                      # ResearchAgent docs
├── COPYWRITER_README.md           # CopywriterAgent docs
└── AGENTS_OVERVIEW.md             # This file
```

---

## Next Steps

1. **Set up environment**: Install dependencies and configure API key
2. **Test agents**: Run test scripts to verify setup
3. **Integrate agents**: Use in your application
4. **Monitor costs**: Track API usage and costs
5. **Optimize prompts**: Customize for your use case

---

## Support & Feedback

For issues, questions, or feedback:
- Check documentation files
- Review test examples
- Examine error messages
- Verify API key and environment setup

---

## License

Part of the Autonomous Content Factory project.

**Version**: 0.2.0  
**Last Updated**: April 9, 2026
