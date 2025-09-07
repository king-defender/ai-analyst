"""
Configuration for ML pipeline tests.
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def mock_transformers():
    """Mock transformers library."""
    with patch('transformers.pipeline') as mock_pipeline:
        mock_model = Mock()
        mock_model.return_value = [{"label": "POSITIVE", "score": 0.95}]
        mock_pipeline.return_value = mock_model
        yield mock_pipeline


@pytest.fixture
def mock_openai_ml():
    """Mock OpenAI for ML pipeline."""
    with patch('openai.OpenAI') as mock_client:
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        
        # Mock completion response
        mock_choice = Mock()
        mock_choice.message.content = '{"risk_score": 65, "factors": ["Short runway"]}'
        
        mock_response = Mock()
        mock_response.choices = [mock_choice]
        
        mock_instance.chat.completions.create.return_value = mock_response
        
        yield mock_instance


@pytest.fixture
def sample_document_text():
    """Sample extracted document text for testing."""
    return """
    Company: TechFlow Solutions
    Founded: 2022
    Industry: SaaS
    Stage: Series A
    
    Metrics:
    - ARR: $2.5M
    - Growth Rate: 25% MoM
    - Customers: 150
    - Runway: 18 months
    
    Team:
    CEO: John Doe (Former Google Engineer, 10 years experience)
    CTO: Jane Smith (Former Microsoft, 8 years experience)
    
    Market:
    TAM: $50B
    Competition: Slack, Microsoft Teams
    """


@pytest.fixture
def sample_risk_data():
    """Sample data for risk assessment testing."""
    return {
        "company_name": "TechFlow Solutions",
        "metrics": {
            "runway_months": 6,  # Short runway - high risk
            "churn_rate": 0.12,  # High churn - medium risk
            "monthly_growth_rate": -0.02,  # Negative growth - high risk
            "burn_rate": 200000,
            "revenue_arr": 1000000
        },
        "team": [
            {"name": "John Doe", "experience_years": 2}  # Low experience
        ],
        "market_data": {
            "total_addressable_market": 100000000,  # Small market
            "competitors": ["Comp1", "Comp2", "Comp3", "Comp4", "Comp5"]  # High competition
        },
        "industry": "fintech",  # Regulated industry
        "product_info": {
            "development_stage": "alpha",  # Early stage
            "intellectual_property": []  # No IP protection
        }
    }