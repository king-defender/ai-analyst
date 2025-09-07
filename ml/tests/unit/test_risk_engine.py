"""
Unit tests for ML risk engine.
"""
import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add the ML pipeline to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from pipeline.risk_engine import RiskEngine


class TestRiskEngine:
    """Test cases for RiskEngine."""
    
    @pytest.fixture
    def risk_engine(self, mock_openai_ml):
        """Create RiskEngine instance with mocked dependencies."""
        return RiskEngine()
    
    @pytest.mark.asyncio
    async def test_assess_startup_basic(self, risk_engine, sample_risk_data):
        """Test basic startup assessment."""
        result = await risk_engine.assess_startup(sample_risk_data)
        
        assert "overall_risk_score" in result
        assert "risk_factors" in result
        assert "red_flags" in result
        assert "yellow_flags" in result
        
        # Should be high risk due to multiple red flags
        assert result["overall_risk_score"] > 60
        assert len(result["risk_factors"]) > 0
    
    def test_calculate_runway_risk(self, risk_engine):
        """Test runway risk calculation."""
        short_runway_data = {"runway_months": 3}
        long_runway_data = {"runway_months": 24}
        
        short_risk = risk_engine.calculate_runway_risk(short_runway_data)
        long_risk = risk_engine.calculate_runway_risk(long_runway_data)
        
        assert short_risk > long_risk
        assert short_risk >= 80  # Short runway should be high risk
        assert long_risk <= 20   # Long runway should be low risk
    
    def test_calculate_growth_risk(self, risk_engine):
        """Test growth rate risk calculation."""
        negative_growth = {"monthly_growth_rate": -0.05}
        positive_growth = {"monthly_growth_rate": 0.15}
        
        negative_risk = risk_engine.calculate_growth_risk(negative_growth)
        positive_risk = risk_engine.calculate_growth_risk(positive_growth)
        
        assert negative_risk > positive_risk
        assert negative_risk >= 70  # Negative growth is high risk
        assert positive_risk <= 30  # Strong growth is low risk
    
    def test_calculate_churn_risk(self, risk_engine):
        """Test churn rate risk calculation."""
        high_churn = {"churn_rate": 0.20}
        low_churn = {"churn_rate": 0.02}
        
        high_risk = risk_engine.calculate_churn_risk(high_churn)
        low_risk = risk_engine.calculate_churn_risk(low_churn)
        
        assert high_risk > low_risk
        assert high_risk >= 60  # High churn is medium-high risk
        assert low_risk <= 20   # Low churn is low risk
    
    def test_calculate_team_risk(self, risk_engine):
        """Test team composition risk calculation."""
        inexperienced_team = {
            "team": [
                {"name": "John", "experience_years": 1},
                {"name": "Jane", "experience_years": 2}
            ]
        }
        
        experienced_team = {
            "team": [
                {"name": "John", "experience_years": 10},
                {"name": "Jane", "experience_years": 8},
                {"name": "Bob", "experience_years": 12}
            ]
        }
        
        inexperienced_risk = risk_engine.calculate_team_risk(inexperienced_team)
        experienced_risk = risk_engine.calculate_team_risk(experienced_team)
        
        assert inexperienced_risk > experienced_risk
    
    def test_calculate_market_risk(self, risk_engine):
        """Test market risk calculation."""
        small_market = {
            "total_addressable_market": 100000000,  # $100M
            "competitors": ["A", "B", "C", "D", "E", "F"]  # Many competitors
        }
        
        large_market = {
            "total_addressable_market": 50000000000,  # $50B
            "competitors": ["A", "B"]  # Few competitors
        }
        
        small_market_risk = risk_engine.calculate_market_risk(small_market)
        large_market_risk = risk_engine.calculate_market_risk(large_market)
        
        assert small_market_risk > large_market_risk
    
    def test_identify_red_flags(self, risk_engine, sample_risk_data):
        """Test red flag identification."""
        red_flags = risk_engine.identify_red_flags(sample_risk_data)
        
        assert isinstance(red_flags, list)
        assert len(red_flags) > 0
        
        # Should identify specific red flags from sample data
        flag_types = [flag["risk_type"] for flag in red_flags]
        assert "Short Runway" in flag_types  # 6 months runway
        assert "Negative Growth" in flag_types  # -2% growth
    
    def test_identify_yellow_flags(self, risk_engine, sample_risk_data):
        """Test yellow flag identification."""
        yellow_flags = risk_engine.identify_yellow_flags(sample_risk_data)
        
        assert isinstance(yellow_flags, list)
        # May or may not have yellow flags depending on thresholds
    
    def test_calculate_industry_risk(self, risk_engine):
        """Test industry-specific risk calculation."""
        fintech_risk = risk_engine.calculate_industry_risk({"industry": "fintech"})
        saas_risk = risk_engine.calculate_industry_risk({"industry": "saas"})
        
        assert fintech_risk > saas_risk  # Fintech is more regulated
        assert isinstance(fintech_risk, (int, float))
        assert isinstance(saas_risk, (int, float))
    
    def test_calculate_product_risk(self, risk_engine):
        """Test product development stage risk."""
        alpha_product = {
            "product_info": {
                "development_stage": "alpha",
                "intellectual_property": []
            }
        }
        
        production_product = {
            "product_info": {
                "development_stage": "production",
                "intellectual_property": ["patent1", "patent2"]
            }
        }
        
        alpha_risk = risk_engine.calculate_product_risk(alpha_product)
        production_risk = risk_engine.calculate_product_risk(production_product)
        
        assert alpha_risk > production_risk
    
    def test_risk_score_bounds(self, risk_engine):
        """Test that risk scores are within valid bounds."""
        test_data = {"runway_months": 12}
        
        risk_score = risk_engine.calculate_runway_risk(test_data)
        
        assert 0 <= risk_score <= 100
        assert isinstance(risk_score, (int, float))