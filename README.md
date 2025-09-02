# AI Analyst MVP

An AI-powered analyst that ingests startup pitch decks, benchmarks startups against peers, flags risks with explainable reasoning, and delivers investor-ready deal notes.

## 🎯 Project Overview

The AI Analyst MVP is designed to automate the initial screening and analysis of startup investments by:

- **Ingesting** pitch decks (PDF) and call transcripts
- **Extracting** key company data, metrics, and team information
- **Benchmarking** against peer companies and industry standards
- **Flagging** potential risks with evidence-based reasoning
- **Generating** concise, investor-ready deal memos

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│    Frontend     │    │     Backend      │    │   ML Pipeline   │
│   (React/TS)    │◄──►│  (Python/FastAPI)│◄──►│ (Vertex AI/LLM) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   GCP Services   │
                    │ • Cloud Vision   │
                    │ • Vertex AI      │
                    │ • BigQuery       │
                    │ • Cloud Storage  │
                    └──────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Google Cloud SDK
- GCP Project with enabled APIs

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/king-defender/ai-analyst.git
   cd ai-analyst
   ```

2. **Setup Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   # Configure your GCP credentials and project settings
   ```

3. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   cp .env.local.example .env.local
   # Configure API endpoints
   ```

4. **GCP Configuration**
   ```bash
   # Follow the setup guide in docs/gcp-setup.md
   gcloud auth application-default login
   gcloud config set project YOUR_PROJECT_ID
   ```

### Development

```bash
# Start backend (from backend/)
uvicorn main:app --reload --port 8000

# Start frontend (from frontend/)
npm run dev

# Run ML pipeline (from ml/)
python -m pipeline.main
```

## 📁 Project Structure

```
ai-analyst/
├── frontend/          # React/TypeScript web application
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/           # Python FastAPI server
│   ├── app/
│   ├── tests/
│   └── requirements.txt
├── ml/               # ML pipeline and models
│   ├── pipeline/
│   ├── prompts/
│   └── models/
├── infra/            # Infrastructure as Code
│   ├── terraform/
│   └── gcp/
├── sample_data/      # Sample datasets and examples
│   ├── pitch_decks/
│   ├── benchmarks/
│   └── outputs/
└── docs/            # Documentation
    ├── api/
    ├── setup/
    └── guides/
```

## 🔧 Tech Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **File Upload**: React Dropzone
- **PDF Viewing**: React PDF

### Backend
- **Framework**: FastAPI (Python)
- **Database**: Cloud Firestore
- **File Storage**: Google Cloud Storage
- **OCR**: Google Cloud Vision API
- **Authentication**: Firebase Auth

### ML & AI
- **LLM**: Google Vertex AI (Gemini)
- **Vector Search**: Vertex AI Vector Search
- **Data Processing**: BigQuery
- **Prompt Engineering**: Custom templates

### Infrastructure
- **Cloud Provider**: Google Cloud Platform
- **Deployment**: Cloud Run
- **Monitoring**: Cloud Logging & Monitoring
- **CI/CD**: GitHub Actions

## 📊 Core Features

### 1. Document Ingestion
- PDF pitch deck upload and processing
- OCR extraction from slides and images
- Text parsing and structure detection

### 2. Data Extraction
- Company information and metrics
- Team background and experience
- Financial projections and KPIs
- Market size and opportunity

### 3. Benchmarking Engine
- Peer company comparison
- Industry standard metrics
- Growth rate analysis
- Valuation benchmarks

### 4. Risk Assessment
- Red flag detection with evidence
- Financial risk analysis
- Market risk evaluation
- Team and execution risks

### 5. Memo Generation
- Structured deal note format
- Executive summary
- Investment recommendation
- Supporting evidence and data

## 🔐 Security & Privacy

- End-to-end encryption for sensitive documents
- Role-based access control
- Audit logging for all actions
- GDPR compliance for data handling
- Secure credential management

## 🧪 Testing

```bash
# Backend tests
cd backend && python -m pytest

# Frontend tests
cd frontend && npm test

# Integration tests
cd backend && python -m pytest tests/integration/

# ML pipeline tests
cd ml && python -m pytest tests/
```

## 📈 Performance Targets

- **Processing Time**: < 15 minutes per pitch deck
- **Risk Detection**: > 70% recall on known red flags
- **Extraction Accuracy**: > 90% for key metrics
- **Uptime**: 99.5% availability
- **Response Time**: < 2 seconds for API calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Documentation

### User Documentation
- 📖 **[User Guide](docs/USER_GUIDE.md)**: Complete guide for using the application
- 🔧 **[Troubleshooting](docs/TROUBLESHOOTING.md)**: Solutions to common issues and debugging

### Developer Documentation
- 🤝 **[Contributing Guide](docs/CONTRIBUTING.md)**: Guidelines for contributors
- 🏗️ **[API Reference](docs/api-reference.md)**: Comprehensive API documentation
- ⚙️ **[GCP Setup](docs/gcp-setup.md)**: Google Cloud Platform configuration
- 🚀 **[Deployment Guide](docs/deployment.md)**: Production deployment instructions

### Operations Documentation
- 👥 **[Team Structure](docs/TEAM_STRUCTURE.md)**: Roles, responsibilities, and organization
- 🔧 **[Operations Manual](docs/OPERATIONS.md)**: System operations and monitoring procedures

## 🆘 Support

- 📖 **Documentation**: [docs/](docs/)
- 🐛 **Issues**: [GitHub Issues](https://github.com/king-defender/ai-analyst/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/king-defender/ai-analyst/discussions)

## 🎯 Roadmap

See our [Project Board](https://github.com/king-defender/ai-analyst/projects) for detailed progress and upcoming features.

### MVP Milestones
- [x] Repository and infrastructure setup
- [ ] Basic document ingestion pipeline
- [ ] Core extraction and parsing
- [ ] Benchmarking system implementation
- [ ] Risk assessment engine
- [ ] Memo generation and export
- [ ] Frontend UI/UX implementation
- [ ] End-to-end testing and validation