from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
import io
from typing import Dict, Any
from app.services.analysis_service import AnalysisService
from app.services.memo_service import MemoService

router = APIRouter(prefix="/memos", tags=["memos"])

analysis_service = AnalysisService()
memo_service = MemoService()

@router.post("/generate")
async def generate_memo():
    """Generate investment memo"""
    return {"message": "Memo generation endpoint - implementation pending"}

@router.get("/{job_id}")
async def get_memo(job_id: str):
    """Get investor memo data for a completed analysis."""
    try:
        result = await analysis_service.get_analysis_result(job_id)
        memo_data = result.get("investor_memo")
        
        if not memo_data:
            raise HTTPException(status_code=404, detail="Memo not found")
        
        return memo_data
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=500, detail=f"Failed to get memo: {str(e)}")

@router.get("/{job_id}/pdf")
async def download_memo_pdf(job_id: str):
    """Download memo as PDF"""
    try:
        # Get memo data
        result = await analysis_service.get_analysis_result(job_id)
        memo_data = result.get("investor_memo")
        startup_data = result.get("startup_data")
        
        if not memo_data:
            raise HTTPException(status_code=404, detail="Memo not found")
        
        # For MVP, return a simple PDF response
        # In production, this would generate actual PDF using reportlab or similar
        
        company_name = startup_data.get("company_name", "Startup") if startup_data else "Startup"
        
        # Generate simple PDF content (in production, use proper PDF library)
        pdf_content = f"""
        INVESTMENT MEMO: {company_name}
        
        Generated on: {memo_data.get('generated_at', 'N/A')}
        
        EXECUTIVE SUMMARY
        {memo_data.get('executive_summary', {}).get('company_overview', 'N/A')}
        
        RECOMMENDATION
        {memo_data.get('recommendation', {}).get('recommendation', 'N/A')}
        
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

@router.get("/{job_id}/executive-summary")
async def get_executive_summary(job_id: str):
    """Get executive summary section only."""
    try:
        result = await analysis_service.get_analysis_result(job_id)
        memo_data = result.get("investor_memo", {})
        
        return memo_data.get("executive_summary", {})
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=500, detail=f"Failed to get executive summary: {str(e)}")