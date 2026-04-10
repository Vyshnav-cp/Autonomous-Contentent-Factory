#!/bin/bash

# Autonomous Content Factory - Backend Startup Script

set -e

echo "🚀 Starting Autonomous Content Factory Backend..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Using .env.example as template."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "📋 Created .env from .env.example"
        echo "⚠️  Please update .env with your OpenAI API key!"
    fi
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📚 Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY environment variable not set"
    echo "   Please set it before running the server:"
    echo "   export OPENAI_API_KEY='your-api-key-here'"
fi

# Create uploads directory
mkdir -p uploads
echo "📁 Uploads directory ready"

# Start the API server
echo ""
echo "════════════════════════════════════════════"
echo "  Autonomous Content Factory API"
echo "════════════════════════════════════════════"
echo ""
echo "Server starting on: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Redoc: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop"
echo "════════════════════════════════════════════"
echo ""

# Determine if running in development or production
ENV=${ENVIRONMENT:-development}
PORT=${PORT:-8000}

if [ "$ENV" = "development" ]; then
    # Run with auto-reload in development
    python3 -m uvicorn api:app --reload --host 0.0.0.0 --port $PORT
else
    # Run without reload in production
    python3 -m uvicorn api:app --host 0.0.0.0 --port $PORT --workers 4
fi
