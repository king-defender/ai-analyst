# Testing Guide for AI Analyst MVP

This document provides comprehensive information about the testing infrastructure and practices for the AI Analyst MVP project.

## 📋 Overview

Our testing strategy covers multiple levels of validation to ensure code quality and reliability:

- **Unit Tests**: Test individual functions and components in isolation
- **Integration Tests**: Test interactions between modules and services
- **End-to-End Tests**: Test complete user workflows
- **Mock/Emulation**: Test external dependencies without actual API calls
- **Coverage Reporting**: Track test coverage across all components
- **CI/CD Integration**: Automated testing on every commit and PR

## 🏗️ Test Organization Structure

```
backend/
├── tests/
│   ├── conftest.py          # Shared test configuration and fixtures
│   ├── unit/                # Unit tests for individual components
│   │   ├── test_file_service.py
│   │   ├── test_ocr_service.py
│   │   └── test_risk_service.py
│   ├── integration/         # Integration tests for workflows
│   │   └── test_api_endpoints.py
│   ├── e2e/                 # End-to-end tests
│   └── test_main.py         # Main application tests

frontend/src/__tests__/
├── unit/                    # Unit tests for React components
│   ├── upload.test.tsx
│   └── data-display.test.tsx
├── integration/             # Integration tests for user flows
└── e2e/                     # End-to-end browser tests

ml/
├── tests/
│   ├── conftest.py          # ML test configuration
│   ├── unit/                # Unit tests for ML pipeline
│   │   └── test_risk_engine.py
│   └── integration/         # Integration tests for ML workflows
```

## 🧪 Running Tests

### Backend Tests

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run all tests
python -m pytest

# Run specific test categories
python -m pytest tests/unit/ -v                    # Unit tests only
python -m pytest tests/integration/ -v             # Integration tests only
python -m pytest tests/unit/test_file_service.py   # Specific test file

# Run with coverage
python -m pytest --cov=app --cov-report=html --cov-report=term

# Run tests with specific markers
python -m pytest -m "not slow"                     # Skip slow tests
python -m pytest tests/integration/ --slow         # Run integration tests
```

### Frontend Tests

```bash
# Install dependencies
cd frontend
npm install

# Run all tests
npm test

# Run tests in watch mode (for development)
npm run test:watch

# Run tests with coverage
npm test -- --coverage

# Run specific test files
npm test -- upload.test.tsx
npm test -- --testPathPattern=unit
```

### ML Pipeline Tests

```bash
# Install dependencies
cd ml
pip install -r requirements.txt

# Run ML tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=pipeline --cov-report=html
```

### End-to-End Tests

```bash
# Run full integration tests
scripts/test-e2e.sh

# Or individual E2E test categories
cd backend && python -m pytest tests/e2e/ -v
cd frontend && npm run test:e2e
```

## 🎯 Test Categories

### Unit Tests

**Purpose**: Test individual functions and components in isolation

**Backend Examples**:
```python
# Test file validation
def test_validate_file_type_valid_pdf(file_service):
    result = file_service.validate_file_type("test.pdf", "application/pdf")
    assert result is True

# Test risk calculation
def test_calculate_runway_risk(risk_service):
    short_runway = {"runway_months": 6}
    risk_score = risk_service.calculate_runway_risk(short_runway)
    assert risk_score > 60  # Should be high risk
```

**Frontend Examples**:
```typescript
// Test component rendering
test('renders upload area', () => {
  render(<FileUpload onFileUpload={mockCallback} />);
  expect(screen.getByText('Drag and drop files here')).toBeInTheDocument();
});

// Test user interactions
test('handles file selection', () => {
  render(<FileUpload onFileUpload={mockCallback} />);
  const file = new File(['content'], 'test.pdf', { type: 'application/pdf' });
  fireEvent.change(fileInput, { target: { files: [file] } });
  expect(mockCallback).toHaveBeenCalledWith(file);
});
```

### Integration Tests

**Purpose**: Test interactions between modules and services

**Examples**:
```python
# Test complete document upload workflow
async def test_document_upload_workflow(test_client):
    files = {"file": ("test.pdf", test_file, "application/pdf")}
    response = test_client.post("/api/documents/upload", files=files)
    assert response.status_code == 200
    assert "job_id" in response.json()

# Test risk assessment with real data flow
async def test_risk_assessment_integration(risk_service, sample_data):
    result = await risk_service.assess_startup(sample_data)
    assert "overall_risk_score" in result
    assert len(result["risk_factors"]) > 0
