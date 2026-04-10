# 🚀 Autonomous Content Factory - System Running Guide

**Status**: ✅ **BOTH FRONTEND AND BACKEND RUNNING**

## 📊 Current Server Status

| Component | URL | Port | Status |
|-----------|-----|------|--------|
| **Frontend** | http://localhost:3000 | 3000 | ✅ Running |
| **Backend API** | http://localhost:8000 | 8000 | ✅ Running |
| **API Docs** | http://localhost:8000/docs | 8000 | ✅ Available |

---

## 🌐 Access the Application

### Frontend
Open your browser and navigate to:
```
http://localhost:3000
```

### Backend API Documentation
View all available endpoints:
```
http://localhost:8000/docs
```

---

## 📝 How to Use

### 1. **Upload a Document**

**Via Frontend:**
- Navigate to http://localhost:3000
- Click on the "Upload" button
- Select a file (.txt, .md, .pdf, .csv, or .json)
- Click "Upload"

**Via API:**
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@/path/to/file.txt"
```

### 2. **Generate a Campaign**

**Prerequisites:**
First, set your OpenAI API key:
```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

Get your key from: https://platform.openai.com/api-keys

**Via Frontend:**
- Fill in the product name and description
- Click "Generate Campaign"
- View the generated content (blog, Twitter posts, email, etc.)

**Via API:**
```bash
curl -X POST http://localhost:8000/api/generate-campaign \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "CloudVault Pro",
    "product_description": "Secure cloud storage solution for enterprises",
    "target_audience": "Enterprise teams",
    "tone": "professional"
  }'
```

### 3. **Response Structure**

The campaign generation returns:
```json
{
  "status": "success",
  "campaign_id": "550e8400-e29b-41d4-a716-446655440000",
  "content": {
    "blog": "Blog post content...",
    "twitter": [
      "Tweet 1 content",
      "Tweet 2 content",
      "Tweet 3 content"
    ],
    "email": {
      "subject": "Subject line",
      "greeting": "Hello",
      "body": "Email body content",
      "cta": "Call to action",
      "signature": "Signature"
    },
    "description": "Product description content"
  },
  "timestamp": "2026-04-10T10:30:45.123456"
}
```

---

## 🎯 API Endpoints

### Health Check
```
GET /health
```
Returns: Health status and AI availability

### Campaign Generation
```
POST /api/generate-campaign
```
Generates full campaign (blog + Twitter + email + description)

### Quick Campaign
```
POST /api/generate-campaign/quick
```
Generates only blog + Twitter content

### File Upload
```
POST /api/upload
```
Upload a single file

### Multiple Files
```
POST /api/upload/multiple
```
Upload multiple files at once

### Text Analysis
```
POST /api/analyze-text
```
Analyze raw text for product information

---

## 🧪 Testing the System

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

### Test 2: Upload a File
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@sample.txt"
```

### Test 3: Generate Campaign (with API key)
```bash
export OPENAI_API_KEY="sk-your-key"
curl -X POST http://localhost:8000/api/generate-campaign \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Test Product",
    "product_description": "Test description"
  }'
```

---

## 📂 File Organization

```
Autonomous-Contentent-Factory/
├── frontend/                    # Frontend application
│   ├── src/
│   │   ├── App.js
│   │   ├── components/
│   │   │   ├── UploadPage.jsx
│   │   │   ├── CampaignView.jsx
│   │   │   ├── CampaignForm.js
│   │   │   └── ...
│   │   └── index.js
│   └── public/
│       └── index.html
│
├── backend/                     # Backend API
│   ├── api.py                  # Main FastAPI app
│   ├── openai_client.py        # OpenAI wrapper
│   ├── agents/
│   │   ├── campaign_service.py # Campaign generation
│   │   ├── research_agent.py
│   │   └── ...
│   ├── venv/                   # Virtual environment
│   ├── requirements.txt        # Python dependencies
│   └── uploads/                # Uploaded files
│
└── docker-compose.yml          # Docker configuration
```

---

## 🔧 Troubleshooting

### Frontend Won't Load
```bash
# Restart frontend server
cd frontend
python3 -m http.server 3000
```

### Backend API Won't Start
```bash
# Check virtual environment
cd backend
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
pip install python-multipart

# Start server
python3 -m uvicorn api:app --host 0.0.0.0 --port 8000
```

### Campaign Generation Not Working
1. Check OpenAI API key is set:
   ```bash
   echo $OPENAI_API_KEY
   ```

2. Verify the key is correct at: https://platform.openai.com/api-keys

3. Make sure you have enough credits in your OpenAI account

### Port Already in Use
```bash
# Find process using port
lsof -i :8000
# Kill it
kill -9 <PID>
```

---

## 📊 Supported File Formats

- **Text**: `.txt`, `.md`
- **Documents**: `.pdf`
- **Data**: `.csv`, `.json`

---

## 🎯 Features

### Campaign Generation
- ✅ Blog posts
- ✅ Twitter/X posts (3 variations)
- ✅ Email marketing templates
- ✅ Product descriptions
- ✅ Customizable tone (professional, casual, creative)
- ✅ Target audience specification

### File Upload
- ✅ Single file upload
- ✅ Multiple file upload
- ✅ Format validation
- ✅ Automatic storage

### API
- ✅ Health checks
- ✅ Error handling
- ✅ CORS support
- ✅ API documentation
- ✅ Interactive Swagger UI

---

## 📚 Documentation

- **Full API Docs**: http://localhost:8000/docs
- **Backend Guide**: `backend/API_DOCUMENTATION_COMPLETE.md`
- **Setup Guide**: `backend/SETUP_TROUBLESHOOTING_GUIDE.md`
- **Implementation**: `backend/BACKEND_IMPLEMENTATION_COMPLETE.md`

---

## ⚡ Next Steps

1. **Set Your OpenAI API Key**
   ```bash
   export OPENAI_API_KEY="sk-your-api-key-here"
   ```

2. **Open the Frontend**
   - Browser: http://localhost:3000

3. **Test Campaign Generation**
   - Fill in product name and description
   - Click "Generate Campaign"
   - View the generated content

4. **Try File Upload**
   - Upload a sample text file
   - See the file appear in `backend/uploads/`

---

## 🎉 You're All Set!

Both servers are running and ready to use:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

Enjoy using the Autonomous Content Factory! 🚀
