-- Query to get peer companies for benchmarking
-- Input parameters: @industry, @stage, @exclude_company_id

SELECT 
  c.company_id,
  c.company_name,
  c.industry,
  c.stage,
  c.founded_year,
  c.total_funding,
  c.last_funding_date,
  fm.revenue_arr,
  fm.revenue_growth_rate_monthly,
  fm.customer_count,
  fm.churn_rate_monthly,
  fm.gross_margin,
  fm.ltv_cac_ratio,
  fm.burn_rate_monthly,
  fm.cash_runway_months
FROM 
  `ai_analyst.companies` c
JOIN 
  `ai_analyst.financial_metrics` fm 
  ON c.company_id = fm.company_id
WHERE 
  c.industry = @industry
  AND c.stage = @stage
  AND c.company_id != @exclude_company_id
  AND fm.metric_date = (
    SELECT MAX(metric_date) 
    FROM `ai_analyst.financial_metrics` fm2 
    WHERE fm2.company_id = c.company_id
  )
  AND fm.revenue_arr IS NOT NULL
ORDER BY 
  fm.revenue_arr DESC
LIMIT 20;