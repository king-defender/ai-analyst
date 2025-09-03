import asyncio
from typing import Dict, Any, List
from app.models.startup import StartupData

class BenchmarkService:
    """Service for comparing startups against industry peers."""
    
    def __init__(self):
        # In production, this would connect to BigQuery
        pass
    
    async def get_benchmarks(self, file_id: str) -> Dict[str, Any]:
        """Get benchmark data for a file."""
        
        # For MVP, return sample benchmark data
        # In production, this would analyze the actual extracted data and query BigQuery
        
        sample_benchmark_data = {
            "peer_companies": [
                {
                    "name": "WorkflowMax",
                    "revenue": 3200000,
                    "growth_rate": 0.18,
                    "valuation": 45000000,
                    "stage": "Series A"
                },
                {
                    "name": "ProcessPro", 
                    "revenue": 4100000,
                    "growth_rate": 0.22,
                    "valuation": 58000000,
                    "stage": "Series A"
                },
                {
                    "name": "AutoFlow",
                    "revenue": 2800000,
                    "growth_rate": 0.15,
                    "valuation": 38000000,
                    "stage": "Series A"
                },
                {
                    "name": "StreamlineOps",
                    "revenue": 3800000,
                    "growth_rate": 0.20,
                    "valuation": 52000000,
                    "stage": "Series A"
                },
                {
                    "name": "FlowBuilder",
                    "revenue": 2200000,
                    "growth_rate": 0.12,
                    "valuation": 28000000,
                    "stage": "Series A"
                }
            ],
            "industry_metrics": {
                "median_revenue": 3200000,
                "median_growth": 0.18,
                "median_valuation": 45000000,
                "percentile_rank": 72
            }
        }
        
        return sample_benchmark_data
    
    async def get_benchmarks_detailed(self, startup_data: StartupData) -> Dict[str, Any]:
        """Get benchmark data for a startup."""
        
        # Simulate BigQuery processing delay
        await asyncio.sleep(2)
        
        # For MVP, return sample benchmark data
        # In production, this would query BigQuery for real peer data
        
        return {
            "peer_group": await self._get_peer_companies(startup_data),
            "industry_averages": await self._get_industry_averages(startup_data.industry),
            "percentile_rankings": await self._calculate_percentile_rankings(startup_data),
            "growth_comparisons": await self._get_growth_comparisons(startup_data)
        }
    
    async def _get_peer_companies(self, startup_data: StartupData) -> List[Dict[str, Any]]:
        """Get list of peer companies for benchmarking."""
        
        # Sample peer data for MVP
        return [
            {
                "name": "WorkflowMax",
                "stage": "Series A",
                "industry": "SaaS",
                "metrics": {
                    "revenue_arr": 3200000,
                    "monthly_growth_rate": 0.18,
                    "customer_count": 180,
                    "churn_rate": 0.04,
                    "gross_margin": 0.88
                },
                "last_funding_date": "2023-03-15",
                "total_funding": 12000000
            },
            {
                "name": "ProcessPro",
                "stage": "Series A",
                "industry": "SaaS",
                "metrics": {
                    "revenue_arr": 4100000,
                    "monthly_growth_rate": 0.22,
                    "customer_count": 220,
                    "churn_rate": 0.06,
                    "gross_margin": 0.82
                },
                "last_funding_date": "2023-01-20",
                "total_funding": 18000000
            },
            {
                "name": "AutoFlow",
                "stage": "Series A",
                "industry": "SaaS",
                "metrics": {
                    "revenue_arr": 2800000,
                    "monthly_growth_rate": 0.15,
                    "customer_count": 140,
                    "churn_rate": 0.05,
                    "gross_margin": 0.85
                },
                "last_funding_date": "2023-06-10",
                "total_funding": 8500000
            },
            {
                "name": "StreamlineOps",
                "stage": "Series A", 
                "industry": "SaaS",
                "metrics": {
                    "revenue_arr": 3800000,
                    "monthly_growth_rate": 0.20,
                    "customer_count": 195,
                    "churn_rate": 0.045,
                    "gross_margin": 0.87
                },
                "last_funding_date": "2023-04-05",
                "total_funding": 15000000
            },
            {
                "name": "FlowBuilder",
                "stage": "Series A",
                "industry": "SaaS", 
                "metrics": {
                    "revenue_arr": 2200000,
                    "monthly_growth_rate": 0.12,
                    "customer_count": 110,
                    "churn_rate": 0.07,
                    "gross_margin": 0.80
                },
                "last_funding_date": "2023-08-15",
                "total_funding": 6000000
            }
        ]
    
    async def _get_industry_averages(self, industry: str) -> Dict[str, Any]:
        """Get industry average metrics."""
        
        # Sample industry averages for SaaS
        return {
            "median_arr_growth": 0.18,
            "median_churn_rate": 0.05,
            "median_cac_payback": 8,
            "median_gross_margin": 0.85,
            "typical_funding_amounts": {
                "seed": 2000000,
                "series_a": 10000000,
                "series_b": 25000000
            }
        }
    
    async def _calculate_percentile_rankings(self, startup_data: StartupData) -> Dict[str, float]:
        """Calculate percentile rankings against peers."""
        
        # For MVP, return sample percentile rankings
        # In production, this would calculate actual rankings from peer data
        
        arr = startup_data.metrics.revenue_arr or 2500000
        growth = startup_data.metrics.monthly_growth_rate or 0.25
        
        # Simulate ranking calculation
        revenue_percentile = min(95, max(5, (arr / 5000000) * 100))
        growth_percentile = min(95, max(5, (growth / 0.3) * 100))
        
        return {
            "revenue_growth": growth_percentile,
            "customer_growth": 78,
            "funding_efficiency": 82,
            "team_experience": 88,
            "market_position": 72
        }
    
    async def _get_growth_comparisons(self, startup_data: StartupData) -> List[Dict[str, Any]]:
        """Get detailed growth comparisons against peers."""
        
        arr = startup_data.metrics.revenue_arr or 2500000
        growth_rate = startup_data.metrics.monthly_growth_rate or 0.25
        customers = startup_data.metrics.customer_count or 150
        
        return [
            {
                "metric": "revenue_growth",
                "company_value": growth_rate,
                "peer_median": 0.18,
                "peer_75th_percentile": 0.22,
                "peer_90th_percentile": 0.28,
                "ranking": "top_10" if growth_rate > 0.22 else "top_25" if growth_rate > 0.18 else "median"
            },
            {
                "metric": "annual_revenue",
                "company_value": arr,
                "peer_median": 3200000,
                "peer_75th_percentile": 3800000,
                "peer_90th_percentile": 4100000,
                "ranking": "below_median" if arr < 3200000 else "median"
            },
            {
                "metric": "customer_count",
                "company_value": customers,
                "peer_median": 180,
                "peer_75th_percentile": 200,
                "peer_90th_percentile": 220,
                "ranking": "below_median" if customers < 180 else "median"
            },
            {
                "metric": "funding_efficiency",
                "company_value": arr / (startup_data.financial_data.total_funding_raised / 1000000),
                "peer_median": 0.32,
                "peer_75th_percentile": 0.28,
                "peer_90th_percentile": 0.25,
                "ranking": "top_25"
            }
        ]
    
    async def get_market_positioning(self, startup_data: StartupData) -> Dict[str, Any]:
        """Get market positioning analysis."""
        
        return {
            "market_size_assessment": "Large and growing market",
            "competitive_positioning": "Strong differentiation",
            "market_share_potential": 0.05,
            "go_to_market_fit": "Strong product-market fit evidenced by growth",
            "barriers_to_entry": [
                "Network effects",
                "Data advantages", 
                "Integration complexity"
            ]
        }