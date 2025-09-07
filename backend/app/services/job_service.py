from typing import Dict, Optional, List
from datetime import datetime
from app.models.startup import Job, JobStatus, JobStage

from fastapi import APIRouter, UploadFile, File, HTTPException
import json
import json
from google.cloud import firestore
import uuid

import os
if os.environ.get("FIRESTORE_EMULATOR_HOST"):
    db = firestore.Client(project="demo-project")
else:
    db = firestore.Client()
JOBS_COLLECTION = "analysis_jobs"

import logging

def save_job(job_id, job_data):
    logging.info(f"Saving job {job_id} to Firestore with data: {job_data}")
    db.collection(JOBS_COLLECTION).document(job_id).set(job_data)
    logging.info(f"Job {job_id} saved.")

def get_job(job_id):
    logging.info(f"Retrieving job {job_id} from Firestore.")
    doc = db.collection(JOBS_COLLECTION).document(job_id).get()
    if doc.exists:
        logging.info(f"Job {job_id} found: {doc.to_dict()}")
        return doc.to_dict()
    logging.warning(f"Job {job_id} not found.")
    return None

def delete_job(job_id):
    db.collection(JOBS_COLLECTION).document(job_id).delete()

router = APIRouter()

@router.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    content_type = file.content_type
    content = await file.read()
    
    if content_type == "application/json":
        try:
            data = json.loads(content)
            # Validate schema, run analysis pipeline directly
            job_id = str(uuid.uuid4())
            job_data = {"status": "processing", "input": data}
            save_job(job_id, job_data)
            # ... call analysis logic here ...
            return {"job_id": job_id, "status": "processing"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
    elif content_type in ["application/pdf", "text/plain"]:
        # Existing PDF/TXT pipeline logic here
        ...
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

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