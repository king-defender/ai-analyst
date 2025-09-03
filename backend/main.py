from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime

from app.routers import documents, analysis, memos, jobs
from app.core import settings
from app.schemas.api import HealthResponse

app = FastAPI(
    title="AI Analyst API",
    description="AI-powered startup analysis and investor memo generation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")
app.include_router(memos.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "AI Analyst API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )

@app.get("/health")
async def health_check_legacy():
    """Legacy health check endpoint."""
    return {"status": "healthy"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    print("AI Analyst API starting up...")
    print(f"Debug mode: {settings.DEBUG}")
    print(f"Environment: {settings.ENVIRONMENT}")

@app.on_event("shutdown") 
async def shutdown_event():
    """Cleanup on shutdown."""
    print("AI Analyst API shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )