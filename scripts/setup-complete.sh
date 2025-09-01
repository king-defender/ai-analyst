#!/bin/bash

# AI Analyst MVP - Complete Development Setup Script
# This script sets up the full development environment for the AI Analyst MVP

set -e

echo "🚀 Setting up AI Analyst MVP Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 18+ and try again."
        exit 1
    fi
    
    NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        print_error "Node.js version 18+ is required. Current version: $(node -v)"
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.9+ and try again."
        exit 1
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_warning "Docker is not installed. Docker is recommended for local development."
    fi
    
    print_status "✅ System requirements check passed"
}

# Setup Backend
setup_backend() {
    print_status "Setting up backend environment..."
    
    cd backend
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Create uploads directory
    mkdir -p uploads
    
    # Copy environment file
    if [ ! -f ".env" ]; then
        cp .env.example .env
        print_status "Created .env file from .env.example"
        print_warning "Please update .env file with your configuration"
    fi
    
    cd ..
    print_status "✅ Backend setup completed"
}

# Setup Frontend
setup_frontend() {
    print_status "Setting up frontend environment..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    # Copy environment file
    if [ ! -f ".env.local" ]; then
        cp .env.local.example .env.local
        print_status "Created .env.local file from .env.local.example"
    fi
    
    cd ..
    print_status "✅ Frontend setup completed"
}

# Setup ML Pipeline
setup_ml() {
    print_status "Setting up ML pipeline..."
    
    cd ml
    
    # Install ML dependencies
    print_status "Installing ML dependencies..."
    pip install -r requirements.txt
    
    cd ..
    print_status "✅ ML pipeline setup completed"
}

# Setup Database (Local Development)
setup_database() {
    print_status "Setting up local database..."
    
    # Create sample data directories
    mkdir -p sample_data/processed
    mkdir -p sample_data/benchmarks
    
    print_status "✅ Database setup completed"
}

# Run tests
run_tests() {
    print_status "Running test suite..."
    
    # Backend tests
    cd backend
    source venv/bin/activate
    
    print_status "Running backend tests..."
    python -m pytest tests/ -v || print_warning "Some backend tests failed"
    
    cd ../frontend
    
    print_status "Running frontend tests..."
    npm test -- --watchAll=false || print_warning "Some frontend tests failed"
    
    cd ..
    print_status "✅ Test suite completed"
}

# Start development servers
start_dev_servers() {
    print_status "Starting development servers..."
    
    # Check if tmux is available for better session management
    if command -v tmux &> /dev/null; then
        print_status "Using tmux for session management..."
        
        # Create tmux session
        tmux new-session -d -s ai-analyst
        
        # Backend window
        tmux new-window -t ai-analyst -n backend
        tmux send-keys -t ai-analyst:backend "cd backend && source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000" Enter
        
        # Frontend window
        tmux new-window -t ai-analyst -n frontend
        tmux send-keys -t ai-analyst:frontend "cd frontend && npm run dev" Enter
        
        print_status "✅ Development servers started in tmux session 'ai-analyst'"
        print_status "Use 'tmux attach -t ai-analyst' to view the session"
        print_status "Use 'tmux kill-session -t ai-analyst' to stop all servers"
        
    else
        print_warning "tmux not found. Starting servers in background..."
        
        # Start backend
        cd backend
        source venv/bin/activate
        nohup uvicorn main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
        BACKEND_PID=$!
        
        # Start frontend
        cd ../frontend
        nohup npm run dev > ../frontend.log 2>&1 &
        FRONTEND_PID=$!
        
        cd ..
        
        # Save PIDs
        echo $BACKEND_PID > backend.pid
        echo $FRONTEND_PID > frontend.pid
        
        print_status "✅ Development servers started in background"
        print_status "Backend PID: $BACKEND_PID (logs: backend.log)"
        print_status "Frontend PID: $FRONTEND_PID (logs: frontend.log)"
        print_status "Use 'kill \$(cat backend.pid frontend.pid)' to stop servers"
    fi
}

# Show final information
show_info() {
    echo ""
    echo "🎉 AI Analyst MVP setup completed successfully!"
    echo ""
    echo "📍 Service URLs:"
    echo "   Frontend:  http://localhost:3000"
    echo "   Backend:   http://localhost:8000"
    echo "   API Docs:  http://localhost:8000/docs"
    echo ""
    echo "📁 Project Structure:"
    echo "   frontend/     - Next.js frontend application"
    echo "   backend/      - FastAPI backend application"
    echo "   ml/           - ML pipeline and models"
    echo "   infra/        - Infrastructure configurations"
    echo "   docs/         - Documentation"
    echo ""
    echo "🔧 Development Commands:"
    echo "   Backend:  cd backend && source venv/bin/activate && uvicorn main:app --reload"
    echo "   Frontend: cd frontend && npm run dev"
    echo "   Tests:    npm test (frontend) | python -m pytest (backend)"
    echo ""
    echo "📚 Documentation:"
    echo "   API Reference: docs/api-reference.md"
    echo "   Deployment:    docs/deployment.md"
    echo "   Contributing:  docs/CONTRIBUTING.md"
    echo ""
    echo "🚀 Ready to start developing!"
}

# Main execution
main() {
    echo "AI Analyst MVP - Complete Development Setup"
    echo "=========================================="
    
    check_requirements
    setup_backend
    setup_frontend
    setup_ml
    setup_database
    
    # Ask if user wants to run tests
    read -p "Do you want to run the test suite? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_tests
    fi
    
    # Ask if user wants to start dev servers
    read -p "Do you want to start development servers now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        start_dev_servers
    fi
    
    show_info
}

# Run main function
main "$@"