# Troubleshooting Guide

This guide provides solutions to common issues, debugging procedures, and escalation paths for the AI Analyst MVP.

## 🚨 Quick Issue Resolution

### System Status Check

Before troubleshooting, check system status:

```bash
# Check API health
curl https://api.ai-analyst.app/health

# Check frontend accessibility
curl -I https://ai-analyst.app

# Verify database connectivity
gcloud sql connect ai-analyst-db --user=postgres
```

### Common Error Codes

| Error Code | Description | Quick Fix |
|------------|-------------|-----------|
| `FILE_TOO_LARGE` | File exceeds 50MB limit | Compress or split the file |
| `INVALID_FORMAT` | Unsupported file type | Convert to PDF/DOCX/TXT |
| `OCR_FAILED` | Text extraction failed | Improve image quality |
| `QUOTA_EXCEEDED` | API rate limit reached | Wait or upgrade plan |
| `PROCESSING_TIMEOUT` | Analysis took too long | Retry or contact support |
| `AUTH_EXPIRED` | Session expired | Log in again |

## 🔧 Frontend Issues

### File Upload Problems

#### Issue: Upload Button Not Responding
**Symptoms**: Click upload button, nothing happens
**Debugging Steps**:
```javascript
// Check browser console
console.log('Upload button clicked');

// Verify file input
const fileInput = document.querySelector('input[type="file"]');
console.log('File input element:', fileInput);

// Check file size and type
if (file.size > 50 * 1024 * 1024) {
  console.error('File too large:', file.size);
}
```

**Solutions**:
1. Clear browser cache and cookies
2. Disable browser extensions
3. Try different browser (Chrome, Firefox, Safari)
4. Check JavaScript console for errors
5. Verify file meets requirements

#### Issue: Upload Progress Stuck
**Symptoms**: Progress bar stops at specific percentage
**Debugging Steps**:
```bash
# Check network activity in browser dev tools
# Monitor XHR requests for failures

# Check backend logs
gcloud logging read "resource.type=cloud_run_revision AND textPayload:upload" --limit=20
```

**Solutions**:
1. Retry upload with smaller file
2. Check internet connection stability
3. Try uploading during off-peak hours
4. Split large files into smaller chunks

### User Interface Issues

#### Issue: Page Not Loading
**Symptoms**: White screen or loading spinner indefinitely
**Debugging Steps**:
```javascript
// Check React error boundaries
console.log('React version:', React.version);

// Verify API connectivity
fetch('/api/health')
  .then(response => response.json())
  .then(data => console.log('API health:', data))
  .catch(error => console.error('API error:', error));
```

**Solutions**:
1. Hard refresh (Ctrl+F5 or Cmd+Shift+R)
2. Clear browser cache
3. Check for JavaScript errors in console
4. Disable ad blockers and extensions
5. Try incognito/private browsing mode

#### Issue: Data Not Displaying
**Symptoms**: Analysis completed but results not showing
**Debugging Steps**:
```javascript
// Check state management
console.log('Current state:', useStore.getState());

// Verify API response
const response = await fetch(`/api/v1/analysis/${jobId}`);
const data = await response.json();
console.log('API response:', data);
```

**Solutions**:
1. Refresh the page
2. Check browser console for errors
3. Verify user permissions
4. Clear local storage data
5. Re-run analysis if data corrupted

## 🔧 Backend Issues

### API Performance Problems

#### Issue: Slow Response Times
**Symptoms**: API calls taking > 5 seconds
**Debugging Steps**:
```bash
# Check API response times
curl -w "@curl-format.txt" -o /dev/null -s "https://api.ai-analyst.app/v1/health"

# Monitor Cloud Run metrics
gcloud monitoring metrics list --filter="resource.type=cloud_run_revision"

# Check database performance
bq query --use_legacy_sql=false \
  'SELECT job_id, total_time_ms 
   FROM `project.region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT` 
   WHERE total_time_ms > 5000'
```

**Solutions**:
1. Scale Cloud Run instances
2. Optimize database queries
3. Implement response caching
4. Add database indexes
5. Use CDN for static assets

#### Issue: 500 Internal Server Errors
**Symptoms**: Server errors on API requests
**Debugging Steps**:
```bash
# Check application logs
gcloud logging read "resource.type=cloud_run_revision AND severity>=ERROR" --limit=20

# Check Python exceptions
grep -r "Traceback" /var/log/app/

# Verify environment variables
printenv | grep AI_ANALYST_
```

**Solutions**:
1. Check application logs for stack traces
2. Verify environment configuration
3. Restart service instances
4. Check dependency compatibility
5. Review recent code changes

### Document Processing Issues

#### Issue: OCR Extraction Failing
**Symptoms**: Documents stuck in "processing" state
**Debugging Steps**:
```python
# Test OCR manually
from google.cloud import vision

client = vision.ImageAnnotatorClient()
with open('test-image.jpg', 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)
response = client.text_detection(image=image)

if response.error.message:
    print(f'OCR Error: {response.error.message}')
else:
    print(f'Extracted text: {response.text_annotations[0].description}')
```

**Solutions**:
1. Check Google Cloud Vision API quotas
2. Verify image quality and resolution
3. Retry with different image formats
4. Implement fallback OCR service
5. Contact Google Cloud support

#### Issue: Data Parsing Errors
**Symptoms**: Incorrect or missing data extraction
**Debugging Steps**:
```python
# Debug parsing pipeline
from ml.pipeline.parsing import DocumentParser

parser = DocumentParser()
try:
    result = parser.parse_document(document_text)
    print(f'Parsed data: {result}')
except Exception as e:
    print(f'Parsing error: {e}')
    import traceback
    traceback.print_exc()
```

**Solutions**:
1. Improve document text quality
2. Update parsing rules and patterns
3. Retrain ML models with new data
4. Add manual review step
5. Implement confidence scoring

## 🔧 Database Issues

### BigQuery Problems

#### Issue: Query Timeouts
**Symptoms**: BigQuery jobs failing with timeout errors
**Debugging Steps**:
```bash
# Check running jobs
bq ls -j --max_results=10

# Monitor job performance
bq show -j job_id

# Check query complexity
bq query --dry_run --use_legacy_sql=false 'YOUR_QUERY_HERE'
```

**Solutions**:
1. Optimize query performance
2. Add appropriate table partitioning
3. Use query caching
4. Increase job timeout limits
5. Split complex queries

#### Issue: Data Inconsistency
**Symptoms**: Benchmark data showing unexpected results
**Debugging Steps**:
```sql
-- Check data freshness
SELECT 
  table_name,
  MAX(last_modified_time) as last_update
FROM `project.dataset.INFORMATION_SCHEMA.TABLES`
WHERE table_name LIKE 'benchmark_%'
GROUP BY table_name;

-- Validate data quality
SELECT 
  COUNT(*) as total_rows,
  COUNT(DISTINCT company_id) as unique_companies,
  COUNT(CASE WHEN revenue IS NULL THEN 1 END) as missing_revenue
FROM `project.dataset.benchmark_data`;
```

**Solutions**:
1. Refresh benchmark datasets
2. Validate data import processes
3. Check data transformation logic
4. Implement data quality checks
5. Update data validation rules

### Connection Issues

#### Issue: Database Connection Failures
**Symptoms**: Cannot connect to BigQuery or Cloud SQL
**Debugging Steps**:
```python
# Test BigQuery connection
from google.cloud import bigquery

try:
    client = bigquery.Client()
    query = "SELECT 1 as test"
    results = client.query(query)
    print("BigQuery connection successful")
except Exception as e:
    print(f"BigQuery connection failed: {e}")

# Test Cloud SQL connection
import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="ai_analyst",
        user="postgres",
        password="password"
    )
    print("Cloud SQL connection successful")
except Exception as e:
    print(f"Cloud SQL connection failed: {e}")
```

**Solutions**:
1. Check service account permissions
2. Verify network connectivity
3. Update connection credentials
4. Check firewall rules
5. Restart database services

## 🔧 ML Pipeline Issues

### Model Performance Problems

#### Issue: Low Risk Detection Accuracy
**Symptoms**: Missing obvious red flags or false positives
**Debugging Steps**:
```python
# Evaluate model performance
from ml.evaluation import RiskAssessmentEvaluator

evaluator = RiskAssessmentEvaluator()
metrics = evaluator.evaluate_model(test_data)
print(f"Precision: {metrics['precision']}")
print(f"Recall: {metrics['recall']}")
print(f"F1 Score: {metrics['f1_score']}")

# Analyze feature importance
feature_importance = evaluator.get_feature_importance()
print("Top risk indicators:", feature_importance[:10])
```

**Solutions**:
1. Retrain model with recent data
2. Update risk assessment rules
3. Adjust confidence thresholds
4. Add new risk categories
5. Implement ensemble methods

#### Issue: Slow Processing Times
**Symptoms**: Document analysis taking > 20 minutes
**Debugging Steps**:
```python
# Profile processing pipeline
import time
from ml.pipeline import ProcessingPipeline

pipeline = ProcessingPipeline()
start_time = time.time()

# Time each stage
ocr_start = time.time()
text_result = pipeline.extract_text(document)
ocr_time = time.time() - ocr_start

parsing_start = time.time()
parsed_data = pipeline.parse_data(text_result)
parsing_time = time.time() - parsing_start

print(f"OCR time: {ocr_time:.2f}s")
print(f"Parsing time: {parsing_time:.2f}s")
```

