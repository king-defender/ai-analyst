# User Guide

This guide provides step-by-step instructions for using the AI Analyst MVP to analyze startup pitch decks and generate investment memos.

## 🎯 Overview

The AI Analyst MVP helps investors and analysts:
- Upload and process startup pitch decks
- Extract key business metrics and information
- Benchmark companies against industry peers
- Identify potential risks and red flags
- Generate professional investment memos

## 🚀 Getting Started

### Account Setup

1. **Sign Up**
   - Visit [https://ai-analyst.app](https://ai-analyst.app)
   - Click "Sign Up" and enter your email
   - Verify your email address
   - Complete your profile information

2. **Subscription Setup**
   - Choose your plan (Starter, Professional, or Enterprise)
   - Enter payment information
   - Confirm subscription

3. **First Login**
   - Access the dashboard
   - Review the quick start tutorial
   - Configure notification preferences

### Dashboard Overview

The main dashboard provides:
- **Upload Section**: Drag-and-drop area for pitch decks
- **Recent Analysis**: List of recent processing jobs
- **Quick Stats**: Processing statistics and usage metrics
- **Notifications**: System alerts and job status updates

## 📄 Document Processing

### Supported File Types

The system accepts the following document formats:
- **PDF**: Pitch deck presentations (preferred)
- **PowerPoint**: .pptx files
- **Word Documents**: .docx and .doc files
- **Excel Spreadsheets**: .xlsx and .xls files
- **JSON**: Structured data files
- **Text Files**: .txt files for transcripts

### File Requirements

- **Maximum Size**: 50 MB per file
- **Page Limit**: Up to 100 slides/pages
- **Language**: English (primary), with limited support for other languages
- **Quality**: Clear, readable text and images

### Upload Process

1. **Drag and Drop**
   ```
   1. Navigate to the main dashboard
   2. Drag your pitch deck file to the upload area
   3. Or click "Browse Files" to select manually
   4. Wait for file validation confirmation
   ```

2. **File Information**
   - Enter company name (if not auto-detected)
   - Select industry category
   - Choose analysis priority (Standard or Expedited)
   - Add any special notes or context

3. **Start Processing**
   - Review file details
   - Click "Start Analysis"
   - Monitor progress in real-time

### Processing Stages

The analysis pipeline consists of 6 stages:

#### Stage 1: Document Upload ✅
- File validation and virus scanning
- Storage in secure cloud infrastructure
- Initial metadata extraction

#### Stage 2: OCR & Text Extraction 🔍
- Optical Character Recognition for images
- Text extraction from slides
- Structure and layout analysis

#### Stage 3: Data Parsing 📊
- AI-powered information extraction
- Company metrics identification
- Team and market data parsing

#### Stage 4: Peer Benchmarking 📈
- Industry comparison analysis
- Percentile ranking calculation
- Market positioning assessment

#### Stage 5: Risk Assessment ⚠️
- Red flag identification
- Risk category analysis
- Evidence-based scoring

#### Stage 6: Memo Generation 📝
- Investment memo creation
- Executive summary generation
- Recommendation formulation

**Typical Processing Time**: 10-15 minutes per document

## 📊 Analysis Results

### Data Extraction View

After processing, review the extracted information:

#### Company Information
- **Basic Details**: Name, industry, location, founding date
- **Business Model**: Revenue streams, target market
- **Stage**: Funding stage and previous rounds
- **Team**: Founder backgrounds and key personnel

#### Financial Metrics
- **Revenue**: Historical and projected revenue
- **Growth Rates**: Year-over-year growth trends
- **Unit Economics**: CAC, LTV, gross margins
- **Fundraising**: Amount seeking, valuation, use of funds

#### Market Analysis
- **Market Size**: TAM, SAM, SOM estimates
- **Competition**: Competitive landscape analysis
- **Positioning**: Unique value proposition
- **Growth Strategy**: Go-to-market approach

### Benchmarking Results

Compare the startup against industry peers:

#### Performance Metrics
- **Revenue Growth**: Percentile ranking vs. peers
- **Team Experience**: Founder background comparison
- **Market Opportunity**: Market size assessment
- **Competitive Position**: Differentiation analysis

#### Benchmark Categories
- **Industry**: Sector-specific comparisons
- **Stage**: Funding stage peer analysis
- **Geography**: Regional market dynamics
- **Business Model**: Similar revenue model companies

### Risk Assessment

Review identified risks across multiple categories:

#### Financial Risks
- **Burn Rate**: Cash runway concerns
- **Revenue Model**: Business model viability
- **Projections**: Unrealistic growth assumptions
- **Market Size**: Addressable market questions

#### Team Risks
- **Experience**: Founder and team background
- **Completeness**: Key role gaps
- **Commitment**: Full-time dedication
- **Track Record**: Previous startup experience

#### Market Risks
- **Competition**: Competitive threats
- **Timing**: Market readiness
- **Regulation**: Regulatory challenges
- **Technology**: Technical feasibility

#### Product Risks
- **Development**: Product completion status
- **Market Fit**: Product-market fit evidence
- **Scalability**: Technical scalability
- **IP Protection**: Intellectual property risks

### Investment Memo

The generated memo includes:

#### Executive Summary
- Investment recommendation (Pass, Consider, Recommend)
- Key highlights and concerns
- Recommended next steps

#### Company Overview
- Business description and model
- Market opportunity assessment
- Competitive positioning

#### Financial Analysis
- Historical performance review
- Financial projections evaluation
- Valuation assessment

#### Risk Analysis
- Critical risk factors
- Mitigation strategies
- Due diligence recommendations

#### Investment Recommendation
- Final recommendation with rationale
- Suggested terms and conditions
- Follow-up actions

## 💾 Exporting Results

### PDF Export

1. **Generate PDF**
   - Click "Export to PDF" on any results page
   - Choose export options (full report or sections)
   - Wait for PDF generation

2. **Download Options**
   - **Executive Summary**: 2-page overview
   - **Full Report**: Complete analysis (15-20 pages)
   - **Data Only**: Extracted metrics and benchmarks
   - **Custom**: Select specific sections

### Data Export

Export structured data in multiple formats:

#### JSON Export
```json
{
  "company": {
    "name": "ExampleCorp",
    "industry": "SaaS",
    "stage": "Series A"
  },
  "metrics": {
    "revenue": 5000000,
    "growth_rate": 0.45,
    "burn_rate": 200000
  },
  "risks": [
    {
      "category": "financial",
      "level": "medium",
      "description": "High burn rate relative to revenue"
    }
  ]
}
```

#### CSV Export
- Tabular data for spreadsheet analysis
- Metrics comparison across multiple companies
- Risk assessment summary

#### API Access
```bash
# Get analysis results via API
curl -H "Authorization: Bearer $TOKEN" \
  https://api.ai-analyst.app/v1/analysis/{job_id}
```

## 🔍 Advanced Features

### Bulk Processing

Process multiple documents simultaneously:

1. **Upload Multiple Files**
   - Select up to 10 files at once
   - Assign batch processing settings
   - Monitor progress for each document

2. **Batch Analysis**
   - Compare multiple companies side-by-side
   - Generate comparative analysis reports
   - Export batch results

### Custom Templates

Create custom memo templates:

1. **Template Editor**
   - Access template customization
   - Modify sections and formatting
   - Save custom templates

2. **Template Options**
   - **Standard**: Default investment memo format
   - **Detailed**: Comprehensive analysis template
   - **Executive**: Summary-focused template
   - **Custom**: User-defined template

### Collaboration Features

Share and collaborate on analysis:

1. **Team Workspaces**
   - Create shared workspaces
   - Invite team members
   - Manage permissions

2. **Comments and Notes**
   - Add comments to specific sections
   - Track discussion threads
   - Export comments with reports

3. **Review Workflow**
   - Submit for review
   - Approval workflows
   - Version control

## ⚙️ Settings & Preferences

### Account Settings

Configure your account preferences:

#### Profile Information
- Update contact details
- Change password
- Manage subscription

#### Notification Preferences
- Email notifications for completed analysis
- SMS alerts for critical issues
- In-app notification settings

#### Analysis Preferences
- Default industry categories
- Risk threshold settings
- Memo template preferences

### Integration Settings

Connect with external tools:

#### CRM Integration
- Salesforce connection
- HubSpot synchronization
- Custom API integrations

#### Data Sources
- Additional benchmarking databases
- Market research connections
- Financial data providers

## 🆘 Troubleshooting

### Common Issues

#### Upload Problems
**Issue**: File upload fails or hangs
**Solutions**:
- Check file size (must be under 50MB)
- Verify file format is supported
- Try uploading from different browser
- Clear browser cache and cookies

#### Processing Delays
**Issue**: Analysis takes longer than expected
**Solutions**:
- Check system status page
- Verify document quality and clarity
- Contact support for priority processing

#### Extraction Errors
**Issue**: Important information not extracted
**Solutions**:
- Ensure text is clearly readable
- Try higher quality scan/export
- Manually verify and correct data
- Provide feedback for improvement

### Getting Help

#### Support Channels
- **Help Center**: In-app help articles and FAQs
- **Email Support**: support@ai-analyst.app
- **Live Chat**: Available during business hours
- **Phone Support**: Available for Enterprise customers

#### Resources
- **Video Tutorials**: Step-by-step guides
- **Webinars**: Regular training sessions
- **User Community**: Forum for questions and tips
- **API Documentation**: For developers and integrations

## 📈 Best Practices

### Document Preparation

1. **Quality Guidelines**
   - Use high-resolution scans
   - Ensure text is clearly readable
   - Include all relevant slides
   - Remove password protection

2. **Content Optimization**
   - Include executive summary
   - Provide clear financial projections
   - Add team background information
   - Include market sizing data

### Analysis Review

1. **Data Validation**
   - Review extracted metrics for accuracy
   - Verify industry classification
   - Check benchmark comparisons
   - Validate risk assessments

2. **Contextual Review**
   - Add market context and notes
   - Consider qualitative factors
   - Include external research
   - Document assumptions

### Report Usage

1. **Investment Process**
   - Use as initial screening tool
   - Supplement with due diligence
   - Share with investment committee
   - Track investment outcomes

2. **Portfolio Management**
   - Compare portfolio companies
   - Track performance over time
   - Identify best practices
   - Support value creation

---

*For additional assistance, contact our support team or visit the help center.*