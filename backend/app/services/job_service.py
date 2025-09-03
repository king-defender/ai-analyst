from typing import Dict, Optional, List
from datetime import datetime
from app.models.startup import Job, JobStatus, JobStage

class JobService:
    def __init__(self):
        # In-memory storage for MVP (use database in production)
        self.jobs: Dict[str, Job] = {}
        self.file_to_job: Dict[str, str] = {}  # file_id -> job_id mapping
    
    async def create_job(self, job: Job) -> Job:
        """Create a new job."""
        self.jobs[job.id] = job
        if job.file_id:
            self.file_to_job[job.file_id] = job.id
        return job
    
    async def get_job(self, job_id: str) -> Optional[Job]:
        """Get a job by ID."""
        return self.jobs.get(job_id)
    
    async def get_job_by_file_id(self, file_id: str) -> Optional[Job]:
        """Get a job by file ID."""
        job_id = self.file_to_job.get(file_id)
        if job_id:
            return self.jobs.get(job_id)
        return None
    
    async def update_job(
        self, 
        job_id: str, 
        status: Optional[JobStatus] = None,
        stage: Optional[JobStage] = None,
        progress: Optional[int] = None,
        message: Optional[str] = None,
        result: Optional[Dict] = None,
        error: Optional[str] = None
    ) -> Optional[Job]:
        """Update a job's status and details."""
        job = self.jobs.get(job_id)
        if not job:
            return None
        
        if status is not None:
            job.status = status
        if stage is not None:
            job.stage = stage
        if progress is not None:
            job.progress = progress
        if message is not None:
            job.message = message
        if result is not None:
            job.result = result
        if error is not None:
            job.error = error
        
        job.updated_at = datetime.utcnow()
        
        return job
    
    async def list_jobs(self, limit: int = 100) -> List[Job]:
        """List all jobs."""
        return list(self.jobs.values())[:limit]
    
    async def delete_job(self, job_id: str) -> bool:
        """Delete a job."""
        job = self.jobs.get(job_id)
        if not job:
            return False
        
        # Remove from mappings
        if job.file_id and job.file_id in self.file_to_job:
            del self.file_to_job[job.file_id]
        
        del self.jobs[job_id]
        return True
    
    async def get_jobs_by_status(self, status: JobStatus) -> List[Job]:
        """Get all jobs with a specific status."""
        return [job for job in self.jobs.values() if job.status == status]