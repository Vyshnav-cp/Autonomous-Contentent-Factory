"""
FastAPI Application for Autonomous Content Factory

Provides REST endpoints for campaign generation using the CampaignService.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import sys
import os
import json
from datetime import datetime

# Add agents module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agents'))

from campaign_service import CampaignService

# Initialize FastAPI app
app = FastAPI(
    title="Autonomous Content Factory API",
    description="AI-powered content generation and validation pipeline",
    version="1.0.0"
)

# Initialize CampaignService
campaign_service = CampaignService()


# ==================== Request/Response Models ====================

class GenerateCampaignRequest(BaseModel):
    """Request model for campaign generation"""
    document_text: str = Field(
        ...,
        description="Raw product description or document text",
        min_length=50,
        example="CloudVault Pro is an enterprise cloud storage solution..."
    )
    export_format: Optional[str] = Field(
        default="json",
        description="Export format: json, markdown, or plain",
        pattern="^(json|markdown|plain)$"
    )


class CampaignResponse(BaseModel):
    """Response model for campaign generation"""
    status: str
    campaign_id: str
    product_name: str
    campaign_status: str
    confidence_score: int
    processing_time_seconds: float
    content: dict
    factsheet: dict
    validation: dict
    recommendations: List[str]
    next_steps: List[str]


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    timestamp: str
    service: str
    version: str


class ErrorResponse(BaseModel):
    """Response model for errors"""
    status: str
    error: str
    detail: Optional[str] = None
    timestamp: str


# ==================== Health Check ====================

@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health check endpoint
    
    Returns:
        HealthResponse: Service status and version
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Autonomous Content Factory API",
        "version": "1.0.0"
    }


# ==================== Campaign Generation ====================

@app.post("/generate-campaign", response_model=dict)
def generate_campaign(request: GenerateCampaignRequest):
    """
    Generate a complete marketing campaign from product text.
    
    This endpoint orchestrates the full workflow:
    1. Research phase: Extract product information
    2. Copywriting phase: Generate blog, tweets, email
    3. Editing phase: Validate quality and accuracy
    
    Args:
        request (GenerateCampaignRequest): Contains document_text and optional export_format
    
    Returns:
        dict: Complete campaign with all content and validation results
    
    Raises:
        HTTPException: If campaign generation fails
    
    Example:
        POST /generate-campaign
        {
            "document_text": "CloudVault Pro is an enterprise cloud storage solution...",
            "export_format": "json"
        }
    """
    try:
        # Validate input
        if not request.document_text or len(request.document_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Document text must be at least 50 characters"
            )
        
        # Create campaign
        campaign = campaign_service.create_campaign(request.document_text)
        
        # Check if campaign creation was successful
        if campaign.get("status") != "success":
            raise HTTPException(
                status_code=500,
                detail=campaign.get("error", "Campaign creation failed")
            )
        
        # Export if format requested
        if request.export_format and request.export_format != "json":
            exported = campaign_service.export_campaign(
                campaign,
                format=request.export_format
            )
            campaign["exported_format"] = request.export_format
            campaign["exported_content"] = exported
        
        return {
            "status": "success",
            "data": campaign
        }
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Campaign generation failed: {str(e)}"
        )


# ==================== Batch Campaign Generation ====================

class BatchCampaignRequest(BaseModel):
    """Request model for batch campaign generation"""
    products: List[dict] = Field(
        ...,
        description="List of products with name and text",
        example=[
            {
                "name": "Product A",
                "text": "Product A description..."
            }
        ]
    )


@app.post("/generate-campaigns-batch")
def generate_campaigns_batch(request: BatchCampaignRequest):
    """
    Generate campaigns for multiple products in batch.
    
    Args:
        request (BatchCampaignRequest): List of products with name and text
    
    Returns:
        dict: Results for all campaigns with individual status
    
    Example:
        POST /generate-campaigns-batch
        {
            "products": [
                {"name": "Product A", "text": "..."},
                {"name": "Product B", "text": "..."}
            ]
        }
    """
    try:
        if not request.products:
            raise HTTPException(
                status_code=400,
                detail="Products list cannot be empty"
            )
        
        # Create campaigns
        results = campaign_service.create_campaign_batch(request.products)
        
        # Categorize results
        successful = [r for r in results if r["status"] == "success"]
        failed = [r for r in results if r["status"] != "success"]
        
        return {
            "status": "completed",
            "total_campaigns": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "results": results,
            "summary": {
                "approval_rate": f"{(len(successful) / len(results) * 100):.1f}%",
                "timestamp": datetime.now().isoformat()
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch generation failed: {str(e)}"
        )


# ==================== Export Campaign ====================

class ExportRequest(BaseModel):
    """Request model for campaign export"""
    campaign_data: dict = Field(
        ...,
        description="Complete campaign data to export"
    )
    format: str = Field(
        default="json",
        description="Export format: json, markdown, or plain",
        pattern="^(json|markdown|plain)$"
    )


@app.post("/export-campaign")
def export_campaign(request: ExportRequest):
    """
    Export a campaign in different formats.
    
    Args:
        request (ExportRequest): Campaign data and desired format
    
    Returns:
        dict: Exported campaign in requested format
    
    Example:
        POST /export-campaign
        {
            "campaign_data": {...},
            "format": "markdown"
        }
    """
    try:
        exported = campaign_service.export_campaign(
            request.campaign_data,
            format=request.format
        )
        
        return {
            "status": "success",
            "format": request.format,
            "content": exported,
            "timestamp": datetime.now().isoformat()
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid format: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Export failed: {str(e)}"
        )


# ==================== Campaign Status Check ====================

class StatusCheckRequest(BaseModel):
    """Request model for status check"""
    campaign_id: str = Field(
        ...,
        description="Campaign ID to check"
    )


@app.post("/campaign-status")
def check_campaign_status(request: StatusCheckRequest):
    """
    Check the status of a campaign.
    
    Args:
        request (StatusCheckRequest): Campaign ID
    
    Returns:
        dict: Campaign status information
    """
    # Note: This would require a database/cache in production
    return {
        "status": "info",
        "message": "Campaign status tracking requires database integration",
        "campaign_id": request.campaign_id,
        "note": "Implement persistent storage to track campaign status"
    }


# ==================== System Information ====================

@app.get("/info")
def system_info():
    """
    Get system information and capabilities.
    
    Returns:
        dict: API and system information
    """
    return {
        "service": "Autonomous Content Factory API",
        "version": "1.0.0",
        "endpoints": {
            "health": {
                "method": "GET",
                "path": "/health",
                "description": "Health check"
            },
            "generate_campaign": {
                "method": "POST",
                "path": "/generate-campaign",
                "description": "Generate single campaign"
            },
            "batch_campaigns": {
                "method": "POST",
                "path": "/generate-campaigns-batch",
                "description": "Generate multiple campaigns"
            },
            "export": {
                "method": "POST",
                "path": "/export-campaign",
                "description": "Export campaign in different formats"
            },
            "info": {
                "method": "GET",
                "path": "/info",
                "description": "System information"
            }
        },
        "agents": {
            "research": "Extracts product information",
            "copywriter": "Generates marketing content",
            "editor": "Validates quality and accuracy"
        },
        "export_formats": ["json", "markdown", "plain"],
        "processing_time": "17-30 seconds per campaign",
        "estimated_cost": "$0.15-0.30 per campaign"
    }


# ==================== Error Handlers ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )


# ==================== Root Endpoint ====================

@app.get("/")
def root():
    """Root endpoint with API documentation link"""
    return {
        "message": "Autonomous Content Factory API",
        "version": "1.0.0",
        "documentation": "/docs",
        "interactive_docs": "/redoc",
        "quick_start": "/info"
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run the API server
    print("🚀 Starting Autonomous Content Factory API...")
    print("📍 Server: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("🔄 ReDoc: http://localhost:8000/redoc")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
