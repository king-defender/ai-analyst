-- Create tables for AI Analyst benchmarking data

-- Companies table for peer benchmarking
CREATE TABLE IF NOT EXISTS `ai_analyst_benchmarks.companies` (
  company_id STRING NOT NULL,
  company_name STRING NOT NULL,
  industry STRING,
  stage STRING,
  founded_year INT64,
  employees_count INT64,
  headquarters_location STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Financial metrics table
CREATE TABLE IF NOT EXISTS `ai_analyst_benchmarks.financial_metrics` (
  metric_id STRING NOT NULL,
  company_id STRING NOT NULL,
  year INT64 NOT NULL,
  quarter INT64,
  revenue FLOAT64,
  arr FLOAT64,
  gross_margin FLOAT64,
  burn_rate FLOAT64,
  runway_months INT64,
  valuation FLOAT64,
  funding_amount FLOAT64,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Growth metrics table
CREATE TABLE IF NOT EXISTS `ai_analyst_benchmarks.growth_metrics` (
  growth_id STRING NOT NULL,
  company_id STRING NOT NULL,
  year INT64 NOT NULL,
  quarter INT64,
  revenue_growth_rate FLOAT64,
  customer_growth_rate FLOAT64,
  user_growth_rate FLOAT64,
  churn_rate FLOAT64,
  ltv_cac_ratio FLOAT64,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Risk indicators table
CREATE TABLE IF NOT EXISTS `ai_analyst_benchmarks.risk_indicators` (
  risk_id STRING NOT NULL,
  company_id STRING NOT NULL,
  risk_type STRING NOT NULL,
  risk_level STRING NOT NULL,
  description STRING,
  evidence TEXT,
  detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Industry benchmarks view
CREATE OR REPLACE VIEW `ai_analyst_benchmarks.industry_benchmarks` AS
SELECT 
  industry,
  stage,
  COUNT(*) as company_count,
  PERCENTILE_CONT(revenue, 0.25) OVER (PARTITION BY industry, stage) as revenue_p25,
  PERCENTILE_CONT(revenue, 0.5) OVER (PARTITION BY industry, stage) as revenue_median,
  PERCENTILE_CONT(revenue, 0.75) OVER (PARTITION BY industry, stage) as revenue_p75,
  PERCENTILE_CONT(revenue_growth_rate, 0.25) OVER (PARTITION BY industry, stage) as growth_p25,
  PERCENTILE_CONT(revenue_growth_rate, 0.5) OVER (PARTITION BY industry, stage) as growth_median,
  PERCENTILE_CONT(revenue_growth_rate, 0.75) OVER (PARTITION BY industry, stage) as growth_p75
FROM `ai_analyst_benchmarks.companies` c
JOIN `ai_analyst_benchmarks.financial_metrics` f ON c.company_id = f.company_id
JOIN `ai_analyst_benchmarks.growth_metrics` g ON c.company_id = g.company_id
WHERE f.year = EXTRACT(YEAR FROM CURRENT_DATE()) - 1
  AND g.year = EXTRACT(YEAR FROM CURRENT_DATE()) - 1;