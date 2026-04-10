# API Documentation - Autonomous Content Factory

Complete API reference for the Autonomous Content Factory backend.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Authentication](#authentication)
3. [Endpoints](#endpoints)
4. [Request/Response Examples](#requestresponse-examples)
5. [Error Handling](#error-handling)
6. [Environment Variables](#environment-variables)

---

## Quick Start

### Starting the Server

```bash
cd backend
bash start_server.sh
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Quick Test

```bash
# Health check
curl http://localhost:8000/health

# Generate a campaign
curl -X POST http://localhost:8000/api/generate-campaign \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "CloudVault Pro",
    "product_description": "Secure cloud storage for teams",
    "target_audience": "Enterprise",
    "tone": "professional"
  }'
```

---

## Authentication

Currently, the API does not require authentication. In production, implement:

- API Key authentication
- JWT tokens
- OAuth 2.0

**Note**: The OpenAI API key is configured via environment variable `OPENAI_API_KEY`.

---

## Endpoints

### Health & Status

#### GET /health
Check if API is running and AI services are available.

**Response:**
```json
{
  "status": "healthy",
  "ai_available": true,
  "version": "1.0.0"
}
```

#### GET /
Get API information and available endpoints.

**Response:**
```json
{
  "name": "Autonomous Content Factory API",
  "version": "1.0.0",
  "endpoints": {
    "health": "/health",
    "generate_campaign": "/api/generate-campaign",
    "upload": "/api/upload"
  }
}
```

---

### Campaign Generation

#### POST /api/generate-campaign
Generate a complete marketing campaign with multiple content formats.

**Request:**
```json
{
  "product_name": "CloudVault Pro",
  "product_description": "Secure cloud storage solution for enterprises",
  "target_audience": "Enterprise teams and data-driven organizations",
  "tone": "professional",
  "content_type": "full"
}
```

**Parameters:**
- `product_name` (string, required): Name of the product
- `product_description` (string, required): Description of the product
- `target_audience` (string, optional): Intended audience
- `tone` (string, optional): Writing tone - 'professional', 'casual', or 'creative' (default: 'professional')
- `content_type` (string, optional): 'full', 'blog_only', 'twitter_only' (default: 'full')

**Response:**
```json
{
  "status": "success",
  "campaign_id": "550e8400-e29b-41d4-a716-446655440000",
  "content": {
    "blog": "Blog post content here...",
    "twitter": [
      "Tweet 1 content",
      "Tweet 2 content",
      "Tweet 3 content"
    ],
    "email": {
      "subject": "Subject line",
      "greeting": "Hello",
      "body": "Email body",
      "cta": "Call to action",
      "signature": "Signature"
    },
    "description": "Product description"
  },
  "timestamp": "2026-04-10T10:30:45.123456"
}
```

#### POST /api/generate-campaign/quick
Generate a quick campaign with essential content only (blog + Twitter).

**Request:**
```json
{
  "product_name": "DataFlow",
  "product_description": "Real-time data pipeline tool",
  "tone": "casual"
}
```

**Response:**
```json
{
  "status": "success",
  "content": {
    "blog": "Blog content...",
    "twitter": ["Tweet 1", "Tweet 2", "Tweet 3"]
  }
}
```

---

### File Uploads

#### POST /api/upload
Upload a single file.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- File parameter: `file`

**Supported File Types:**
- `.txt` - Text files
- `.md` - Markdown files
- `.pdf` - PDF documents
- `.csv` - CSV data
- `.json` - JSON data

**Example:**
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@/path/to/file.txt"
```

**Response:**
```json
{
  "status": "success",
  "filename": "product_info.txt",
  "size": 1024,
  "path": "uploads/product_info.txt",
  "message": "File uploaded successfully"
}
```

#### POST /api/upload/multiple
Upload multiple files at once.

**Request:**
```bash
curl -X POST http://localhost:8000/api/upload/multiple \
  -F "files=@file1.txt" \
  -F "files=@file2.csv" \
  -F "files=@file3.json"
```

**Response:**
```json
{
  "status": "completed",
  "total": 3,
  "successful": 3,
  "results": [
    {
      "status": "success",
      "filename": "file1.txt",
      "size": 512,
      "path": "uploads/file1.txt"
    },
    {
      "status": "success",
      "filename": "file2.csv",
      "size": 256,
      "path": "uploads/file2.csv"
    },
    {
      "status": "success",
      "filename": "file3.json",
      "size": 1024,
      "path": "uploads/file3.json"
    }
  ]
}
```

---

### Content Analysis

#### POST /api/analyze-text
Analyze raw text for product information extraction.

**Request:**
```json
{
  "text": "CloudVault is a secure storage solution offering military-grade encryption..."
}
```

**Response:**
```json
{
  "status": "success",
  "analysis": "Extracted analysis content..."
}
```

---

## Request/Response Examples

### Example 1: Generate Professional Blog Post

```bash
curl -X POST http://localhost:8000/api/generate-campaign \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "TaskMaster 360",
    "product_description": "Project management tool with AI-powered task prioritization",
    "target_audience": "Remote teams and small businesses",
    "tone": "professional",
    "content_type": "blog_only"
  }'
```

### Example 2: Generate Creative Social Media Campaign

```bash
curl -X POST http://localhost:8000/api/generate-campaign \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "DesignStudio Pro",
    "product_description": "AI-powered graphic design tool",
    "target_audience": "Freelance designers",
    "tone": "creative",
    "content_type": "twitter_only"
  }'
```

### Example 3: Quick Campaign Generation

```bash
curl -X POST http://localhost:8000/api/generate-campaign/quick \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "DataAnalytics Hub",
    "product_description": "Real-time analytics and reporting",
    "tone": "professional"
  }'
```

### Example 4: Upload and Analyze

```bash
# Upload file
curl -X POST http://localhost:8000/api/upload \
  -F "file=@product_description.txt"

# Then analyze with API
curl -X POST http://localhost:8000/api/analyze-text \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your product description here..."
  }'
```

---

## Error Handling

### Error Response Format

All errors return this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Status Codes

| Code | Status | Meaning |
|------|--------|---------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request parameters |
| 503 | Service Unavailable | AI service not available (check API key) |
| 500 | Internal Error | Server error during processing |

### Error Examples

**Missing Required Field:**
```bash
curl -X POST http://localhost:8000/api/generate-campaign \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Test"}'
```

Response:
```json
{
  "detail": "product_name and product_description are required"
}
```

**Unsupported File Type:**
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@file.exe"
```

Response:
```json
{
  "detail": "File type not allowed. Allowed types: .txt, .md, .pdf, .csv, .json"
}
```

**AI Service Unavailable:**
```json
{
  "detail": "Campaign service unavailable. Please check your OpenAI API key."
}
```

---

## Environment Variables

### Required Variables

**`OPENAI_API_KEY`** (required)
- Your OpenAI API key
- Get from: https://platform.openai.com/api-keys
- Set with: `export OPENAI_API_KEY="sk-..."`

### Optional Variables

**`PORT`** (default: 8000)
- Server port
- Example: `export PORT=5000`

**`HOST`** (default: 0.0.0.0)
- Server host
- Example: `export HOST=localhost`

**`ENVIRONMENT`** (default: development)
- Set to 'production' to disable auto-reload
- Example: `export ENVIRONMENT=production`

### Setting Environment Variables

**Option 1: Using .env file**
```bash
# Create .env in backend directory
OPENAI_API_KEY=sk-your-key-here
PORT=8000
ENVIRONMENT=development
```

**Option 2: Export in terminal**
```bash
export OPENAI_API_KEY="sk-your-key-here"
export PORT=8000
```

**Option 3: Docker**
```bash
docker run -e OPENAI_API_KEY="sk-..." -p 8000:8000 app:latest
```

---

## Advanced Usage

### CORS Configuration

The API allows requests from any origin. For production, update `api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
```

### Custom Model Selection

To use a different OpenAI model, modify in `api.py`:

```python
openai_client = OpenAIClientWrapper(model="gpt-4")  # or gpt-3.5-turbo
```

### Rate Limiting

Add rate limiting middleware for production:

```bash
pip install slowapi
```

Then add to `api.py`:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

---

## Troubleshooting

### "OpenAI API key not provided"
- Set `OPENAI_API_KEY` environment variable
- Check `.env` file exists and has the key
- Verify key is valid on https://platform.openai.com/account/api-keys

### "Campaign service unavailable"
- Check OpenAI API key is set
- Verify internet connection
- Check OpenAI API status

### "File upload failed"
- Check file size (should be reasonable)
- Verify file type is supported
- Check `uploads` directory exists and is writable

### Port already in use
```bash
# Find and kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Or use different port
export PORT=8001
```

---

## Next Steps

- Read [Campaign Service Documentation](agents/CAMPAIGN_SERVICE_README.md)
- Check [Backend README](README.md)
- Run tests: `python test_openai_client.py`
- Try examples: `python integration_examples.py`

---

## Support

For issues or questions:
1. Check this documentation
2. Review error messages carefully
3. Check [Troubleshooting](#troubleshooting) section
4. Review code examples in `integration_examples.py`
