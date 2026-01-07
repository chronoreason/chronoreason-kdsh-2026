#!/bin/bash

# ChronoReason Pipeline Runner
# Executes the main narrative consistency analysis pipeline

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${PROJECT_DIR}/.venv"
PYTHON="${VENV_DIR}/bin/python"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== ChronoReason Pipeline Runner ===${NC}"
echo "Project directory: $PROJECT_DIR"
echo ""

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${RED}❌ Virtual environment not found at $VENV_DIR${NC}"
    echo "Run './setup.sh' first to initialize the environment"
    exit 1
fi

# Check if API key is set
if [ -z "$OPENAI_API_KEY" ] && [ ! -f "$PROJECT_DIR/.env" ]; then
    echo -e "${YELLOW}⚠️  Warning: OPENAI_API_KEY not set and .env file not found${NC}"
    echo "Pipeline will use fallback labels for claim validation"
    echo "To use actual OpenAI API, set OPENAI_API_KEY or create .env file"
    echo ""
fi

# Run the main pipeline
echo -e "${BLUE}Running narrative consistency analysis...${NC}"
echo ""

cd "$PROJECT_DIR"
$PYTHON main.py

echo ""
echo -e "${GREEN}✓ Pipeline execution completed${NC}"
