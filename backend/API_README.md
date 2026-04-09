# Autonomous Content Factory REST API

Complete REST API for the Autonomous Content Factory system using FastAPI.

## 🚀 Quick Start

### 1. Prerequisites

```bash
# Python 3.8+
python --version

# API key
export OPENAI_API_KEY="sk-your-api-key"
```

### 2. Start the API

```bash
cd backend
python api.py
```

### 3. Access Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Info**: http://localhost:8000/info

### 4. Make Your First Request

```bash
curl -X POST "http://localhost:8000/generate-campaign" \
  -H "Content-Type: application/json" \
  -d '{
    "document_text": "CloudVault Pro is an enterprise cloud storage solution with encryption and collaboration features..."
  }'
```

## 📋 Main Endpoint

### `POST /generate-campaign`

Generate a complete marketing campaign from product text.

**Request:**
```json
{
  "document_text": "Product description here (min 50 chars)",
  "export_format": "json"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "campaign_id": "CAMP-20260409101530",
    "product_name": "CloudVault Pro",
    "campaign_status": "APPROVED",
    "confidence_score": 92,
    "processing_time_seconds": 25.5,
    "factsheet": {...},
    "content": {
      "blog_post": "...",
      "tweet_thread": [...],
      "email_teaser": "..."
    },
    "validation": {...},
    "recommendations": [...],
    "next_steps": [...]
  }
}
```

**Time**: 17-30 seconds
**Cost**: $0.15-0.30

## 🔄 Workflow

```
Raw Product Text
      ↓
API Receives Request
      ↓
ResearchAgent: Extract Info
      ↓
CopywriterAgent: Generate Content
      ↓
EditorAgent: Validate Quality
      ↓
Return Complete Campaign
```

## 📚 Other Endpoints

### Health Check
```
GET /health
```
Returns: `{"status": "healthy", "service": "...", "version": "..."}`

### Batch Processing
```
POST /generate-campaigns-batch
```
Generate multiple campaigns in one request.

### Export Campaign
```
POST /export-campaign
```
Export campaign in JSON, Markdown, or Plain Text format.

### System Info
```
GET /info
```
Returns API capabilities and configuration.

## 📦 Project Structure

```
backend/
├── api.py                      # Main FastAPI application
├── API_DOCUMENTATION.md        # Full API documentation
├── API_QUICKSTART.md          # 5-minute quick start
├── api_examples.py             # Code examples
├── agents/
│   ├── campaign_service.py     # Orchestration layer
│   ├── research_agent.py       # Product info extraction
│   ├── copywriter_agent.py     # Content generation
│   └── editor_agent.py         # Quality validation
├── requirements.txt            # Dependencies
└── openai_client.py           # OpenAI wrapper
```

## 🛠 Installation

### 1. Clone Repository
```bash
git clone <repo>
cd Autonomous-Contentent-Factory
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Set API Key
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

### 5. Run API
```bash
python api.py
```

## 📖 Usage Examples

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/generate-campaign",
    json={"document_text": "Your product description..."}
)

campaign = response.json()["data"]
print(f"Status: {campaign['campaign_status']}")
print(f"Blog: {campaign['content']['blog_post'][:100]}...")
```

### JavaScript/Node.js
```javascript
const response = await fetch('http://localhost:8000/generate-campaign', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    document_text: 'Your product description...'
  })
});

const campaign = await response.json();
console.log(campaign.data.campaign_status);
```

### cURL
```bash
curl -X POST "http://localhost:8000/generate-campaign" \
  -H "Content-Type: application/json" \
  -d '{"document_text": "..."}'
```

## ⚙️ Configuration

### Environment Variables
```bash
OPENAI_API_KEY=sk-...           # Required: OpenAI API key
API_HOST=0.0.0.0                # Default: localhost
API_PORT=8000                   # Default: 8000
LOG_LEVEL=info                  # Default: info
```

### Custom Port
```bash
python api.py --port 8001
```

### Different Host
```bash
# Listen on all interfaces
python api.py --host 0.0.0.0
```

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t content-factory-api .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY="sk-..." \
  content-factory-api
```

### Docker Compose
```yaml
version: '3'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    restart: always
```

## 🔐 Security

### For Production

1. **Add Authentication**
```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/generate-campaign")
def generate_campaign(request: GenerateCampaignRequest, 
                     credentials = Depends(security)):
    # Verify token
    pass
```

2. **Enable HTTPS**
```bash
# Using Let's Encrypt
certbot certonly --standalone -d yourdomain.com
python api.py --ssl-keyfile=/etc/letsencrypt/live/yourdomain.com/privkey.pem \
               --ssl-certfile=/etc/letsencrypt/live/yourdomain.com/fullchain.pem
```

3. **Add Rate Limiting**
```bash
pip install slowapi