**Solutions**:
1. Optimize image preprocessing
2. Implement parallel processing
3. Cache intermediate results
4. Use faster ML models
5. Scale compute resources

## 🔧 Infrastructure Issues

### Cloud Platform Problems

#### Issue: Cloud Run Out of Memory
**Symptoms**: Services crashing with memory errors
**Debugging Steps**:
```bash
# Check memory usage
gcloud run services describe ai-analyst-backend \
  --region=us-central1 \
  --format="value(spec.template.spec.containers[0].resources.limits.memory)"

# Monitor memory metrics
gcloud logging read "resource.type=cloud_run_revision AND textPayload:memory" --limit=20
```

**Solutions**:
1. Increase memory allocation
2. Optimize memory usage in code
3. Implement memory profiling
4. Use streaming processing
5. Scale horizontally

#### Issue: API Gateway Timeouts
**Symptoms**: 504 Gateway Timeout errors
**Debugging Steps**:
```bash
# Check gateway configuration
gcloud api-gateway gateways describe ai-analyst-gateway \
  --location=us-central1

# Monitor timeout metrics
gcloud logging read "resource.type=api_gateway" --limit=20
```

**Solutions**:
1. Increase gateway timeout limits
2. Optimize backend response times
3. Implement request queuing
4. Add load balancing
5. Use async processing

### Authentication Issues

#### Issue: JWT Token Validation Errors
**Symptoms**: Authentication failures for valid users
**Debugging Steps**:
```python
# Debug JWT validation
import jwt
from datetime import datetime

try:
    decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
    print(f"Token valid, user: {decoded['user_id']}")
    print(f"Expires: {datetime.fromtimestamp(decoded['exp'])}")
except jwt.ExpiredSignatureError:
    print("Token expired")
except jwt.InvalidTokenError as e:
    print(f"Invalid token: {e}")
```

**Solutions**:
1. Check token expiration handling
2. Verify signing key configuration
3. Update token refresh logic
4. Check clock synchronization
5. Review authentication flow

## 📞 Escalation Procedures

### Issue Severity Levels

#### Critical (P0)
- System completely down
- Data loss or corruption
- Security breach
- **Response Time**: 30 minutes
- **Escalation**: Immediately to on-call engineer

#### High (P1)
- Major functionality broken
- Performance severely degraded
- Authentication failures
- **Response Time**: 2 hours
- **Escalation**: Technical lead within 1 hour

#### Medium (P2)
- Minor functionality issues
- Non-critical performance issues
- UI/UX problems
- **Response Time**: 8 hours
- **Escalation**: Team lead within 4 hours

#### Low (P3)
- Feature requests
- Documentation updates
- Minor cosmetic issues
- **Response Time**: 48 hours
- **Escalation**: Next sprint planning

### Contact Information

#### Development Team
- **On-call Engineer**: +1-xxx-xxx-xxxx
- **Technical Lead**: tech-lead@company.com
- **DevOps Engineer**: devops@company.com

#### Management
- **Product Manager**: product@company.com
- **Engineering Manager**: engineering@company.com

#### External Support
- **Google Cloud Support**: Filed through Cloud Console
- **Vendor Support**: As per SLA agreements

### Incident Management

#### Incident Response Process
1. **Detection**: Automated monitoring or user report
2. **Assessment**: Determine severity and impact
3. **Response**: Assign appropriate resources
4. **Communication**: Update stakeholders
5. **Resolution**: Fix the issue
6. **Documentation**: Post-mortem and lessons learned

#### Communication Templates

**Critical Issue Alert**:
```
CRITICAL: AI Analyst System Down
Impact: All users unable to access application
ETA: Under investigation
Updates: Every 15 minutes
Contact: on-call@company.com
```

**Resolution Notice**:
```
RESOLVED: AI Analyst System Restored
Duration: 45 minutes
Root Cause: Database connection timeout
Prevention: Increased connection pool size
Post-mortem: Link to incident report
```

## 📋 Maintenance Procedures

### Regular Maintenance Tasks

#### Daily
- Monitor system health dashboards
- Review error logs and alerts
- Check processing queue status
- Validate backup completion

#### Weekly
- Update security patches
- Review performance metrics
- Clean up temporary files
- Test disaster recovery procedures

#### Monthly
- Conduct security audits
- Review and update documentation
- Analyze usage trends
- Plan capacity scaling

#### Quarterly
- Conduct penetration testing
- Review and update incident procedures
- Evaluate and update monitoring
- Business continuity testing

---

*This troubleshooting guide should be updated based on new issues and solutions discovered.*