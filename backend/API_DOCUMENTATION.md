# Autonomous Content Factory API

FastAPI-based REST API for the Autonomous Content Factory system.

## Quick Start

### 1. Start the Server

```bash
cd backend
python api.py
```

Output:
```
🚀 Starting Autonomous Content Factory API...
📍 Server: http://localhost:8000
📚 Docs: http://localhost:8000/docs
🔄 ReDoc: http://localhost:8000/redoc
```

### 2. Access Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Make Your First Request

```bash
curl -X POST "http://localhost:8000/generate-campaign" \
  -H "Content-Type: application/json" \
  -d '{
    "document_text": "CloudVault Pro is an enterprise cloud storage solution with unlimited storage, AES-256 encryption, and real-time collaboration. Target: Mid-market teams. Value: Secure, scalable team storage."
  }'
```

## Endpoints

### 1. Health Check

```
GET /health
```

**Description**: Check API status

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2026-04-09T10:15:30.123456",
  "service": "Autonomous Content Factory API",
  "version": "1.0.0"
}
```

### 2. Generate Campaign (Main Endpoint)

```
POST /generate-campaign
```

**Description**: Generate a complete marketing campaign from product text

**Request Body**:
```json
{
  "document_text": "CloudVault Pro is an enterprise cloud storage solution...",
  "export_format": "json"
}
```

**Parameters**:
- `document_text` (string, required): Raw product description (min 50 chars)
- `export_format` (string, optional): json, markdown, or plain (default: json)

**Response** (Status 200):
```json
{
  "status": "success",
  "data": {
    "campaign_id": "CAMP-20260409101530",
    "product_name": "CloudVault Pro",
    "campaign_status": "APPROVED",
    "confidence_score": 92,
    "processing_time_seconds": 25.5,
    "factsheet": {
      "product_name": "CloudVault Pro",
      "key_features": ["Encryption", "Collaboration", "Scalable"],
      "technical_specs": {...},
      "target_audience": "Mid-market teams",
      "value_proposition": "Secure, scalable team storage",
      "ambiguous_statements": []
    },
    "content": {
      "blog_post": "500-word blog post...",
      "tweet_thread": [
        "1/ CloudVault Pro: Enterprise storage...",
        "2/ With AES-256 encryption..."
      ],
      "email_teaser": "Discover CloudVault Pro..."
    },
    "validation": {
      "approval_status": "APPROVED",
      "confidence_score": 92,
      "hallucinations_detected": 0,
      "blog_review": {...},
      "tweet_review": {...},
      "email_review": {...}
    },
    "recommendations": [
      "✅ Campaign approved for publication",
      "Consider adding social proof to tweets"
    ],
    "next_steps": [
      "1. Review campaign output",
      "2. Schedule content posting",
      "3. Monitor engagement metrics"
    ]
  }
}
```

**Errors**:
- `400`: Invalid input (text too short)
- `500`: Campaign generation failed

### 3. Batch Campaign Generation

```
POST /generate-campaigns-batch
```

**Description**: Generate campaigns for multiple products

**Request Body**:
```json
{
  "products": [
    {
      "name": "Product A",
      "text": "Product A description..."
    },
    {
      "name": "Product B",
      "text": "Product B description..."
    }
  ]
}
```

**Response** (Status 200):
```json
{
  "status": "completed",
  "total_campaigns": 2,
  "successful": 2,
  "failed": 0,
  "results": [
    {
      "status": "success",
      "campaign_id": "CAMP-20260409101530",
      "product_name": "Product A",
      "campaign_status": "APPROVED",
      "data": {...}
    },
    {
      "status": "success",
      "campaign_id": "CAMP-20260409101545",
      "product_name": "Product B",
      "campaign_status": "NEEDS_REVISION",
      "data": {...}
    }
  ],
  "summary": {
    "approval_rate": "100.0%",
    "timestamp": "2026-04-09T10:16:00.123456"
  }
}
```

### 4. Export Campaign

```
POST /export-campaign
```

**Description**: Export a campaign in different formats

**Request Body**:
```json
{
  "campaign_data": {...},
  "format": "markdown"
}
```

**Parameters**:
- `campaign_data` (object, required): Complete campaign object
- `format` (string, required): json, markdown, or plain

**Response** (Status 200):
```json
{
  "status": "success",
  "format": "markdown",
  "content": "# CloudVault Pro Campaign\n\n## Factsheet\n...",
  "timestamp": "2026-04-09T10:15:30.123456"
}
```

### 5. System Information

```
GET /info
```

**Description**: Get API capabilities and configuration

**Response**:
```json
{
  "service": "Autonomous Content Factory API",
  "version": "1.0.0",
  "endpoints": {...},
  "agents": {
    "research": "Extracts product information",
    "copywriter": "Generates marketing content",
    "editor": "Validates quality and accuracy"
  },
  "export_formats": ["json", "markdown", "plain"],
  "processing_time": "17-30 seconds per campaign",
  "estimated_cost": "$0.15-0.30 per campaign"
}
```

## Examples

### Python Example

```python
import requests

# Generate a campaign
response = requests.post(
    "http://localhost:8000/generate-campaign",
    json={
        "document_text": "Your product description here...",
        "export_format": "json"
    }
)

campaign = response.json()
print(f"Status: {campaign['data']['campaign_status']}")
print(f"Blog: {campaign['data']['content']['blog_post'][:100]}...")
```

### cURL Example

```bash
# Single campaign
curl -X POST "http://localhost:8000/generate-campaign" \
  -H "Content-Type: application/json" \
  -d '{"document_text": "Product description..."}'

# Check health
curl "http://localhost:8000/health"

# Get info
curl "http://localhost:8000/info"
```

### JavaScript/Node.js Example

```javascript
// Using fetch API
const response = await fetch('http://localhost:8000/generate-campaign', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    document_text: 'Your product description...',
    export_format: 'json'
  })
});

const campaign = await response.json();
console.log(campaign.data.campaign_status);
```

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (validation error) |
| 500 | Server error |

## Campaign Status Values

- **APPROVED**: Content is ready for publication
- **NEEDS_REVISION**: Minor issues found, can be revised
- **REJECTED**: Major issues, needs rework
- **FAILED**: Campaign creation failed

## Processing

### Workflow
1. **Research Phase** (2-5s): Extract product information
2. **Copywriting Phase** (5-10s): Generate content
3. **Editing Phase** (10-15s): Validate quality
4. **Total**: 17-30 seconds per campaign

### Cost
- Approximately $0.15-0.30 per campaign
- Varies by product complexity

## Authentication

Currently no authentication required. For production:

```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/generate-campaign")
def generate_campaign(request: GenerateCampaignRequest, credentials = Depends(security)):
    # Verify credentials
    pass
```

## Rate Limiting

For production, add rate limiting:

```bash
pip install slowapi
```

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/generate-campaign")
@limiter.limit("10/minute")
def generate_campaign(request: GenerateCampaignRequest):
    pass
```

## Error Handling

All errors include:
- `status`: "error"
- `error`: Error message
- `detail`: Additional details (if applicable)
- `timestamp`: ISO format timestamp

Example:
```json
{
  "status": "error",
  "error": "Document text must be at least 50 characters",
  "timestamp": "2026-04-09T10:15:30.123456"
}
```

## Database Integration

To persist campaigns, integrate a database:

```python
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import Session

class Campaign(Base):
    __tablename__ = "campaigns"
    
    campaign_id = Column(String, primary_key=True)
    product_name = Column(String)
    status = Column(String)
    data = Column(JSON)
    created_at = Column(DateTime)

# Save campaign
campaign_db = Campaign(
    campaign_id=campaign['campaign_id'],
    product_name=campaign['product_name'],
    status=campaign['campaign_status'],
    data=campaign,
    created_at=datetime.now()
)
db.add(campaign_db)
db.commit()
```

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "api.py"]
```

### Build and Run

```bash
docker build -t content-factory-api .
docker run -p 8000:8000 content-factory-api
```

## Production Checklist

- [ ] Add authentication (HTTPBearer or OAuth2)
- [ ] Enable rate limiting
- [ ] Add CORS configuration
- [ ] Implement database persistence
- [ ] Add request logging
- [ ] Configure error reporting
- [ ] Set up monitoring/alerts
- [ ] Use HTTPS
- [ ] Add API versioning
- [ ] Document API contracts
- [ ] Add request validation
- [ ] Implement caching

## Monitoring

Monitor these metrics:

```python
import logging

logger = logging.getLogger(__name__)

# Log campaign creation
logger.info(f"Campaign created: {campaign['campaign_id']}")
logger.info(f"Status: {campaign['campaign_status']}")
logger.info(f"Duration: {campaign['duration_seconds']}s")
logger.info(f"Confidence: {campaign['validation']['confidence_score']}%")
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 already in use | `python api.py --port 8001` |
| API key not found | Set OPENAI_API_KEY environment variable |
| Slow response | Expected 17-30 seconds for full campaign |
| Campaign rejected | Review input text, ensure complete product info |

## Support

For issues or questions:
1. Check `/docs` endpoint for interactive documentation
2. Review error messages for details
3. Check logs for debugging information

## Version

- **API Version**: 1.0.0
- **Last Updated**: April 9, 2026

## License

Part of the Autonomous Content Factory project.
