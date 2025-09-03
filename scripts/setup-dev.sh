#!/bin/bash

# AI Analyst MVP - Development Setup Script

set -e

echo "🚀 Setting up AI Analyst MVP development environment..."

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ required. Current version: $(node --version)"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f2)
if [ "$PYTHON_VERSION" -lt 9 ]; then
    echo "❌ Python 3.9+ required. Current version: $(python3 --version)"
    exit 1
fi

# Check gcloud (optional for local development)
if command -v gcloud &> /dev/null; then
    echo "✅ Google Cloud SDK found"
else
    echo "⚠️  Google Cloud SDK not found. Install for full functionality."
fi

echo "✅ Prerequisites check passed"

# Setup backend
echo "🐍 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating backend environment file..."
    cp .env.example .env
    echo "⚠️  Please configure your .env file with actual values"
fi

cd ..

# Setup frontend
echo "⚛️  Setting up frontend..."
cd frontend

echo "Installing Node.js dependencies..."
npm install

if [ ! -f ".env.local" ]; then
    echo "Creating frontend environment file..."
    cp .env.local.example .env.local
    echo "⚠️  Please configure your .env.local file with actual values"
fi

cd ..

# Setup ML pipeline
echo "🤖 Setting up ML pipeline..."
cd ml

if [ ! -d "venv" ]; then
    echo "Creating ML Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating ML virtual environment..."
source venv/bin/activate

echo "Installing ML dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

cd ..

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p tmp
mkdir -p sample_data/pitch_decks
mkdir -p sample_data/outputs

# Setup git hooks (optional)
if [ -d ".git" ]; then
    echo "⚙️  Setting up git hooks..."
    
    # Pre-commit hook for formatting
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Format Python code
cd backend && source venv/bin/activate && black . && isort .
cd ../frontend && npm run lint:fix
EOF
    chmod +x .git/hooks/pre-commit
fi

echo "✅ Development environment setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Configure your environment files:"
echo "   - backend/.env"
echo "   - frontend/.env.local"
echo ""
echo "2. Start the development servers:"
echo "   Backend:  cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "   Frontend: cd frontend && npm run dev"
echo ""
echo "3. Visit http://localhost:3000 to see the application"
echo ""
echo "📖 For more information, see docs/CONTRIBUTING.md"