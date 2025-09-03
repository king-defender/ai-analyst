import asyncio
import json
import re
from typing import Dict, Any, Optional, List
from datetime import datetime

from app.models.startup import (
    StartupData, TeamMember, StartupMetrics, FinancialData, 
    UnitEconomics, MarketData, ProductInfo, TractionData,
    UserGrowthMetrics, BusinessMetrics, Partnership, FundingRound,
    Competitor
)

class ParsingService:
    """Service for parsing startup data from extracted text using LLM."""
    
    def __init__(self):
        # In production, this would initialize Vertex AI/Gemini client
        pass
    
    async def parse_startup_data(self, extracted_text: str) -> Optional[StartupData]:
        """Parse startup data from extracted text using AI."""
        
        if not extracted_text or len(extracted_text.strip()) < 50:
            return None
        
        # Simulate LLM processing delay
        await asyncio.sleep(3)
        
        # For MVP, return sample parsed data based on common patterns
        # In production, this would use Vertex AI/Gemini with structured prompts
        
        parsed_data = await self._extract_with_llm_simulation(extracted_text)
        
        try:
            return StartupData(**parsed_data)
        except Exception as e:
            print(f"Error creating StartupData: {e}")
            return None
    
    async def _extract_with_llm_simulation(self, text: str) -> Dict[str, Any]:
        """Simulate LLM extraction of structured data."""
        
        # Extract company name
        company_name = self._extract_company_name(text)
        
        # Extract financial metrics
        arr = self._extract_number(text, r'(\$?[\d.]+[MK]?)\s*ARR')
        growth_rate = self._extract_percentage(text, r'(\d+)%\s*(?:month|growth)')
        customer_count = self._extract_number(text, r'(\d+)\+?\s*(?:customers|clients)')
        
        # Extract funding information
        funding_amount = self._extract_number(text, r'(\$[\d.]+[MK]?)\s*(?:Series|seed|funding)')
        total_funding = self._extract_number(text, r'total.*?(\$[\d.]+[MK]?)')
        
        # Extract market data
        tam = self._extract_number(text, r'(\$[\d.]+[BM]?)\s*(?:TAM|Total.*Market)')
        sam = self._extract_number(text, r'(\$[\d.]+[BM]?)\s*(?:SAM|Serviceable.*Market)')
        
        return {
            "id": f"startup_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "company_name": company_name,
            "founded_year": 2022,  # Default for MVP
            "industry": self._extract_industry(text),
            "stage": self._extract_stage(text),
            "description": self._extract_description(text),
            "team": self._extract_team_members(text),
            "metrics": {
                "revenue_arr": arr,
                "monthly_growth_rate": growth_rate / 100 if growth_rate else None,
                "customer_count": customer_count,
                "churn_rate": 0.05,  # Default 5%
                "ltv_cac_ratio": 3.5,
                "gross_margin": 0.85,
                "burn_rate": 150000,  # $150K/month
                "runway_months": 18
            },
            "financial_data": {
                "current_valuation": None,
                "last_funding_amount": funding_amount,
                "total_funding_raised": total_funding or funding_amount or 2000000,
                "burn_rate": 150000,
                "runway_months": 18,
                "revenue_streams": ["SaaS Subscriptions", "Enterprise Licenses"],
                "unit_economics": {
                    "cac": 500,
                    "ltv": 1750,
                    "payback_period_months": 8
                }
            },
            "market_data": {
                "total_addressable_market": tam or 50000000000,
                "serviceable_addressable_market": sam or 8000000000,
                "target_market_size": 500000000,
                "market_growth_rate": 0.15,
                "competitors": self._extract_competitors(text),
                "market_position": "Growing market leader"
            },
            "product_info": {
                "product_name": company_name.split()[0] if company_name else "Platform",
                "product_type": "SaaS Platform",
                "key_features": [
                    "Automated workflow management",
                    "Real-time analytics",
                    "Third-party integrations",
                    "Mobile app"
                ],
                "technology_stack": ["Python", "React", "PostgreSQL", "AWS"],
                "intellectual_property": ["Workflow optimization algorithm"],
                "development_stage": "Production"
            },
            "traction": {
                "user_growth_metrics": {
                    "monthly_active_users": customer_count * 50 if customer_count else 7500,
                    "user_growth_rate": 0.25,
                    "user_retention_rate": 0.92
                },
                "business_metrics": {
                    "revenue_growth": growth_rate / 100 if growth_rate else 0.25,
                    "customer_acquisition_rate": 0.15,
                    "market_penetration": 0.02
                },
                "partnerships": [
                    {
                        "partner_name": "Microsoft",
                        "partnership_type": "Technology Integration",
                        "description": "Azure marketplace listing",
                        "value": "Additional distribution channel"
                    }
                ],
                "awards_recognition": ["Best SaaS Startup 2023"]
            },
            "funding_history": [
                {
                    "round_type": "Seed",
                    "amount": 2000000,
                    "date": "2023-01-15",
                    "lead_investor": "TechVentures",
                    "participating_investors": ["AngelList", "Individual Angels"],
                    "valuation": 10000000,
                    "use_of_funds": ["Product Development", "Team Expansion"]
                }
            ]
        }
    
    def _extract_company_name(self, text: str) -> str:
        """Extract company name from text."""
        # Look for patterns like "Company Name - Pitch Deck" or "Company Name Inc."
        patterns = [
            r'^([A-Z][a-zA-Z\s]+(?:Inc|LLC|Corp)?)\s*-',
            r'([A-Z][a-zA-Z\s]+(?:Solutions|Technologies|Systems|Pro|Flow))',
            r'^([A-Z][a-zA-Z\s]{2,20})\s*(?:Pitch|Deck|Overview)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "TechFlow Solutions"  # Default
    
    def _extract_number(self, text: str, pattern: str) -> Optional[float]:
        """Extract numerical value from text using regex pattern."""
        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            return None
        
        value_str = match.group(1).replace('$', '').replace(',', '')
        
        # Handle K and M suffixes
        if value_str.endswith('K'):
            return float(value_str[:-1]) * 1000
        elif value_str.endswith('M'):
            return float(value_str[:-1]) * 1000000
        elif value_str.endswith('B'):
            return float(value_str[:-1]) * 1000000000
        
        try:
            return float(value_str)
        except ValueError:
            return None
    
    def _extract_percentage(self, text: str, pattern: str) -> Optional[float]:
        """Extract percentage value from text."""
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                pass
        return None
    
    def _extract_industry(self, text: str) -> str:
        """Extract industry from text."""
        industries = {
            'saas': 'SaaS',
            'software': 'Software',
            'fintech': 'FinTech',
            'healthtech': 'HealthTech',
            'edtech': 'EdTech',
            'ecommerce': 'E-commerce',
            'marketplace': 'Marketplace',
            'data': 'Data & Analytics'
        }
        
        text_lower = text.lower()
        for keyword, industry in industries.items():
            if keyword in text_lower:
                return industry
        
        return 'Technology'
    
    def _extract_stage(self, text: str) -> str:
        """Extract funding stage from text."""
        text_lower = text.lower()
        
        if 'series a' in text_lower:
            return 'Series A'
        elif 'series b' in text_lower:
            return 'Series B'
        elif 'seed' in text_lower:
            return 'Seed'
        elif 'pre-seed' in text_lower:
            return 'Pre-Seed'
        
        return 'Seed'
    
    def _extract_description(self, text: str) -> str:
        """Extract company description."""
        # Look for common description patterns
        lines = text.split('\n')
        for line in lines:
            if any(word in line.lower() for word in ['overview', 'company', 'platform', 'solution']):
                if len(line.strip()) > 50:
                    return line.strip()
        
        return "AI-powered platform serving enterprise customers."
    
    def _extract_team_members(self, text: str) -> List[Dict[str, Any]]:
        """Extract team member information."""
        # For MVP, return sample team data
        # In production, would parse names, roles, and experience from text
        
        return [
            {
                "name": "Sarah Chen",
                "role": "CEO & Co-founder",
                "bio": "Former VP at Salesforce with 15 years in enterprise software",
                "experience_years": 15,
                "previous_companies": ["Salesforce", "Oracle"],
                "education": ["Stanford MBA", "UC Berkeley CS"]
            },
            {
                "name": "Mike Rodriguez",
                "role": "CTO & Co-founder", 
                "bio": "Ex-Google engineer with PhD in Computer Science",
                "experience_years": 12,
                "previous_companies": ["Google", "Microsoft"],
                "education": ["MIT PhD CS", "Caltech BS"]
            },
            {
                "name": "Lisa Wang",
                "role": "VP of Sales",
                "bio": "Built sales teams at 3 successful SaaS startups",
                "experience_years": 10,
                "previous_companies": ["HubSpot", "Zendesk"],
                "education": ["Harvard Business School"]
            }
        ]
    
    def _extract_competitors(self, text: str) -> List[Dict[str, Any]]:
        """Extract competitor information."""
        return [
            {
                "name": "WorkflowMax",
                "description": "Enterprise workflow management platform",
                "funding_raised": 50000000,
                "employee_count": 200,
                "market_share": 0.15
            },
            {
                "name": "ProcessPro",
                "description": "Automated business process management",
                "funding_raised": 75000000,
                "employee_count": 350,
                "market_share": 0.22
            }
        ]