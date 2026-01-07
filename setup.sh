#!/bin/bash

# ChronoReason Setup Script
# Initializes the development environment with venv and dependencies

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${PROJECT_DIR}/.venv"
PYTHON_VERSION="3.11"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== ChronoReason Setup ===${NC}"
echo "Project directory: $PROJECT_DIR"
echo ""

# Check Python version
PYTHON_CMD=$(command -v python$PYTHON_VERSION 2>/dev/null || command -v python3 2>/dev/null || echo "")

if [ -z "$PYTHON_CMD" ]; then
    echo -e "${RED}❌ Python $PYTHON_VERSION not found${NC}"
    echo "Please install Python $PYTHON_VERSION and try again"
    exit 1
fi

echo "Using Python: $PYTHON_CMD"
$PYTHON_CMD --version
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${BLUE}Creating virtual environment at $VENV_DIR...${NC}"
    $PYTHON_CMD -m venv "$VENV_DIR"
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}Virtual environment already exists${NC}"
fi

echo ""

# Activate venv
echo -e "${BLUE}Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo -e "${GREEN}✓ pip upgraded${NC}"

echo ""

# Install dependencies from requirements.txt
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    echo -e "${BLUE}Installing project dependencies from requirements.txt...${NC}"
    pip install -r "$PROJECT_DIR/requirements.txt" > /dev/null 2>&1
    echo -e "${GREEN}✓ Dependencies installed${NC}"
fi

# Install test dependencies
echo -e "${BLUE}Installing test dependencies...${NC}"
pip install pytest pytest-cov > /dev/null 2>&1
echo -e "${GREEN}✓ Test dependencies installed${NC}"

echo ""

# Create .env template if it doesn't exist
if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo -e "${BLUE}Creating .env template...${NC}"
    cat > "$PROJECT_DIR/.env" << 'EOF'
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-key-here

# Claim Validator Fallback
# Used when OpenAI API is unavailable (options: support, contradict, neutral)
CLAIM_VALIDATOR_FALLBACK_LABEL=neutral
EOF
    echo -e "${GREEN}✓ .env template created at $PROJECT_DIR/.env${NC}"
    echo -e "${YELLOW}⚠️  Please update OPENAI_API_KEY in .env file${NC}"
else
    echo -e "${YELLOW}.env file already exists${NC}"
fi

echo ""

# Summary
echo -e "${GREEN}=== Setup Complete ===${NC}"
echo ""
echo "Next steps:"
echo "1. Update .env with your OPENAI_API_KEY"
echo "2. Run tests:     ./run_tests.sh"
echo "3. Run pipeline:  ./run_pipeline.sh"
echo ""
echo "To activate the virtual environment manually:"
echo "  source $VENV_DIR/bin/activate"
