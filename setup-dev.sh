#!/bin/bash

# Gotham Chess Engine - Development Setup Script

echo "🔥 Setting up Gotham Chess Engine Web Platform..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Python is installed
if ! command -v python &> /dev/null; then
    print_error "Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

print_status "Python and Node.js found!"

# Setup API dependencies
echo "📦 Installing API dependencies..."
cd web/api
if pip install -r requirements.txt; then
    print_status "API dependencies installed"
else
    print_error "Failed to install API dependencies"
    exit 1
fi

# Setup frontend dependencies
echo "📦 Installing frontend dependencies..."
cd ../frontend
if npm install; then
    print_status "Frontend dependencies installed"
else
    print_error "Failed to install frontend dependencies"
    exit 1
fi

cd ../..

print_status "Setup complete!"

echo ""
echo "🚀 To start development:"
echo ""
echo "1. Start the API server:"
echo "   cd web/api && python main.py"
echo ""
echo "2. In another terminal, start the frontend:"
echo "   cd web/frontend && npm start"
echo ""
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "🔥 Happy coding!"