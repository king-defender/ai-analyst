-- Query to calculate percentile ranking for a company
-- Input parameters: @company_revenue_arr, @company_growth_rate, @industry, @stage

WITH peer_metrics AS (
  SELECT 
    fm.revenue_arr,
    fm.revenue_growth_rate_monthly,
    fm.customer_count,
    fm.ltv_cac_ratio,
    c.total_funding,
    c.employee_count
  FROM 
    `ai_analyst.companies` c
  JOIN 
    `ai_analyst.financial_metrics` fm 
    ON c.company_id = fm.company_id
  WHERE 
    c.industry = @industry
    AND c.stage = @stage
    AND fm.metric_date = (
      SELECT MAX(metric_date) 
      FROM `ai_analyst.financial_metrics` fm2 
      WHERE fm2.company_id = c.company_id
    )
    AND fm.revenue_arr IS NOT NULL
    AND fm.revenue_arr > 0
)

SELECT 
  -- Revenue percentile
  PERCENT_RANK() OVER (ORDER BY revenue_arr) * 100 as revenue_percentile_rank,
  
  -- Growth percentile  
  PERCENT_RANK() OVER (ORDER BY revenue_growth_rate_monthly) * 100 as growth_percentile_rank,
  
  -- Customer count percentile
  PERCENT_RANK() OVER (ORDER BY customer_count) * 100 as customer_percentile_rank,
  
  -- Unit economics percentile
  PERCENT_RANK() OVER (ORDER BY ltv_cac_ratio) * 100 as unit_economics_percentile_rank,
  
  -- Funding efficiency percentile (revenue per funding dollar)
  PERCENT_RANK() OVER (ORDER BY revenue_arr / NULLIF(total_funding, 0)) * 100 as funding_efficiency_percentile,
  
  COUNT(*) OVER() as total_companies
  
FROM peer_metrics
WHERE 
  revenue_arr <= @company_revenue_arr
  AND revenue_growth_rate_monthly <= @company_growth_rate
LIMIT 1;