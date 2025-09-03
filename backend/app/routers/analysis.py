from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
from app.models.startup import JobStatus
from app.schemas.api import StartAnalysisRequest, StartAnalysisResponse
from app.services.job_service import JobService
from app.services.analysis_service import AnalysisService
from app.services.benchmark_service import BenchmarkService
from app.services.risk_service import RiskService

router = APIRouter(prefix="/analysis", tags=["analysis"])

job_service = JobService()
analysis_service = AnalysisService()
benchmark_service = BenchmarkService()
risk_service = RiskService()

@router.post("/start", response_model=StartAnalysisResponse)
async def start_analysis(
    request: StartAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """Start comprehensive analysis of a startup pitch deck."""
    try:
        # Check if file exists and get associated job
        job = await job_service.get_job_by_file_id(request.file_id)
        if not job:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Return existing job if already processing/completed
        if job.status in [JobStatus.PROCESSING, JobStatus.COMPLETED]:
            return StartAnalysisResponse(job_id=job.id)
        
        # If job failed, restart it
        if job.status == JobStatus.FAILED:
            await job_service.update_job(
                job.id,
                status=JobStatus.PENDING,
                stage=job.stage,
                error=None
            )
        
        return StartAnalysisResponse(job_id=job.id)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start analysis: {str(e)}")

@router.get("/{file_id}/benchmarks")
async def get_benchmark_data(file_id: str):
    """Get benchmarking data for a file."""
    try:
        # For MVP, return sample benchmark data
        # In production, this would query actual benchmark database
        benchmark_data = await benchmark_service.get_benchmarks(file_id)
        return benchmark_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get benchmarks: {str(e)}")

@router.get("/{file_id}/risks")
async def get_risk_assessment(file_id: str):
    """Get risk assessment for a file."""
    try:
        # For MVP, return sample risk assessment
        # In production, this would run actual risk analysis
        risk_assessment = await risk_service.assess_risks(file_id)
        return risk_assessment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get risk assessment: {str(e)}")

@router.get("/{job_id}/result")
async def get_analysis_result(job_id: str):
    """Get complete analysis results for a job."""
    try:
        result = await analysis_service.get_analysis_result(job_id)
        return {
            "job_id": job_id,
            "result": result
        }
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        elif "not completed" in str(e).lower():
            raise HTTPException(status_code=400, detail=str(e))
        else:
            raise HTTPException(status_code=500, detail=f"Failed to get analysis result: {str(e)}")

@router.get("/{job_id}/startup-data")
async def get_startup_data(job_id: str):
    """Get extracted startup data only."""
    try:
        result = await analysis_service.get_analysis_result(job_id)
        return result.get("startup_data")
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=500, detail=f"Failed to get startup data: {str(e)}")

@router.post("/{job_id}/cancel")
async def cancel_analysis(job_id: str):
    """Cancel an ongoing analysis."""
    try:
        success = await analysis_service.cancel_analysis(job_id)
        if not success:
            raise HTTPException(status_code=400, detail="Cannot cancel analysis")
        
        return {"message": "Analysis cancelled successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel analysis: {str(e)}")