from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/generate-campaign")
@limiter.limit("10/minute")
def generate_campaign(request: GenerateCampaignRequest):
    pass
```

4. **CORS Configuration**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 Monitoring

### Logging
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Campaign created: {campaign['campaign_id']}")
logger.info(f"Status: {campaign['campaign_status']}")
logger.info(f"Duration: {campaign['duration_seconds']}s")
```

### Metrics to Track
- Campaigns generated per day
- Average processing time
- Approval rate
- Average confidence score
- Error rate by type

### Health Monitoring
```bash
# Check API health
curl http://localhost:8000/health

# Monitor logs
docker logs -f content-factory-api
```

## 🚀 Deployment Options

### 1. Heroku
```bash
git push heroku main
```

### 2. AWS
- EC2: Deploy on Ubuntu instance
- ECS: Use Docker container
- Lambda: Serverless with Zappa

### 3. Google Cloud
- Cloud Run: Serverless container
- App Engine: Managed platform

### 4. DigitalOcean
- App Platform: Simple deployment
- Kubernetes: Production-grade

### 5. Self-Hosted
- Docker Swarm
- Kubernetes
- Direct on VPS

## 📝 API Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (validation error) |
| 500 | Server error |

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
python api.py --port 8001
```

### API Key Error
```bash
# Verify key is set
echo $OPENAI_API_KEY

# Set if missing
export OPENAI_API_KEY="sk-..."
```

### Slow Response
Normal for complex products. API takes 17-30 seconds to:
1. Extract product info (2-5s)
2. Generate content (5-10s)
3. Validate quality (10-15s)

### Campaign Rejected
Improve input text:
- Provide complete product description
- Include features, specs, audience
- Clarify value proposition
- Use natural language

## 📚 Documentation

- **[API Documentation](./API_DOCUMENTATION.md)** - Full API reference
- **[Quick Start](./API_QUICKSTART.md)** - 5-minute setup guide
- **[Examples](./api_examples.py)** - Python code examples
- **[Interactive Docs](http://localhost:8000/docs)** - Swagger UI
- **[Complete Project Summary](./agents/COMPLETE_PROJECT_SUMMARY.md)** - System overview

## 🧪 Testing

### Run Examples
```bash
python api_examples.py
```

### Test Endpoints
```bash
# Test single campaign
curl -X POST http://localhost:8000/generate-campaign \
  -H "Content-Type: application/json" \
  -d '{"document_text": "..."}'

# Test batch
curl -X POST http://localhost:8000/generate-campaigns-batch \
  -H "Content-Type: application/json" \
  -d '{"products": [...]}'

# Test health
curl http://localhost:8000/health
```

## 📈 Performance

### Benchmarks
- **Single Campaign**: 17-30 seconds
- **Batch (10 items)**: 190-300 seconds
- **Memory Usage**: ~500MB
- **CPU**: ~2 cores recommended

### Optimization
- Use batch processing for multiple items
- Cache results if possible
- Implement request queuing for high load
- Use CDN for static responses

## 💰 Cost

- **per Campaign**: $0.15-0.30
- **100 Campaigns**: $15-30
- **1000 Campaigns**: $150-300

Prices vary based on:
- Product complexity
- Model selection
- API token usage

## 🤝 Integration

### With Frontend
```javascript
// React example
const [campaign, setCampaign] = useState(null);
const [loading, setLoading] = useState(false);

const generateCampaign = async (text) => {
  setLoading(true);
  const response = await fetch('/api/generate-campaign', {
    method: 'POST',
    body: JSON.stringify({ document_text: text })
  });
  setCampaign(await response.json());
  setLoading(false);
};
```

### With Database
```python
# Save campaign to database
campaign_db = Campaign(
    campaign_id=campaign['campaign_id'],
    product_name=campaign['product_name'],
    status=campaign['campaign_status'],
    data=json.dumps(campaign),
    created_at=datetime.now()
)
db.add(campaign_db)
db.commit()
```

## 📞 Support

### Debugging
1. Check logs: `docker logs -f container-id`
2. Test endpoint: Visit `/docs`
3. Verify API key: `echo $OPENAI_API_KEY`
4. Check network: `curl http://localhost:8000/health`

### Common Issues
- **Slow**: Expected 17-30 seconds
- **Rejected campaigns**: Improve input quality
- **API errors**: Check API key and internet connection

## 📄 License

Part of the Autonomous Content Factory project.

## 🎯 Next Steps

1. **Start API**: `python api.py`
2. **Try Examples**: `python api_examples.py`
3. **Read Docs**: `/docs` endpoint
4. **Integrate**: Add to your application
5. **Deploy**: Use Docker or cloud platform

---

**Ready to generate amazing campaigns? Start here:** [API Quick Start](./API_QUICKSTART.md) 🚀
