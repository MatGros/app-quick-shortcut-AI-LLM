# 🧪 Step 4: Testing - Quality Assurance

This folder contains **test plans, guides, and results**.

## Files

- **TEST_PLAN.md** - What tests exist and what they cover
- **QUICK_START_TESTS.md** - How to run tests quickly
- **VSCODE_TESTING_GUIDE.md** - Debugging tests in VS Code
- **TEST_QUALITY_REVIEW.md** - Test coverage analysis
- **UAT_DETAILED_GUIDE.md** - User Acceptance Testing guide
- **PHASE3_ISSUES_INVENTORY.md** - Bugs found (review step, not this folder)

## When to Use

- **Before testing**: Read TEST_PLAN.md
- **Running tests**: Use QUICK_START_TESTS.md
- **Debugging test failures**: Use VSCODE_TESTING_GUIDE.md
- **UAT phase**: Follow UAT_DETAILED_GUIDE.md
- **After finding bugs**: Document in docs/05_review/PHASE3_ISSUES_INVENTORY.md

## Checklist Before Testing

- [ ] Read TEST_PLAN.md
- [ ] Run: `pytest tests/ -v`
- [ ] Verify coverage > 85%
- [ ] Document any test results

---

**See also**:
- docs/03_implementation/ (previous step - code to test)
- docs/05_review/ (next step - validate and fix)
