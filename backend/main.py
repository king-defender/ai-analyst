from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import documents, analysis, memos
from app.core.config import settings

app = FastAPI(
    title="AI Analyst API",
    description="AI-powered analyst for startup pitch decks and investment memos",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])
app.include_router(memos.router, prefix="/api/v1/memos", tags=["memos"])

@app.get("/")
async def root():
    return {"message": "AI Analyst API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)