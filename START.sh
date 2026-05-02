#!/bin/bash
# Quick Start Script for FinAgent-Rec
# This script starts both the backend API and frontend in one go

echo "🚀 Starting FinAgent-Rec System..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   FinAgent-Rec: Multi-Agent Financial Recommendations${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""

# Check if Python exists
if ! command -v python &> /dev/null; then
    echo -e "${YELLOW}❌ Python not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Check if Node exists
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}❌ Node.js not found. Please install Node.js 14+${NC}"
    exit 1
fi

# Check if npm exists
if ! command -v npm &> /dev/null; then
    echo -e "${YELLOW}❌ npm not found. Please install npm${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python found: $(python --version)"
echo -e "${GREEN}✓${NC} Node.js found: $(node --version)"
echo -e "${GREEN}✓${NC} npm found: $(npm --version)"
echo ""

# Setup Python environment
echo -e "${BLUE}Setting up Python environment...${NC}"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo -e "${GREEN}✓${NC} Virtual environment activated"
echo ""

# Install Python dependencies
echo -e "${BLUE}Installing Python dependencies...${NC}"
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✓${NC} Python dependencies installed"
echo ""

# Setup Node dependencies
echo -e "${BLUE}Setting up Frontend...${NC}"
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Installing npm packages..."
    npm install > /dev/null 2>&1
fi
echo -e "${GREEN}✓${NC} Frontend ready"
cd ..
echo ""

# Display instructions
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}System Ready!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""
echo "To start the system, run in two separate terminals:"
echo ""
echo -e "${YELLOW}Terminal 1 (Backend API):${NC}"
echo -e "  python api.py"
echo -e "  → Opens on http://localhost:5000"
echo ""
echo -e "${YELLOW}Terminal 2 (Frontend):${NC}"
echo -e "  cd frontend"
echo -e "  npm start"
echo -e "  → Opens on http://localhost:3000"
echo ""
echo -e "${GREEN}Then open your browser to: http://localhost:3000${NC}"
echo ""
echo "Documentation:"
echo "  • Quick Start: QUICK_REFERENCE.md"
echo "  • Full Setup: FRONTEND_SETUP.md"
echo "  • Deployment: FRONTEND_DEPLOYMENT.md"
echo "  • All Docs: DOCUMENTATION_INDEX.md"
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
