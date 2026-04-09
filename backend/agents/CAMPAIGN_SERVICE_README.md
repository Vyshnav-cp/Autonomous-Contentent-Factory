# CampaignService

A comprehensive orchestration service that manages the complete content creation pipeline: Research → Copywriting → Editing.

## Overview

`CampaignService` is the master orchestrator that:
- Accepts raw product text as input
- Runs ResearchAgent to extract information
- Runs CopywriterAgent to generate content
- Runs EditorAgent to validate quality
- Returns a complete, ready-to-publish campaign

## Architecture

```
Raw Product Text
       ↓
┌──────────────────┐
│ ResearchAgent    │ ← Extract product information
├──────────────────┤
│ CopywriterAgent  │ ← Generate marketing content
├──────────────────┤
│ EditorAgent      │ ← Validate and quality check
└──────────────────┘
       ↓
Campaign Result
(Blog + Tweets + Email + Feedback)
```

## Features

### Single Campaign Creation
- ✅ Full workflow orchestration
- ✅ Automatic phase progression
- ✅ Error handling and recovery
- ✅ Comprehensive result compilation

### Batch Processing
- ✅ Process multiple products
- ✅ Error isolation per campaign
- ✅ Progress tracking
- ✅ Aggregated results

### Export Formats
- ✅ JSON (full structured data)
- ✅ Markdown (formatted for docs)
- ✅ Plain Text (easy-to-read)

### Quality Control
- ✅ Campaign status determination
- ✅ Confidence scoring
- ✅ Actionable recommendations
- ✅ Next steps guidance

## Installation

```bash
pip install -r ../requirements.txt
```

## Configuration

```bash
export OPENAI_API_KEY="sk-your-key-here"
```

## Usage

### Basic Campaign Creation

```python
from campaign_service import CampaignService

# Initialize service
service = CampaignService()

# Create campaign from raw product text
raw_text = """
CloudVault Pro is a secure cloud storage solution...
Features: Unlimited storage, encryption, collaboration
Target: Enterprise teams
Value: Secure, scalable team storage
"""

# Create campaign
campaign = service.create_campaign(raw_text)

# Check status
print(f"Status: {campaign['campaign_status']}")
print(f"Confidence: {campaign['validation']['confidence_score']}%")
```

### Accessing Campaign Results

```python
# Campaign metadata
campaign_id = campaign["campaign_id"]
product_name = campaign["product_name"]
status = campaign["campaign_status"]
duration = campaign["duration_seconds"]

# Content
blog = campaign["content"]["blog_post"]
tweets = campaign["content"]["tweet_thread"]
email = campaign["content"]["email_teaser"]

# Validation
approval = campaign["validation"]["approval_status"]
confidence = campaign["validation"]["confidence_score"]
hallucinations = campaign["validation"]["hallucinations"]

# Recommendations
recommendations = campaign["recommendations"]
next_steps = campaign["next_steps"]
```

### Campaign Status Values

- **APPROVED**: Content ready for publication
- **NEEDS_REVISION**: Minor issues found, can be revised
- **REJECTED**: Major issues, needs complete rework
- **FAILED**: Campaign creation failed

### Batch Campaign Creation

```python
products = [
    {
        "name": "Product A",
        "text": "Product A description..."
    },
    {
        "name": "Product B",
        "text": "Product B description..."
    }
]

campaigns = service.create_campaign_batch(products)

for campaign in campaigns:
    if campaign["status"] == "success":
        print(f"✓ {campaign['product_name']}: {campaign['campaign_status']}")
    else:
        print(f"✗ Error: {campaign['error']}")
```

### Exporting Campaigns

```python
# Export as JSON
json_output = service.export_campaign(campaign, format="json")

# Export as Markdown
md_output = service.export_campaign(campaign, format="markdown")

# Export as Plain Text
txt_output = service.export_campaign(campaign, format="plain")
```

## Output Structure

