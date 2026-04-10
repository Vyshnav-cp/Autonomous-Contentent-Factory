"""
FastAPI Backend for Autonomous Content Factory

Provides endpoints for:
- Campaign generation using AI agents
- File uploads
- Content analysis and processing
"""

import os
import sys
import json
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Add backend directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openai_client import OpenAIClientWrapper
from agents.campaign_service import CampaignService

# Initialize FastAPI app
app = FastAPI(
    title="Autonomous Content Factory API",
    description="AI-powered content generation platform",
    version="1.0.0"
)

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
try:
    openai_client = OpenAIClientWrapper()
    campaign_service = CampaignService()
except ValueError as e:
    print(f"Warning: {e}")
    openai_client = None
    campaign_service = None


# ============================================================================
# Request/Response Models
# ============================================================================

class CampaignRequest(BaseModel):
    """Request model for campaign generation"""
    product_name: str
    product_description: str
    target_audience: Optional[str] = None
    tone: Optional[str] = "professional"  # professional, casual, creative
    content_type: Optional[str] = "full"  # full, blog_only, twitter_only


class CampaignResponse(BaseModel):
    """Response model for campaign generation"""
    status: str
    campaign_id: str
    content: dict
    timestamp: str


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    ai_available: bool
    version: str


# ============================================================================
# Health & Status Endpoints
# ============================================================================

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint to verify API is running and AI services are available
    """
    return {
        "status": "healthy",
        "ai_available": openai_client is not None,
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Autonomous Content Factory API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "generate_campaign": "/api/generate-campaign",
            "upload": "/api/upload",
            "docs": "/docs",
            "openapi": "/openapi.json"
        }
    }


# ============================================================================
# Campaign Generation Endpoints
# ============================================================================

@app.post("/api/generate-campaign", response_model=CampaignResponse)
async def generate_campaign(request: CampaignRequest):
    """
    Generate a complete marketing campaign with multiple content formats.
    
    Args:
        request: CampaignRequest containing product details and preferences
        
    Returns:
        CampaignResponse with generated content (blog, twitter, email, etc.)
        
    Raises:
        HTTPException: If AI service is unavailable or generation fails
    """
    if not campaign_service:
        raise HTTPException(
            status_code=503,
            detail="Campaign service unavailable. Please check your OpenAI API key."
        )

    try:
        # Validate input
        if not request.product_name or not request.product_description:
            raise HTTPException(
                status_code=400,
                detail="product_name and product_description are required"
            )

        # Generate campaign
        result = campaign_service.generate_full_campaign(
            product_name=request.product_name,
            product_description=request.product_description,
            target_audience=request.target_audience,
            tone=request.tone,
            content_type=request.content_type
        )

        return {
            "status": "success",
            "campaign_id": result.get("campaign_id"),
            "content": result.get("content", {}),
            "timestamp": result.get("timestamp")
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Campaign generation failed: {str(e)}"
        )


@app.post("/api/generate-campaign/quick")
async def quick_campaign_generation(request: CampaignRequest):
    """
    Quick campaign generation - returns only essential content (blog + twitter)
    """
    if not campaign_service:
        raise HTTPException(
            status_code=503,
            detail="Campaign service unavailable"
        )

    try:
        result = campaign_service.generate_quick_campaign(
            product_name=request.product_name,
            product_description=request.product_description,
            tone=request.tone
        )
        
        return {
            "status": "success",
            "content": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Quick campaign generation failed: {str(e)}"
        )


# ============================================================================
# File Upload Endpoints
# ============================================================================

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Handle file uploads for campaign content or resources.
    
    Supported formats:
    - .txt, .md (text files)
    - .pdf (documents)
    - .csv (data files)
    - .json (structured data)
    
    Returns:
        JSON response with upload status and file info
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")

        # Check file extension
        allowed_extensions = {'.txt', '.md', '.pdf', '.csv', '.json'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
            )

        # Create uploads directory if it doesn't exist
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)

        # Save file
        file_path = os.path.join(upload_dir, file.filename)
        contents = await file.read()
        
        with open(file_path, "wb") as f:
            f.write(contents)

        return {
            "status": "success",
            "filename": file.filename,
            "size": len(contents),
            "path": file_path,
            "message": "File uploaded successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )


@app.post("/api/upload/multiple")
async def upload_multiple_files(files: list[UploadFile] = File(...)):
    """
    Handle multiple file uploads at once.
    """
    results = []
    
    for file in files:
        try:
            # Validate file
            if not file.filename:
                results.append({
                    "status": "error",
                    "filename": "unknown",
                    "detail": "No filename provided"
                })
                continue

            # Check file extension
            allowed_extensions = {'.txt', '.md', '.pdf', '.csv', '.json'}
            file_ext = os.path.splitext(file.filename)[1].lower()
            
            if file_ext not in allowed_extensions:
                results.append({
                    "status": "error",
                    "filename": file.filename,
                    "detail": f"File type not allowed"
                })
                continue

            # Save file
            upload_dir = "uploads"
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, file.filename)
            contents = await file.read()
            
            with open(file_path, "wb") as f:
                f.write(contents)

            results.append({
                "status": "success",
                "filename": file.filename,
                "size": len(contents),
                "path": file_path
            })

        except Exception as e:
            results.append({
                "status": "error",
                "filename": file.filename,
                "detail": str(e)
            })

    return {
        "status": "completed",
        "total": len(files),
        "successful": sum(1 for r in results if r["status"] == "success"),
        "results": results
    }


# ============================================================================
# Content Analysis Endpoints
# ============================================================================

@app.post("/api/analyze-text")
async def analyze_text(data: dict):
    """
    Analyze raw text for product information extraction.
    
    Args:
        data: JSON with "text" field containing raw text to analyze
        
    Returns:
        Extracted product information
    """
    if not openai_client:
        raise HTTPException(
            status_code=503,
            detail="AI service unavailable"
        )

    try:
        text = data.get("text", "")
        if not text:
            raise HTTPException(
                status_code=400,
                detail="text field is required"
            )

        prompt = f"""
        Analyze the following text and extract:
        1. Main topic/product
        2. Key points (list)
        3. Target audience
        4. Tone and style
        5. Suggested improvements
        
        Text:
        {text}
        
        Provide response as structured JSON.
        """

        response = openai_client.generate_response(
            prompt=prompt,
            temperature=0.3,
            system_prompt="You are a content analyst. Respond only with valid JSON."
        )

        return {
            "status": "success",
            "analysis": response
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions"""
    return JSONResponse(
        status_code=400,
        content={"status": "error", "detail": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    return JSONResponse(
        status_code=500,
        content={"status": "error", "detail": "Internal server error"}
    )


# ============================================================================
# Startup & Shutdown
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("🚀 Autonomous Content Factory API starting...")
    print(f"✅ OpenAI Client: {'Available' if openai_client else 'Not configured'}")
    print(f"✅ Campaign Service: {'Available' if campaign_service else 'Not configured'}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 Autonomous Content Factory API shutting down...")


# ============================================================================
# Development Server
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"Starting server on {host}:{port}")
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=os.getenv("ENVIRONMENT", "development") == "development"
    )
