# Contributing to ChronoReason

Thank you for your interest in contributing to ChronoReason This document provides guidelines and instructions for contributing to the project.

## 🤝 Code of Conduct

Please review our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing. We are committed to providing a welcoming and inclusive environment for all contributors.

## 📋 Getting Started

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   \`\`\`bash
   git clone https://github.com/your-username/chronoreason-kdsh-2026.git
   cd chronoreason-kdsh-2026
   \`\`\`

3. Add upstream remote:
   \`\`\`bash
   git remote add upstream https://github.com/chronoreason/chronoreason-kdsh-2026.git
   \`\`\`

### Set Up Development Environment

1. Create virtual environment:
   \`\`\`bash
   ./setup.sh
   \`\`\`

2. Install development dependencies:
   \`\`\`bash
   .venv/bin/pip install -r requirements.txt
   .venv/bin/pip install pytest pytest-cov black pylint
   \`\`\`

3. Verify setup:
   \`\`\`bash
   ./dev.sh lint
   ./run_tests.sh
   \`\`\`

## 🔄 Development Workflow

### 1. Create Feature Branch

\`\`\`bash
git checkout -b feature/your-feature-name
# or for bug fixes:
git checkout -b fix/issue-description
\`\`\`

Branch naming convention:
- \`feature/\` - New features
- \`fix/\` - Bug fixes
- \`docs/\` - Documentation updates
- \`refactor/\` - Code refactoring
- \`test/\` - Test improvements

### 2. Make Changes

Follow these guidelines:

**Code Style**
- Follow PEP 8
- Use meaningful variable names
- Keep functions focused and small
- Add docstrings to all functions

**Documentation**
- Update docstrings for modified functions
- Add comments for complex logic
- Update README if behavior changes
- Document new configuration options

**Tests**
- Write tests for new features
- Update tests for modified code
- Ensure all tests pass: \`./run_tests.sh\`
- Aim for >90% code coverage

### 3. Commit Changes

Write clear, descriptive commit messages:

\`\`\`bash
# Good commit messages
git commit -m "Add semantic search fallback for timeout errors"
git commit -m "Fix division by zero in contradiction_score"
git commit -m "Improve claim extraction with length filtering"

# Less helpful
git commit -m "Updates"
git commit -m "Fixed stuff"
\`\`\`

### 4. Run Quality Checks

Before pushing:

\`\`\`bash
./dev.sh lint
./run_tests.sh
./dev.sh imports
./dev.sh clean
\`\`\`

### 5. Push and Create Pull Request

\`\`\`bash
git push origin feature/your-feature-name
\`\`\`

## ✅ Checklist Before Submitting PR

- [ ] Code follows PEP 8 style guide
- [ ] All tests pass
- [ ] Code coverage maintained
- [ ] Docstrings added/updated
- [ ] Comments explain complex logic
- [ ] No hardcoded values
- [ ] Error handling is appropriate
- [ ] Edge cases are considered

## 🧪 Testing Guidelines

\`\`\`bash
./run_tests.sh              # All tests
./run_tests.sh -v           # Verbose
./run_tests.sh -cov         # Coverage report
\`\`\`

## 📚 Additional Resources

- [GitHub Guides](https://guides.github.com/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Pytest Documentation](https://docs.pytest.org/)

## ✨ Acknowledgments

Thank you for contributing to ChronoReason Your efforts help make this project better for everyone.

---

**Happy Contributing 🎉**
