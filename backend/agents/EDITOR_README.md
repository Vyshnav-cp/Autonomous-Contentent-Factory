# EditorAgent

An AI-powered agent that validates and reviews marketing content for factual accuracy, hallucinations, tone quality, and compliance.

## Overview

The `EditorAgent` acts as a quality control layer that:
- Validates generated marketing content against source factsheets
- Detects hallucinated or unsupported claims
- Assesses tone and quality
- Identifies inaccuracies and exaggerations
- Provides detailed feedback and recommendations
- Returns APPROVED or REJECTED status

## Features

### Content Validation
- ✅ **Blog Post Review**: Accuracy, tone, quality assessment
- ✅ **Tweet Thread Review**: Engagement, character compliance, tone consistency
- ✅ **Email Teaser Review**: Persuasiveness, compliance, accuracy

### Quality Checks
- ✅ **Hallucination Detection**: Identifies unsupported claims
- ✅ **Factual Accuracy**: Verifies claims against factsheet
- ✅ **Tone Assessment**: Evaluates tone, consistency, professionalism
- ✅ **Compliance**: Checks for marketing compliance and false claims

### Reporting
- ✅ **Overall Status**: APPROVED or REJECTED decision
- ✅ **Detailed Reviews**: Per-content-type analysis
- ✅ **Confidence Score**: 0-100 validation confidence
- ✅ **Recommendations**: Specific improvement suggestions

## Installation

```bash
pip install -r ../requirements.txt
```

## Configuration

```bash
export OPENAI_API_KEY="sk-your-key-here"
```

## Usage

### Basic Usage

```python
from editor_agent import EditorAgent

agent = EditorAgent()

# Factsheet and generated content
factsheet = {
    "product_name": "CloudVault Pro",
    "key_features": ["Storage", "Encryption", "Collaboration"],
    "technical_specs": {"storage": "Unlimited"},
    "target_audience": "Enterprise teams",
    "value_proposition": "Secure cloud storage"
}

generated_content = {
    "blog_post": "CloudVault Pro is a secure cloud storage...",
    "tweet_thread": ["1/ Tweet...", "2/ Tweet...", ...],
    "email_teaser": "Discover CloudVault Pro..."
}

# Validate content
result = agent.validate_content(factsheet, generated_content)

print(f"Status: {result['validation']['overall_status']}")
print(f"Confidence: {result['validation']['confidence_score']}%")
```

### Accessing Validation Results

```python
# Overall status
status = result["validation"]["overall_status"]  # APPROVED or REJECTED

# Individual reviews
blog_review = result["validation"]["blog_post_review"]
tweet_review = result["validation"]["tweet_thread_review"]
email_review = result["validation"]["email_teaser_review"]

# Hallucinations detected
hallucinations = result["validation"]["hallucinations_detected"]

# Recommendations
recommendations = result["recommendations"]

# Confidence in validation
confidence = result["validation"]["confidence_score"]  # 0-100
```

### Blog Post Validation

```python
# Returns review with:
# - is_accurate: boolean
# - accuracy_score: 0-100
# - tone_score: 0-100
# - inaccuracies: list of strings
# - missing_info: list of strings
# - excessive_claims: list of strings
# - overall_quality: EXCELLENT/GOOD/ADEQUATE/POOR
```

### Tweet Thread Validation

```python
# Returns review with:
# - is_accurate: boolean
# - accuracy_score: 0-100
# - engagement_score: 0-100
# - character_compliance: list per tweet
# - inaccuracies: list of strings
# - hallucinations: list of strings
# - missing_value_prop: boolean
# - tone_consistency: string
# - overall_quality: EXCELLENT/GOOD/ADEQUATE/POOR
```

### Email Teaser Validation

```python
# Returns review with:
# - is_accurate: boolean
# - accuracy_score: 0-100
# - compliance_score: 0-100
# - persuasiveness: 0-100
# - inaccuracies: list of strings
# - hallucinations: list of strings
# - call_to_action: string assessment
# - overall_quality: EXCELLENT/GOOD/ADEQUATE/POOR
```

### Batch Validation

