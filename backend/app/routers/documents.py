from fastapi import APIRouter

router = APIRouter()

@router.post("/upload")
async def upload_document():
    """Upload and process a document"""
    return {"message": "Document upload endpoint - implementation pending"}

@router.get("/{document_id}/status")
async def get_document_status(document_id: str):
    """Get document processing status"""
    return {"document_id": document_id, "status": "pending"}

@router.get("/{document_id}/extracted")
async def get_extracted_data(document_id: str):
    """Get extracted data from document"""
    return {"document_id": document_id, "data": {}}