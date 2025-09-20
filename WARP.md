# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

Project summary
- Monorepo with three primary parts:
  - frontend/ (Next.js 14 + TypeScript)
  - backend/ (Python FastAPI API server)
  - ml/ (Python ML utilities and risk engine)
- See README.md for prerequisites (Node.js, Python, optional Docker, GCP auth setup) and docs/ for detailed guides.

Common commands

Frontend (Next.js)
- Install: cd frontend && npm install
- Dev server: cd frontend && npm run dev
- Build: cd frontend && npm run build
- Start (prod): cd frontend && npm start
- Lint: cd frontend && npm run lint
- Lint (fix): cd frontend && npm run lint:fix
- Format: cd frontend && npm run format
- Type check: cd frontend && npm run type-check
- Tests (all): cd frontend && npm test
- Tests (watch): cd frontend && npm run test:watch
- Tests (coverage): cd frontend && npm run test:coverage
- Test a single file: cd frontend && npm test -- src/path/to/testfile.test.tsx
- Run a single test by name: cd frontend && npm test -- -t "test name substring"
- Environment: NEXT_PUBLIC_API_URL controls API base (defaults to http://localhost:8000). Create .env.local from .env.local.example.

Backend (FastAPI)
- Install: cd backend && pip install -r requirements.txt
- Dev server (reload): cd backend && uvicorn main:app --reload --port 8000
- Health check: GET http://localhost:8000/api/health
- Lint (flake8): cd backend && flake8 app tests
- Format check: cd backend && black --check . && isort --check-only .
- Format write: cd backend && black . && isort .
- Type check: cd backend && mypy app
- Tests (all): cd backend && python -m pytest
- Tests (by folder): cd backend && python -m pytest tests/unit/  or  tests/integration/
- Tests (single file): cd backend && python -m pytest tests/unit/test_file_service.py -v
- Tests (single test): cd backend && python -m pytest tests/unit/test_file_service.py::test_saves_file -q
- Filter by keyword: cd backend && python -m pytest -k "upload and not slow"
- Coverage: pytest.ini is configured to collect coverage for app with HTML/XML reports; coverage is produced automatically by running pytest.
- Test env: Some endpoints/services branch on TESTING=true; for parity, set TESTING=true in the environment when running tests.

ML
- Install: cd ml && pip install -r requirements.txt
- Tests (all): cd ml && python -m pytest tests/ -v
- Tests (single file): cd ml && python -m pytest tests/unit/test_risk_engine.py -v

Docker (developer-focused)
- Backend dev image: cd backend && docker build -f Dockerfile.dev -t ai-analyst-backend-dev .
- Backend dev run (hot reload): docker run -p 8000:8000 -v $(pwd):/app --env-file .env ai-analyst-backend-dev
- Backend prod image: cd backend && docker build -t ai-analyst-backend .
- Backend prod run: docker run -p 8000:8000 --env-file .env ai-analyst-backend

Key architecture and flow

High-level
- frontend (Next.js app directory) calls backend REST endpoints; backend orchestrates file upload, job tracking, analysis, memo generation; ml contains a rule-based risk engine and tests. GCP services (Firestore, Storage, Vision, Vertex AI, BigQuery) are targeted in requirements and docs, with stubs or placeholders used for MVP/dev paths.

Frontend
- Entry: frontend/src/app (Next.js App Router). UI components under frontend/src/components/ (e.g., upload, status, memo, risk display). Hooks for polling and uploads under frontend/src/hooks/.
- API client: frontend/src/lib/api.ts centralizes calls to:
  - POST /api/documents/upload (multipart) -> returns { job_id, file_id }
  - GET /api/jobs/{job_id}/status
  - GET /api/analysis/{file_id}/benchmarks
  - GET /api/analysis/{file_id}/risks
  - POST /api/memos/generate
  - GET /api/memos/{memo_id}/pdf
- Environment: NEXT_PUBLIC_API_URL is read for API base; defaults to http://localhost:8000 for local dev.
- Testing: jest with next/jest, jsdom, coverage thresholds configured; tests live under frontend/src/**/__tests__ and *.{test,spec}.tsx.

Backend
- App entrypoint: backend/main.py creates FastAPI app with a lifespan context manager, CORS, and global exception handler.
- Routers included (all prefixed with /api):
  - app/routers/documents.py -> /documents: file upload, file info, extracted data routes. Upload validates content-type, size, JSON-special handling.
  - app/routers/analysis.py -> /analysis: start analysis, fetch benchmarks, risk assessment, results.
  - app/routers/memos.py -> /memos: generate memo and retrieve memo/PDF.
  - app/routers/jobs.py -> /jobs: job status, listing, retry, logs.
- Services (selected):
  - JobService (app/services/job_service.py): in-memory job store for MVP with file_id↔job_id mapping. Firestore helpers exist but main routes rely on in-memory service; CI sets TESTING=true to stub external clients.
  - RiskService (app/services/risk_service.py): returns sample/demonstration risk output; includes a more detailed assess_risks_detailed path with scoring helpers.
  - Additional services (analysis_service.py, file_service.py, benchmark_service.py, memo_service.py, ocr_service.py, parsing_service.py) structure responsibilities for pipeline orchestration, file persistence, OCR, parsing, and output, with MVP behavior noted in code.
- Settings: app/core/config.py uses pydantic-settings with .env; notable fields: DEBUG, ENVIRONMENT, allowed CORS origins, API_HOST/API_PORT, GCP project/location variables, JWT config, OPENAI_API_KEY placeholder.
- CORS: In debug, allows http://localhost:3000/127.0.0.1:3000 by default; otherwise uses ALLOWED_HOSTS from settings.
- Health: /api/health (structured), and legacy /health.

ML
- Core: ml/pipeline/risk_engine.py implements a rule-based risk engine with enumerated categories and severity levels; exposes assess_startup plus helpers for scoring and mitigation suggestions. This is validated by ml/tests.
- Status: Not directly wired into backend services in current MVP; integration points are planned/represented via RiskService placeholders in the backend.

Continuous Integration (reference parity locally)
- Backend jobs (GitHub Actions) install from backend/requirements.txt, set TESTING=true, and run:
  - Unit tests with coverage: python -m pytest tests/unit/ -v --cov=app --cov-report=xml
  - Integration tests: python -m pytest tests/integration/ -v
  - A targeted test: python -m pytest tests/test_main.py::test_basic_service_imports -v
- Frontend jobs install with npm ci, run lint, type-check, and jest coverage (watchAll=false).
- ML jobs install ml/requirements.txt and run pytest with coverage on pipeline.
- Replicate locally as needed with the commands above; set TESTING=true for backend parity when tests expect stubbed services.

Important references from repository docs
- Root README.md contains Quick Start (including optional Docker dev), testing commands per subproject, and the architecture diagram; consult it for environment prerequisites and GCP auth steps (gcloud auth application-default login).
- docs/ includes GCP setup, deployment, API references, and troubleshooting. Use these when configuring cloud credentials and deploying to Cloud Run.

Notes for future Warp instances
- Prefer running subproject commands from their directories (frontend/, backend/, ml/). The top-level package.json is not used to orchestrate tasks.
- For local full-stack dev: start backend on :8000 and frontend on :3000; ensure NEXT_PUBLIC_API_URL points at the backend URL.
- Some backend services are MVP stubs; if you need real cloud integrations during development, review app/core/config.py and service implementations to ensure required GCP credentials and resources are configured.
