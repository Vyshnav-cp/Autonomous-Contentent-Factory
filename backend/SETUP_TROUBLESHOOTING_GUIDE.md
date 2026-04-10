# Backend Setup & Troubleshooting Guide

Complete guide to set up and troubleshoot the Autonomous Content Factory backend.

## Quick Setup (2 minutes)

### Step 1: Set OpenAI API Key

```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

Get your API key from: https://platform.openai.com/api-keys

### Step 2: Start the Server

```bash
cd backend
bash start_server.sh
```

### Step 3: Verify It Works

```bash
# In another terminal
curl http://localhost:8000/health
```

You should see:
```json
{
  "status": "healthy",
  "ai_available": true,
  "version": "1.0.0"
}
```

---

## Detailed Setup

### 1. Clone Repository

```bash
git clone https://github.com/Vyshnav-cp/Autonomous-Contentent-Factory.git
cd Autonomous-Contentent-Factory
```

### 2. Navigate to Backend

```bash
cd backend
```

### 3. Create & Activate Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment

**Option A: Using .env file (Recommended)**

```bash
# Copy example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# Open .env in your editor and change:
#   OPENAI_API_KEY=sk-your-api-key-here
# to your actual key:
#   OPENAI_API_KEY=sk-abc123xyz...
```

**Option B: Export environment variable**

```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

### 6. Test Configuration

```bash
# Run the test suite
python3 test_api_setup.py
```

You should see:
```
✅ PASS - File Compilation
✅ PASS - Imports
✅ PASS - API Structure
✅ PASS - OpenAI Client
✅ PASS - Campaign Service

Total: 5/5 tests passed
🎉 All tests passed! API is ready to run.
```

### 7. Start the Server

```bash
bash start_server.sh
```

You should see:
```
════════════════════════════════════════════
  Autonomous Content Factory API
════════════════════════════════════════════

Server starting on: http://localhost:8000
API Docs: http://localhost:8000/docs
Redoc: http://localhost:8000/redoc

Press Ctrl+C to stop
════════════════════════════════════════════
```

### 8. Test Campaign Generation

```bash
# In another terminal
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

## Troubleshooting

### Issue 1: "OPENAI_API_KEY not set"

**Problem:** Tests fail with "OPENAI_API_KEY not set"

**Solutions:**

1. **Check if environment variable is set:**
   ```bash
   echo $OPENAI_API_KEY
   ```
   Should print your API key. If empty, set it:
   ```bash
   export OPENAI_API_KEY="sk-your-key"
   ```

2. **Use .env file:**
   ```bash
   cp .env.example .env
   # Edit .env and add your key
   # Then run start_server.sh which loads .env
   ```

3. **Verify the key is correct:**
   - Go to https://platform.openai.com/api-keys
   - Create a new API key if needed
   - Copy the full key (starts with `sk-`)

### Issue 2: "Command not found: bash"

**Problem:** `bash start_server.sh` doesn't work

**Solution:** Use `sh` instead:
```bash
sh start_server.sh
```

Or run manually:
```bash
source venv/bin/activate
python3 -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Issue 3: "Port 8000 is already in use"

**Problem:** "Address already in use" error

**Solutions:**

1. **Use a different port:**
   ```bash
   export PORT=8001
   bash start_server.sh
   ```

2. **Find and kill process using port 8000:**
   ```bash
   lsof -i :8000
   kill -9 <PID>
   ```

3. **On Windows:**
   ```powershell
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   ```

### Issue 4: "ModuleNotFoundError: No module named 'fastapi'"

**Problem:** Dependencies not installed

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Or install individually
pip install fastapi uvicorn pydantic openai python-dotenv
```

### Issue 5: "API returns 503 Service Unavailable"

**Problem:** Campaign generation returns "AI service unavailable"

**Solutions:**

1. **Check OpenAI API key:**
   ```bash
   # Verify key is set
   echo $OPENAI_API_KEY
   # Should print your key, not empty
   ```

2. **Verify key is valid:**
   ```bash
   # Check key format (should start with sk-)
   # Test with OpenAI CLI
   openai api completions.create -m text-davinci-003 -p "test"
   ```

3. **Check OpenAI API status:**
   - Visit https://status.openai.com
   - Make sure there are no outages

4. **Check quota/billing:**
   - Go to https://platform.openai.com/account/billing
   - Ensure you have credits or active billing

### Issue 6: "Connection refused" when testing API

**Problem:** Can't connect to `http://localhost:8000`

