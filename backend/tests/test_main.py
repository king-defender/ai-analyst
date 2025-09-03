import pytest
import asyncio
from main import app

# Simple tests that don't rely on TestClient for now
def test_app_creation():
    """Test that the app is created successfully"""
    assert app is not None
    assert app.title == "AI Analyst API"

def test_app_routes():
    """Test that expected routes are registered"""
    routes = [route.path for route in app.routes]
    
    # Check if main routes exist
    assert "/" in routes
    assert "/health" in routes
    
    # Check for API routes (may be registered under sub-routers)
    assert any("/api" in route for route in routes)

@pytest.mark.asyncio
async def test_basic_functionality():
    """Test basic app functionality"""
    # Test that we can import the main components
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