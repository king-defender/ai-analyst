import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "AI Analyst API"

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_documents_endpoints():
    """Test document endpoints return expected structure"""
    # Test document status endpoint
    response = client.get("/api/v1/documents/test-id/status")
    assert response.status_code == 200
    assert "document_id" in response.json()
    
    # Test extracted data endpoint
    response = client.get("/api/v1/documents/test-id/extracted")
    assert response.status_code == 200
    assert "document_id" in response.json()