# ChronoReason: Narrative Consistency Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**ChronoReason** is an AI-powered tool for analyzing narrative consistency and detecting contradictions in extended text. It combines semantic search, natural language processing, and reasoning to validate claims against evidence sources.

## 🎯 Features

- **Semantic Search**: Uses embedding models to find relevant evidence from source texts
- **Claim Extraction**: Automatically extracts verifiable claims from narratives
- **AI Validation**: Validates claims using GPT models (with fallback support)
- **Contradiction Detection**: Identifies contradictions between backstories and source materials
- **Interactive Dashboard**: Streamlit web interface for easy analysis
- **Multiple Modes**: Quick analysis, detailed analysis, and custom input
- **Export Results**: Download results as CSV or TXT formats
- **Comprehensive Testing**: Full test suite with edge case coverage

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/chronoreason/chronoreason-kdsh-2026.git
cd chronoreason-kdsh-2026

# Run setup script (creates venv and installs dependencies)
./setup.sh
```

### Run the Dashboard

```bash
./run_streamlit.sh
```

The Streamlit dashboard will open at `http://localhost:8501`

### Run Tests

```bash
./run_tests.sh              # Run all tests
./run_tests.sh -v           # Verbose output
./run_tests.sh -cov         # With coverage report
```

### Run the CLI Pipeline

```bash
./run_pipeline.sh
```

## 📖 Usage

### Via Streamlit Dashboard

The interactive dashboard provides three analysis modes:

#### 1. **Quick Analysis**
- Select pre-loaded sample backstories
- Automatically loads source text
- One-click analysis with customizable parameters

#### 2. **Detailed Analysis**
- Paste custom backstory and evidence text
- See claim-by-claim breakdown with supporting evidence
- Detailed statistics and interpretation

#### 3. **Custom Input**
- Full control over both inputs
- Adjustable chunk size, overlap, and consistency threshold
- Ideal for testing and exploration

### Via Command Line

```bash
# Run the main pipeline
python3.11 main.py

# Run tests
pytest tests/ -v

# Check syntax
./dev.sh lint
```

## 🏗️ Project Structure

```
chronoreason-kdsh-2026/
├── src/
│   ├── ingestion/
│   │   └── chunker.py              # Text chunking with overlap
│   ├── reasoning/
│   │   ├── claim_extractor.py      # Extract claims from text
│   │   ├── claim_validator.py      # Validate claims using AI
│   │   ├── contradiction_score.py  # Calculate consistency metrics
│   │   ├── decision_engine.py      # Final decision logic
│   │   └── timeline_builder.py     # Build event timelines
│   ├── retrieval/
│   │   └── pathway_store.py        # Semantic search with embeddings
│   └── visualization/
│       └── timeline_graph.py       # Visualize timelines
├── data/
│   └── sample/                     # Sample datasets
├── tests/
│   └── test_*.py                   # Comprehensive test suite
├── app.py                          # Streamlit dashboard
├── main.py                         # CLI pipeline
├── run*.sh                         # Runner scripts
├── dev.sh                          # Developer utilities
└── README.md                       # This file
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI API Key (required for live API calls)
OPENAI_API_KEY=sk-your-key-here

# Fallback label when API is unavailable
# Options: support, contradict, neutral (default: neutral)
CLAIM_VALIDATOR_FALLBACK_LABEL=neutral
```

### Streamlit Settings

Adjust parameters in the dashboard sidebar:

- **Chunk Size**: Words per document chunk (default: 800)
- **Chunk Overlap**: Overlapping words between chunks (default: 100)
- **Consistency Threshold**: Cutoff score for inconsistency (default: 0.6)

## 🧪 Testing

The project includes comprehensive tests for all modules:

```bash
# Run all tests
./run_tests.sh

# Run with verbose output
./run_tests.sh -v

# Run with coverage report
./run_tests.sh -cov
```

Test coverage includes:
- Empty input handling
- Edge cases and boundary conditions
- Integration testing of the full pipeline
- Mock OpenAI API responses

## 📊 How It Works

### Pipeline Flow

```
1. Load Texts
   ↓
2. Chunk Source Text (with overlap)
   ↓
3. Build Semantic Index
   ↓
4. Extract Claims from Backstory
   ↓
5. For Each Claim:
   - Search for relevant evidence
   - Validate against evidence
   ↓
6. Calculate Contradiction Score
   ↓
7. Generate Final Decision
   - CONSISTENT: score < threshold
   - INCONSISTENT: score ≥ threshold
```

### Scoring System

- **Support** (no penalty): Evidence supports the claim
- **Neutral** (0.5 point): Evidence is neutral/unclear
- **Contradict** (1.0 point): Evidence contradicts the claim

**Final Score** = Total Points / Number of Claims (0-1 range)

**Interpretation**:
- `< 0.3`: Highly consistent ✅
- `0.3-0.6`: Mostly consistent ℹ️
- `0.6-threshold`: Moderately inconsistent ⚠️
- `>= threshold`: Highly inconsistent ❌

## 🛠️ Developer Tools

Quick commands for development:

```bash
./dev.sh lint           # Check code syntax
./dev.sh validate       # Run tests
./dev.sh imports        # Validate imports
./dev.sh clean          # Remove cache
./dev.sh shell          # Activate venv
./dev.sh repl           # Python REPL
```

## 📦 Dependencies

Key packages:
- `streamlit`: Web dashboard
- `sentence-transformers`: Semantic embeddings
- `openai`: GPT models for validation
- `langchain`: LLM orchestration
- `networkx`: Graph visualization
- `pytest`: Testing framework

Full dependency list in [requirements.txt](requirements.txt)

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Code Standards

- Python 3.11+ compatible
- PEP 8 compliant
- Comprehensive docstrings
- Full test coverage for new features

## 📋 Sample Datasets

Three narrative scenarios included:

- **backstory1.txt**: Cautious aristocrat (contradiction with actual events)
- **backstory2.txt**: Heroic aristocrat (alignment with actual events)
- **backstory3.txt**: Transformation narrative (evolution of character)
- **In_search_of_the_castaways.txt**: Full Jules Verne novel (evidence source)

Run quick analysis to see the tool in action!

## 🐛 Troubleshooting

### Virtual Environment Issues
```bash
# Recreate venv
rm -rf .venv
./setup.sh
```

### OpenAI API Errors
- Verify API key in `.env`
- Check account quota and billing
- App uses fallback labels if API unavailable

### Import Errors
```bash
./dev.sh imports          # Diagnose import issues
./dev.sh lint             # Check syntax
```

### Streamlit Won't Start
```bash
# Reinstall streamlit
pip install --upgrade streamlit

# Run with debug
streamlit run app.py --logger.level=debug
```

## 📚 Documentation

- [README.md](README.md) - Project overview (this file)
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - Community standards
- [LICENSE](LICENSE) - MIT License

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/chronoreason/chronoreason-kdsh-2026/issues)
- **Discussions**: [GitHub Discussions](https://github.com/chronoreason/chronoreason-kdsh-2026/discussions)
- **Documentation**: See `/docs` folder

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## ✨ Key Improvements Made

Recent updates include:
- ✅ Fixed OpenAI API compatibility (v1.0+)
- ✅ Added graceful fallback for rate limits
- ✅ Replaced Pathway with efficient numpy-based search
- ✅ Enhanced all modules with edge case handling
- ✅ Expanded sample backstories with rich narratives
- ✅ Comprehensive test suite with 90%+ coverage
- ✅ Professional Streamlit dashboard with multiple modes
- ✅ Full bash automation scripts
- ✅ Complete documentation

## 🎓 Academic References

This tool is inspired by work in:
- Natural Language Processing
- Semantic Search and Embeddings
- Narrative Analysis
- Automated Reasoning

---

**ChronoReason v1.0** | Made with ❤️ for narrative analysis
