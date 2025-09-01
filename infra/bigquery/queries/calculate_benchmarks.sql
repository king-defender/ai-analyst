-- Query to calculate industry benchmarks
-- Input parameters: @industry, @stage

SELECT 
  @industry as industry,
  @stage as stage,
  -- Revenue metrics
  APPROX_QUANTILES(fm.revenue_arr, 100)[OFFSET(10)] as revenue_arr_p10,
  APPROX_QUANTILES(fm.revenue_arr, 100)[OFFSET(25)] as revenue_arr_p25,
  APPROX_QUANTILES(fm.revenue_arr, 100)[OFFSET(50)] as revenue_arr_median,
  APPROX_QUANTILES(fm.revenue_arr, 100)[OFFSET(75)] as revenue_arr_p75,
  APPROX_QUANTILES(fm.revenue_arr, 100)[OFFSET(90)] as revenue_arr_p90,
  
  -- Growth metrics
  APPROX_QUANTILES(fm.revenue_growth_rate_monthly, 100)[OFFSET(50)] as growth_rate_median,
  APPROX_QUANTILES(fm.revenue_growth_rate_monthly, 100)[OFFSET(75)] as growth_rate_p75,
  APPROX_QUANTILES(fm.revenue_growth_rate_monthly, 100)[OFFSET(90)] as growth_rate_p90,
  
  -- Churn metrics
  APPROX_QUANTILES(fm.churn_rate_monthly, 100)[OFFSET(50)] as churn_rate_median,
  APPROX_QUANTILES(fm.churn_rate_monthly, 100)[OFFSET(25)] as churn_rate_p25,
  APPROX_QUANTILES(fm.churn_rate_monthly, 100)[OFFSET(10)] as churn_rate_p10,
  
  -- Unit economics
  APPROX_QUANTILES(fm.ltv_cac_ratio, 100)[OFFSET(50)] as ltv_cac_median,
  APPROX_QUANTILES(fm.gross_margin, 100)[OFFSET(50)] as gross_margin_median,
  APPROX_QUANTILES(fm.customer_acquisition_cost, 100)[OFFSET(50)] as cac_median,
  
  -- Funding metrics
  APPROX_QUANTILES(c.total_funding, 100)[OFFSET(50)] as total_funding_median,
  APPROX_QUANTILES(c.total_funding, 100)[OFFSET(75)] as total_funding_p75,
  
  COUNT(*) as sample_size,
  CURRENT_TIMESTAMP() as calculated_at
  
FROM 
  `ai_analyst.companies` c
JOIN 
  `ai_analyst.financial_metrics` fm 
  ON c.company_id = fm.company_id
WHERE 
  c.industry = @industry
  AND c.stage = @stage
  AND fm.metric_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
  AND fm.revenue_arr IS NOT NULL
  AND fm.revenue_arr > 0
GROUP BY 
  industry, stage;