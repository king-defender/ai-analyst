import asyncio
from typing import Dict, Any
from datetime import datetime
from app.models.startup import StartupData, RiskAssessment, InvestmentRecommendation

class MemoService:
    """Service for generating investor memos using AI."""
    
    def __init__(self):
        # In production, this would use Vertex AI/Gemini for memo generation
        pass
    
    async def generate_memo(
        self, 
        startup_data: StartupData, 
        benchmark_data: Dict[str, Any],
        risk_assessment: RiskAssessment
    ) -> Dict[str, Any]:
        """Generate comprehensive investor memo."""
        
        # Simulate AI memo generation delay
        await asyncio.sleep(3)
        
        # For MVP, generate structured memo content
        # In production, this would use LLM with sophisticated prompts
        
        memo_id = f"memo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        executive_summary = await self._generate_executive_summary(startup_data, risk_assessment)
        investment_thesis = await self._generate_investment_thesis(startup_data, benchmark_data)
        market_analysis = await self._generate_market_analysis(startup_data, benchmark_data)
        team_assessment = await self._generate_team_assessment(startup_data)
        financial_analysis = await self._generate_financial_analysis(startup_data, benchmark_data)
        risk_analysis = await self._generate_risk_analysis(risk_assessment)
        recommendation = await self._generate_recommendation(startup_data, benchmark_data, risk_assessment)
        
        return {
            "id": memo_id,
            "company_name": startup_data.company_name,
            "generated_at": datetime.now().isoformat(),
            "executive_summary": executive_summary,
            "investment_thesis": investment_thesis,
            "market_analysis": market_analysis,
            "team_assessment": team_assessment,
            "financial_analysis": financial_analysis,
            "risk_analysis": risk_analysis,
            "recommendation": recommendation,
            "appendix": {
                "data_sources": ["Company pitch deck", "Industry databases", "Competitive analysis"],
                "analysis_date": datetime.now().strftime('%Y-%m-%d'),
                "analyst": "AI Analyst MVP",
                "confidence_level": 0.85
            }
        }
    
    async def _generate_executive_summary(self, startup_data: StartupData, risk_assessment: RiskAssessment) -> Dict[str, Any]:
        """Generate executive summary section."""
        
        # Determine key highlights
        highlights = []
        if startup_data.metrics.monthly_growth_rate and startup_data.metrics.monthly_growth_rate > 0.2:
            highlights.append(f"Strong growth trajectory: {startup_data.metrics.monthly_growth_rate:.1%} monthly growth")
        
        if startup_data.metrics.revenue_arr:
            highlights.append(f"${startup_data.metrics.revenue_arr/1000000:.1f}M ARR with proven revenue model")
        
        if len(startup_data.team) >= 3:
            highlights.append("Experienced founding team with relevant industry background")
        
        # Determine concerns
        concerns = []
        if risk_assessment.red_flags:
            concerns.extend([flag.type for flag in risk_assessment.red_flags[:2]])
        
        if risk_assessment.overall_risk_score > 70:
            concerns.append("Elevated overall risk profile requires careful monitoring")
        
        return {
            "company_overview": f"{startup_data.company_name} is a {startup_data.stage} {startup_data.industry} company that {startup_data.description.lower()}. Founded in {startup_data.founded_year}, the company has built a strong position in the {startup_data.industry.lower()} market.",
            "key_highlights": highlights or ["Strong market opportunity", "Experienced team", "Growing customer base"],
            "investment_highlights": [
                f"Large market opportunity: ${startup_data.market_data.total_addressable_market/1000000000:.1f}B TAM",
                f"Proven business model with {startup_data.metrics.gross_margin or 0.85:.0%} gross margins",
                "Clear path to scale with existing infrastructure"
            ],
            "concerns": concerns or ["Standard early-stage execution risks"],
            "recommendation_summary": f"{'Strong' if risk_assessment.overall_risk_score < 50 else 'Cautious'} investment opportunity with {'compelling' if startup_data.metrics.monthly_growth_rate and startup_data.metrics.monthly_growth_rate > 0.15 else 'solid'} growth potential."
        }
    
    async def _generate_investment_thesis(self, startup_data: StartupData, benchmark_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate investment thesis section."""
        
        return {
            "value_proposition": f"{startup_data.company_name} addresses the critical need for {startup_data.product_info.product_type.lower()} in the {startup_data.industry.lower()} market. Their solution provides significant value through automation and efficiency gains.",
            "market_opportunity": f"The {startup_data.industry.lower()} market represents a ${startup_data.market_data.total_addressable_market/1000000000:.1f}B opportunity growing at {startup_data.market_data.market_growth_rate:.1%} annually. With only ${startup_data.market_data.serviceable_addressable_market/1000000000:.1f}B serviceable addressable market, there's significant room for expansion.",
            "competitive_advantage": [
                f"First-mover advantage in {startup_data.industry.lower()} automation",
                "Strong technical team with deep domain expertise",
                "Proven customer traction and retention",
                "Scalable technology platform"
            ],
            "growth_potential": f"With current {startup_data.metrics.monthly_growth_rate or 0.2:.1%} monthly growth and expanding market, {startup_data.company_name} is well-positioned to capture significant market share over the next 3-5 years.",
            "exit_strategy": "Strategic acquisition by larger enterprise software companies or potential IPO path given market size and growth trajectory."
        }
    
    async def _generate_market_analysis(self, startup_data: StartupData, benchmark_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate market analysis section."""
        
        return {
            "market_size_assessment": f"Large and expanding market with ${startup_data.market_data.total_addressable_market/1000000000:.1f}B TAM growing at {startup_data.market_data.market_growth_rate:.1%} annually. Strong tailwinds from digital transformation trends.",
            "growth_projections": f"Market expected to reach ${startup_data.market_data.total_addressable_market * (1 + startup_data.market_data.market_growth_rate)**5 / 1000000000:.1f}B by 2029 based on current growth trajectory.",
            "competitive_landscape": f"Competitive but fragmented market with {len(startup_data.market_data.competitors)} major players. Opportunity for differentiation through superior product and customer experience.",
            "market_positioning": f"{startup_data.company_name} is positioned as {startup_data.market_data.market_position.lower()} with clear differentiation in their target segment.",
            "customer_validation": f"Strong customer validation evidenced by {startup_data.metrics.customer_count or 'growing'} customers and {startup_data.metrics.revenue_arr or 'significant'} ARR."
        }
    
    async def _generate_team_assessment(self, startup_data: StartupData) -> Dict[str, Any]:
        """Generate team assessment section."""
        
        total_experience = sum(member.experience_years for member in startup_data.team)
        avg_experience = total_experience / len(startup_data.team) if startup_data.team else 0
        
        return {
            "leadership_strength": f"Strong leadership team with average {avg_experience:.0f} years of relevant experience. Founding team brings complementary skills in technology, business, and market expertise.",
            "team_completeness": f"Core team of {len(startup_data.team)} members covers key functional areas. {('Additional hires needed in sales and engineering.' if len(startup_data.team) < 5 else 'Well-rounded team ready for scale.')}",
            "execution_capability": "Demonstrated execution capability through product development and customer acquisition milestones achieved to date.",
            "domain_expertise": "Team brings deep domain expertise from previous roles at leading technology companies and relevant industry experience.",
            "concerns": ["Team size may need expansion for rapid scaling"] if len(startup_data.team) < 4 else []
        }
    
    async def _generate_financial_analysis(self, startup_data: StartupData, benchmark_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate financial analysis section."""
        
        return {
            "revenue_model_assessment": f"Strong SaaS business model with {startup_data.metrics.revenue_arr or 'recurring'} ARR and proven unit economics. Multiple revenue streams provide diversification.",
            "unit_economics_analysis": f"Healthy unit economics with ${startup_data.financial_data.unit_economics.ltv or 1750:,.0f} LTV and ${startup_data.financial_data.unit_economics.cac or 500:,.0f} CAC, resulting in {(startup_data.financial_data.unit_economics.ltv or 1750)/(startup_data.financial_data.unit_economics.cac or 500):.1f}x LTV/CAC ratio.",
            "growth_trajectory": f"Strong growth momentum with {startup_data.metrics.monthly_growth_rate or 0.25:.1%} monthly growth rate above industry benchmarks.",
            "funding_requirements": f"${startup_data.financial_data.total_funding_raised/1000000:.1f}M raised to date. Additional funding will accelerate growth and market expansion.",
            "burn_rate_analysis": f"Current burn rate of ${startup_data.metrics.burn_rate or 150000:,.0f}/month provides {startup_data.metrics.runway_months or 18} months runway.",
            "runway_assessment": "Sufficient runway to achieve key milestones and reach next funding round with proper execution."
        }
    
    async def _generate_risk_analysis(self, risk_assessment: RiskAssessment) -> Dict[str, Any]:
        """Generate risk analysis section."""
        
        return {
            "key_risks": [factor.description for factor in risk_assessment.risk_factors[:5]],
            "risk_mitigation": "Management team aware of key risks with mitigation strategies in place. Board oversight and regular monitoring recommended.",
            "red_flags_summary": f"{'Critical issues identified requiring immediate attention' if risk_assessment.red_flags else 'No critical red flags identified in current analysis'}",
            "monitoring_recommendations": risk_assessment.risk_mitigation_suggestions[:3]
        }
    
    async def _generate_recommendation(
        self, 
        startup_data: StartupData, 
        benchmark_data: Dict[str, Any],
        risk_assessment: RiskAssessment
    ) -> Dict[str, Any]:
        """Generate investment recommendation."""
        
        # Determine recommendation based on multiple factors
        growth_score = min(100, (startup_data.metrics.monthly_growth_rate or 0.2) * 400)
        risk_score = 100 - risk_assessment.overall_risk_score
        market_score = min(100, startup_data.market_data.total_addressable_market / 100000000)
        
        overall_score = (growth_score + risk_score + market_score) / 3
        
        if overall_score >= 75:
            recommendation = InvestmentRecommendation.BUY
            confidence = 0.85
        elif overall_score >= 60:
            recommendation = InvestmentRecommendation.BUY
            confidence = 0.75
        elif overall_score >= 40:
            recommendation = InvestmentRecommendation.HOLD
            confidence = 0.65
        else:
            recommendation = InvestmentRecommendation.PASS
            confidence = 0.55
        
        valuation_low = (startup_data.metrics.revenue_arr or 2500000) * 8
        valuation_high = (startup_data.metrics.revenue_arr or 2500000) * 12
        
        return {
            "recommendation": recommendation.value,
            "confidence_level": confidence,
            "reasoning": [
                f"Strong growth trajectory: {startup_data.metrics.monthly_growth_rate or 0.25:.1%} monthly",
                f"Large market opportunity: ${startup_data.market_data.total_addressable_market/1000000000:.1f}B TAM",
                f"Risk-adjusted return profile: {overall_score:.0f}/100 score",
                "Experienced team with execution track record"
            ],
            "suggested_valuation_range": {
                "low": valuation_low,
                "high": valuation_high
            },
            "investment_amount_suggestion": min(5000000, valuation_low * 0.2),
            "terms_suggestions": [
                "Standard Series A terms with board seat",
                "Anti-dilution protection and pro-rata rights",
                "Performance milestones for follow-on investment"
            ],
            "next_steps": [
                "Conduct detailed due diligence on technology and IP",
                "Reference calls with existing customers",
                "Financial audit and legal review",
                "Negotiate term sheet and closing timeline"
            ]
        }