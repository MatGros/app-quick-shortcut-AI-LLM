---
name: test
description: Run all tests with coverage report and validate documentation
---

# Test Skill

Run comprehensive test suite including unit tests, integration tests, and documentation validation.

## What This Does

1. **Run pytest** - All tests in tests/ with coverage reporting
2. **Check coverage** - Ensure > 80% code coverage
3. **Validate documentation** - Run docs/verify_docs.py
4. **Show summary** - Display pass/fail results

## Steps

```bash
# 1. Run all tests with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# 2. Validate documentation structure
python docs/verify_docs.py

# 3. If all pass, you're good to commit
# If failures, show them and suggest fixes
```

## Expected Output

```
===== test session starts =====
collected 365 items
tests/test_core/... PASSED
tests/test_ui/... PASSED
tests/test_services/... PASSED
tests/test_docs/... PASSED
===== 365 passed in X.XXs =====

✓ Documentation Summary:
  Total MD files: 45
```

## When to Use

- Before committing code: `/test`
- When debugging test failures
- To check code coverage
- Before submitting pull request

## Failure Handling

If tests fail:
1. Show the failed test output
2. Suggest what might be wrong
3. Offer to fix it (if simple)
4. Ask for more context (if complex)

## Coverage Requirements

- **Target:** > 80% for new code
- **Current:** 89% overall
- If coverage drops, explain why and suggest fixes
