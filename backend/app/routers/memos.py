from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import io
from typing import Dict, Any
from app.services.analysis_service import AnalysisService
from app.services.memo_service import MemoService

router = APIRouter(prefix="/memos", tags=["memos"])

analysis_service = AnalysisService()
memo_service = MemoService()

class GenerateMemoRequest(BaseModel):
    file_id: str

@router.post("/generate")
async def generate_memo(request: GenerateMemoRequest):
    """Generate investment memo from file analysis"""
    try:
        memo_data = await memo_service.generate_memo(request.file_id)
        return memo_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate memo: {str(e)}")

@router.get("/{memo_id}")
async def get_memo(memo_id: str):
    """Get investor memo data by memo ID."""
    try:
        memo_data = await memo_service.get_memo(memo_id)
        
        if not memo_data:
            raise HTTPException(status_code=404, detail="Memo not found")
        
        return memo_data
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=500, detail=f"Failed to get memo: {str(e)}")

@router.get("/{memo_id}/pdf")
async def download_memo_pdf(memo_id: str):
    """Download memo as PDF"""
    try:
        # Get memo data
        memo_data = await memo_service.get_memo(memo_id)
        
        if not memo_data:
            raise HTTPException(status_code=404, detail="Memo not found")
        
        # For MVP, return a simple PDF response
        # In production, this would generate actual PDF using reportlab or similar
        
        company_name = memo_data.get("company_name", "Startup")
        
        # Generate simple PDF content (in production, use proper PDF library)
        pdf_content = f"""
        INVESTMENT MEMO: {company_name}
        
        Generated on: {memo_data.get('created_at', 'N/A')}
        
        EXECUTIVE SUMMARY
        {memo_data.get('executive_summary', 'N/A')}
        
        INVESTMENT THESIS
        {memo_data.get('investment_thesis', 'N/A')}
        
        RECOMMENDATION
        {memo_data.get('recommendation', 'N/A')}
        
        [This is a simplified PDF for MVP demonstration]
        """.encode('utf-8')
        
        # Return as downloadable PDF
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={company_name.replace(' ', '_')}_memo.pdf"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")

@router.get("/{memo_id}/executive-summary")
async def get_executive_summary(memo_id: str):
    """Get executive summary section only."""
    try:
        memo_data = await memo_service.get_memo(memo_id)
        
        return {"executive_summary": memo_data.get("executive_summary", "")}
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=500, detail=f"Failed to get executive summary: {str(e)}")