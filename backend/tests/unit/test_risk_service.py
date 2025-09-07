"""
Unit tests for risk assessment service.
"""
import pytest
from unittest.mock import Mock, patch
from app.services.risk_service import RiskService


class TestRiskService:
    """Test cases for RiskService."""
    
    @pytest.fixture
    def risk_service(self, mock_openai):
        """Create RiskService instance with mocked OpenAI."""
        return RiskService()
    
    @pytest.mark.asyncio
    async def test_assess_startup_success(self, risk_service, sample_startup_data):
        """Test successful startup risk assessment."""
        result = await risk_service.assess_startup(sample_startup_data)
        
        assert "overall_risk_score" in result
        assert "risk_factors" in result
        assert "red_flags" in result
        assert "yellow_flags" in result
        assert "recommendations" in result
        
        assert isinstance(result["overall_risk_score"], (int, float))
        assert 0 <= result["overall_risk_score"] <= 100
        assert isinstance(result["risk_factors"], list)
    
    @pytest.mark.asyncio
    async def test_calculate_financial_risk(self, risk_service, sample_startup_data):
        """Test financial risk calculation."""
        financial_data = sample_startup_data["financial_data"]
        metrics = sample_startup_data["metrics"]
        
        result = await risk_service.calculate_financial_risk(financial_data, metrics)
        
        assert "score" in result
        assert "factors" in result
        assert isinstance(result["score"], (int, float))
        assert isinstance(result["factors"], list)
    
    @pytest.mark.asyncio
    async def test_calculate_market_risk(self, risk_service, sample_startup_data):
        """Test market risk calculation."""
        market_data = sample_startup_data["market_data"]
        
        result = await risk_service.calculate_market_risk(market_data)
        
        assert "score" in result
        assert "factors" in result
        assert isinstance(result["score"], (int, float))
        assert isinstance(result["factors"], list)
    
    @pytest.mark.asyncio
    async def test_calculate_team_risk(self, risk_service, sample_startup_data):
        """Test team risk calculation."""
        team_data = sample_startup_data["team"]
        
        result = await risk_service.calculate_team_risk(team_data)
        
        assert "score" in result
        assert "factors" in result
        assert isinstance(result["score"], (int, float))
        assert isinstance(result["factors"], list)
    
    def test_identify_red_flags(self, risk_service, sample_startup_data):
        """Test red flag identification."""
        # Create high-risk scenario
        high_risk_data = sample_startup_data.copy()
        high_risk_data["metrics"]["runway_months"] = 3  # Very short runway
        high_risk_data["metrics"]["churn_rate"] = 0.25  # High churn
        
        result = risk_service.identify_red_flags(high_risk_data)
        
        assert isinstance(result, list)
        assert len(result) > 0  # Should have red flags
    
    def test_identify_yellow_flags(self, risk_service, sample_startup_data):
        """Test yellow flag identification."""
        result = risk_service.identify_yellow_flags(sample_startup_data)
        
        assert isinstance(result, list)
        # May or may not have yellow flags depending on data
    
    @pytest.mark.asyncio
    async def test_generate_recommendations(self, risk_service):
        """Test recommendation generation."""
        risk_factors = [
            {"risk_type": "Short Runway", "severity": "high"},
            {"risk_type": "High Churn Rate", "severity": "medium"}
        ]
        
        result = await risk_service.generate_recommendations(risk_factors)
        
        assert isinstance(result, list)
        assert len(result) > 0
        for recommendation in result:
            assert "category" in recommendation
            assert "suggestion" in recommendation
            assert "priority" in recommendation
    
    def test_calculate_runway_risk(self, risk_service):
        """Test runway risk calculation."""
        short_runway = {"runway_months": 6}
        long_runway = {"runway_months": 24}
        
        short_risk = risk_service.calculate_runway_risk(short_runway)
        long_risk = risk_service.calculate_runway_risk(long_runway)
        
        assert short_risk > long_risk
        assert isinstance(short_risk, (int, float))
        assert isinstance(long_risk, (int, float))
    
    def test_calculate_burn_rate_risk(self, risk_service):
        """Test burn rate risk calculation."""
        high_burn = {"burn_rate": 500000, "revenue_arr": 1000000}
        low_burn = {"burn_rate": 100000, "revenue_arr": 1000000}
        
        high_risk = risk_service.calculate_burn_rate_risk(high_burn)
        low_risk = risk_service.calculate_burn_rate_risk(low_burn)
        
        assert high_risk > low_risk
        assert isinstance(high_risk, (int, float))
        assert isinstance(low_risk, (int, float))
    
    def test_calculate_growth_risk(self, risk_service):
        """Test growth rate risk calculation."""
        negative_growth = {"monthly_growth_rate": -0.05}
        positive_growth = {"monthly_growth_rate": 0.15}
        
        negative_risk = risk_service.calculate_growth_risk(negative_growth)
        positive_risk = risk_service.calculate_growth_risk(positive_growth)
        
        assert negative_risk > positive_risk
        assert isinstance(negative_risk, (int, float))
        assert isinstance(positive_risk, (int, float))