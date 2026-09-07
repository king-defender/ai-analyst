from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# Enums
class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobStage(str, Enum):
    UPLOAD = "upload"
    OCR = "ocr"
    PARSING = "parsing"
    BENCHMARK = "benchmark"
    RISKS = "risks"
    MEMO = "memo"

class RiskSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RiskCategory(str, Enum):
    MARKET = "market"
    TEAM = "team"
    FINANCIAL = "financial"
    PRODUCT = "product"
    COMPETITIVE = "competitive"
    REGULATORY = "regulatory"

class InvestmentRecommendation(str, Enum):
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    HOLD = "hold"
    PASS = "pass"
    STRONG_PASS = "strong_pass"

# Base Models
class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TeamMember(BaseModel):
    name: str
    role: str
    bio: Optional[str] = None
    experience_years: Optional[int] = None
    previous_companies: Optional[List[str]] = []
    education: Optional[List[str]] = []

class StartupMetrics(BaseModel):
    revenue_arr: Optional[float] = None
    monthly_growth_rate: Optional[float] = None
    customer_count: Optional[int] = None
    churn_rate: Optional[float] = None
    ltv_cac_ratio: Optional[float] = None
    gross_margin: Optional[float] = None
    burn_rate: Optional[float] = None
    runway_months: Optional[int] = None

class UnitEconomics(BaseModel):
    cac: Optional[float] = None
    ltv: Optional[float] = None
    payback_period_months: Optional[int] = None

class FinancialData(BaseModel):
    current_valuation: Optional[float] = None
    last_funding_amount: Optional[float] = None
    total_funding_raised: Optional[float] = None
    burn_rate: Optional[float] = None
    runway_months: Optional[int] = None
    revenue_streams: List[str] = []
    unit_economics: UnitEconomics = UnitEconomics()

class Competitor(BaseModel):
    name: str
    description: str
    funding_raised: Optional[float] = None
    employee_count: Optional[int] = None
    market_share: Optional[float] = None

class MarketData(BaseModel):
    total_addressable_market: Optional[float] = None
    serviceable_addressable_market: Optional[float] = None
    target_market_size: Optional[float] = None
    market_growth_rate: Optional[float] = None
    competitors: List[Competitor] = []
    market_position: Optional[str] = None

class ProductInfo(BaseModel):
    product_name: Optional[str] = None
    product_type: Optional[str] = None
    key_features: List[str] = []
    technology_stack: Optional[List[str]] = []
    intellectual_property: List[str] = []
    development_stage: Optional[str] = None

class Partnership(BaseModel):
    partner_name: str
    partnership_type: str
    description: str
    value: Optional[str] = None

class UserGrowthMetrics(BaseModel):
    monthly_active_users: Optional[int] = None
    user_growth_rate: Optional[float] = None
    user_retention_rate: Optional[float] = None

class BusinessMetrics(BaseModel):
    revenue_growth: Optional[float] = None
    customer_acquisition_rate: Optional[float] = None
    market_penetration: Optional[float] = None

class TractionData(BaseModel):
    user_growth_metrics: UserGrowthMetrics = UserGrowthMetrics()
    business_metrics: BusinessMetrics = BusinessMetrics()
    partnerships: List[Partnership] = []
    awards_recognition: List[str] = []

class FundingRound(BaseModel):
    round_type: str
    amount: float
    date: str
    lead_investor: Optional[str] = None
    participating_investors: List[str] = []
    valuation: Optional[float] = None
    use_of_funds: List[str] = []

class StartupData(BaseModel):
    id: str
    company_name: str
    founded_year: int
    industry: str
    stage: str
    description: str
    team: List[TeamMember] = []
    metrics: StartupMetrics
    financial_data: FinancialData
    market_data: MarketData
    product_info: ProductInfo
    traction: TractionData
    funding_history: List[FundingRound] = []

class RiskFactor(BaseModel):
    category: RiskCategory
    risk_type: str
    severity: RiskSeverity
    description: str
    evidence: List[str] = []
    impact_description: str
    likelihood: float = Field(ge=0, le=1)
    potential_impact: int = Field(ge=1, le=10)

class RedFlag(BaseModel):
    type: str
    description: str
    evidence: List[str] = []
    severity_score: int = Field(ge=1, le=10)
    recommendation: str

class YellowFlag(BaseModel):
    type: str
    description: str
    evidence: List[str] = []
    monitoring_suggestion: str

class RiskAssessment(BaseModel):
    overall_risk_score: int = Field(ge=0, le=100)
    risk_factors: List[RiskFactor] = []
    red_flags: List[RedFlag] = []
    yellow_flags: List[YellowFlag] = []
    risk_mitigation_suggestions: List[str] = []

class Job(BaseModel):
    id: str
    status: JobStatus
    stage: JobStage
    progress: Optional[int] = Field(default=None, ge=0, le=100)
    message: Optional[str] = None
    file_id: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)