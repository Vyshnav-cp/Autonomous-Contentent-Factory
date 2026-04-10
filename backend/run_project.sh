#!/bin/bash

# ============================================================================
# Autonomous Content Factory - Complete Setup & Run Script
# ============================================================================

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║   Autonomous Content Factory - Backend Setup & Run             ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================================
# Step 1: Check if we're in the right directory
# ============================================================================

if [ ! -f "api.py" ]; then
    echo "❌ Error: api.py not found. Please run this script from the backend directory."
    echo "   Run: cd backend && bash run_project.sh"
    exit 1
fi

echo "✅ Running from backend directory"

# ============================================================================
# Step 2: Check virtual environment
# ============================================================================

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating..."
    python3 -m venv venv
fi

echo "✅ Virtual environment exists"

# ============================================================================
# Step 3: Activate virtual environment
# ============================================================================

source venv/bin/activate
echo "✅ Virtual environment activated"

# ============================================================================
# Step 4: Install dependencies
# ============================================================================

echo "📦 Installing dependencies..."
pip install -q -r requirements.txt 2>/dev/null || pip install -r requirements.txt
pip install -q python-multipart 2>/dev/null || pip install python-multipart
echo "✅ Dependencies installed"

# ============================================================================
# Step 5: Create uploads directory
# ============================================================================

mkdir -p uploads
echo "✅ Uploads directory ready"

# ============================================================================
# Step 6: Check OpenAI API Key
# ============================================================================

echo ""
echo "🔑 OpenAI API Key Configuration:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -z "$OPENAI_API_KEY" ]; then
    # Try to load from .env file
    if [ -f ".env" ]; then
        set -a
        source .env
        set +a
    fi
fi

if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY is not set!"
    echo ""
    echo "To set it, run one of these commands:"
    echo ""
    echo "  1. Export in terminal:"
    echo "     export OPENAI_API_KEY='sk-your-api-key-here'"
    echo ""
    echo "  2. Create .env file in backend directory:"
    echo "     cp .env.example .env"
    echo "     # Edit .env and add your key"
    echo ""
    echo "  3. Get your API key from:"
    echo "     https://platform.openai.com/api-keys"
    echo ""
    echo "⚠️  Continuing without API key (campaign generation will fail)"
    echo ""
else
    echo "✅ OPENAI_API_KEY is set"
    echo "   Key preview: ${OPENAI_API_KEY:0:10}...${OPENAI_API_KEY: -4}"
fi

echo ""

# ============================================================================
# Step 7: Run tests
# ============================================================================

echo "🧪 Running diagnostic tests..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python3 test_api_setup.py 2>/dev/null || echo "⚠️  Some tests require API key"

echo ""

# ============================================================================
# Step 8: Start the server
# ============================================================================

echo "🚀 Starting Autonomous Content Factory API Server..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 Server URL: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "📖 ReDoc: http://localhost:8000/redoc"
echo ""
echo "✅ Health Check:"
echo "   curl http://localhost:8000/health"
echo ""
echo "🎯 Generate Campaign:"
echo "   curl -X POST http://localhost:8000/api/generate-campaign \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"product_name\":\"Test\",\"product_description\":\"Test product\"}'"
echo ""
echo "📤 Upload File:"
echo "   curl -X POST http://localhost:8000/api/upload \\"
echo "     -F 'file=@yourfile.txt'"
echo ""
echo "⏹️  Press Ctrl+C to stop the server"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ============================================================================
# Step 9: Run the server
# ============================================================================

python3 -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload

# ============================================================================
# End
# ============================================================================
