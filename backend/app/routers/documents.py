from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
import uuid
import json
import logging
import traceback

from app.models.startup import Job, JobStatus, JobStage
from app.schemas.api import UploadResponse
from app.services.file_service import FileService
from app.services.job_service import JobService
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/documents", tags=["documents"])

# Set up logger for this module
logger = logging.getLogger(__name__)

file_service = FileService()
job_service = JobService()
analysis_service = AnalysisService()


@router.post("/upload", response_model=UploadResponse)
@router.post("/upload", response_model=UploadResponse)
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Upload a pitch deck document for analysis.
    Supports PDF, TXT, DOC, DOCX, XLS, XLSX, and JSON files with comprehensive error handling.
    """
    try:
        # Validate file exists and has a name
        if not file or not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No file provided or file has no name. Please select a file to upload.",
            )

        allowed_content_types = {
            "application/pdf": ".pdf",
            "text/plain": ".txt",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
            "application/msword": ".doc",
            "application/vnd.ms-excel": ".xls",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
            "application/json": ".json",
        }

        file_extension = file.filename.lower().split(".")[-1] if "." in file.filename else ""

        if file.content_type not in allowed_content_types:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"File type '{file.content_type}' is not supported. "
                    "Please upload a PDF, TXT, DOC, DOCX, XLS, XLSX, or JSON file."
                ),
            )

        expected_extension = allowed_content_types[file.content_type].lstrip(".")
        if file_extension != expected_extension:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"File extension '.{file_extension}' does not match content type "
                    f"'{file.content_type}'. Please ensure your file is properly formatted."
                ),
            )

        max_size = 50 * 1024 * 1024  # 50MB
        file_content = await file.read()

        if len(file_content) == 0:
            raise HTTPException(
                status_code=400, detail="File is empty. Please upload a file with content."
            )

        if len(file_content) > max_size:
            size_mb = len(file_content) / (1024 * 1024)
            raise HTTPException(
                status_code=413,
                detail=(
                    f"File size ({size_mb:.1f}MB) exceeds the 50MB limit. "
                    "Please compress your file or split it into smaller parts."
                ),
            )

        # Generate IDs
        file_id = str(uuid.uuid4())
        job_id = str(uuid.uuid4())

        # --- MAIN FIX: Handle JSON files separately ---
        if file.content_type == "application/json":
            try:
                data = None
                try:
                    data = json.loads(file_content)
                except Exception as e:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Failed to parse JSON: {str(e)}"
                    )

                job = Job(
                    id=job_id,
                    status=JobStatus.PENDING,
                    stage=JobStage.UPLOAD,
                    file_id=file_id,
                    progress=10,
                    message="JSON uploaded successfully",
                )

                from app.services.job_service import save_job
                save_job(job_id, job.dict())
                # Instead of file path, pass the parsed JSON directly
                background_tasks.add_task(
                    analysis_service.start_analysis_pipeline,
                    job_id=job_id,
                    file_id=file_id,
                    file_path=None,
                    json_data=data
                )

                response = UploadResponse(
                    job_id=job_id,
                    file_id=file_id,
                    filename=file.filename or "unknown",
                    status="uploaded"
                )
                logger.info(
                    f"JSON upload successful: file_id={file_id}, "
                    f"job_id={job_id}, filename={file.filename}"
                )
                return response
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"JSON upload error: {str(e)}")
                traceback.print_exc()
                raise HTTPException(
                    status_code=500,
                    detail=(
                        "An error occurred processing the JSON file. Please try again or "
                        "contact support if the problem persists."
                    ),
                )

        # --- Otherwise, handle as regular file upload ---
        await file.seek(0)
        try:
            file_path = await file_service.save_file(file, file_id)
        except Exception as e:
            logger.error(f"File save error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=(
                    f"Failed to save file: {str(e)}. Please try again or contact support "
                    "if the problem persists."
                ),
            )

        job = Job(
            id=job_id,
            status=JobStatus.PENDING,
            stage=JobStage.UPLOAD,
            file_id=file_id,
            progress=10,
            message="File uploaded successfully",
        )

        try:
            from app.services.job_service import save_job
            save_job(job_id, job.dict())
        except Exception as e:
            logger.error(f"Job creation error: {str(e)}")
            try:
                await file_service.delete_file(file_id)
            except Exception:
                pass
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create processing job: {str(e)}. Please try again.",
            )

        try:
            background_tasks.add_task(
                analysis_service.start_analysis_pipeline,
                job_id=job_id,
                file_id=file_id,
                file_path=file_path,
            )
        except Exception as e:
            logger.warning(f"Failed to start analysis pipeline: {str(e)}")

        response = UploadResponse(
            job_id=job_id, file_id=file_id, filename=file.filename or "unknown", status="uploaded"
        )
        logger.info(
            f"Upload successful: file_id={file_id}, job_id={job_id}, filename={file.filename}"
        )
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected upload error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred during file upload. Please try again or "
                "contact support if the problem persists."
            ),
        )

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
