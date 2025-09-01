# Google Cloud Platform Setup Guide

This guide walks you through setting up the necessary GCP services for the AI Analyst MVP.

## Prerequisites

- Google Cloud account with billing enabled
- `gcloud` CLI installed and configured
- Project owner or editor permissions

## 1. Create and Configure Project

```bash
# Create a new project (optional)
gcloud projects create ai-analyst-mvp --name="AI Analyst MVP"

# Set the project
gcloud config set project ai-analyst-mvp

# Enable billing (replace BILLING_ACCOUNT_ID)
gcloud billing projects link ai-analyst-mvp --billing-account=BILLING_ACCOUNT_ID
```

## 2. Enable Required APIs

```bash
# Enable all required APIs
gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  storage-api.googleapis.com \
  vision.googleapis.com \
  aiplatform.googleapis.com \
  bigquery.googleapis.com \
  firestore.googleapis.com \
  secretmanager.googleapis.com \
  monitoring.googleapis.com \
  logging.googleapis.com
```

## 3. Create Service Accounts

### Backend Service Account
```bash
# Create service account for backend
gcloud iam service-accounts create ai-analyst-backend \
  --display-name="AI Analyst Backend Service Account"

# Grant necessary roles
gcloud projects add-iam-policy-binding ai-analyst-mvp \
  --member="serviceAccount:ai-analyst-backend@ai-analyst-mvp.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding ai-analyst-mvp \
  --member="serviceAccount:ai-analyst-backend@ai-analyst-mvp.iam.gserviceaccount.com" \
  --role="roles/vision.annotate"

gcloud projects add-iam-policy-binding ai-analyst-mvp \
  --member="serviceAccount:ai-analyst-backend@ai-analyst-mvp.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding ai-analyst-mvp \
  --member="serviceAccount:ai-analyst-backend@ai-analyst-mvp.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding ai-analyst-mvp \
  --member="serviceAccount:ai-analyst-backend@ai-analyst-mvp.iam.gserviceaccount.com" \
  --role="roles/datastore.user"

# Download service account key
gcloud iam service-accounts keys create ./ai-analyst-backend-key.json \
  --iam-account=ai-analyst-backend@ai-analyst-mvp.iam.gserviceaccount.com
```

## 4. Create Cloud Storage Buckets

```bash
# Create bucket for document storage
gsutil mb gs://ai-analyst-documents-prod

# Create bucket for processed data
gsutil mb gs://ai-analyst-processed-prod

# Set appropriate permissions
gsutil iam ch serviceAccount:ai-analyst-backend@ai-analyst-mvp.iam.gserviceaccount.com:admin gs://ai-analyst-documents-prod
gsutil iam ch serviceAccount:ai-analyst-backend@ai-analyst-mvp.iam.gserviceaccount.com:admin gs://ai-analyst-processed-prod
```

## 5. Setup Firestore Database

```bash
# Create Firestore database
gcloud firestore databases create --region=us-central1
```

## 6. Setup BigQuery Dataset

```bash
# Create dataset for benchmarking data
bq mk --dataset --location=US ai-analyst-mvp:ai_analyst_benchmarks

# Create tables (run the SQL scripts in infra/bigquery/)
bq query --use_legacy_sql=false < infra/bigquery/create_tables.sql
```

## 7. Configure Vertex AI

```bash
# Set default region for Vertex AI
gcloud config set ai/region us-central1

# Verify Vertex AI is enabled
gcloud ai models list --region=us-central1
```

## 8. Setup Cloud Run (for deployment)

```bash
# Build and deploy backend
gcloud run deploy ai-analyst-backend \
  --source=./backend \
  --region=us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=ai-analyst-mvp"

# Build and deploy frontend
gcloud run deploy ai-analyst-frontend \
  --source=./frontend \
  --region=us-central1 \
  --allow-unauthenticated
```

## 9. Setup Monitoring and Alerts

```bash
# Create notification channel (replace EMAIL)
gcloud alpha monitoring channels create \
  --display-name="AI Analyst Alerts" \
  --type=email \
  --channel-labels=email_address=YOUR_EMAIL@example.com
```

## 10. Environment Configuration

After completing the setup, update your environment files:

### Backend (.env)
```env
GOOGLE_CLOUD_PROJECT=ai-analyst-mvp
GOOGLE_APPLICATION_CREDENTIALS=./ai-analyst-backend-key.json
GCS_BUCKET_NAME=ai-analyst-documents-prod
VERTEX_AI_LOCATION=us-central1
BIGQUERY_DATASET=ai_analyst_benchmarks
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=https://ai-analyst-backend-hash-uc.a.run.app
```

## Security Considerations

1. **Service Account Keys**: Store securely and never commit to version control
2. **IAM Principles**: Follow least privilege access
3. **Network Security**: Configure VPC and firewall rules as needed
4. **Data Encryption**: Enable encryption at rest and in transit
5. **Audit Logging**: Enable Cloud Audit Logs for compliance

## Cost Optimization

1. **Storage Classes**: Use appropriate storage classes for different data types
2. **Compute Resources**: Right-size Cloud Run instances
3. **API Quotas**: Set appropriate quotas and budgets
4. **Data Retention**: Implement lifecycle policies for storage

## Troubleshooting

### Common Issues

1. **Permission Denied**: Check IAM roles and service account configuration
2. **API Not Enabled**: Ensure all required APIs are enabled
3. **Quota Exceeded**: Check and increase quotas if needed
4. **Network Issues**: Verify VPC and firewall configurations

### Useful Commands

```bash
# Check API status
gcloud services list --enabled

# View IAM policies
gcloud projects get-iam-policy ai-analyst-mvp

# Check quotas
gcloud compute project-info describe --project=ai-analyst-mvp

# View logs
gcloud logging read "resource.type=cloud_run_revision" --limit=50
```

## Next Steps

1. Run the development setup scripts in `scripts/setup-dev.sh`
2. Deploy the application using `scripts/deploy.sh`
3. Configure monitoring dashboards
4. Set up CI/CD pipelines