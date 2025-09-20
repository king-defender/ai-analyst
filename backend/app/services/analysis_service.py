import asyncio
from typing import Dict, Any
from datetime import datetime
import uuid

from app.models.startup import JobStatus, JobStage, StartupData, RiskAssessment
from app.services.job_service import JobService
from app.services.ocr_service import OCRService
from app.services.parsing_service import ParsingService
from app.services.benchmark_service import BenchmarkService
from app.services.risk_service import RiskService
from app.services.memo_service import MemoService

class AnalysisService:
    def __init__(self):
        from app.services.job_service import shared_job_service
        self.job_service = shared_job_service
        self.ocr_service = OCRService()
        self.parsing_service = ParsingService()
        self.benchmark_service = BenchmarkService()
        self.risk_service = RiskService()
        self.memo_service = MemoService()
    
    async def start_analysis_pipeline(
        self, 
        job_id: str, 
        file_id: str, 
        file_path: str | None = None,
        json_data: Dict[str, Any] | None = None,
    ):
        """Run the complete analysis pipeline for a startup pitch deck.

        Supports two input modes:
        - file_path: run OCR -> parsing -> benchmarks -> risks -> memo
        - json_data: treat provided JSON as pre-parsed startup data and run a lightweight path
        """
        
        try:
            # If JSON payload is provided, follow a lightweight pipeline
            if json_data is not None:
                await self.job_service.update_job(
                    job_id,
                    status=JobStatus.PROCESSING,
                    stage=JobStage.PARSING,
                    progress=40,
                    message="Processing JSON data..."
                )

                # Benchmarks (sample for MVP)
                await self.job_service.update_job(
                    job_id,
                    stage=JobStage.BENCHMARK,
                    progress=60,
                    message="Computing benchmarks...",
                )
                benchmark_data = await self.benchmark_service.get_benchmarks(file_id)

                # Risk assessment using dict-based helper suitable for MVP
                await self.job_service.update_job(
                    job_id,
                    stage=JobStage.RISKS,
                    progress=80,
                    message="Assessing risks...",
                )
                risk_assessment = await self.risk_service.assess_startup(json_data)

                # Generate a simple memo for JSON uploads as well (MVP sample)
                await self.job_service.update_job(
                    job_id,
                    stage=JobStage.MEMO,
                    progress=90,
                    message="Generating memo...",
                )
                investor_memo = await self.memo_service.generate_memo(file_id)

                # Complete the job with provided JSON as startup_data
                result = {
                    "startup_data": json_data,
                    "benchmark_data": benchmark_data,
                    "risk_assessment": risk_assessment,
                    "investor_memo": investor_memo,
                    "confidence_scores": {
                        "data_extraction": 1.0,  # JSON provided
                        "risk_assessment": 0.75,
                        "benchmark_accuracy": 0.9,
                        "memo_quality": 0.6,
                    },
                }

                await self.job_service.update_job(
                    job_id,
                    status=JobStatus.COMPLETED,
                    progress=100,
                    message="Analysis completed successfully",
                    result=result,
                )
                return

            # Otherwise, require a file path and run the full pipeline
            if not file_path:
                raise ValueError("file_path is required when json_data is not provided")

            # Stage 1: Text Extraction (OCR)
            await self.job_service.update_job(
                job_id,
                status=JobStatus.PROCESSING,
                stage=JobStage.OCR,
                progress=20,
                message="Extracting text from document..."
            )
            
            extracted_text = await self.ocr_service.extract_text(file_path)
            
            # Stage 2: Data Parsing
            await self.job_service.update_job(
                job_id,
                stage=JobStage.PARSING,
                progress=40,
                message="Parsing startup information..."
            )
            
            startup_data = await self.parsing_service.parse_startup_data(extracted_text)
            
            # Stage 3: Benchmarking
            await self.job_service.update_job(
                job_id,
                stage=JobStage.BENCHMARK,
                progress=60,
                message="Comparing against peer companies..."
            )
            
            benchmark_data = await self.benchmark_service.get_benchmarks(file_id)
            
            # Stage 4: Risk Assessment
            await self.job_service.update_job(
                job_id,
                stage=JobStage.RISKS,
                progress=80,
                message="Analyzing potential risks..."
            )
            
            # Use detailed risk assessment for structured startup data + benchmarks
            risk_assessment = await self.risk_service.assess_risks_detailed(startup_data, benchmark_data)
            
            # Stage 5: Memo Generation
            await self.job_service.update_job(
                job_id,
                stage=JobStage.MEMO,
                progress=90,
                message="Generating investor memo..."
            )
            
            investor_memo = await self.memo_service.generate_memo_detailed(
                startup_data, benchmark_data, risk_assessment
            )
            
            # Complete the job
            result = {
                "startup_data": startup_data.dict() if startup_data else None,
                "benchmark_data": benchmark_data,
                "risk_assessment": risk_assessment.dict() if hasattr(risk_assessment, "dict") else risk_assessment,
                "investor_memo": investor_memo,
                "confidence_scores": {
                    "data_extraction": 0.85,
                    "risk_assessment": 0.78,
                    "benchmark_accuracy": 0.92,
                    "memo_quality": 0.88
                }
            }
            
            await self.job_service.update_job(
                job_id,
                status=JobStatus.COMPLETED,
                progress=100,
                message="Analysis completed successfully",
                result=result
            )
            
        except Exception as e:
            await self.job_service.update_job(
                job_id,
                status=JobStatus.FAILED,
                error=f"Analysis failed: {str(e)}"
            )
    
    async def get_analysis_result(self, job_id: str) -> Dict[str, Any]:
        """Get the complete analysis result for a job."""
        job = await self.job_service.get_job(job_id)
        
        if not job:
            raise Exception("Job not found")
        
        if job.status != JobStatus.COMPLETED:
            raise Exception(f"Job not completed. Current status: {job.status}")
        
        return job.result or {}
    
    async def cancel_analysis(self, job_id: str) -> bool:
        """Cancel an ongoing analysis."""
        job = await self.job_service.get_job(job_id)
        
        if not job:
            return False
        
        if job.status in [JobStatus.COMPLETED, JobStatus.FAILED]:
            return False  # Cannot cancel completed or failed jobs
        
        await self.job_service.update_job(
            job_id,
            status=JobStatus.FAILED,
            error="Analysis cancelled by user"
        )
        
        return True