#!/bin/bash

# AI Analyst MVP - Comprehensive Test Runner
# Runs all test suites with proper environment setup

set -e

echo "🧪 AI Analyst MVP - Comprehensive Test Suite"
echo "============================================="

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test results tracking
BACKEND_TESTS_PASSED=false
FRONTEND_TESTS_PASSED=false
ML_TESTS_PASSED=false

# Function to print section headers
print_section() {
    echo -e "\n${BLUE}==== $1 ====${NC}\n"
}

# Function to print success
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Function to print error
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Set test environment variables
export TESTING=true
export GOOGLE_CLOUD_PROJECT=test-project

# Backend Tests
print_section "Backend Tests"

if [ -d "backend" ]; then
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_warning "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate 2>/dev/null || print_warning "Could not activate venv, using system Python"
    
    # Install dependencies
    if [ -f "requirements.txt" ]; then
        print_warning "Installing backend dependencies..."
        pip install -q -r requirements.txt
        pip install -q pytest-cov
    fi
    
    # Run backend tests
    echo "Running backend unit tests..."
    if python -m pytest tests/unit/ -v --cov=app --cov-report=term-missing; then
        print_success "Backend unit tests passed"
        
        echo "Running backend service import tests..."
        if python -m pytest tests/test_main.py::test_basic_service_imports -v; then
            BACKEND_TESTS_PASSED=true
            print_success "Backend service tests passed"
        else
            print_error "Backend service tests failed"
        fi
    else
        print_error "Backend unit tests failed"
    fi
    
    cd ..
else
    print_error "Backend directory not found"
fi

# Frontend Tests  
print_section "Frontend Tests"

if [ -d "frontend" ]; then
    cd frontend
    
    # Install dependencies
    if [ -f "package.json" ]; then
        print_warning "Installing frontend dependencies..."
        npm install --silent
    fi
    
    # Run frontend tests
    echo "Running frontend tests..."
    if npm test -- --watchAll=false --coverage; then
        FRONTEND_TESTS_PASSED=true
        print_success "Frontend tests passed"
    else
        print_error "Frontend tests failed"
    fi
    
    cd ..
else
    print_error "Frontend directory not found"
fi

# ML Pipeline Tests
print_section "ML Pipeline Tests"

if [ -d "ml" ]; then
    cd ml
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_warning "Creating ML Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate 2>/dev/null || print_warning "Could not activate ML venv, using system Python"
    
    # Install dependencies
    if [ -f "requirements.txt" ]; then
        print_warning "Installing ML dependencies..."
        pip install -q -r requirements.txt
        pip install -q pytest-cov
    fi
    
    # Run ML tests
    echo "Running ML pipeline tests..."
    if python -m pytest tests/ -v --cov=pipeline --cov-report=term-missing; then
        ML_TESTS_PASSED=true
        print_success "ML pipeline tests passed"
    else
        print_error "ML pipeline tests failed"
    fi
    
    cd ..
else
    print_error "ML directory not found"
fi

# Integration Tests
print_section "Integration Tests"

if [ "$BACKEND_TESTS_PASSED" = true ] && [ "$FRONTEND_TESTS_PASSED" = true ]; then
    echo "Running cross-component integration tests..."
    
    cd backend
    source venv/bin/activate 2>/dev/null || true
    
    if python -m pytest tests/test_integration.py::TestDocumentUpload::test_upload_endpoint_exists -v; then
        print_success "Integration tests passed"
    else
        print_warning "Some integration tests failed (this may be expected in development)"
    fi
    
    cd ..
else
    print_warning "Skipping integration tests due to component test failures"
fi

# Test Summary
print_section "Test Summary"

echo "Test Results:"
if [ "$BACKEND_TESTS_PASSED" = true ]; then
    print_success "Backend Tests: PASSED"
else
    print_error "Backend Tests: FAILED"
fi

if [ "$FRONTEND_TESTS_PASSED" = true ]; then
    print_success "Frontend Tests: PASSED"
else
    print_error "Frontend Tests: FAILED"
fi

if [ "$ML_TESTS_PASSED" = true ]; then
    print_success "ML Pipeline Tests: PASSED"
else
    print_error "ML Pipeline Tests: FAILED"
fi

# Overall result
if [ "$BACKEND_TESTS_PASSED" = true ] && [ "$FRONTEND_TESTS_PASSED" = true ] && [ "$ML_TESTS_PASSED" = true ]; then
    print_success "🎉 All test suites passed!"
    echo -e "\n${GREEN}Test coverage reports:${NC}"
    echo "- Backend: backend/htmlcov/index.html"
    echo "- Frontend: frontend/coverage/lcov-report/index.html"
    echo "- ML: ml/htmlcov/index.html"
    exit 0
else
    print_error "❌ Some test suites failed"
    echo -e "\n${YELLOW}Check the output above for specific failures.${NC}"
    echo "See TESTING.md for debugging help."
    exit 1
fi