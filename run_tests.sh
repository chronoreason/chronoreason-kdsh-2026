#!/bin/bash

# ChronoReason Test Suite Runner
# Executes all unit and integration tests

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${PROJECT_DIR}/.venv"
PYTHON="${VENV_DIR}/bin/python"
PYTEST="${VENV_DIR}/bin/pytest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== ChronoReason Test Suite ===${NC}"
echo "Project directory: $PROJECT_DIR"
echo ""

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${RED}❌ Virtual environment not found at $VENV_DIR${NC}"
    echo "Run './setup.sh' first to initialize the environment"
    exit 1
fi

# Check if pytest is installed
if [ ! -f "$PYTEST" ]; then
    echo -e "${YELLOW}⚠️  pytest not found. Installing test dependencies...${NC}"
    $PYTHON -m pip install pytest pytest-cov > /dev/null 2>&1
fi

cd "$PROJECT_DIR"

# Run tests with coverage
echo -e "${BLUE}Running tests with coverage report...${NC}"
echo ""

if [ "$1" == "-v" ] || [ "$1" == "--verbose" ]; then
    $PYTEST tests/ -v --tb=short
elif [ "$1" == "-cov" ] || [ "$1" == "--coverage" ]; then
    $PYTEST tests/ -v --cov=src --cov-report=html --cov-report=term-missing
    echo ""
    echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}"
else
    $PYTEST tests/ -v --tb=short
fi

echo ""
echo -e "${GREEN}✓ All tests completed${NC}"
