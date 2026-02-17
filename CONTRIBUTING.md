# Contributing to Quick Shortcut AI LLM Assistant

Thank you for your interest in contributing! This document outlines the standards and workflows for this project to ensure a clean, fluid, and high-quality codebase.

---

## 📚 Documentation Workflow

Our documentation follows a **7-step workflow** that mirrors the development process:

```
01_input/        ← Specs, requirements, client issues
     ↓
02_planning/     ← Plans, scope, task lists (TODO.md)
     ↓
03_implementation/ ← Technical decisions, architecture
     ↓
04_testing/      ← Tests, UAT results, bug inventory
     ↓
05_review/       ← Feedback, validation, decisions
     ↓
06_release/      ← Updated specs, release notes
     ↓
07_archive/      ← Old versions, obsolete docs
```

### Directory Structure

```
docs/
├── 01_input/        - Cahier des charges, SPEC.md, PROJECT_DEFINITION.md
├── 02_planning/     - Phase plans, TODO.md (source of truth for tasks)
├── 03_implementation/ - Technical decisions, architecture notes
├── 04_testing/      - Test plans, guides, results
├── 05_review/       - Review feedback, issues to fix, validation
├── 06_release/      - Updated specs after validation, release notes
└── 07_archive/      - Historical versions, obsolete documents
```

---

## 🔄 Development Workflow

We follow a strict **Task → Plan → Implementation → Testing → Review → Release** cycle for all significant changes.

### 1. Task Definition (Planning Phase)

- **Read**: docs/01_input/ (specs, requirements)
- **Plan**: Define what you'll do in docs/02_planning/
- **Create**: Task in TODO.md with clear scope
- **Checklist**: Break down work into atomic steps

### 2. Implementation

- **Read**: docs/02_planning/TODO.md (your exact task)
- **Read**: docs/03_implementation/TECHNICAL_DECISIONS.md (context)
- **Code**: Follow PEP 8 standards, use `black` and `ruff`
- **Document**: Add docstrings (Google style)
- **Separation of Concerns**:
  - `src/core`: Business logic, interfaces, data models
  - `src/ui`: PySide6 widgets and windows
  - `src/services`: Background agents, OS integration
  - `src/utils`: Helper functions

### 3. Testing

- **Unit Tests**: Write tests in `tests/` for every new component
- **Run Tests**: `pytest tests/ -v`
- **Coverage**: Ensure > 85% coverage: `pytest --cov=src tests/`
- **Document**: Update docs/04_testing/TEST_PLAN.md with results

### 4. Review & Validation

- **Create PR**: Include clear description
- **Run checks**: All tests must pass
- **Address feedback**: Update docs/05_review/REVIEW_FEEDBACK.md
- **Decision**: Approve or request changes

### 5. Release & Documentation Update

