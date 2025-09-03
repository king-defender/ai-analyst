# API Reference

## Overview

The AI Analyst API provides comprehensive endpoints for analyzing startup pitch decks, generating benchmarks, assessing risks, and creating investor memos.

Base URL: `http://localhost:8000`

## Authentication

Currently, the API doesn't require authentication for MVP purposes. In production, implement JWT or API key authentication.

## Core Endpoints

### Document Upload

#### POST `/api/documents/upload`

Upload a pitch deck for analysis.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: File upload (PDF, TXT, or DOCX)

**Response:**
```json
{
  "job_id": "uuid-string",
  "file_id": "uuid-string", 
  "filename": "deck.pdf",
  "status": "uploaded"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@pitch_deck.pdf"
```

### Job Status Tracking

#### GET `/api/jobs/{job_id}/status`

Get the current status of an analysis job.

**Response:**
```json
{
  "id": "job-uuid",
  "status": "processing|completed|failed",
  "stage": "upload|ocr|parsing|benchmark|risks|memo",
  "progress": 75,
  "message": "Analyzing potential risks...",
  "created_at": "2023-12-01T10:00:00Z",
  "updated_at": "2023-12-01T10:05:00Z"
}
```

### Analysis Results

#### GET `/api/analysis/{job_id}/result`

Get complete analysis results for a completed job.

**Response:**
```json
{
  "job_id": "job-uuid",
  "result": {
    "startup_data": { /* extracted company data */ },
    "benchmark_data": { /* peer comparisons */ },
    "risk_assessment": { /* risk analysis */ },
    "investor_memo": { /* generated memo */ },
    "confidence_scores": {
      "data_extraction": 0.85,
      "risk_assessment": 0.78,
      "benchmark_accuracy": 0.92,
      "memo_quality": 0.88
    }
  }
}
```

#### GET `/api/analysis/{job_id}/startup-data`

Get only the extracted startup data.

#### GET `/api/analysis/{job_id}/benchmarks`

Get only the benchmark analysis.

#### GET `/api/analysis/{job_id}/risks`

Get only the risk assessment.

### Investor Memos

#### GET `/api/memos/{job_id}`

Get the generated investor memo.

#### GET `/api/memos/{job_id}/pdf`

Download the memo as a PDF file.

**Response:** PDF file download

#### GET `/api/memos/{job_id}/executive-summary`

Get only the executive summary section.

#### GET `/api/memos/{job_id}/recommendation`

Get only the investment recommendation.

### Health Check

#### GET `/api/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2023-12-01T10:00:00Z",
  "version": "1.0.0"
}
```

## Data Models

### StartupData

```json
{
  "company_name": "string",
  "founded_year": 2022,
  "industry": "SaaS|FinTech|HealthTech|...",
  "stage": "Pre-Seed|Seed|Series A|...",
  "description": "string",
  "team": [
    {
      "name": "string",
      "role": "string", 
      "bio": "string",
      "experience_years": 10,
      "previous_companies": ["string"],
      "education": ["string"]
    }
  ],
  "metrics": {
    "revenue_arr": 2500000,
    "monthly_growth_rate": 0.25,
    "customer_count": 150,
    "churn_rate": 0.03,
    "ltv_cac_ratio": 3.5,
    "gross_margin": 0.85,
    "burn_rate": 150000,
    "runway_months": 18
  },
  "financial_data": {
    "current_valuation": 25000000,
    "total_funding_raised": 12000000,
    "unit_economics": {
      "cac": 750,
      "ltv": 2625,
      "payback_period_months": 8
    }
  },
  "market_data": {
    "total_addressable_market": 50000000000,
    "serviceable_addressable_market": 8000000000,
    "market_growth_rate": 0.15,
    "competitors": [
      {
        "name": "string",
        "description": "string",
        "funding_raised": 50000000,
        "employee_count": 200
      }
    ]
  }
}
```

### RiskAssessment

```json
{
  "overall_risk_score": 65,
  "risk_factors": [
    {
      "category": "financial|market|team|product|competitive|regulatory",
      "risk_type": "string",
      "severity": "low|medium|high|critical",
      "description": "string",
      "evidence": ["string"],
      "likelihood": 0.7,
      "potential_impact": 8
    }
  ],
  "red_flags": [
    {
      "type": "string",
      "description": "string",
      "evidence": ["string"],
      "severity_score": 9,
      "recommendation": "string"
    }
  ],
  "yellow_flags": [
    {
      "type": "string", 
      "description": "string",
      "evidence": ["string"],
      "monitoring_suggestion": "string"
    }
  ]
}
```

### InvestorMemo

```json
{
  "id": "memo-uuid",
  "company_name": "string",
  "generated_at": "2023-12-01T10:00:00Z",
  "executive_summary": {
    "company_overview": "string",
    "key_highlights": ["string"],
    "investment_highlights": ["string"],
    "concerns": ["string"],
    "recommendation_summary": "string"
  },
  "recommendation": {
    "recommendation": "strong_buy|buy|hold|pass|strong_pass",
    "confidence_level": 0.85,
    "reasoning": ["string"],
    "suggested_valuation_range": {
      "low": 20000000,
      "high": 30000000
    },
    "investment_amount_suggestion": 5000000,
    "terms_suggestions": ["string"],
    "next_steps": ["string"]
  }
}
```

## Error Handling

All endpoints return errors in the following format:

```json
{
  "error": "string",
  "details": "string",
  "code": "string"
}
```

Common HTTP status codes:
- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found (job/file not found)
- `422` - Validation Error
- `500` - Internal Server Error

## Rate Limiting

Currently no rate limiting is implemented for MVP. In production, implement:
- 100 requests per minute per IP
- 10 file uploads per hour per IP
- 5 analysis jobs per hour per user

## WebSocket Support (Future)

Real-time job status updates via WebSocket will be available at:
`ws://localhost:8000/ws/jobs/{job_id}`

## SDKs and Libraries

### JavaScript/TypeScript
```javascript
import { apiClient } from '@ai-analyst/client';

const result = await apiClient.uploadFile(file);
const status = await apiClient.getJobStatus(result.job_id);
```

### Python
```python
from ai_analyst_client import AIAnalystClient

client = AIAnalystClient()
result = client.upload_file('pitch_deck.pdf')
status = client.get_job_status(result.job_id)
```

## Examples

### Complete Analysis Workflow

```javascript
// 1. Upload file
const uploadResult = await fetch('/api/documents/upload', {
  method: 'POST',
  body: formData
});
const { job_id } = await uploadResult.json();

// 2. Poll for completion
const pollStatus = async () => {
  const statusResult = await fetch(`/api/jobs/${job_id}/status`);
  const status = await statusResult.json();
  
  if (status.status === 'completed') {
    // 3. Get results
    const analysisResult = await fetch(`/api/analysis/${job_id}/result`);
    const analysis = await analysisResult.json();
    
    // 4. Download memo PDF
    const pdfResult = await fetch(`/api/memos/${job_id}/pdf`);
    const pdfBlob = await pdfResult.blob();
    
    return { analysis, pdfBlob };
  } else if (status.status === 'failed') {
    throw new Error(status.error);
  } else {
    // Continue polling
    setTimeout(pollStatus, 2000);
  }
};

await pollStatus();
```