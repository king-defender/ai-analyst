import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from backend.main import app

class TestDocumentUpload:
    """Test cases for document upload functionality."""
    
    def test_upload_endpoint_exists(self):
        """Test that upload endpoint exists and returns correct status."""
        client = TestClient(app)
        
        # Test with no file
        response = client.post("/api/documents/upload")
        assert response.status_code in [400, 422]  # Should require file
    
    def test_health_check(self):
        """Test health check endpoint."""
        client = TestClient(app)
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

@pytest.mark.asyncio
class TestAnalysisFlow:
    """Test cases for analysis workflow."""
    
    async def test_analysis_components_import(self):
        """Test that all analysis components can be imported."""
        try:
            from backend.app.services.analysis_service import AnalysisService
            from backend.app.services.parsing_service import ParsingService
            from backend.app.services.risk_service import RiskService
            from backend.app.services.memo_service import MemoService
            
            # Test instantiation
            analysis_service = AnalysisService()
            assert analysis_service is not None
            
        except ImportError as e:
            pytest.fail(f"Failed to import analysis components: {e}")
    
    async def test_job_service(self):
        """Test job service functionality."""
        from backend.app.services.job_service import JobService
        from backend.app.models.startup import Job, JobStatus, JobStage
        
        job_service = JobService()
        
        # Create test job
        test_job = Job(
            id="test-job-123",
            status=JobStatus.PENDING,
            stage=JobStage.UPLOAD,
            file_id="test-file-123"
        )
        
        # Test create job
        created_job = await job_service.create_job(test_job)
        assert created_job.id == "test-job-123"
        
        # Test get job
        retrieved_job = await job_service.get_job("test-job-123")
        assert retrieved_job is not None
        assert retrieved_job.id == "test-job-123"
        
        # Test update job
        updated_job = await job_service.update_job(
            "test-job-123",
            status=JobStatus.PROCESSING,
            progress=50
        )
        assert updated_job.status == JobStatus.PROCESSING
        assert updated_job.progress == 50

class TestMLPipeline:
    """Test cases for ML pipeline components."""
    
    def test_risk_engine_import(self):
        """Test risk engine can be imported and instantiated."""
        try:
            from ml.pipeline.risk_engine import RiskEngine
            risk_engine = RiskEngine()
            assert risk_engine is not None
            assert len(risk_engine.rules) > 0
        except ImportError as e:
            pytest.fail(f"Failed to import risk engine: {e}")
    
    @pytest.mark.asyncio
    async def test_risk_assessment(self):
        """Test risk assessment with sample data."""
        from ml.pipeline.risk_engine import RiskEngine
        
        risk_engine = RiskEngine()
        
        # Sample startup data
        sample_data = {
            "company_name": "Test Startup",
            "metrics": {
                "runway_months": 6,  # Should trigger short runway risk
                "churn_rate": 0.12,  # Should trigger high churn risk
                "monthly_growth_rate": -0.05  # Should trigger negative growth risk
            },
            "team": [{"name": "John Doe", "experience_years": 3}],  # Small team
            "market_data": {
                "total_addressable_market": 500000000,  # Small market
                "competitors": ["Comp1", "Comp2", "Comp3", "Comp4", "Comp5", "Comp6"]  # High competition
            },
            "industry": "fintech",  # Regulated industry
            "product_info": {
                "development_stage": "alpha",  # Early stage
                "intellectual_property": []  # No IP
            }
        }
        
        assessment = await risk_engine.assess_startup(sample_data)
        
        assert "overall_risk_score" in assessment
        assert "risk_factors" in assessment
        assert "red_flags" in assessment
        assert "yellow_flags" in assessment
        
        # Should have high risk score due to multiple risk factors
        assert assessment["overall_risk_score"] > 60
        
        # Should have red flags for critical issues
        assert len(assessment["red_flags"]) > 0
        
        # Check for specific risks
        risk_types = [rf["risk_type"] for rf in assessment["risk_factors"]]
        assert "Short Runway" in risk_types
        assert "High Churn Rate" in risk_types
        assert "Negative Growth" in risk_types

class TestDataModels:
    """Test cases for data models and validation."""
    
    def test_startup_data_model(self):
        """Test StartupData model validation."""
        from backend.app.models.startup import StartupData, StartupMetrics, FinancialData, UnitEconomics
        
        # Valid data should pass
        valid_data = {
            "id": "test-123",
            "company_name": "Test Company",
            "founded_year": 2022,
            "industry": "SaaS",
            "stage": "Seed",
            "description": "Test description",
            "metrics": {
                "revenue_arr": 1000000,
                "monthly_growth_rate": 0.15
            },
            "financial_data": {
                "total_funding_raised": 2000000,
                "unit_economics": {}
            },
            "market_data": {
                "total_addressable_market": 10000000000,
                "serviceable_addressable_market": 1000000000,
                "target_market_size": 100000000,
                "market_growth_rate": 0.1,
                "market_position": "test"
            },
            "product_info": {
                "product_name": "Test Product",
                "product_type": "SaaS",
                "development_stage": "Production"
            },
            "traction": {
                "user_growth_metrics": {},
                "business_metrics": {}
            }
        }
        
        try:
            startup = StartupData(**valid_data)
            assert startup.company_name == "Test Company"
            assert startup.metrics.revenue_arr == 1000000
        except Exception as e:
            pytest.fail(f"Valid data should not raise exception: {e}")
    
    def test_job_model(self):
        """Test Job model validation."""
        from backend.app.models.startup import Job, JobStatus, JobStage
        
        job_data = {
            "id": "job-123",
            "status": JobStatus.PENDING,
            "stage": JobStage.UPLOAD
        }
        
        job = Job(**job_data)
        assert job.id == "job-123"
        assert job.status == JobStatus.PENDING

class TestAPIIntegration:
    """Integration tests for API endpoints."""
    
    def test_api_documentation(self):
        """Test that API documentation is accessible."""
        client = TestClient(app)
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_openapi_schema(self):
        """Test that OpenAPI schema is valid."""
        client = TestClient(app)
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema

if __name__ == "__main__":
    pytest.main([__file__, "-v"])