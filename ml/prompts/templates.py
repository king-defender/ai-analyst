"""
Prompt templates for AI Analyst ML pipeline.
"""

STARTUP_DATA_EXTRACTION_PROMPT = """
You are an expert startup analyst. Extract structured information from this pitch deck text and return it as JSON.

IMPORTANT: Return ONLY valid JSON without any additional text or formatting.

Extract the following information:

REQUIRED FIELDS:
- company_name: string
- founded_year: integer (estimate if not provided)
- industry: string (SaaS, FinTech, HealthTech, etc.)
- stage: string (Pre-Seed, Seed, Series A, B, C, etc.)
- description: string (1-2 sentence company description)

TEAM INFORMATION:
- team: array of objects with name, role, bio, experience_years

FINANCIAL METRICS:
- revenue_arr: number (annual recurring revenue)
- monthly_growth_rate: number (as decimal, e.g., 0.25 for 25%)
- customer_count: integer
- burn_rate: number (monthly burn rate)
- total_funding_raised: number

MARKET DATA:
- total_addressable_market: number
- market_growth_rate: number (as decimal)
- competitors: array of competitor names

PRODUCT INFORMATION:
- product_name: string
- product_type: string
- key_features: array of strings

If information is not available, use reasonable estimates based on industry standards or mark as null.

PITCH DECK TEXT:
{pitch_deck_text}

JSON OUTPUT:
"""

RISK_ASSESSMENT_PROMPT = """
You are a senior investment analyst specializing in startup risk assessment. Analyze this startup data and identify potential risks.

Return a JSON object with the following structure:

{{
  "risk_factors": [
    {{
      "category": "market|team|financial|product|competitive|regulatory",
      "risk_type": "string",
      "severity": "low|medium|high|critical", 
      "description": "string",
      "evidence": ["string"],
      "likelihood": 0.0-1.0,
      "potential_impact": 1-10
    }}
  ],
  "red_flags": [
    {{
      "type": "string",
      "description": "string", 
      "evidence": ["string"],
      "severity_score": 1-10,
      "recommendation": "string"
    }}
  ],
  "yellow_flags": [
    {{
      "type": "string",
      "description": "string",
      "evidence": ["string"], 
      "monitoring_suggestion": "string"
    }}
  ],
  "risk_mitigation_suggestions": ["string"]
}}

STARTUP DATA:
{startup_data}

BENCHMARK DATA:
{benchmark_data}

Focus on:
1. Financial sustainability and burn rate
2. Market competition and positioning
3. Team experience and completeness
4. Product-market fit indicators
5. Regulatory or compliance risks
6. Execution risks

Be thorough but realistic in your assessment.

JSON OUTPUT:
"""

MEMO_GENERATION_PROMPT = """
You are a senior investment analyst at a top-tier VC firm. Generate a comprehensive investment memo for this startup.

Return a JSON object with the following structure:

{{
  "executive_summary": {{
    "company_overview": "string",
    "key_highlights": ["string"],
    "investment_highlights": ["string"],
    "concerns": ["string"],
    "recommendation_summary": "string"
  }},
  "investment_thesis": {{
    "value_proposition": "string",
    "market_opportunity": "string", 
    "competitive_advantage": ["string"],
    "growth_potential": "string",
    "exit_strategy": "string"
  }},
  "market_analysis": {{
    "market_size_assessment": "string",
    "growth_projections": "string",
    "competitive_landscape": "string",
    "market_positioning": "string",
    "customer_validation": "string"
  }},
  "team_assessment": {{
    "leadership_strength": "string",
    "team_completeness": "string", 
    "execution_capability": "string",
    "domain_expertise": "string",
    "concerns": ["string"]
  }},
  "financial_analysis": {{
    "revenue_model_assessment": "string",
    "unit_economics_analysis": "string",
    "growth_trajectory": "string", 
    "funding_requirements": "string",
    "burn_rate_analysis": "string",
    "runway_assessment": "string"
  }},
  "risk_analysis": {{
    "key_risks": ["string"],
    "risk_mitigation": "string",
    "red_flags_summary": "string",
    "monitoring_recommendations": ["string"]
  }},
  "recommendation": {{
    "recommendation": "strong_buy|buy|hold|pass|strong_pass",
    "confidence_level": 0.0-1.0,
    "reasoning": ["string"],
    "suggested_valuation_range": {{
      "low": number,
      "high": number
    }},
    "investment_amount_suggestion": number,
    "terms_suggestions": ["string"],
    "next_steps": ["string"]
  }}
}}

STARTUP DATA:
{startup_data}

BENCHMARK DATA:
{benchmark_data}

RISK ASSESSMENT:
{risk_assessment}

Write in a professional, analytical tone suitable for institutional investors. Be specific with numbers and provide clear reasoning for all assessments.

JSON OUTPUT:
"""

