from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# API Response Models
class APIResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class UploadResponse(BaseModel):
    job_id: str
    file_id: str
    filename: str
    status: str

class JobStatusResponse(BaseModel):
    id: str
    status: str
    stage: str
    progress: Optional[int] = None
    message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str = "1.0.0"

class StartAnalysisRequest(BaseModel):
    file_id: str

class StartAnalysisResponse(BaseModel):
    job_id: str

# Request Models
class FileUploadRequest(BaseModel):
    filename: str
    content_type: str
    size: int

class BenchmarkQuery(BaseModel):
    industry: str
    stage: str
    metrics: Dict[str, Any]

class RiskAnalysisRequest(BaseModel):
    startup_data: Dict[str, Any]
    industry_context: Optional[Dict[str, Any]] = None

class MemoGenerationRequest(BaseModel):
    startup_data: Dict[str, Any]
    benchmark_data: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    analysis_context: Optional[Dict[str, Any]] = None