```json
{
  "status": "success",
  "campaign_id": "CAMP-20260409101530",
  "timestamp": "2026-04-09T10:15:30.123456",
  "duration_seconds": 25.5,
  "campaign_status": "APPROVED",
  "product_name": "CloudVault Pro",
  "phases": {
    "research": {
      "status": "success",
      "features_extracted": 5,
      "ambiguities_found": 1
    },
    "copywriting": {
      "status": "success",
      "blog_words": 487,
      "tweets_generated": 5
    },
    "editing": {
      "status": "success",
      "overall_status": "APPROVED",
      "confidence_score": 92,
      "hallucinations_detected": 0
    }
  },
  "factsheet": {
    "product_name": "CloudVault Pro",
    "key_features": [...],
    "technical_specs": {...},
    "target_audience": "...",
    "value_proposition": "..."
  },
  "content": {
    "blog_post": "500-word blog post...",
    "tweet_thread": ["1/ tweet...", "2/ tweet...", ...],
    "email_teaser": "Email teaser paragraph..."
  },
  "validation": {
    "approval_status": "APPROVED",
    "confidence_score": 92,
    "blog_review": {...},
    "tweet_review": {...},
    "email_review": {...},
    "hallucinations": [],
    "tone_quality": {...}
  },
  "metrics": {
    "processing_time": 25.5,
    "research_metrics": {...},
    "content_metrics": {...},
    "quality_metrics": {...}
  },
  "recommendations": [
    "✅ Campaign approved for publication",
    ...
  ],
  "next_steps": [
    "1. Review campaign output",
    "2. Schedule content posting",
    ...
  ]
}
```

## Campaign Phases

### Phase 1: Research
- **Input**: Raw product text
- **Process**: Extract product information
- **Output**: Factsheet with all product details
- **Time**: 2-5 seconds

### Phase 2: Copywriting
- **Input**: Factsheet
- **Process**: Generate marketing content
- **Output**: Blog, tweets, email
- **Time**: 5-10 seconds

### Phase 3: Editing
- **Input**: Factsheet + Generated content
- **Process**: Validate quality and accuracy
- **Output**: APPROVED/REJECTED with feedback
- **Time**: 10-15 seconds

### Total Processing Time
- **Average**: 20-30 seconds per campaign
- **Minimum**: 17-18 seconds (no revisions)
- **Maximum**: 30-40 seconds (complex products)

## Quality Metrics

### Campaign Status Determination
- **APPROVED**: All phases pass with confidence > 70%
- **NEEDS_REVISION**: Some issues but correctable
- **REJECTED**: Major issues or confidence < 50%

### Confidence Score
- Calculated based on validation results
- Range: 0-100%
- Target: > 85% for approval

### Metrics Tracked
- Processing time per phase
- Features extracted
- Content statistics
- Accuracy scores
- Quality ratings

## Configuration Options

### Model Selection

```python
service = CampaignService(
    research_model="gpt-4",
    copywriter_model="gpt-4o-mini",
    editor_model="gpt-4o-mini"
)
```

### Custom API Key

```python
service = CampaignService(api_key="sk-custom-key")
```

## Best Practices

### 1. Input Quality
- Provide complete product descriptions
- Include all key features and specs
- Be specific about target audience
- Clearly state value proposition

### 2. Batch Processing
- Use for multiple products to save overhead
- Monitor individual campaign status
- Handle errors per campaign

### 3. Export Strategy
- Use JSON for programmatic access
- Use Markdown for documentation
- Use Plain Text for email/sharing

### 4. Campaign Management
- Track campaign IDs for reference
- Monitor approval rates
- Review recommendations
- Iterate on failed campaigns

## API Reference

### Methods

#### `create_campaign(raw_product_text: str) -> Dict`

Create a single campaign from raw product text.

**Parameters:**
- `raw_product_text`: Raw product description (required)

**Returns:**
- Campaign result dictionary

**Raises:**
- `ValueError`: If input is empty or invalid
- `Exception`: If workflow fails

#### `create_campaign_batch(products: List[Dict]) -> List`

Create campaigns for multiple products.

**Parameters:**
- `products`: List of {"name": str, "text": str} dicts

**Returns:**
- List of campaign results

#### `export_campaign(result: Dict, format: str) -> str`

Export campaign in specified format.

**Parameters:**
- `result`: Campaign result dictionary
- `format`: "json", "markdown", or "plain"

**Returns:**
- Formatted campaign output

#### `to_json(result: Dict) -> str`

Convert result to JSON string.

**Parameters:**
- `result`: Campaign result dictionary

