# Operations Manual

This document provides operational procedures, monitoring guidelines, and troubleshooting information for the AI Analyst MVP.

## 🚀 System Operations

### Deployment Operations

#### Production Deployment Process
1. **Pre-deployment Checklist**
   - [ ] All tests passing in CI/CD
   - [ ] Security scans completed
   - [ ] Performance benchmarks validated
   - [ ] Database migrations tested
   - [ ] Rollback plan prepared

2. **Deployment Steps**
   ```bash
   # 1. Deploy backend services
   gcloud run deploy ai-analyst-backend \
     --source . \
     --region=us-central1 \
     --allow-unauthenticated

   # 2. Deploy frontend
   npm run build
   gcloud app deploy app.yaml

   # 3. Run database migrations
   python manage.py migrate

   # 4. Validate deployment
   ./scripts/health-check.sh
   ```

3. **Post-deployment Verification**
   - [ ] Health checks passing
   - [ ] API endpoints responding
   - [ ] Frontend loading correctly
   - [ ] Key user flows functional
   - [ ] Monitoring alerts configured

#### Rollback Procedures
```bash
# Emergency rollback
gcloud run services replace-traffic ai-analyst-backend \
  --to-revisions=PREVIOUS_REVISION=100

# Gradual rollback
gcloud run services replace-traffic ai-analyst-backend \
  --to-revisions=PREVIOUS_REVISION=50,CURRENT_REVISION=50
```

### Environment Management

#### Development Environment
- **Purpose**: Local development and testing
- **URL**: http://localhost:3000 (frontend), http://localhost:8000 (backend)
- **Database**: Local PostgreSQL or SQLite
- **Authentication**: Test accounts
- **Monitoring**: Local logs only

#### Staging Environment
- **Purpose**: Integration testing and QA validation
- **URL**: https://staging-ai-analyst.app
- **Database**: Staging BigQuery dataset
- **Authentication**: Test accounts with real auth flow
- **Monitoring**: Basic monitoring and alerting

#### Production Environment
- **Purpose**: Live user-facing application
- **URL**: https://ai-analyst.app
- **Database**: Production BigQuery dataset
- **Authentication**: Full authentication and authorization
- **Monitoring**: Comprehensive monitoring, alerting, and logging

## 📊 Monitoring & Observability

### Key Performance Indicators (KPIs)

#### System Performance
- **Response Time**: 95th percentile < 2 seconds
- **Availability**: > 99.5% uptime
- **Error Rate**: < 0.1% of requests
- **Throughput**: Support 100 concurrent users

#### Business Metrics
- **Document Processing**: Average completion time < 15 minutes
- **Risk Detection Accuracy**: > 90% precision
- **User Satisfaction**: > 4.5/5 rating
- **Conversion Rate**: Pitch deck to memo completion > 85%

### Monitoring Setup

#### Google Cloud Monitoring
```yaml
# monitoring.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ai-analyst-backend
spec:
  selector:
    matchLabels:
      app: ai-analyst-backend
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

#### Custom Dashboards
- **System Overview**: Response times, error rates, resource utilization
- **Business Metrics**: Processing times, completion rates, user activity
- **Infrastructure**: Database performance, storage usage, network traffic
- **Security**: Authentication failures, suspicious activity, access patterns

#### Alerting Rules
```yaml
# alerts.yaml
groups:
- name: ai-analyst.rules
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.01
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: High error rate detected

  - alert: DocumentProcessingDelay
    expr: histogram_quantile(0.95, document_processing_duration_seconds) > 900
    for: 10m
    labels:
      severity: critical
    annotations:
      summary: Document processing taking too long
```

### Logging Strategy

#### Log Levels
- **DEBUG**: Detailed diagnostic information
- **INFO**: General operational messages
- **WARNING**: Potentially harmful situations
- **ERROR**: Error events but application continues
- **CRITICAL**: Serious errors that may cause application failure

#### Structured Logging Format
```python
# Example log format
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "document-processor",
  "user_id": "user123",
  "job_id": "job456",
  "message": "Document processing completed",
  "duration_ms": 850,
  "file_size_mb": 5.2
}
```

## 🔧 Troubleshooting Guide

### Common Issues

#### Document Processing Failures

**Symptom**: Documents stuck in processing state
```bash
# Check processing queue
kubectl get jobs -n ai-analyst

# Check worker pod logs
kubectl logs -n ai-analyst -l app=document-processor

# Check BigQuery processing jobs
bq ls -j --max_results=10
```

**Common Causes & Solutions**:
1. **OCR API quota exceeded**
   - Check Cloud Vision API quotas
   - Implement backoff and retry logic
   - Scale processing across regions

2. **Large file timeout**
   - Increase Cloud Run timeout limits
   - Implement chunked processing
   - Add progress tracking

3. **Memory exhaustion**
   - Monitor memory usage
   - Optimize image processing
   - Scale instance memory

#### API Performance Issues

**Symptom**: Slow response times or timeouts
```bash
# Check API metrics
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=ai-analyst-backend" \
  --limit=50 --format="table(timestamp,severity,textPayload)"

# Check database performance
bq query --use_legacy_sql=false \
  'SELECT job_id, creation_time, end_time 
   FROM `project.dataset.INFORMATION_SCHEMA.JOBS_BY_PROJECT` 
   WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)'
