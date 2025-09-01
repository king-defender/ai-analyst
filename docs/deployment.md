# Deployment Guide

## Overview

This guide covers deploying the AI Analyst MVP to Google Cloud Platform with production-ready configurations.

## Prerequisites

- Google Cloud Platform account
- `gcloud` CLI installed and configured
- Docker installed
- Node.js 18+ and Python 3.9+ for local development

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   Cloud Run      │    │   Cloud Storage │
│   (HTTPS/SSL)   │────│   (Backend API)  │────│   (File Storage)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Vertex AI      │    │   BigQuery      │
                       │   (LLM Services) │    │   (Benchmarks)  │
                       └──────────────────┘    └─────────────────┘
                                
┌─────────────────┐    ┌──────────────────┐
│   Vercel/Netlify│    │   Cloud Vision   │
│   (Frontend)    │────│   (OCR)          │
└─────────────────┘    └──────────────────┘
```

## Environment Setup

### 1. Google Cloud Project

```bash
# Create new project
gcloud projects create ai-analyst-prod --name="AI Analyst Production"

# Set current project
gcloud config set project ai-analyst-prod

# Enable required APIs
gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  vision.googleapis.com \
  aiplatform.googleapis.com \
  bigquery.googleapis.com \
  storage.googleapis.com \
  firestore.googleapis.com
```

### 2. Service Account Setup

```bash
# Create service account
gcloud iam service-accounts create ai-analyst-service \
  --display-name="AI Analyst Service Account"

# Grant necessary permissions
gcloud projects add-iam-policy-binding ai-analyst-prod \
  --member="serviceAccount:ai-analyst-service@ai-analyst-prod.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding ai-analyst-prod \
  --member="serviceAccount:ai-analyst-service@ai-analyst-prod.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"

gcloud projects add-iam-policy-binding ai-analyst-prod \
  --member="serviceAccount:ai-analyst-service@ai-analyst-prod.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding ai-analyst-prod \
  --member="serviceAccount:ai-analyst-service@ai-analyst-prod.iam.gserviceaccount.com" \
  --role="roles/vision.annotator"

# Download service account key
gcloud iam service-accounts keys create ./service-account-key.json \
  --iam-account=ai-analyst-service@ai-analyst-prod.iam.gserviceaccount.com
```

### 3. BigQuery Setup

```bash
# Create dataset
bq mk --dataset ai-analyst-prod:startup_data

# Create tables
bq mk --table ai-analyst-prod:startup_data.companies \
  infra/bigquery/schemas/companies.json

bq mk --table ai-analyst-prod:startup_data.financial_metrics \
  infra/bigquery/schemas/financial_metrics.json

bq mk --table ai-analyst-prod:startup_data.industry_benchmarks \
  infra/bigquery/schemas/industry_benchmarks.json

# Load sample data
bq load --source_format=NEWLINE_DELIMITED_JSON \
  ai-analyst-prod:startup_data.companies \
  sample_data/companies.jsonl
```

### 4. Cloud Storage

```bash
# Create buckets
gsutil mb gs://ai-analyst-prod-uploads
gsutil mb gs://ai-analyst-prod-memos

# Set CORS for uploads bucket
echo '[{"origin": ["*"], "method": ["GET", "POST", "PUT"], "responseHeader": ["*"], "maxAgeSeconds": 3600}]' > cors.json
gsutil cors set cors.json gs://ai-analyst-prod-uploads
```

## Backend Deployment

### 1. Prepare Docker Image

```dockerfile
# backend/Dockerfile.prod
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8080

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 2. Build and Deploy

```bash
# Build image
gcloud builds submit --tag gcr.io/ai-analyst-prod/backend ./backend

# Deploy to Cloud Run
gcloud run deploy ai-analyst-backend \
  --image gcr.io/ai-analyst-prod/backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="ENVIRONMENT=production" \
  --set-env-vars="GCP_PROJECT_ID=ai-analyst-prod" \
  --set-env-vars="BIGQUERY_DATASET=startup_data" \
  --service-account=ai-analyst-service@ai-analyst-prod.iam.gserviceaccount.com \
  --memory=2Gi \
  --cpu=2 \
  --max-instances=10
```

### 3. Environment Variables

```bash
# Set additional environment variables
gcloud run services update ai-analyst-backend \
  --set-env-vars="UPLOADS_BUCKET=ai-analyst-prod-uploads" \
  --set-env-vars="MEMOS_BUCKET=ai-analyst-prod-memos" \
  --set-env-vars="VERTEX_AI_LOCATION=us-central1" \
  --region=us-central1
```

## Frontend Deployment

### 1. Environment Configuration

