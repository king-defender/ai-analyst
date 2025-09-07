from typing import Dict, Optional, List
from datetime import datetime, timezone
from app.models.startup import Job, JobStatus, JobStage

from fastapi import APIRouter, UploadFile, File, HTTPException
import logging
import os
import json
import uuid
from google.cloud import firestore

JOBS_COLLECTION = "analysis_jobs"

# Cache for Firestore client to avoid repeated initialization
_firestore_client = None


def _get_firestore_client():
    """
    Get cached Firestore client - lazy initialization for testing.

    Uses module-level caching to avoid creating new client instances
    on every operation, improving performance and reducing connection overhead.
    """
    global _firestore_client

    if _firestore_client is None:
        if os.environ.get("TESTING") == "true":
            from unittest.mock import Mock

            _firestore_client = Mock()
        elif os.environ.get("FIRESTORE_EMULATOR_HOST"):
            _firestore_client = firestore.Client(project="demo-project")
        else:
            _firestore_client = firestore.Client()

    return _firestore_client


def save_job(job_id, job_data):
    """Save job data to Firestore with comprehensive error handling."""
    logging.info(f"Saving job {job_id} to Firestore with data: {job_data}")
    try:
        db = _get_firestore_client()
        db.collection(JOBS_COLLECTION).document(job_id).set(job_data)
        logging.info(f"Job {job_id} saved successfully.")
    except Exception as e:
        logging.error(f"Failed to save job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save job: {str(e)}")


def get_job(job_id):
    """
    Retrieve job from Firestore with error handling and 404 responses.

    Returns job data if found, raises HTTPException with 404 if not found.
    """
    logging.info(f"Retrieving job {job_id} from Firestore.")
    try:
        db = _get_firestore_client()
        doc = db.collection(JOBS_COLLECTION).document(job_id).get()
        if doc.exists:
            job_data = doc.to_dict()
            logging.info(f"Job {job_id} found: {job_data}")
            return job_data
        else:
            logging.warning(f"Job {job_id} not found.")
            raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    except HTTPException:
        # Re-raise HTTP exceptions (like 404)
        raise
    except Exception as e:
        logging.error(f"Failed to retrieve job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve job: {str(e)}")


def delete_job(job_id):
    """Delete job from Firestore with error handling."""
    logging.info(f"Deleting job {job_id} from Firestore.")
    try:
        db = _get_firestore_client()
        db.collection(JOBS_COLLECTION).document(job_id).delete()
        logging.info(f"Job {job_id} deleted successfully.")
    except Exception as e:
        logging.error(f"Failed to delete job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete job: {str(e)}")


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
    """
    In-memory job service for MVP development.

    WARNING: This implementation uses in-memory storage and is suitable for MVP/development only.
    In production, replace with a proper database backend (PostgreSQL, MongoDB, etc.) to ensure:
    - Data persistence across server restarts
    - Horizontal scaling capabilities
    - Transactional consistency
    - Backup and recovery features

    Note: Methods are marked as async to maintain API compatibility with the expected interface,
    but they execute synchronously since they operate on in-memory data structures.
    In a production database implementation, these would perform actual async I/O operations.
    """

    def __init__(self):
        # In-memory storage for MVP (use database in production)
        self.jobs: Dict[str, Job] = {}
        self.file_to_job: Dict[str, str] = {}  # file_id -> job_id mapping

    async def create_job(self, job: Job) -> Job:
        """Create a new job in memory."""
        self.jobs[job.id] = job
        if job.file_id:
            self.file_to_job[job.file_id] = job.id
        return job

    async def get_job(self, job_id: str) -> Optional[Job]:
        """Get a job by ID. Returns None if not found."""
        return self.jobs.get(job_id)

    async def get_job_by_file_id(self, file_id: str) -> Optional[Job]:
        """Get a job by file ID. Returns None if not found."""
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
        error: Optional[str] = None,
    ) -> Optional[Job]:
        """Update a job's status and details. Returns None if job not found."""
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

        # Use timezone-aware datetime to avoid deprecation warnings
        job.updated_at = datetime.now(timezone.utc)

        return job

    async def list_jobs(self, limit: int = 100) -> List[Job]:
        """List all jobs with optional limit."""
        return list(self.jobs.values())[:limit]

    async def delete_job(self, job_id: str) -> bool:
        """Delete a job. Returns True if job was found and deleted, False otherwise."""
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
