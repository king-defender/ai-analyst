# API Documentation

The AI Analyst API provides endpoints for document processing, risk assessment, and investment memo generation.

## Base URL
```
Development: http://localhost:8000
Production: https://api.ai-analyst.com
```

## Authentication
API uses JWT tokens for authentication. Include in headers:
```
Authorization: Bearer <token>
```

## Endpoints

### Document Processing

#### Upload Document
```http
POST /api/v1/documents/upload
Content-Type: multipart/form-data

{
  "file": <file>,
  "type": "pitch_deck" | "transcript"
}
```

#### Get Processing Status
```http
GET /api/v1/documents/{document_id}/status
```

#### Get Extracted Data
```http
GET /api/v1/documents/{document_id}/extracted
```

### Analysis

#### Run Risk Assessment
```http
POST /api/v1/analysis/risks
Content-Type: application/json

{
  "document_id": "string",
  "options": {
    "include_evidence": true
  }
}
```

#### Get Benchmarks
```http
GET /api/v1/analysis/benchmarks?industry=saas&stage=series_a
```

### Memo Generation

#### Generate Memo
```http
POST /api/v1/memos/generate
Content-Type: application/json

{
  "document_id": "string",
  "template": "standard" | "detailed",
  "options": {
    "include_risks": true,
    "include_benchmarks": true
  }
}
```

#### Download Memo PDF
```http
GET /api/v1/memos/{memo_id}/pdf
```

## Response Format

All API responses follow this format:
```json
{
  "success": true,
  "data": {},
  "message": "string",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

Error responses:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description",
    "details": {}
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Error Codes

- `INVALID_FILE_TYPE`: File type not supported
- `FILE_TOO_LARGE`: File exceeds size limit
- `PROCESSING_FAILED`: Document processing failed
- `INSUFFICIENT_DATA`: Not enough data for analysis
- `QUOTA_EXCEEDED`: API quota exceeded
- `AUTHENTICATION_REQUIRED`: Valid token required
- `PERMISSION_DENIED`: Insufficient permissions

## Rate Limits

- 100 requests per minute per user
- 10 document uploads per hour per user
- 50 memo generations per day per user

## Webhooks

Configure webhooks to receive notifications:

```http
POST /api/v1/webhooks
Content-Type: application/json

{
  "url": "https://your-app.com/webhook",
  "events": ["document.processed", "analysis.completed"]
}
```

Webhook payload:
```json
{
  "event": "document.processed",
  "data": {
    "document_id": "string",
    "status": "completed"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```