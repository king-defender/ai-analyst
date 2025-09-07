"""
Test main application functionality.
"""
import pytest


def test_read_main(test_client):
    """Test main endpoint returns correct response."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert "AI Analyst MVP" in response.json()["message"]


def test_health_check(test_client):
    """Test health check endpoint."""
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_docs_available(test_client):
    """Test API documentation is available."""
    response = test_client.get("/docs")
    assert response.status_code == 200


def test_app_creation(test_client):
    """Test that the app is created successfully."""
    # If we can create a test client, the app is working
    assert test_client is not None


@pytest.mark.asyncio
async def test_basic_service_imports(mock_all_external_services):
    """Test that we can import main services without connection errors."""
    from app.services.file_service import FileService
    from app.services.parsing_service import ParsingService
    from app.services.risk_service import RiskService
    
    # Test service instantiation
    file_service = FileService()
    parsing_service = ParsingService()
    risk_service = RiskService()
    
    assert file_service is not None
    assert parsing_service is not None
    assert risk_service is not None