```bash
# frontend/.env.production
NEXT_PUBLIC_API_URL=https://ai-analyst-backend-xxx-uc.a.run.app
NEXT_PUBLIC_ENVIRONMENT=production
```

### 2. Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel --prod
```

### 3. Deploy to Netlify (Alternative)

```bash
# Build for production
npm run build

# Deploy to Netlify
npx netlify-cli deploy --prod --dir=.next
```

## Database Migration

### 1. Load Benchmark Data

```bash
# Run data loading script
python scripts/load_benchmark_data.py \
  --project ai-analyst-prod \
  --dataset startup_data \
  --source sample_data/benchmark_data.csv
```

### 2. Create Indexes

```sql
-- BigQuery indexes for performance
CREATE INDEX idx_companies_industry_stage 
ON `ai-analyst-prod.startup_data.companies` (industry, stage);

CREATE INDEX idx_metrics_date 
ON `ai-analyst-prod.startup_data.financial_metrics` (metric_date DESC);
```

## Monitoring & Logging

### 1. Cloud Logging

```bash
# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=ai-analyst-backend" \
  --limit=50 \
  --format="table(timestamp,severity,textPayload)"
```

### 2. Cloud Monitoring

```bash
# Create alerting policy
gcloud alpha monitoring policies create \
  --policy-from-file=monitoring/error-rate-policy.yaml
```

### 3. Health Checks

```bash
# Test health endpoint
curl https://ai-analyst-backend-xxx-uc.a.run.app/api/health
```

## Security Configuration

### 1. HTTPS/SSL

Cloud Run automatically provides HTTPS endpoints. For custom domains:

```bash
# Map custom domain
gcloud run domain-mappings create \
  --service ai-analyst-backend \
  --domain api.aianalyst.com \
  --region us-central1
```

### 2. CORS Configuration

```python
# Update CORS settings in main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aianalyst.com", "https://www.aianalyst.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### 3. API Security

```python
# Add rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/documents/upload")
@limiter.limit("10/hour")
async def upload_document(request: Request, ...):
    ...
```

## Performance Optimization

### 1. Caching

```python
# Add Redis for caching
import redis

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    password=os.getenv('REDIS_PASSWORD')
)

@lru_cache(maxsize=100)
async def get_industry_benchmarks(industry: str, stage: str):
    ...
```

### 2. CDN Configuration

```bash
# Configure Cloud CDN
gcloud compute backend-services create ai-analyst-backend-service \
  --global

gcloud compute backend-services add-backend ai-analyst-backend-service \
  --backend-service=ai-analyst-backend \
  --global
```

## Backup & Recovery

### 1. BigQuery Backup

```bash
# Schedule exports
bq mk --transfer_config \
  --project_id=ai-analyst-prod \
  --data_source=scheduled_query \
  --display_name="Daily Backup" \
  --target_dataset=startup_data_backup
```

### 2. File Storage Backup

```bash
# Set lifecycle policy
gsutil lifecycle set storage-lifecycle.json gs://ai-analyst-prod-uploads
```

## Cost Optimization

### 1. Resource Limits

```bash
# Set Cloud Run limits
gcloud run services update ai-analyst-backend \
  --cpu=1 \
  --memory=1Gi \
  --max-instances=5 \
  --region=us-central1
```

### 2. BigQuery Cost Controls

```sql
-- Set query cost controls
ALTER TABLE `ai-analyst-prod.startup_data.companies`
SET OPTIONS (
  max_staleness = INTERVAL 1 HOUR
);
```

## Troubleshooting

### Common Issues

1. **Cold Start Latency**
   ```bash
   # Increase minimum instances
   gcloud run services update ai-analyst-backend \
     --min-instances=1
   ```

2. **Memory Issues**
   ```bash
   # Increase memory allocation
   gcloud run services update ai-analyst-backend \
     --memory=2Gi
   ```

3. **API Timeout**
   ```bash
   # Increase timeout
   gcloud run services update ai-analyst-backend \
     --timeout=900s
   ```

### Logs Analysis

```bash
# Get error logs
gcloud logging read \
  "resource.type=cloud_run_revision AND severity>=ERROR" \
  --limit=20 \
  --format="table(timestamp,textPayload)"
```

## Maintenance

### 1. Regular Updates

```bash
# Update dependencies
pip-compile requirements.in
npm audit fix

# Rebuild and redeploy
gcloud builds submit --tag gcr.io/ai-analyst-prod/backend
```

### 2. Database Maintenance

```bash
# Update benchmark data monthly
python scripts/update_benchmarks.py
```

### 3. Health Monitoring

```bash
# Run health checks
./scripts/health-check.sh production
```