**Solutions:**

1. **Verify server is running:**
   ```bash
   ps aux | grep uvicorn
   ```

2. **Check firewall:**
   - May be blocking port 8000
   - Try `http://127.0.0.1:8000` instead

3. **Check if server started successfully:**
   - Look for error messages in the terminal
   - Check that "Server starting on http://localhost:8000" appears

### Issue 7: Python version incompatibility

**Problem:** Errors about Python syntax or features

**Solution:** Use Python 3.8+
```bash
python3 --version  # Should be 3.8 or higher

# If using Python 2 or old Python 3
# Install Python 3.9+ and use that
python3.9 -m venv venv
```

### Issue 8: Import errors in IDE

**Problem:** Red squiggly lines under imports (fastapi, pydantic, etc.)

**Solution:** Select the correct Python interpreter in your IDE
- VS Code: Ctrl+Shift+P → "Python: Select Interpreter" → choose venv
- PyCharm: File → Settings → Project → Python Interpreter → Add venv

### Issue 9: "generate_campaign endpoint returns empty response"

**Problem:** Campaign generation works but returns empty content

**Solution:**

1. **Check OpenAI API is responsive:**
   ```bash
   python3 test_api_setup.py
   ```

2. **Check token limits:**
   - May need to increase `max_tokens` in campaign_service.py
   - Or use a faster model

3. **Check request is valid:**
   ```bash
   curl -X POST http://localhost:8000/api/generate-campaign \
     -H "Content-Type: application/json" \
     -d '{
       "product_name": "Test",
       "product_description": "A test product"
     }'
   ```

---

## File Structure

```
backend/
├── api.py                          # Main FastAPI application
├── openai_client.py               # OpenAI client wrapper
├── start_server.sh                # Server startup script
├── test_api_setup.py              # API test suite
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .env                           # Environment variables (DO NOT COMMIT)
├── uploads/                       # Uploaded files directory
└── agents/
    ├── campaign_service.py        # Campaign generation logic
    ├── research_agent.py          # Product research agent
    ├── copywriter_agent.py        # Copy generation agent
    └── editor_agent.py            # Content editing agent
```

---

## Quick Commands

### Start Server
```bash
bash start_server.sh
```

### Run Tests
```bash
python3 test_api_setup.py
```

### Test Campaign Generation
```bash
curl -X POST http://localhost:8000/api/generate-campaign \
  -H "Content-Type: application/json" \
  -d '{"product_name":"Test","product_description":"Test product"}'
```

### Upload File
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@myfile.txt"
```

### View API Documentation
```
http://localhost:8000/docs         # Interactive Swagger UI
http://localhost:8000/redoc        # ReDoc documentation
```

### Stop Server
```bash
Ctrl+C
```

### Deactivate Virtual Environment
```bash
deactivate
```

---

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | (required) | Your OpenAI API key |
| `PORT` | 8000 | Server port |
| `HOST` | 0.0.0.0 | Server host |
| `ENVIRONMENT` | development | development or production |

---

## Production Deployment

For production, follow these steps:

```bash
# Set environment to production
export ENVIRONMENT=production

# Use a proper WSGI server
pip install gunicorn

# Run with gunicorn (multiple workers)
gunicorn api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# Or use the startup script with production flag
ENVIRONMENT=production bash start_server.sh
```

---

## Performance Tips

1. **Use GPT-3.5-turbo for faster responses:**
   - Edit `openai_client.py` and change model to `gpt-3.5-turbo`

2. **Increase cache TTL:**
   - Add caching for repeated requests

3. **Use connection pooling:**
   - FastAPI handles this automatically

4. **Monitor API usage:**
   - Check https://platform.openai.com/account/usage

---

## Support

**Need help?**

1. Check [API_DOCUMENTATION_COMPLETE.md](API_DOCUMENTATION_COMPLETE.md)
2. Review [Campaign Service README](agents/CAMPAIGN_SERVICE_README.md)
3. Check error messages in server output
4. Run `python3 test_api_setup.py` for diagnostic information
5. Review source code comments for details

---

## Next Steps

- Read [API Documentation](API_DOCUMENTATION_COMPLETE.md)
- Test the [Generate Campaign endpoint](#troubleshooting)
- Try uploading files
- Build frontend integration
- Deploy to production

Enjoy! 🚀
