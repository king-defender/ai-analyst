from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from contextlib import asynccontextmanager

from app.routers import documents, analysis, memos, jobs
from app.core import settings
from app.schemas.api import HealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    # Startup
    print("AI Analyst API starting up...")
    print(f"Debug mode: {settings.DEBUG}")
    print(f"Environment: {settings.ENVIRONMENT}")
    
    yield
    
    # Shutdown
    print("AI Analyst API shutting down...")


app = FastAPI(
    title="AI Analyst API",
    description="AI-powered startup analysis and investor memo generation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - configured for development and production
allowed_origins = ["*"] if settings.DEBUG else settings.ALLOWED_HOSTS

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(documents.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")
app.include_router(memos.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")

@app.options("/{full_path:path}")
async def options_handler():
    """Handle CORS preflight requests for all paths."""
    return {"message": "OK"}

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )