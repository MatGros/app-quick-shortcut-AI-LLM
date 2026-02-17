# GitHub Actions Workflows

This directory contains CI/CD automation workflows that validate code quality, run tests, and ensure documentation standards on every push and pull request.

---

## 📋 Workflows Overview

### 1. **tests.yml** - Tests & Coverage
**Triggers:** Push to main/develop, Pull requests

**What it does:**
- ✅ Runs pytest on multiple Python versions (3.10, 3.11, 3.12)
- ✅ Tests on multiple OS (ubuntu-latest, windows-latest)
- ✅ Generates coverage reports (target: 80%+)
- ✅ Uploads artifacts and coverage metrics
- ✅ Comments coverage on pull requests

**Matrix Strategy:**
- Python: 3.10, 3.11, 3.12
- OS: Ubuntu, Windows (ensures Windows compatibility)

**Artifacts Generated:**
- `test-results-*.xml` (JUnit format)
- `htmlcov/` (HTML coverage report)

**Quality Gate:** All tests must pass, coverage must stay ≥ 80%

---

### 2. **lint.yml** - Code Quality
**Triggers:** Push to main/develop, Pull requests

**What it does:**
- ✅ Lint code with ruff (catches style issues)
- ✅ Format check with black (ensures consistent style)
- ✅ Type checking with mypy (optional, non-blocking)

**Tools Used:**
- **Ruff** - Fast Python linter (catches bugs, style issues)
- **Black** - Code formatter (ensures consistent style)
- **Mypy** - Type checker (non-blocking)

**Quality Gate:** Linting and formatting checks must pass

---

### 3. **docs.yml** - Documentation Validation
**Triggers:** Push to main/develop, Pull requests (when docs/ or .md files change)

**What it does:**
- ✅ Runs documentation structure tests (27 pytest tests)
- ✅ Validates documentation with verify_docs.py
- ✅ Checks for broken references (old-style paths)
- ✅ Ensures 7-step workflow structure intact

**Tests Run:**
- TestDocumentationStructure (3 tests)
- TestFilePlacement (6 tests)
- TestFileNameConventions (4 tests)
- TestPlacementRules (4 tests)
- TestReferenceIntegrity (2 tests)
- TestWorkflowCoherence (1 test)
- TestContentQuality (2 tests)
- TestRootLevelFiles (3 tests)
- TestOptionalFiles (1 test)
- TestDocumentationSummary (1 test)

**Quality Gate:** All documentation tests must pass

---

## 🚀 How They Work

### On Push
```
Push to main/develop
        ↓
All 3 workflows run in parallel
├── tests.yml (5-10 minutes)
├── lint.yml (2-3 minutes)
└── docs.yml (1-2 minutes)
        ↓
Results appear in GitHub Actions tab
```

### On Pull Request
```
Create/update PR
        ↓
All 3 workflows run
        ↓
Status checks required to merge
├── Tests must pass ✅
├── Linting must pass ✅
└── Docs must pass ✅
```

---

## ✅ Quality Gates

### Tests (tests.yml)
- ✅ All tests must pass on all Python versions
- ✅ Coverage must stay ≥ 80%
- ✅ No regression in coverage

### Code Quality (lint.yml)
- ✅ Ruff lint must pass (no errors)
- ✅ Black format must match
- ✅ Type hints recommended (mypy non-blocking)

### Documentation (docs.yml)
- ✅ 27 documentation tests must pass
- ✅ No old-style paths (docs/technical/, docs/planning/)
- ✅ Correct folder structure (01_input...07_archive)

---

## 📊 Workflow Status

Check status at: **https://github.com/YOUR_USERNAME/app-quick-shortcut-AI-LLM/actions**

**Green ✅** = All checks passing → Can merge
**Red ❌** = Some checks failing → Fix before merge

---

## 🔧 Common Issues & Fixes

### Tests Failing?
```bash
# Run locally first:
pytest tests/ -v --cov=src

# Fix any failures, then push again
```

### Code Format Issues?
```bash
# Auto-fix with black:
black src/ tests/

# Check ruff issues:
ruff check src/ tests/
```

### Documentation Validation Failing?
```bash
# Validate locally:
python docs/verify_docs.py

# Or run pytest tests:
pytest tests/test_docs/ -v
```

---

## 📝 Local Testing Before Push

### Before committing, run locally:
```bash
# Run all quality checks
pytest tests/ -v --cov=src
python docs/verify_docs.py
ruff check src/ tests/
black --check src/ tests/
```

### Use Claude Code Skill (easier):
```
/test    # Runs all tests
/docs    # Validates documentation
/commit  # Creates conventional commit
```

---

## 🛠️ Modifying Workflows

If you need to update these workflows:

1. **For new test dependencies:** Update requirements.txt
2. **For new Python versions:** Update `matrix.python-version`
3. **For new OS testing:** Update `matrix.os`
4. **For new quality checks:** Add new job in appropriate workflow

**Example:** Add Python 3.13 testing
```yaml
matrix:
  python-version: ['3.10', '3.11', '3.12', '3.13']  # Added 3.13
```

---

## 📞 Troubleshooting

### "Action failed with: Resource not available"
- Check branch protection rules are set correctly
- Ensure GitHub Actions are enabled in repository settings

### "Workflow runs on ubuntu but fails on windows"
- Some tests may be platform-specific
- Check that PySide6 installation works on both
- Run tests locally on Windows

### "Coverage dropped below 80%"
- Add tests for new code
- Run: `pytest --cov=src --cov-report=term-missing`
- This shows which lines aren't covered

---

## 🎯 Workflow Best Practices

1. **Keep workflows fast** - Under 15 minutes total
2. **Use caching** - Cache pip dependencies
3. **Matrix testing** - Test on multiple Python versions
4. **Clear artifacts** - Store test results for debugging
5. **Fail fast** - Stop on first failure (fail-fast: false for flexibility)

---

## 📖 Learn More

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Black Documentation](https://black.readthedocs.io/)

---

**Last Updated:** 2026-02-17
**Status:** Ready for use