```

### End-to-End Tests

**Purpose**: Test complete user workflows from frontend to backend

**Examples**:
- File upload → OCR processing → Risk assessment → Memo generation
- User registration → Document upload → Report generation → PDF export
- Error handling workflows → User feedback → Recovery processes

## 🎭 Mocking and Test Doubles

### External Service Mocking

We mock all external dependencies to ensure tests are:
- **Fast**: No network calls or external API dependencies
- **Reliable**: Tests don't fail due to external service issues
- **Isolated**: Each test focuses on the component being tested

**Mocked Services**:
```python
# Google Cloud Services
@pytest.fixture
def mock_firestore():
    with patch('google.cloud.firestore.Client') as mock:
        # Mock Firestore operations
        yield mock

@pytest.fixture 
def mock_vision():
    with patch('google.cloud.vision.ImageAnnotatorClient') as mock:
        # Mock OCR text extraction
        yield mock

@pytest.fixture
def mock_openai():
    with patch('openai.AsyncOpenAI') as mock:
        # Mock AI completions
        yield mock
```

### Test Data and Fixtures

**Sample Data**:
```python
@pytest.fixture
def sample_startup_data():
    return {
        "company_name": "TechFlow Solutions",
        "metrics": {
            "revenue_arr": 2500000,
            "monthly_growth_rate": 0.25,
            "runway_months": 18
        },
        "team": [{"name": "John Doe", "experience_years": 10}]
    }
```

## 📊 Coverage Reporting

### Coverage Targets

- **Backend**: Minimum 80% code coverage
- **Frontend**: Minimum 75% code coverage  
- **ML Pipeline**: Minimum 70% code coverage
- **Critical Paths**: 95% coverage for core business logic

### Generating Coverage Reports

```bash
# Backend HTML coverage report
cd backend
python -m pytest --cov=app --cov-report=html
open htmlcov/index.html

# Frontend coverage report
cd frontend  
npm test -- --coverage
open coverage/lcov-report/index.html

# ML pipeline coverage
cd ml
python -m pytest --cov=pipeline --cov-report=html
open htmlcov/index.html
```

### Coverage Integration

Coverage reports are automatically:
- Generated on every test run
- Uploaded to Codecov in CI/CD
- Tracked for coverage trends
- Used as quality gates for PRs

## 🔄 Continuous Integration

### GitHub Actions Workflow

Our CI pipeline runs on every push and pull request:

1. **Parallel Test Execution**:
   - Backend tests (Python 3.9, 3.10, 3.11)
   - Frontend tests (Node 18.x, 20.x)
   - ML pipeline tests (Python 3.11)

2. **Quality Checks**:
   - Code linting and formatting
   - Type checking (TypeScript)
   - Security scanning
   - Coverage reporting

3. **Integration Validation**:
   - Cross-service integration tests
   - API contract validation
   - Build verification

### Quality Gates

All PRs must pass:
- ✅ All tests passing
- ✅ Coverage thresholds met
- ✅ No linting errors
- ✅ Security scan clean
- ✅ Type checking passed

## 🛠️ Testing Best Practices

### Writing Good Tests

1. **Test Structure (AAA Pattern)**:
   ```python
   def test_calculate_risk():
       # Arrange
       data = {"runway_months": 6}
       service = RiskService()
       
       # Act
       result = service.calculate_runway_risk(data)
       
       # Assert
       assert result > 60
   ```

2. **Descriptive Test Names**:
   ```python
   # Good
   def test_short_runway_returns_high_risk_score()
   
   # Bad  
   def test_risk()
   ```

3. **Test One Thing**:
   ```python
   # Good - focused test
   def test_validates_pdf_files():
       assert service.validate_file_type("test.pdf", "application/pdf")
   
   # Bad - testing multiple concerns
   def test_file_processing():
       # Tests validation AND upload AND processing
   ```

### Test Data Management

```python
# Use factories for complex data
def create_startup_data(**overrides):
    defaults = {
        "company_name": "Test Company",
        "metrics": {"runway_months": 12}
    }
    defaults.update(overrides)
    return defaults

# Use parameterized tests for multiple scenarios
@pytest.mark.parametrize("runway,expected_risk", [
    (3, "high"),
    (12, "medium"), 
    (24, "low")
])
def test_runway_risk_levels(runway, expected_risk):
    data = {"runway_months": runway}
    risk = service.calculate_runway_risk(data)
    assert risk.level == expected_risk
