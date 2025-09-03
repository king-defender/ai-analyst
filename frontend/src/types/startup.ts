export interface StartupData {
  id: string;
  company_name: string;
  founded_year: number;
  industry: string;
  stage: string;
  description: string;
  team: TeamMember[];
  metrics: StartupMetrics;
  financial_data: FinancialData;
  market_data: MarketData;
  product_info: ProductInfo;
  traction: TractionData;
  funding_history: FundingRound[];
}

export interface TeamMember {
  name: string;
  role: string;
  bio: string;
  experience_years: number;
  previous_companies?: string[];
  education?: string[];
}

export interface StartupMetrics {
  revenue_arr?: number;
  monthly_growth_rate?: number;
  customer_count?: number;
  churn_rate?: number;
  ltv_cac_ratio?: number;
  gross_margin?: number;
  burn_rate?: number;
  runway_months?: number;
}

export interface FinancialData {
  current_valuation?: number;
  last_funding_amount?: number;
  total_funding_raised: number;
  burn_rate?: number;
  runway_months?: number;
  revenue_streams: string[];
  unit_economics: {
    cac?: number;
    ltv?: number;
    payback_period_months?: number;
  };
}

export interface MarketData {
  total_addressable_market: number;
  serviceable_addressable_market: number;
  target_market_size: number;
  market_growth_rate: number;
  competitors: Competitor[];
  market_position: string;
}

export interface Competitor {
  name: string;
  description: string;
  funding_raised?: number;
  employee_count?: number;
  market_share?: number;
}

export interface ProductInfo {
  product_name: string;
  product_type: string;
  key_features: string[];
  technology_stack?: string[];
  intellectual_property: string[];
  development_stage: string;
}

export interface TractionData {
  user_growth_metrics: {
    monthly_active_users?: number;
    user_growth_rate?: number;
    user_retention_rate?: number;
  };
  business_metrics: {
    revenue_growth?: number;
    customer_acquisition_rate?: number;
    market_penetration?: number;
  };
  partnerships: Partnership[];
  awards_recognition: string[];
}

export interface Partnership {
  partner_name: string;
  partnership_type: string;
  description: string;
  value?: string;
}

export interface FundingRound {
  round_type: string;
  amount: number;
  date: string;
  lead_investor?: string;
  participating_investors: string[];
  valuation?: number;
  use_of_funds: string[];
}

export interface BenchmarkData {
  peer_group: PeerCompany[];
  industry_averages: IndustryMetrics;
  percentile_rankings: PercentileRankings;
  growth_comparisons: GrowthComparison[];
}

export interface PeerCompany {
  name: string;
  stage: string;
  industry: string;
  metrics: StartupMetrics;
  last_funding_date: string;
  total_funding: number;
}

export interface IndustryMetrics {
  median_arr_growth: number;
  median_churn_rate: number;
  median_cac_payback: number;
  median_gross_margin: number;
  typical_funding_amounts: Record<string, number>;
}

export interface PercentileRankings {
  revenue_growth: number;
  customer_growth: number;
  funding_efficiency: number;
  team_experience: number;
  market_position: number;
}

export interface GrowthComparison {
  metric: string;
  company_value: number;
  peer_median: number;
  peer_75th_percentile: number;
  peer_90th_percentile: number;
  ranking: 'top_10' | 'top_25' | 'median' | 'below_median';
}

export interface RiskAssessment {
  overall_risk_score: number;
  risk_factors: RiskFactor[];
  red_flags: RedFlag[];
  yellow_flags: YellowFlag[];
  risk_mitigation_suggestions: string[];
}

export interface RiskFactor {
  category: 'market' | 'team' | 'financial' | 'product' | 'competitive' | 'regulatory';
  risk_type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  evidence: string[];
  impact_description: string;
  likelihood: number;
  potential_impact: number;
}

export interface RedFlag {
  type: string;
  description: string;
  evidence: string[];
  severity_score: number;
  recommendation: string;
}

export interface YellowFlag {
  type: string;
  description: string;
  evidence: string[];
  monitoring_suggestion: string;
}

export interface InvestorMemo {
  id: string;
  company_name: string;
  generated_at: string;
  executive_summary: ExecutiveSummary;
  investment_thesis: InvestmentThesis;
  market_analysis: MarketAnalysis;
  team_assessment: TeamAssessment;
  financial_analysis: FinancialAnalysis;
  risk_analysis: RiskAnalysisSection;
  recommendation: InvestmentRecommendation;
  appendix: MemoAppendix;
}

export interface ExecutiveSummary {
  company_overview: string;
  key_highlights: string[];
  investment_highlights: string[];
  concerns: string[];
  recommendation_summary: string;
}

export interface InvestmentThesis {
  value_proposition: string;
  market_opportunity: string;
  competitive_advantage: string[];
  growth_potential: string;
  exit_strategy: string;
}

export interface MarketAnalysis {
  market_size_assessment: string;
  growth_projections: string;
  competitive_landscape: string;
  market_positioning: string;
  customer_validation: string;
}

export interface TeamAssessment {
  leadership_strength: string;
  team_completeness: string;
  execution_capability: string;
  domain_expertise: string;
  concerns: string[];
}

export interface FinancialAnalysis {
  revenue_model_assessment: string;
  unit_economics_analysis: string;
  growth_trajectory: string;
  funding_requirements: string;
  burn_rate_analysis: string;
  runway_assessment: string;
}

export interface RiskAnalysisSection {
  key_risks: string[];
  risk_mitigation: string;
  red_flags_summary: string;
  monitoring_recommendations: string[];
}

export interface InvestmentRecommendation {
  recommendation: 'strong_buy' | 'buy' | 'hold' | 'pass' | 'strong_pass';
  confidence_level: number;
  reasoning: string[];
  suggested_valuation_range: {
    low: number;
    high: number;
  };
  investment_amount_suggestion: number;
  terms_suggestions: string[];
  next_steps: string[];
}

export interface MemoAppendix {
  raw_data: any;
  methodology: string;
  assumptions: string[];
  data_sources: string[];
  confidence_scores: {
    financial_analysis: number;
    market_analysis: number;
    team_assessment: number;
    risk_analysis: number;
  };
}