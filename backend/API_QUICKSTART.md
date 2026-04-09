# FastAPI - Quick Start (5 minutes)

Get the API running and make your first campaign in 5 minutes.

## Step 1: Start the Server (1 minute)

```bash
cd backend
export OPENAI_API_KEY="sk-your-key-here"
python api.py
```

**Output:**
```
🚀 Starting Autonomous Content Factory API...
📍 Server: http://localhost:8000
📚 Docs: http://localhost:8000/docs
🔄 ReDoc: http://localhost:8000/redoc

INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ API is running and ready!

## Step 2: Open Interactive Documentation (1 minute)

Visit: **http://localhost:8000/docs**

You'll see:
- All available endpoints
- Request/response models
- "Try it out" button for testing

## Step 3: Make Your First Request (2 minutes)

### Option A: Using the Web UI (Easiest)

1. Go to http://localhost:8000/docs
2. Find the `POST /generate-campaign` endpoint
3. Click "Try it out"
4. Enter sample text:
   ```
   CloudVault Pro is a secure cloud storage solution for enterprise teams. Features: 500GB storage, AES-256 encryption, real-time collaboration. Target: Mid-market teams (10-100 people). Value: Secure, scalable, affordable team storage.
   ```
5. Click "Execute"
6. Wait 20-30 seconds for results

### Option B: Using cURL

```bash
curl -X POST "http://localhost:8000/generate-campaign" \
  -H "Content-Type: application/json" \
  -d '{
    "document_text": "CloudVault Pro is a secure cloud storage solution for enterprise teams. Features: 500GB storage, AES-256 encryption, real-time collaboration. Target: Mid-market teams. Value: Secure, scalable, affordable team storage."
  }'
```

### Option C: Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/generate-campaign",
    json={
        "document_text": "Your product description here..."
    }
)

result = response.json()
print(result["data"]["campaign_status"])  # APPROVED/NEEDS_REVISION/REJECTED
print(result["data"]["content"]["blog_post"][:200])
```

## Step 4: Explore Results (1 minute)

The response contains:

```json
{
  "status": "success",
  "data": {
    "campaign_id": "CAMP-20260409101530",
    "campaign_status": "APPROVED",
    "confidence_score": 92,
    "content": {
      "blog_post": "500-word professional blog...",
      "tweet_thread": ["Tweet 1...", "Tweet 2...", ...],
      "email_teaser": "Email paragraph..."
    },
    "recommendations": [...]
  }
}
```

## Key Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Get API Info
```bash
curl http://localhost:8000/info
```

### Generate Single Campaign
```bash
curl -X POST http://localhost:8000/generate-campaign \
  -H "Content-Type: application/json" \
  -d '{"document_text": "Your text..."}'
```

### Generate Multiple Campaigns
```bash
curl -X POST http://localhost:8000/generate-campaigns-batch \
  -H "Content-Type: application/json" \
  -d '{
    "products": [
      {"name": "Product A", "text": "Description A..."},
      {"name": "Product B", "text": "Description B..."}
    ]
  }'
```

### Export in Different Format
```bash
curl -X POST http://localhost:8000/export-campaign \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_data": {...},
    "format": "markdown"
  }'
```

## What You Get

✅ **Factsheet**: Product info extracted
✅ **Blog Post**: 500-word professional content
✅ **Tweet Thread**: 5 engaging tweets
✅ **Email Teaser**: 1-paragraph persuasive copy
✅ **Validation**: Quality scores and recommendations
✅ **Status**: APPROVED/NEEDS_REVISION/REJECTED

## Tips

- Provide **complete** product descriptions (50+ characters minimum)
- Include **features, specs, target audience, value proposition**
- API takes **20-30 seconds** per campaign (normal)
- Cost: **$0.15-0.30** per campaign

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | Kill process: `lsof -ti:8000 \| xargs kill -9` |
| API key error | Set: `export OPENAI_API_KEY="sk-..."` |
| Slow response | Normal for complex products, wait 20-30s |
| Campaign rejected | Improve input: be more specific about product |

## Next Steps

1. ✅ API is running
2. 👉 **Try the examples**: `python api_examples.py`
3. 📖 **Read full docs**: See `API_DOCUMENTATION.md`
4. 🔧 **Integrate into your app**
5. 🚀 **Deploy to production**

## Full Documentation

- **API Docs**: http://localhost:8000/docs
- **API Info**: http://localhost:8000/info
- **Documentation**: See `API_DOCUMENTATION.md`
- **Examples**: Run `python api_examples.py`

---

**That's it!** Your API is ready to generate amazing campaigns! 🎉