```python
validations = [
    {
        "factsheet": factsheet1,
        "generated_content": content1
    },
    {
        "factsheet": factsheet2,
        "generated_content": content2
    }
]

results = agent.batch_validate(validations)

for result in results:
    if result["status"] == "success":
        print(f"Status: {result['validation']['overall_status']}")
    else:
        print(f"Error: {result['error']}")
```

## Output Structure

```json
{
  "status": "success",
  "timestamp": "2026-04-09T10:30:45.123456",
  "product_name": "CloudVault Pro",
  "validation": {
    "overall_status": "APPROVED",
    "blog_post_review": {
      "is_accurate": true,
      "accuracy_score": 92,
      "tone_score": 88,
      "overall_quality": "EXCELLENT",
      "inaccuracies": [],
      "excessive_claims": [],
      "strengths": [...],
      "improvement_areas": [...]
    },
    "tweet_thread_review": {
      "is_accurate": true,
      "accuracy_score": 95,
      "engagement_score": 85,
      "overall_quality": "EXCELLENT",
      "character_compliance": [true, true, true, true, true],
      "inaccuracies": [],
      "hallucinations": [],
      "missing_value_prop": false
    },
    "email_teaser_review": {
      "is_accurate": true,
      "accuracy_score": 90,
      "compliance_score": 95,
      "persuasiveness": 82,
      "overall_quality": "GOOD",
      "inaccuracies": [],
      "hallucinations": []
    },
    "hallucinations_detected": [],
    "tone_quality": {
      "tone_consistency": 92,
      "brand_alignment": 88,
      "audience_fit": 85,
      "professionalism": 90,
      "persuasiveness": 85,
      "overall_score": 88
    },
    "confidence_score": 92
  },
  "recommendations": [
    "Blog: Consider adding more specific customer benefits",
    "Tweets: Tweet #3 could be more engaging"
  ]
}
```

## Approval Criteria

Content is **APPROVED** when:
- ✅ Average accuracy score > 70%
- ✅ Fewer than 3 hallucinations detected
- ✅ No more than 1 content format rated POOR
- ✅ Value proposition is clearly communicated
- ✅ No critical compliance issues

Content is **REJECTED** when:
- ❌ More than 3 hallucinations detected
- ❌ Average accuracy score < 70%
- ❌ More than 1 content format rated POOR
- ❌ Critical claims not supported by factsheet
- ❌ Compliance score < 60%

## Validation Metrics

### Accuracy Score (0-100)
- 90-100: Highly accurate, fully supported by factsheet
- 70-89: Mostly accurate, minor issues
- 50-69: Some inaccuracies or unsupported claims
- 0-49: Significant inaccuracies, hallucinations

### Engagement Score (0-100)
- 90-100: Highly engaging, viral-worthy
- 70-89: Good engagement potential
- 50-69: Moderate engagement
- 0-49: Low engagement

### Compliance Score (0-100)
- 90-100: Fully compliant, no false claims
- 70-89: Minor compliance concerns
- 50-69: Notable compliance issues
- 0-49: Serious compliance violations

### Tone Consistency (0-100)
- 90-100: Perfect consistency across formats
- 70-89: Good consistency with minor variations
- 50-69: Inconsistent tone
- 0-49: Highly inconsistent

## Common Validations

### Check for Hallucinations

```python
result = agent.validate_content(factsheet, content)
hallucinations = result["validation"]["hallucinations_detected"]

if hallucinations:
    print(f"Found {len(hallucinations)} hallucinations:")
    for h in hallucinations:
        print(f"  - {h}")
```

### Check Accuracy Scores

```python
blog_acc = result["validation"]["blog_post_review"]["accuracy_score"]
tweet_acc = result["validation"]["tweet_thread_review"]["accuracy_score"]
email_acc = result["validation"]["email_teaser_review"]["accuracy_score"]

print(f"Blog: {blog_acc}%, Tweets: {tweet_acc}%, Email: {email_acc}%")
```

### Get Improvement Recommendations

```python
recommendations = result["recommendations"]
for rec in recommendations:
    print(f"→ {rec}")
```

### Check Tone Quality

```python
tone = result["validation"]["tone_quality"]
print(f"Overall Tone Score: {tone['overall_score']}/100")
print(f"Consistency: {tone['tone_consistency']}/100")
print(f"Professionalism: {tone['professionalism']}/100")
```

