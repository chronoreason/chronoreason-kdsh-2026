#!/bin/bash

# ChronoReason All-in-One Runner
# Setup → Tests → Pipeline in one command

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$PROJECT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

show_usage() {
    echo -e "${BLUE}Usage:${NC}"
    echo "  $0                    Run setup → tests → pipeline (full workflow)"
    echo "  $0 setup              Run setup only"
    echo "  $0 test               Run tests only"
    echo "  $0 pipeline           Run pipeline only"
    echo "  $0 test -v            Run tests in verbose mode"
    echo "  $0 test -cov          Run tests with coverage report"
    echo ""
}

# Make scripts executable
chmod +x "$SCRIPTS_DIR/setup.sh" 2>/dev/null || true
chmod +x "$SCRIPTS_DIR/run_tests.sh" 2>/dev/null || true
chmod +x "$SCRIPTS_DIR/run_pipeline.sh" 2>/dev/null || true

# Parse command
COMMAND="${1:-full}"
ARGS="${@:2}"

case "$COMMAND" in
    setup)
        echo -e "${CYAN}▶ Running setup...${NC}"
        "$SCRIPTS_DIR/setup.sh"
        ;;
    test)
        echo -e "${CYAN}▶ Running tests...${NC}"
        "$SCRIPTS_DIR/run_tests.sh" $ARGS
        ;;
    pipeline)
        echo -e "${CYAN}▶ Running pipeline...${NC}"
        "$SCRIPTS_DIR/run_pipeline.sh"
        ;;
    full)
        echo -e "${BLUE}=== ChronoReason Full Workflow ===${NC}"
        echo ""
        
        # Step 1: Setup
        echo -e "${CYAN}Step 1/3: Setup Environment${NC}"
        "$SCRIPTS_DIR/setup.sh"
        echo ""
        
        # Step 2: Tests
        echo -e "${CYAN}Step 2/3: Run Tests${NC}"
        "$SCRIPTS_DIR/run_tests.sh"
        echo ""
        
        # Step 3: Pipeline
        echo -e "${CYAN}Step 3/3: Run Pipeline${NC}"
        "$SCRIPTS_DIR/run_pipeline.sh"
        echo ""
        
        echo -e "${GREEN}=== All Done! ===${NC}"
        ;;
    -h|--help|help)
        show_usage
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $COMMAND${NC}"
        echo ""
        show_usage
        exit 1
        ;;
esac