```

### Async Testing

```python
# Testing async functions
@pytest.mark.asyncio
async def test_async_service():
    result = await service.process_document(file_data)
    assert result is not None

# Testing with mock async calls
@pytest.mark.asyncio
async def test_with_mock_async():
    with patch.object(service, 'external_call', new_callable=AsyncMock) as mock:
        mock.return_value = {"success": True}
        result = await service.process()
        assert result["success"]
```

## 🚀 Running Tests in Development

### Pre-commit Testing

```bash
# Quick test suite (before commits)
cd backend && python -m pytest tests/unit/ -x -v
cd frontend && npm test -- --watchAll=false --bail

# Full test suite (before PRs)
scripts/run-all-tests.sh
```

### Test-Driven Development (TDD)

1. **Write failing test first**:
   ```python
   def test_new_feature():
       result = service.new_feature("input")
       assert result == "expected_output"
   ```

2. **Implement minimal code to pass**
3. **Refactor and improve**
4. **Repeat cycle**

### Debugging Tests

```bash
# Run specific test with debugging
python -m pytest tests/unit/test_file_service.py::test_upload -v -s

# Drop into debugger on failure
python -m pytest --pdb

# Run with verbose output
python -m pytest -vvv
```

## 📈 Performance Testing

### Load Testing

```python
# Example load test for API endpoints
import asyncio
import aiohttp

async def load_test_upload():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(100):  # 100 concurrent uploads
            task = upload_file(session, f"test_file_{i}.pdf")
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        success_rate = sum(1 for r in results if r.status == 200) / len(results)
        assert success_rate > 0.95  # 95% success rate
```

### Performance Benchmarks

```python
# Benchmark critical operations
def test_ocr_performance():
    start_time = time.time()
    result = ocr_service.extract_text(large_document)
    duration = time.time() - start_time
    
    assert duration < 30  # Should complete within 30 seconds
    assert len(result) > 0
```

## 🔧 Test Configuration

### Environment Variables

```bash
# Test environment settings
export TESTING=true
export GOOGLE_CLOUD_PROJECT=test-project
export DATABASE_URL=sqlite:///test.db
export REDIS_URL=redis://localhost:6379/1
```

### Test Database Setup

```python
# Database fixtures for integration tests
@pytest.fixture(scope="session")
def test_db():
    # Create test database
    db = create_test_database()
    yield db
    # Cleanup
    db.drop_all()
```

## 🎯 Advanced Testing Patterns

### Property-Based Testing

```python
from hypothesis import given, strategies as st

@given(st.integers(min_value=1, max_value=60))
def test_runway_risk_properties(runway_months):
    """Test risk calculation properties across input range"""
    risk = service.calculate_runway_risk({"runway_months": runway_months})
    
    # Properties that should always hold
    assert 0 <= risk <= 100
    assert isinstance(risk, (int, float))
    
    # Risk should increase as runway decreases
    if runway_months <= 6:
        assert risk >= 60  # High risk for short runway
```

### Contract Testing

```python
# API contract tests
def test_upload_endpoint_contract():
    """Ensure API contract is maintained"""
    response = client.post("/api/documents/upload", files=test_file)
    
    # Response structure contract
    assert "job_id" in response.json()
    assert "file_id" in response.json()
    assert "filename" in response.json()
    assert isinstance(response.json()["job_id"], str)
```

## 📚 Resources

### Documentation
- [pytest Documentation](https://docs.pytest.org/)
- [Jest Testing Framework](https://jestjs.io/docs/getting-started)
- [Testing Library React](https://testing-library.com/docs/react-testing-library/intro/)

### Tools
- **Backend**: pytest, pytest-asyncio, pytest-cov, httpx
- **Frontend**: Jest, Testing Library, MSW (Mock Service Worker)
- **E2E**: Playwright, Cypress
- **Coverage**: Codecov, Coverage.py

### Best Practices
- [Google Testing Blog](https://testing.googleblog.com/)
- [Martin Fowler - Testing](https://martinfowler.com/testing/)
- [Test Pyramid Concept](https://martinfowler.com/articles/practical-test-pyramid.html)

---

## 🆘 Getting Help

If you encounter issues with tests:

1. **Check the logs**: Review test output for specific error messages
2. **Verify environment**: Ensure all dependencies are installed
3. **Check mocks**: Verify external services are properly mocked
4. **Run individual tests**: Isolate failing tests for debugging
5. **Ask for help**: Create an issue or reach out to the team

Happy testing! 🚀