## Best Practices

### 1. Provide Accurate Factsheets
- Include all key information
- Be specific with technical specs
- Clearly state value proposition

### 2. Review Failed Content
- Read the hallucinations list carefully
- Check accuracy scores for each format
- Review recommendations

### 3. Batch Validation
- Validate multiple products together
- Track approval rates
- Identify patterns in rejections

### 4. Iterate on Content
- Use recommendations for improvement
- Re-run validation after changes
- Aim for > 90% accuracy

### 5. Monitor Confidence
- Confidence < 70% means less reliable validation
- Review results with lower confidence more carefully
- Check if factsheet is clear and complete

## Error Handling

```python
try:
    result = agent.validate_content(factsheet, content)
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"API error: {e}")
```

Common errors:
- Missing factsheet fields
- Empty generated content
- Invalid API key
- Network issues

## API Reference

### Methods

#### `validate_content(factsheet, generated_content) -> Dict`

Validate generated content against a factsheet.

**Parameters:**
- `factsheet`: Product information dictionary
- `generated_content`: Generated content (blog_post, tweet_thread, email_teaser)

**Returns:**
- Validation result with overall_status, reviews, and recommendations

#### `batch_validate(validations) -> List`

Validate multiple content items.

**Parameters:**
- `validations`: List of {factsheet, generated_content} dicts

**Returns:**
- List of validation results

#### `to_json(result) -> str`

Convert result to formatted JSON.

**Parameters:**
- `result`: Validation result dictionary

**Returns:**
- Pretty-printed JSON string

## Configuration Options

### Model Selection

```python
# Default: gpt-4o-mini
agent = EditorAgent(model="gpt-4o-mini")

# More capable (higher cost)
agent = EditorAgent(model="gpt-4")
```

### Custom API Key

```python
agent = EditorAgent(api_key="sk-custom-key")
```

## Performance

- **Latency**: 10-15 seconds per validation (multiple API calls)
- **Tokens**: ~2000-3000 tokens per validation
- **Cost**: ~$0.10-0.20 per validation with gpt-4o-mini

## Validation Workflow

```
Generated Content
       ↓
Blog Post Validation
    ↓  ↓  ↓
    Accuracy, Tone, Quality
       ↓
Tweet Thread Validation
    ↓  ↓  ↓
    Accuracy, Engagement, Compliance
       ↓
Email Teaser Validation
    ↓  ↓  ↓
    Accuracy, Persuasiveness, Compliance
       ↓
Hallucination Detection
       ↓
Tone Quality Assessment
       ↓
Overall Decision
(APPROVED / REJECTED)
```

## Integration with Other Agents

### Research → Copywriting → Editing Pipeline

```python
from research_agent import ResearchAgent
from copywriter_agent import CopywriterAgent
from editor_agent import EditorAgent

# Step 1: Extract product information
researcher = ResearchAgent()
analysis = researcher.analyze(raw_text)
factsheet = {...}

# Step 2: Generate content
copywriter = CopywriterAgent()
content = copywriter.generate_content(factsheet)

# Step 3: Validate content
editor = EditorAgent()
validation = editor.validate_content(
    factsheet,
    content["content"]
)

if validation["validation"]["overall_status"] == "APPROVED":
    print("✓ Content approved for publication")
else:
    print("✗ Content needs revision")
    for rec in validation["recommendations"]:
        print(f"  - {rec}")
```

## Limitations

- Validation based on factsheet accuracy (garbage in = garbage out)
- May not catch subjective tone issues
- Heavily hallucinated content may confuse validator
- Temperature set to 0.3 for consistency (not creative)

## Testing

Run tests:

```bash
cd backend/agents
python test_editor_agent.py
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| All content rejected | Check factsheet accuracy and completeness |
| Low confidence scores | Ensure factsheet fields are specific |
| Slow validation | Normal - multiple API calls required |
| API errors | Verify API key and connection |

## Next Steps

1. Set up environment and API key
2. Run test_editor_agent.py to verify
3. Integrate into content workflow
4. Monitor approval rates
5. Iterate on content based on feedback

---

**Version**: 0.1.0  
**Last Updated**: April 9, 2026
