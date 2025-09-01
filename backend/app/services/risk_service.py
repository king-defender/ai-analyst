import asyncio
from typing import Dict, Any
from app.models.startup import (
    StartupData, RiskAssessment, RiskFactor, RedFlag, YellowFlag,
    RiskSeverity, RiskCategory
)

class RiskService:
    """Service for assessing investment risks in startups."""
    
    def __init__(self):
        # In production, this would use Vertex AI for risk analysis
        pass
    
    async def assess_risks(
        self, 
        startup_data: StartupData, 
        benchmark_data: Dict[str, Any]
    ) -> RiskAssessment:
        """Perform comprehensive risk assessment."""
        
        # Simulate AI risk analysis delay
        await asyncio.sleep(2)
        
        risk_factors = await self._analyze_risk_factors(startup_data, benchmark_data)
        red_flags = await self._identify_red_flags(startup_data, benchmark_data)
        yellow_flags = await self._identify_yellow_flags(startup_data, benchmark_data)
        
        # Calculate overall risk score
        overall_risk_score = await self._calculate_overall_risk_score(
            risk_factors, red_flags, yellow_flags
        )
        
        mitigation_suggestions = await self._generate_mitigation_suggestions(
            risk_factors, red_flags
        )
        
        return RiskAssessment(
            overall_risk_score=overall_risk_score,
            risk_factors=risk_factors,
            red_flags=red_flags,
            yellow_flags=yellow_flags,
            risk_mitigation_suggestions=mitigation_suggestions
        )
    
    async def _analyze_risk_factors(
        self, 
        startup_data: StartupData, 
        benchmark_data: Dict[str, Any]
    ) -> list[RiskFactor]:
        """Identify and analyze various risk factors."""
        
        risk_factors = []
        
        # Market risks
        if startup_data.market_data.market_growth_rate < 0.1:
            risk_factors.append(RiskFactor(
                category=RiskCategory.MARKET,
                risk_type="Slow Market Growth",
                severity=RiskSeverity.MEDIUM,
                description="Market is growing slower than industry average",
                evidence=[f"Market growth rate: {startup_data.market_data.market_growth_rate:.1%}"],
                impact_description="Limited expansion opportunities and increased competition",
                likelihood=0.7,
                potential_impact=6
            ))
        
        # Financial risks
        if startup_data.metrics.runway_months and startup_data.metrics.runway_months < 12:
            risk_factors.append(RiskFactor(
                category=RiskCategory.FINANCIAL,
                risk_type="Short Runway",
                severity=RiskSeverity.HIGH,
                description="Limited cash runway may require immediate funding",
                evidence=[f"Current runway: {startup_data.metrics.runway_months} months"],
                impact_description="Risk of running out of cash before next funding round",
                likelihood=0.8,
                potential_impact=9
            ))
        
        # Team risks
        if len(startup_data.team) < 3:
            risk_factors.append(RiskFactor(
                category=RiskCategory.TEAM,
                risk_type="Small Team Size",
                severity=RiskSeverity.MEDIUM,
                description="Limited team size may constrain execution",
                evidence=[f"Current team size: {len(startup_data.team)} members"],
                impact_description="Potential bottlenecks in product development and customer support",
                likelihood=0.6,
                potential_impact=5
            ))
        
        # Competitive risks
        if len(startup_data.market_data.competitors) > 5:
            risk_factors.append(RiskFactor(
                category=RiskCategory.COMPETITIVE,
                risk_type="High Competition",
                severity=RiskSeverity.MEDIUM,
                description="Crowded competitive landscape",
                evidence=[f"Number of identified competitors: {len(startup_data.market_data.competitors)}"],
                impact_description="Difficulty in market differentiation and customer acquisition",
                likelihood=0.7,
                potential_impact=6
            ))
        
        # Product risks
        if startup_data.product_info.development_stage not in ["Production", "Beta"]:
            risk_factors.append(RiskFactor(
                category=RiskCategory.PRODUCT,
                risk_type="Early Development Stage",
                severity=RiskSeverity.HIGH,
                description="Product still in early development phase",
                evidence=[f"Development stage: {startup_data.product_info.development_stage}"],
                impact_description="Uncertainty in product-market fit and time to market",
                likelihood=0.5,
                potential_impact=8
            ))
        
        return risk_factors
    
    async def _identify_red_flags(
        self, 
        startup_data: StartupData, 
        benchmark_data: Dict[str, Any]
    ) -> list[RedFlag]:
        """Identify critical red flags."""
        
        red_flags = []
        
        # High churn rate
        if startup_data.metrics.churn_rate and startup_data.metrics.churn_rate > 0.1:
            red_flags.append(RedFlag(
                type="High Customer Churn",
                description="Customer churn rate significantly above industry average",
                evidence=[
                    f"Current churn rate: {startup_data.metrics.churn_rate:.1%}",
                    f"Industry average: ~5%"
                ],
                severity_score=8,
                recommendation="Immediate focus on customer success and product improvements required"
            ))
        
        # Negative growth
        if startup_data.metrics.monthly_growth_rate and startup_data.metrics.monthly_growth_rate < 0:
            red_flags.append(RedFlag(
                type="Negative Growth",
                description="Company showing negative month-over-month growth",
                evidence=[f"Monthly growth rate: {startup_data.metrics.monthly_growth_rate:.1%}"],
                severity_score=9,
                recommendation="Critical business model and strategy review needed"
            ))
        
        # Very short runway
        if startup_data.metrics.runway_months and startup_data.metrics.runway_months < 6:
            red_flags.append(RedFlag(
                type="Critical Cash Position",
                description="Less than 6 months of cash runway remaining",
                evidence=[f"Cash runway: {startup_data.metrics.runway_months} months"],
                severity_score=10,
                recommendation="Immediate fundraising or cost reduction measures required"
            ))
        
        return red_flags
    
    async def _identify_yellow_flags(
        self, 
        startup_data: StartupData, 
        benchmark_data: Dict[str, Any]
    ) -> list[YellowFlag]:
        """Identify areas requiring monitoring."""
        
        yellow_flags = []
        
        # Below-average growth
        industry_avg_growth = benchmark_data.get("industry_averages", {}).get("median_arr_growth", 0.18)
        if (startup_data.metrics.monthly_growth_rate and 
            startup_data.metrics.monthly_growth_rate < industry_avg_growth):
            yellow_flags.append(YellowFlag(
                type="Below Average Growth",
                description="Growth rate below industry median",
                evidence=[
                    f"Company growth: {startup_data.metrics.monthly_growth_rate:.1%}",
                    f"Industry median: {industry_avg_growth:.1%}"
                ],
                monitoring_suggestion="Track growth metrics monthly and identify acceleration strategies"
            ))
        
        # Limited funding history
        if len(startup_data.funding_history) < 2:
            yellow_flags.append(YellowFlag(
                type="Limited Funding History",
                description="Few previous funding rounds may indicate investor concerns",
                evidence=[f"Number of funding rounds: {len(startup_data.funding_history)}"],
                monitoring_suggestion="Monitor investor interest and funding pipeline closely"
            ))
        
        # High burn rate relative to revenue
        if (startup_data.metrics.burn_rate and startup_data.metrics.revenue_arr and
            startup_data.metrics.burn_rate * 12 > startup_data.metrics.revenue_arr * 0.8):
            yellow_flags.append(YellowFlag(
                type="High Burn Rate",
                description="Burn rate high relative to current revenue",
                evidence=[
                    f"Annual burn: ${startup_data.metrics.burn_rate * 12:,.0f}",
                    f"ARR: ${startup_data.metrics.revenue_arr:,.0f}"
                ],
                monitoring_suggestion="Track path to profitability and unit economics improvement"
            ))
        
        return yellow_flags
    
    async def _calculate_overall_risk_score(
        self, 
        risk_factors: list[RiskFactor], 
        red_flags: list[RedFlag], 
        yellow_flags: list[YellowFlag]
    ) -> int:
        """Calculate overall risk score (0-100, higher = riskier)."""
        
        base_score = 30  # Base risk score
        
        # Add points for risk factors
        for factor in risk_factors:
            severity_multiplier = {
                RiskSeverity.LOW: 1,
                RiskSeverity.MEDIUM: 2,
                RiskSeverity.HIGH: 4,
                RiskSeverity.CRITICAL: 6
            }.get(factor.severity, 2)
            
            base_score += factor.potential_impact * factor.likelihood * severity_multiplier
        
        # Add heavy penalty for red flags
        for flag in red_flags:
            base_score += flag.severity_score * 2
        
        # Add minor penalty for yellow flags
        base_score += len(yellow_flags) * 3
        
        return min(100, max(0, int(base_score)))
    
    async def _generate_mitigation_suggestions(
        self, 
        risk_factors: list[RiskFactor], 
        red_flags: list[RedFlag]
    ) -> list[str]:
        """Generate risk mitigation suggestions."""
        
        suggestions = []
        
        # Category-based suggestions
        categories = set(factor.category for factor in risk_factors)
        
        if RiskCategory.FINANCIAL in categories:
            suggestions.append("Develop detailed financial forecasts and establish clear metrics for fundraising triggers")
            suggestions.append("Consider revenue-based financing or venture debt to extend runway")
        
        if RiskCategory.MARKET in categories:
            suggestions.append("Conduct regular competitive analysis and market research")
            suggestions.append("Develop clear differentiation strategy and unique value proposition")
        
        if RiskCategory.TEAM in categories:
            suggestions.append("Plan strategic hiring to fill key skill gaps")
            suggestions.append("Implement strong advisory board with relevant industry experience")
        
        if RiskCategory.PRODUCT in categories:
            suggestions.append("Establish regular customer feedback loops and product iteration cycles")
            suggestions.append("Develop comprehensive product roadmap with clear milestones")
        
        # Red flag specific suggestions
        if red_flags:
            suggestions.append("Address critical red flags immediately with board oversight")
            suggestions.append("Consider bringing in experienced interim executives for crisis management")
        
        return suggestions[:6]  # Limit to top 6 suggestions