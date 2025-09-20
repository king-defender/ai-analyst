from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models.startup import JobStatus
from app.schemas.api import JobStatusResponse
from app.services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["jobs"])

from app.services.job_service import shared_job_service as job_service

@router.get("/{job_id}/status", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """Get the status of a specific job."""
    try:
        job = await job_service.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return JobStatusResponse(
            id=job.id,
            status=job.status.value,
            stage=job.stage.value,
            progress=job.progress,
            message=job.message,
            result=job.result,
            error=job.error,
            created_at=job.created_at,
            updated_at=job.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get job status: {str(e)}")

@router.get("/", response_model=List[JobStatusResponse])
async def list_jobs(
    status: Optional[JobStatus] = None,
    limit: int = 50
):
    """List all jobs with optional status filter."""
    try:
        if status:
            jobs = await job_service.get_jobs_by_status(status)
        else:
            jobs = await job_service.list_jobs(limit=limit)
        
        return [
            JobStatusResponse(
                id=job.id,
                status=job.status.value,
                stage=job.stage.value,
                progress=job.progress,
                message=job.message,
                result=job.result,
                error=job.error,
                created_at=job.created_at,
                updated_at=job.updated_at
            )
            for job in jobs
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list jobs: {str(e)}")

@router.delete("/{job_id}")
async def delete_job(job_id: str):
    """Delete a job and its associated data."""
    try:
        success = await job_service.delete_job(job_id)
        if not success:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return {"message": "Job deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete job: {str(e)}")

@router.post("/{job_id}/retry")
async def retry_job(job_id: str):
    """Retry a failed job."""
    try:
        job = await job_service.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        if job.status != JobStatus.FAILED:
            raise HTTPException(status_code=400, detail="Only failed jobs can be retried")
        
        # Reset job to pending status
        await job_service.update_job(
            job_id,
            status=JobStatus.PENDING,
            error=None,
            message="Job queued for retry"
        )
        
        return {"message": "Job queued for retry"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retry job: {str(e)}")

@router.get("/{job_id}/logs")
async def get_job_logs(job_id: str):
    """Get detailed logs for a job (for debugging)."""
    try:
        job = await job_service.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # For MVP, return basic job information as logs
        # In production, this would return detailed execution logs
        
        logs = [
            f"Job created: {job.created_at}",
            f"Current status: {job.status.value}",
            f"Current stage: {job.stage.value}",
        ]
        
        if job.progress:
            logs.append(f"Progress: {job.progress}%")
        
        if job.message:
            logs.append(f"Latest message: {job.message}")
        
        if job.error:
            logs.append(f"Error: {job.error}")
        
        return {"job_id": job_id, "logs": logs}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get job logs: {str(e)}")