- **Update Specs**: docs/06_release/UPDATED_SPEC.md (mark features as deployed)
- **Update Planning**: docs/02_planning/TODO.md (mark task as DONE)
- **Archive Review**: Move docs/05_review/* to docs/07_archive/
- **Commit**: Include migration of docs to archive/

---

## ✅ Pre-Action Checklists

### ✅ Before Starting New Phase/Task

**Checklist**:
- [ ] Read docs/01_input/CAHIER_DES_CHARGES.md
- [ ] Read docs/01_input/SPEC.md
- [ ] Read docs/01_input/PROJECT_DEFINITION.md
- [ ] Understand client issues/feedback
- [ ] Review corresponding phase plan in docs/02_planning/

**Why**: Ensures alignment with requirements before coding

---

### ✅ Before Implementing

**Checklist**:
- [ ] Task clearly defined in docs/02_planning/TODO.md
- [ ] Read docs/03_implementation/TECHNICAL_DECISIONS.md
- [ ] Understand architecture from docs/03_implementation/
- [ ] Create feature branch with clear name
- [ ] Have test strategy in mind

**Why**: Prevents rework and keeps code aligned with decisions

---

### ✅ Before Testing

**Checklist**:
- [ ] Read docs/04_testing/TEST_PLAN.md
- [ ] Code changes complete and committed
- [ ] All new code has corresponding tests
- [ ] Run: `pytest tests/ -v --cov=src`
- [ ] Coverage > 85%?

**Why**: Ensures quality before review

---

### ✅ Before Code Review / PR

**Checklist**:
- [ ] Task from docs/02_planning/TODO.md is 100% complete
- [ ] All tests passing (365+ tests)
- [ ] Code follows PEP 8 (black formatted, ruff clean)
- [ ] PR description references docs/02_planning/ task
- [ ] docs/05_review/REVIEW_DECISION.md has acceptance criteria

**Why**: Saves time for reviewer, clear acceptance criteria

---

### ✅ After Review Approval

**Checklist**:
- [ ] All feedback addressed (docs/05_review/REVIEW_FEEDBACK.md)
- [ ] Update docs/06_release/UPDATED_SPEC.md (feature marked as deployed)
- [ ] Update docs/02_planning/TODO.md (task marked as [x] DONE)
- [ ] Archive docs/05_review/* → docs/07_archive/
- [ ] Merge with clean commit message

**Commit Message Format**:
```
Feature: Brief description

- What was implemented
- Why (reference to docs/02_planning/ or docs/05_review/)
- Any docs updates made

See: docs/02_planning/TODO.md Task X
See: docs/05_review/REVIEW_DECISION.md
```

---

### ✅ Before Starting Next Phase

**Checklist**:
- [ ] All Phase N issues resolved and archived
- [ ] docs/01_input/SPEC.md updated with deployed features
- [ ] Phase review completed (docs/02_planning/PHASE_N_REVIEW.md)
- [ ] New phase plan created (docs/02_planning/PHASE_N+1_PLAN.md)
- [ ] TODO.md reset for new phase

**Why**: Clean transition, proper closure of previous phase

---

## 📋 Key Documents Reference

| Document | Location | Purpose | Updated When |
|----------|----------|---------|--------------|
| **CAHIER_DES_CHARGES.md** | docs/01_input/ | Original requirements | Phase start |
| **SPEC.md** | docs/01_input/ | Technical specification | After phase release |
| **PROJECT_DEFINITION.md** | docs/01_input/ | Phase definitions | Rarely |
| **TODO.md** | docs/02_planning/ | Source of truth for tasks | Every session |
| **PHASE_X_PLAN.md** | docs/02_planning/ | Phase implementation plan | Phase start |
| **TECHNICAL_DECISIONS.md** | docs/03_implementation/ | Architecture decisions | During implementation |
| **TEST_PLAN.md** | docs/04_testing/ | What to test and how | Before testing |
| **PHASE3_ISSUES_INVENTORY.md** | docs/05_review/ | Bugs found and status | During UAT/review |
| **REVIEW_FEEDBACK.md** | docs/05_review/ | Review comments | During review |
| **UPDATED_SPEC.md** | docs/06_release/ | Specs after deployment | After approval |

---

## 🔗 Documentation Synchronization Rules

**Key Principle**: TODO.md is the single source of truth for phase/task status.

When updating status:

| Change | Update These (Same Commit) |
|--------|---------------------------|
| Task completed | TODO.md → [x] DONE |
| Phase complete | docs/02_planning/PHASE_X_PLAN.md + docs/01_input/SPEC.md |
| Bug found | docs/05_review/PHASE3_ISSUES_INVENTORY.md + docs/05_review/REVIEW_FEEDBACK.md |
| Bug fixed | docs/05_review/PHASE3_ISSUES_INVENTORY.md + TODO.md (if task) |
| Feature deployed | docs/06_release/UPDATED_SPEC.md + docs/01_input/SPEC.md |

**Rule**: Never scatter documentation updates across multiple commits. Keep them together to maintain clarity.

---

## 🛠️ Code Standards

- **Formatter**: `black` (auto-formatted)
- **Linter**: `ruff`
- **Type Hints**: Use for function arguments and return values
- **Docstrings**: Google style
- **Testing**: pytest with > 85% coverage

---

## Git Hooks (Optional Automation)

We provide optional git hooks to remind you of documentation checklists at key moments:

### Install hooks (optional):
```bash
# Copy hooks to .git/hooks/
cp .githooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit
```

### Available hooks:
- **pre-commit**: Reminds to update docs/02_planning/TODO.md if changing phase
- **prepare-commit-msg**: Suggests referencing docs/ in commit messages

---

## Asking for Help

- **Testing Issues**: See docs/04_testing/VSCODE_TESTING_GUIDE.md
- **Architecture Questions**: Read docs/03_implementation/TECHNICAL_DECISIONS.md
- **Planning Questions**: Refer to docs/02_planning/TODO.md and phase plans
- **Past Decisions**: Check docs/07_archive/ for historical context

---

## Summary

1. ✅ **Read docs/01_input/** before starting
2. ✅ **Plan in docs/02_planning/TODO.md**
3. ✅ **Implement** with tests
4. ✅ **Test** thoroughly
5. ✅ **Review** with clear criteria
6. ✅ **Release** with updated docs
7. ✅ **Archive** old versions

**Follow the workflow. Update docs at the right steps. Keep checklists in mind.**

---

**Last Updated**: 2026-02-17
**Workflow Version**: 1.0 (with 7-step documentation process)
