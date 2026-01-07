#!/bin/bash

# ChronoReason Streamlit App Runner
# Launches the interactive web dashboard

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${PROJECT_DIR}/.venv"
PYTHON="${VENV_DIR}/bin/python"
STREAMLIT="${VENV_DIR}/bin/streamlit"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== ChronoReason Streamlit Dashboard ===${NC}"
echo "Project directory: $PROJECT_DIR"
echo ""

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${RED}❌ Virtual environment not found at $VENV_DIR${NC}"
    echo "Run './setup.sh' first to initialize the environment"
    exit 1
fi

# Check if streamlit is installed
if [ ! -f "$STREAMLIT" ]; then
    echo -e "${YELLOW}⚠️  streamlit not found. Installing...${NC}"
    $PYTHON -m pip install streamlit > /dev/null 2>&1
    echo -e "${GREEN}✓ streamlit installed${NC}"
fi

# Check if API key is set
if [ -z "$OPENAI_API_KEY" ] && [ ! -f "$PROJECT_DIR/.env" ]; then
    echo -e "${YELLOW}⚠️  Warning: OPENAI_API_KEY not set${NC}"
    echo "Set it before running, or the app will use fallback labels"
    echo ""
fi

# Launch Streamlit app
echo -e "${GREEN}Starting Streamlit dashboard...${NC}"
echo -e "${BLUE}Dashboard will open at: http://localhost:8501${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

cd "$PROJECT_DIR"
$STREAMLIT run app.py