BENCHMARK_QUERY_PROMPT = """
You are a data analyst specializing in startup benchmarking. Based on the provided startup information, generate realistic benchmark data that would be found in a comprehensive industry database.

Return a JSON object with the following structure:

{{
  "peer_group": [
    {{
      "name": "string",
      "stage": "string", 
      "industry": "string",
      "metrics": {{
        "revenue_arr": number,
        "monthly_growth_rate": number,
        "customer_count": number,
        "churn_rate": number,
        "gross_margin": number
      }},
      "last_funding_date": "YYYY-MM-DD",
      "total_funding": number
    }}
  ],
  "industry_averages": {{
    "median_arr_growth": number,
    "median_churn_rate": number,
    "median_cac_payback": number,
    "median_gross_margin": number
  }},
  "percentile_rankings": {{
    "revenue_growth": number,
    "customer_growth": number,
    "funding_efficiency": number,
    "team_experience": number,
    "market_position": number
  }},
  "growth_comparisons": [
    {{
      "metric": "string",
      "company_value": number,
      "peer_median": number,
      "peer_75th_percentile": number,
      "peer_90th_percentile": number,
      "ranking": "top_10|top_25|median|below_median"
    }}
  ]
}}

Generate 8-12 realistic peer companies in the same industry and stage. Use industry-standard metrics and realistic growth rates.

STARTUP DATA:
{startup_data}

JSON OUTPUT:
"""

# Evaluation prompts
EXTRACTION_QUALITY_PROMPT = """
Evaluate the quality of this startup data extraction. Rate each field on accuracy and completeness.

Return a JSON object with scores 0-1 for each category:

{{
  "overall_quality": 0.0-1.0,
  "field_scores": {{
    "company_basics": 0.0-1.0,
    "financial_metrics": 0.0-1.0,
    "team_information": 0.0-1.0,
    "market_data": 0.0-1.0,
    "product_info": 0.0-1.0
  }},
  "missing_fields": ["string"],
  "quality_issues": ["string"],
  "confidence_level": 0.0-1.0
}}

ORIGINAL TEXT:
{original_text}

EXTRACTED DATA:
{extracted_data}

JSON OUTPUT:
"""

RISK_ACCURACY_PROMPT = """
Evaluate the accuracy and completeness of this risk assessment. Focus on whether important risks were identified and properly categorized.

Return a JSON object:

{{
  "overall_accuracy": 0.0-1.0,
  "risk_coverage": {{
    "market_risks": 0.0-1.0,
    "financial_risks": 0.0-1.0,
    "team_risks": 0.0-1.0,
    "product_risks": 0.0-1.0,
    "competitive_risks": 0.0-1.0
  }},
  "severity_accuracy": 0.0-1.0,
  "missing_risks": ["string"],
  "false_positives": ["string"],
  "quality_score": 0.0-1.0
}}

STARTUP DATA:
{startup_data}

RISK ASSESSMENT:
{risk_assessment}

JSON OUTPUT:
"""