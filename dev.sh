#!/bin/bash

# ChronoReason Development Helper Scripts
# Quick commands for common tasks

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${PROJECT_DIR}/.venv"
PYTHON="${VENV_DIR}/bin/python"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Ensure venv is activated
if [ ! -f "$PYTHON" ]; then
    echo "❌ Virtual environment not found. Run './setup.sh' first"
    exit 1
fi

show_help() {
    cat << EOF
${BLUE}ChronoReason Development Commands${NC}

Usage: ./dev.sh <command> [args]

Commands:
  ${GREEN}lint${NC}              Check code with Pylance (syntax validation)
  ${GREEN}format${NC}            Format Python code (show diffs)
  ${GREEN}imports${NC}           Analyze and fix imports
  ${GREEN}validate${NC}          Quick validation of all modules
  ${GREEN}repl${NC}              Start Python REPL with project in path
  ${GREEN}shell${NC}             Activate venv shell (bash)
  ${GREEN}clean${NC}             Remove cache and build artifacts
  ${GREEN}help${NC}              Show this help message

Examples:
  ./dev.sh lint
  ./dev.sh validate
  ./dev.sh shell
EOF
}

case "$1" in
    lint)
        echo "${BLUE}Checking code syntax...${NC}"
        $PYTHON -m py_compile src/**/*.py
        echo "${GREEN}✓ All files have valid syntax${NC}"
        ;;
    format)
        echo "${BLUE}Showing code formatting diffs...${NC}"
        echo "(No formatter installed; use 'pip install black' for auto-formatting)"
        ;;
    imports)
        echo "${BLUE}Analyzing imports...${NC}"
        $PYTHON << 'PYEOF'
import sys
sys.path.append('src')
try:
    from ingestion.chunker import chunk_text
    from reasoning.claim_extractor import extract_claims
    from reasoning.claim_validator import validate_claim
    from reasoning.contradiction_score import contradiction_score
    from reasoning.decision_engine import final_decision
    from reasoning.timeline_builder import build_timeline
    from retrieval.pathway_store import PathwayStore
    from visualization.timeline_graph import draw_timeline
    print('\033[0;32m✓ All imports successful\033[0m')
except ImportError as e:
    print(f'\033[0;31m✗ Import error: {e}\033[0m')
    sys.exit(1)
PYEOF
        ;;
    validate)
        echo "${BLUE}Running validation tests...${NC}"
        "$PROJECT_DIR/run_tests.sh" -v
        ;;
    repl)
        echo "${BLUE}Starting Python REPL...${NC}"
        echo "Path includes: src/"
        cd "$PROJECT_DIR"
        $PYTHON -i << 'PYEOF'
import sys
sys.path.insert(0, 'src')
print("\nChronoReason modules loaded. Try:")
print("  from reasoning import *")
print("  from ingestion import *")
print()
PYEOF
        ;;
    shell)
        echo "${BLUE}Activating virtual environment shell...${NC}"
        exec "$VENV_DIR/bin/bash" --rcfile <(cat ~/.bashrc && echo "source $VENV_DIR/bin/activate")
        ;;
    clean)
        echo "${BLUE}Cleaning cache and artifacts...${NC}"
        find "$PROJECT_DIR" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
        find "$PROJECT_DIR" -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
        find "$PROJECT_DIR" -type d -name .coverage -exec rm -rf {} + 2>/dev/null || true
        find "$PROJECT_DIR" -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
        echo "${GREEN}✓ Cache cleaned${NC}"
        ;;
    help|-h|--help)
        show_help
        ;;
    "")
        show_help
        ;;
    *)
        echo "${YELLOW}Unknown command: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