**Returns:**
- Pretty-printed JSON string

## Performance

### Processing Times
- Research phase: 2-5 seconds
- Copywriting phase: 5-10 seconds
- Editing phase: 10-15 seconds
- Total: 17-30 seconds per campaign

### Cost per Campaign
- Research: $0.01-0.02
- Copywriting: $0.05-0.10
- Editing: $0.10-0.20
- Total: $0.15-0.30

### Batch Processing
- Overhead: ~1-2 seconds setup per batch
- Per-item: Same as single campaign
- Scalable: Unlimited batch size

## Error Handling

```python
try:
    campaign = service.create_campaign(text)
except ValueError as e:
    print(f"Invalid input: {e}")
except Exception as e:
    print(f"Campaign failed: {e}")
```

### Common Errors
| Error | Cause | Solution |
|-------|-------|----------|
| Empty text | No input provided | Provide non-empty product text |
| API key missing | OPENAI_API_KEY not set | Set environment variable |
| Phase failure | Agent error | Check individual agent logs |
| Validation failed | Content issues | Review recommendations |

## Workflow Reliability

### Error Recovery
- Phase-level error handling
- Continues to completion when possible
- Detailed error reporting
- Actionable failure information

### Quality Assurance
- Multi-stage validation
- Confidence scoring
- Hallucination detection
- Tone quality assessment

## Testing

Run the test suite:

```bash
cd backend/agents
python test_campaign_service.py
```

Tests cover:
- ✅ Single campaign creation
- ✅ Batch processing
- ✅ Export formats
- ✅ Phase breakdown
- ✅ Error handling

## Integration Examples

### With Web Framework (FastAPI)

```python
from fastapi import FastAPI
from campaign_service import CampaignService

app = FastAPI()
service = CampaignService()

@app.post("/create-campaign")
async def create_campaign(text: str):
    campaign = service.create_campaign(text)
    return campaign

@app.post("/batch-campaigns")
async def batch_campaigns(products: list):
    campaigns = service.create_campaign_batch(products)
    return campaigns
```

### With Database

```python
from campaign_service import CampaignService
import json

service = CampaignService()
campaign = service.create_campaign(text)

# Save to database
db.campaigns.insert_one({
    "campaign_id": campaign["campaign_id"],
    "product_name": campaign["product_name"],
    "status": campaign["campaign_status"],
    "data": json.dumps(campaign),
    "created_at": datetime.now()
})
```

### With Email Publishing

```python
campaign = service.create_campaign(text)

if campaign["campaign_status"] == "APPROVED":
    # Send email
    send_email(
        subject=f"Campaign: {campaign['product_name']}",
        content=campaign["content"]["email_teaser"],
        attachments=[
            ("blog.md", service.export_campaign(campaign, "markdown")),
            ("campaign.json", service.export_campaign(campaign, "json"))
        ]
    )
```

## Limitations

- Sequential processing (not parallel)
- Requires valid API key
- Batch size limited by rate limits
- Model selection fixed at initialization
- No campaign persistence (save separately)

## Monitoring & Analytics

### Metrics to Track
- Average campaign processing time
- Approval rate by product type
- Confidence score distribution
- Hallucination detection rate
- Phase success rates

### Recommended Logging
```python
import logging

logging.info(f"Campaign created: {campaign['campaign_id']}")
logging.info(f"Status: {campaign['campaign_status']}")
logging.info(f"Duration: {campaign['duration_seconds']}s")
logging.info(f"Confidence: {campaign['validation']['confidence_score']}%")
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| All campaigns rejected | Check product text quality |
| Slow processing | Normal for 3-phase workflow |
| Low confidence | Product info may be unclear |
| Export errors | Check format parameter |
| API errors | Verify API key and connection |

## Next Steps

1. **Setup**: Initialize service with API key
2. **Test**: Run test_campaign_service.py
3. **Create**: Generate first campaign
4. **Validate**: Review approval status
5. **Export**: Export in preferred format
6. **Publish**: Distribute campaign content

## Version History

- **v0.1.0**: Initial release (April 9, 2026)
  - Single campaign creation
  - Batch processing
  - Multiple export formats
  - Complete workflow orchestration

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection
- ~20-30 seconds per campaign

## License

Part of the Autonomous Content Factory project.