```

**Solutions**:
1. **Database query optimization**
   - Add appropriate indexes
   - Optimize complex queries
   - Implement query caching

2. **API rate limiting**
   - Implement proper rate limiting
   - Add request queuing
   - Scale horizontally

#### Authentication Issues

**Symptom**: Users unable to log in or access protected resources
```bash
# Check Firebase Auth logs
gcloud logging read "resource.type=firebase_domain" --limit=20

# Verify JWT token validation
curl -H "Authorization: Bearer $TOKEN" \
  https://ai-analyst.app/api/v1/health
```

**Solutions**:
1. **Token expiration**
   - Implement token refresh logic
   - Check token expiration handling
   - Verify clock synchronization

2. **Permission issues**
   - Review IAM roles and permissions
   - Check service account configurations
   - Validate API key restrictions

### Performance Optimization

#### Database Optimization
```sql
-- Identify slow queries
SELECT 
  query,
  total_time_ms,
  mean_time_ms,
  calls
FROM `project.region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
ORDER BY total_time_ms DESC
LIMIT 10;

-- Add indexes for common queries
CREATE INDEX idx_document_user_id ON documents(user_id);
CREATE INDEX idx_job_status ON processing_jobs(status, created_at);
```

#### Memory Optimization
```python
# Monitor memory usage
import psutil
import gc

def log_memory_usage():
    process = psutil.Process()
    memory_info = process.memory_info()
    logger.info(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")
    
# Implement garbage collection
gc.collect()
```

## 🔒 Security Operations

### Security Monitoring

#### Access Control Monitoring
```bash
# Monitor authentication attempts
gcloud logging read "resource.type=firebase_domain AND severity>=WARNING" \
  --limit=50

# Check API access patterns
gcloud logging read "resource.type=cloud_run_revision AND httpRequest.status>=400" \
  --limit=50
```

#### Vulnerability Management
1. **Dependency Scanning**
   ```bash
   # Python dependencies
   pip-audit
   
   # Node.js dependencies
   npm audit
   
   # Container scanning
   gcloud container images scan IMAGE_URL
   ```

2. **Secret Management**
   ```bash
   # Rotate service account keys
   gcloud iam service-accounts keys create key.json \
     --iam-account=service-account@project.iam.gserviceaccount.com
   
   # Update secrets in Secret Manager
   gcloud secrets versions add secret-name --data-file=secret-value.txt
   ```

### Incident Response

#### Security Incident Procedure
1. **Detection**: Automated alerts or manual discovery
2. **Assessment**: Determine scope and impact
3. **Containment**: Isolate affected systems
4. **Investigation**: Analyze logs and evidence
5. **Recovery**: Restore normal operations
6. **Documentation**: Record incident details and lessons learned

#### Emergency Contacts
- **Security Team**: security@company.com
- **On-call Engineer**: +1-xxx-xxx-xxxx
- **Management**: management@company.com
- **Legal**: legal@company.com

## 📈 Capacity Planning

### Resource Scaling

#### Horizontal Scaling
```bash
# Scale Cloud Run instances
gcloud run services update ai-analyst-backend \
  --concurrency=80 \
  --max-instances=100

# Scale BigQuery slots
bq reservation update \
  --location=us-central1 \
  --slots=500 \
  ai-analyst-reservation
```

#### Vertical Scaling
```bash
# Increase memory and CPU
gcloud run services update ai-analyst-backend \
  --memory=4Gi \
  --cpu=2
```

### Cost Optimization

#### Resource Monitoring
```bash
# Check BigQuery costs
bq query --use_legacy_sql=false \
  'SELECT 
    job_id, 
    total_bytes_processed,
    total_bytes_billed,
    creation_time
   FROM `project.region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
   WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
   ORDER BY total_bytes_billed DESC'

# Monitor Cloud Run costs
gcloud logging read "resource.type=cloud_run_revision" \
  --format="value(timestamp,resource.labels.service_name,request_count)"
```

## 🔄 Backup & Recovery

### Data Backup Strategy

#### Database Backups
```bash
# Export BigQuery datasets
bq extract --destination_format=AVRO \
  project:dataset.table \
  gs://backup-bucket/table_backup_$(date +%Y%m%d).avro

# Schedule automated backups
gcloud scheduler jobs create app-engine backup-job \
  --schedule="0 2 * * *" \
  --url="/backup" \
  --http-method=POST
```

#### File Storage Backups
```bash
# Sync Cloud Storage buckets
gsutil -m rsync -r -d gs://primary-bucket gs://backup-bucket

# Lifecycle management
gsutil lifecycle set lifecycle-config.json gs://backup-bucket
```

### Disaster Recovery

#### Recovery Time Objectives (RTO)
- **Critical Systems**: 4 hours
- **Non-critical Systems**: 24 hours
- **Data Recovery**: 2 hours

#### Recovery Point Objectives (RPO)
- **Database**: 1 hour
- **File Storage**: 24 hours
- **Configuration**: 4 hours

#### Recovery Procedures
1. **Assess Impact**: Determine scope of outage
2. **Activate DR Site**: Switch to backup infrastructure
3. **Restore Data**: Recover from latest backups
4. **Validate Systems**: Ensure functionality
5. **Resume Operations**: Return to normal service
6. **Post-mortem**: Analyze and improve procedures

---

*This operations manual should be regularly updated as systems and procedures evolve.*