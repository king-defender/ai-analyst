"""
Risk assessment engine with rule-based and ML-based checks.
"""

import asyncio
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class RiskType(Enum):
    FINANCIAL = "financial"
    MARKET = "market"
    TEAM = "team"
    PRODUCT = "product"
    COMPETITIVE = "competitive"
    REGULATORY = "regulatory"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class RiskRule:
    name: str
    category: RiskType
    severity: RiskLevel
    condition: callable
    description: str
    evidence_generator: callable
    impact_score: int  # 1-10
    likelihood: float  # 0-1

class RiskEngine:
    """Rule-based and ML-powered risk assessment engine."""
    
    def __init__(self):
        self.rules = self._initialize_rules()
    
    def _initialize_rules(self) -> List[RiskRule]:
        """Initialize all risk assessment rules."""
        return [
            # Financial Risks
            RiskRule(
                name="Short Runway",
                category=RiskType.FINANCIAL,
                severity=RiskLevel.HIGH,
                condition=lambda data: (
                    data.get("metrics", {}).get("runway_months", 24) < 12
                ),
                description="Company has less than 12 months of cash runway",
                evidence_generator=lambda data: [
                    f"Current runway: {data.get('metrics', {}).get('runway_months', 'unknown')} months"
                ],
                impact_score=9,
                likelihood=0.8
            ),
            
            RiskRule(
                name="High Burn Rate",
                category=RiskType.FINANCIAL,
                severity=RiskLevel.MEDIUM,
                condition=lambda data: (
                    data.get("metrics", {}).get("burn_rate", 0) * 12 > 
                    data.get("metrics", {}).get("revenue_arr", 0) * 0.8
                ),
                description="Monthly burn rate is high relative to revenue",
                evidence_generator=lambda data: [
                    f"Annual burn: ${data.get('metrics', {}).get('burn_rate', 0) * 12:,.0f}",
                    f"ARR: ${data.get('metrics', {}).get('revenue_arr', 0):,.0f}"
                ],
                impact_score=6,
                likelihood=0.7
            ),
            
            RiskRule(
                name="High Churn Rate",
                category=RiskType.FINANCIAL,
                severity=RiskLevel.HIGH,
                condition=lambda data: (
                    data.get("metrics", {}).get("churn_rate", 0) > 0.08
                ),
                description="Customer churn rate above healthy threshold",
                evidence_generator=lambda data: [
                    f"Monthly churn rate: {data.get('metrics', {}).get('churn_rate', 0):.1%}"
                ],
                impact_score=8,
                likelihood=0.9
            ),
            
            RiskRule(
                name="Negative Growth",
                category=RiskType.FINANCIAL,
                severity=RiskLevel.CRITICAL,
                condition=lambda data: (
                    data.get("metrics", {}).get("monthly_growth_rate", 0) < 0
                ),
                description="Company showing negative growth",
                evidence_generator=lambda data: [
                    f"Monthly growth rate: {data.get('metrics', {}).get('monthly_growth_rate', 0):.1%}"
                ],
                impact_score=10,
                likelihood=1.0
            ),
            
            # Market Risks
            RiskRule(
                name="Small Market Size",
                category=RiskType.MARKET,
                severity=RiskLevel.MEDIUM,
                condition=lambda data: (
                    data.get("market_data", {}).get("total_addressable_market", 0) < 1000000000
                ),
                description="Total addressable market is relatively small",
                evidence_generator=lambda data: [
                    f"TAM: ${data.get('market_data', {}).get('total_addressable_market', 0)/1000000:.0f}M"
                ],
                impact_score=5,
                likelihood=0.6
            ),
            
            RiskRule(
                name="Slow Market Growth",
                category=RiskType.MARKET,
                severity=RiskLevel.MEDIUM,
                condition=lambda data: (
                    data.get("market_data", {}).get("market_growth_rate", 0) < 0.1
                ),
                description="Market growing slower than expected",
                evidence_generator=lambda data: [
                    f"Market growth rate: {data.get('market_data', {}).get('market_growth_rate', 0):.1%}"
                ],
                impact_score=6,
                likelihood=0.7
            ),
            
            RiskRule(
                name="High Competition",
                category=RiskType.COMPETITIVE,
                severity=RiskLevel.MEDIUM,
                condition=lambda data: (
                    len(data.get("market_data", {}).get("competitors", [])) > 5
                ),
                description="Highly competitive market with many players",
                evidence_generator=lambda data: [
                    f"Number of competitors: {len(data.get('market_data', {}).get('competitors', []))}"
                ],
                impact_score=5,
                likelihood=0.8
            ),
            
            # Team Risks
            RiskRule(
                name="Small Team Size",
                category=RiskType.TEAM,
                severity=RiskLevel.MEDIUM,
                condition=lambda data: (
                    len(data.get("team", [])) < 3
                ),
                description="Very small founding team may limit execution",
                evidence_generator=lambda data: [
                    f"Team size: {len(data.get('team', []))} members"
                ],
                impact_score=6,
                likelihood=0.6
            ),
            
            RiskRule(
                name="Inexperienced Team",
                category=RiskType.TEAM,
                severity=RiskLevel.HIGH,
                condition=lambda data: (
                    sum(member.get("experience_years", 0) for member in data.get("team", [])) /
                    max(len(data.get("team", [])), 1) < 5
                ),
                description="Team lacks sufficient industry experience",
                evidence_generator=lambda data: [
                    f"Average experience: {sum(member.get('experience_years', 0) for member in data.get('team', [])) / max(len(data.get('team', [])), 1):.1f} years"
                ],
                impact_score=7,
                likelihood=0.8
            ),
            
            # Product Risks
            RiskRule(
                name="Early Stage Product",
                category=RiskType.PRODUCT,
                severity=RiskLevel.HIGH,
                condition=lambda data: (
                    data.get("product_info", {}).get("development_stage", "").lower() 
                    in ["concept", "prototype", "alpha"]
                ),
                description="Product in very early development stage",
                evidence_generator=lambda data: [
                    f"Development stage: {data.get('product_info', {}).get('development_stage', 'unknown')}"
                ],
                impact_score=8,
                likelihood=0.6
            ),
            
            RiskRule(
                name="Limited IP Protection",
                category=RiskType.PRODUCT,
                severity=RiskLevel.MEDIUM,
                condition=lambda data: (
                    len(data.get("product_info", {}).get("intellectual_property", [])) == 0
                ),
                description="No intellectual property protection identified",
                evidence_generator=lambda data: [
                    "No patents, trademarks, or trade secrets mentioned"
                ],
                impact_score=4,
                likelihood=0.5
            ),
            
            # Regulatory Risks
            RiskRule(
                name="Regulated Industry",
                category=RiskType.REGULATORY,
                severity=RiskLevel.MEDIUM,
                condition=lambda data: (
                    data.get("industry", "").lower() in 
                    ["fintech", "healthtech", "finance", "healthcare", "banking"]
                ),
                description="Operating in heavily regulated industry",
                evidence_generator=lambda data: [
                    f"Industry: {data.get('industry', 'unknown')}"
                ],
                impact_score=6,
                likelihood=0.7
            )
        ]
    
    async def assess_startup(self, startup_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run comprehensive risk assessment on startup data."""
        
        risk_factors = []
        red_flags = []
        yellow_flags = []
        
        # Apply all rules
        for rule in self.rules:
            try:
                if rule.condition(startup_data):
                    risk_factor = {
                        "category": rule.category.value,
                        "risk_type": rule.name,
                        "severity": rule.severity.value,
                        "description": rule.description,
                        "evidence": rule.evidence_generator(startup_data),
                        "impact_description": f"Potential impact on {rule.category.value} performance",
                        "likelihood": rule.likelihood,
                        "potential_impact": rule.impact_score
                    }
                    
                    risk_factors.append(risk_factor)
                    
                    # Categorize as red or yellow flag
                    if rule.severity in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                        red_flags.append({
                            "type": rule.name,
                            "description": rule.description,
                            "evidence": rule.evidence_generator(startup_data),
                            "severity_score": rule.impact_score,
                            "recommendation": f"Address {rule.name.lower()} immediately"
                        })
                    elif rule.severity == RiskLevel.MEDIUM:
                        yellow_flags.append({
                            "type": rule.name,
                            "description": rule.description,
                            "evidence": rule.evidence_generator(startup_data),
                            "monitoring_suggestion": f"Monitor {rule.name.lower()} closely"
                        })
                        
            except Exception as e:
                print(f"Error applying rule {rule.name}: {e}")
                continue
        
        # Calculate overall risk score
        overall_risk_score = self._calculate_overall_risk_score(risk_factors)
        
        # Generate mitigation suggestions
        mitigation_suggestions = self._generate_mitigation_suggestions(risk_factors)
        
        return {
            "overall_risk_score": overall_risk_score,
            "risk_factors": risk_factors,
            "red_flags": red_flags,
            "yellow_flags": yellow_flags,
            "risk_mitigation_suggestions": mitigation_suggestions
        }
    
    def _calculate_overall_risk_score(self, risk_factors: List[Dict]) -> int:
        """Calculate overall risk score (0-100)."""
        if not risk_factors:
            return 30  # Base risk for any startup
        
        total_weighted_risk = 0
        total_weight = 0
        
        for factor in risk_factors:
            severity_weights = {
                "low": 1,
                "medium": 2, 
                "high": 4,
                "critical": 6
            }
            
            weight = severity_weights.get(factor["severity"], 2)
            risk_score = factor["potential_impact"] * factor["likelihood"] * weight
            
            total_weighted_risk += risk_score
            total_weight += weight
        
        # Normalize to 0-100 scale
        base_score = 30
        additional_risk = min(70, (total_weighted_risk / max(total_weight, 1)) * 10)
        
        return min(100, int(base_score + additional_risk))
    
    def _generate_mitigation_suggestions(self, risk_factors: List[Dict]) -> List[str]:
        """Generate risk mitigation suggestions."""
        suggestions = []
        categories = set(factor["category"] for factor in risk_factors)
        
        category_suggestions = {
            "financial": [
                "Develop detailed financial forecasting and cash management plans",
                "Consider revenue-based financing or venture debt to extend runway",
                "Implement strict cost controls and milestone-based spending"
            ],
            "market": [
                "Conduct regular competitive analysis and market research", 
                "Develop clear differentiation strategy and value proposition",
                "Consider adjacent markets for expansion opportunities"
            ],
            "team": [
                "Plan strategic hiring to fill critical skill gaps",
                "Establish strong advisory board with relevant expertise",
                "Implement knowledge management and succession planning"
            ],
            "product": [
                "Accelerate product development with clear milestones",
                "Establish regular customer feedback loops",
                "Consider intellectual property protection strategies"
            ],
            "competitive": [
                "Monitor competitor activities and market positioning",
                "Focus on unique value proposition and customer loyalty",
                "Build strong barriers to entry through network effects or data"
            ],
            "regulatory": [
                "Engage regulatory experts and legal counsel early",
                "Build compliance into product development process",
                "Monitor regulatory changes and industry trends"
            ]
        }
        
        for category in categories:
            if category in category_suggestions:
                suggestions.extend(category_suggestions[category][:2])
        
        return suggestions[:6]  # Limit to top 6 suggestions