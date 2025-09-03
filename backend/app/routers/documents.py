from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from typing import List
import uuid
import os
from datetime import datetime

from app.models.startup import Job, JobStatus, JobStage
from app.schemas.api import UploadResponse, StartAnalysisRequest, StartAnalysisResponse
from app.services.file_service import FileService
from app.services.job_service import JobService
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/documents", tags=["documents"])

file_service = FileService()
job_service = JobService()
analysis_service = AnalysisService()

@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Upload a pitch deck document for analysis.
    Supports PDF, TXT, and DOCX files.
    """
    try:
        # Validate file type
        allowed_types = ["application/pdf", "text/plain", 
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
        
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"File type {file.content_type} not supported. Use PDF, TXT, or DOCX."
            )
        
        # Validate file size (50MB max)
        max_size = 50 * 1024 * 1024  # 50MB
        file_content = await file.read()
        if len(file_content) > max_size:
            raise HTTPException(
                status_code=400,
                detail="File size exceeds 50MB limit"
            )
        
        # Reset file pointer
        await file.seek(0)
        
        # Generate IDs
        file_id = str(uuid.uuid4())
        job_id = str(uuid.uuid4())
        
        # Save file
        file_path = await file_service.save_file(file, file_id)
        
        # Create job
        job = Job(
            id=job_id,
            status=JobStatus.PENDING,
            stage=JobStage.UPLOAD,
            file_id=file_id,
            progress=10,
            message="File uploaded successfully"
        )
        
        await job_service.create_job(job)
        
        # Start analysis in background
        background_tasks.add_task(
            analysis_service.start_analysis_pipeline,
            job_id=job_id,
            file_id=file_id,
            file_path=file_path
        )
        
        return UploadResponse(
            job_id=job_id,
            file_id=file_id,
            filename=file.filename or "unknown",
            status="uploaded"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/{document_id}/status")
async def get_document_status(document_id: str):
    """Get document processing status"""
    try:
        # This redirects to job status endpoint
        job = await job_service.get_job_by_file_id(document_id)
        if not job:
            raise HTTPException(status_code=404, detail="Document not found")
        return {"document_id": document_id, "status": job.status, "job_id": job.id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")

@router.get("/{document_id}/extracted-data")
async def get_extracted_data(document_id: str):
    """Get extracted data from document"""
    try:
        extracted_data = await file_service.get_extracted_data(document_id)
        if not extracted_data:
            raise HTTPException(status_code=404, detail="Extracted data not found")
        return extracted_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get extracted data: {str(e)}")

@router.get("/{document_id}/extracted")
async def get_extracted_data_legacy(document_id: str):
    """Get extracted data from document (legacy endpoint)"""
    try:
        extracted_data = await file_service.get_extracted_data(document_id)
        if not extracted_data:
            raise HTTPException(status_code=404, detail="Extracted data not found")
        return {"document_id": document_id, "data": extracted_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get extracted data: {str(e)}")

@router.get("/{file_id}/info")
async def get_file_info(file_id: str):
    """Get information about an uploaded file."""
    try:
        file_info = await file_service.get_file_info(file_id)
        if not file_info:
            raise HTTPException(status_code=404, detail="File not found")
        return file_info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get file info: {str(e)}")

@router.delete("/{file_id}")
async def delete_file(file_id: str):
    """Delete an uploaded file."""
    try:
        success = await file_service.delete_file(file_id)
        if not success:
            raise HTTPException(status_code=404, detail="File not found")
        return {"message": "File deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")