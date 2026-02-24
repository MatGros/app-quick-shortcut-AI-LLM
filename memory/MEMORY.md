# Quick Shortcut AI LLM Assistant - Project Memory

## 📌 LATEST: Audit Technologique Complet (24 Février 2026)

**STATUS**: Root causes identified, Path 1 Fix recommended (1 week, 90% success)

### Audit Findings
- **Root Cause**: pynput + PySide6 incompatible (6+ year unfixed GitHub issues)
- **Solution**: keyboard library + QThread pattern
- **Timeline**: 3-5 working days (Mon-Fri)
- **Success Rate**: 90%
- **Fallback**: Win32 API (2-3 days) or Electron/Tauri rewrite (2-4 weeks)

### 5 Critical Bugs (ALL Fixable)
1. Settings closes app → QDialog issue (2-4h)
2. Icon stuck red → health check not updating (1-2h)
3. Chat freezes → main thread blocking (4-6h with QThread)
4. Menu non-clickable → signal/event issues (2-3h)
5. Windows menu visible → pynput limitation (accepted)

### Key Research
- 20+ web searches, 15+ GitHub issues analyzed
- keyboard library = proven alternative to pynput
- QThread worker pattern = Qt standard solution
- Alternatives evaluated: Electron (2-3w), Tauri (3-4w), C# WinUI (2-3w)

### Audit Documents (In repo root)
- `AUDIT_TECHNOLOGIQUE_COMPLET.md` (20 pages, start here)
- `PLAN_ACTION_SEMAINE.md` (day-by-day tasks Mon-Fri)
- `PRACTICAL_SOLUTIONS_CODE_SNIPPETS.md` (copy-paste ready code)
- `RESEARCH_EXECUTIVE_SUMMARY.md` (5-min overview)
- `RESEARCH_REPORT_ARCHITECTURE_ALTERNATIVES.md` (30 pages detailed)
- `AUDIT_FINAL_RESUME.txt` (this page summary)

---

## Documentation Structure (7-Step Workflow) - FINAL

**CRITICAL RULE**: Documentation is organized into ONLY 7 numbered folders mirroring the development workflow. NO OTHER FOLDERS ALLOWED in docs/.

**What should NOT exist:**
- ❌ `docs/logs/` - Obsolete status file (deleted)
- ❌ `docs/technical/` - Random folder (deleted)
- ❌ `docs/archive/` (without number) - Should be `docs/07_archive/`

**What MUST exist:**

```
docs/01_input/         ← Requirements, SPEC.md, PROJECT_DEFINITION.md
docs/02_planning/      ← TODO.md (SOURCE OF TRUTH), PHASE_X_PLAN.md
docs/03_implementation/ ← TECHNICAL_DECISIONS.md, architecture docs
docs/04_testing/       ← TEST_PLAN.md, VSCODE_TESTING_GUIDE.md, UAT guides
docs/05_review/        ← PHASE3_ISSUES_INVENTORY.md, REVIEW_FEEDBACK.md
docs/06_release/       ← UPDATED_SPEC.md, RELEASE_NOTES.md
docs/07_archive/       ← Obsolete/historical docs
```

**Key Rule**: Folder numbering (01_, 02_, etc.) is essential for workflow clarity. **NOT optional.**

## Single Source of Truth

- **Task Status**: `docs/02_planning/TODO.md` - Update EVERY session
- **Current Issues**: `docs/testing/PHASE3_ISSUES_INVENTORY.md` (Phase 3)
- **Deployed Features**: `docs/technical/SPEC.md`
- **Technical Decisions**: `docs/technical/TECHNICAL_DECISIONS.md` (if exists)

## Documentation Synchronization Rules

When status changes, update in SAME COMMIT:
- Task completed → TODO.md marked [x] DONE
- Phase complete → PHASE_X_PLAN.md + SPEC.md
- Bug found → PHASE3_ISSUES_INVENTORY.md + REVIEW_FEEDBACK.md
- Feature deployed → UPDATED_SPEC.md + SPEC.md (main)

**Rule**: Never scatter doc updates across multiple commits.

## Key Documents

Each docs/ folder has a self-documenting README.md explaining its purpose and workflow transitions.

## File Placement Rules (Critical!)

**Planning folder (02_planning/)**: ONLY task/phase plans
- ✅ TODO.md (task status)
- ✅ PHASE_X_PLAN.md (phase plans)
- ✅ IMPLEMENTATION_PLAN.md (overall architecture)
- ❌ PHASE_X_REVIEW.md (belongs in 05_review - these are RESULTS)

**Testing folder (04_testing/)**: ONLY how to test
- ✅ TEST_PLAN.md
- ✅ QUICK_START_TESTS.md
- ✅ VSCODE_TESTING_GUIDE.md
- ✅ UAT_DETAILED_GUIDE.md
- ❌ PHASE3_ISSUES_INVENTORY.md (belongs in testing - these are bugs FOUND)

**Review folder (05_review/)**: ONLY review/validation results
- ✅ PHASE_X_REVIEW.md (phase reviews)
- ✅ PHASE3_ISSUES_INVENTORY.md (bugs found during testing)
- ✅ REVIEW_FEEDBACK.md (reviewer comments)
- ✅ REVIEW_DECISION.md (approval/rejection)

---

## Current Project Status (Phase 3) - AUDIT COMPLETE

- **Code**: 365 tests passing, 89% coverage - COMPLETE
- **Blockers**: 5 critical UI bugs blocking UAT
- **Root Cause**: pynput + PySide6 incompatible (unfixed since 2020)
- **Solution**: keyboard library + QThread pattern
- **Timeline**: Path 1 = 1 week (Mon-Fri), 90% success
- **Audit Documents**: See above

## Git Hooks

Optional `.githooks/pre-commit` reminds to update `docs/02_planning/TODO.md` when code changes.

Install: `cp .githooks/pre-commit .git/hooks/ && chmod +x .git/hooks/pre-commit`

## Important Pattern: Documentation as Workflow Checkpoint

The 7-folder structure isn't just organization—it's a workflow checkpoint system. Each phase should:
1. Read inputs (01_input/)
2. Plan scope (02_planning/)
3. Document decisions (03_implementation/)
4. Test thoroughly (04_testing/)
5. Validate & review (05_review/)
6. Update specs & release (06_release/)
7. Archive old versions (07_archive/)

Never skip phases, never miss documentation updates.

## Naming Conventions (STRICT - ENFORCED)

**Folders**: Only `0X_lowercase/` format (01_input, 02_planning, ... 07_archive)

**Files by Folder**:
- `01_input/`: CAHIER_DES_CHARGES.md, SPEC.md, PROJECT_DEFINITION.md
- `02_planning/`: TODO.md (updated EVERY session!), PHASE_X_PLAN.md, IMPLEMENTATION_PLAN.md
- `03_implementation/`: TECHNICAL_DECISIONS.md
- `04_testing/`: TEST guides (QUICK_START_TESTS.md, VSCODE_TESTING_GUIDE.md, etc.)
- `05_review/`: PHASE_X_REVIEW.md, PHASE3_ISSUES_INVENTORY.md, REVIEW_*.md
- `06_release/`: UPDATED_SPEC.md, RELEASE_NOTES.md (after approval)
- `07_archive/`: README.md only (CLEAN - no .archived files)

**Naming Rules**:
- ✅ UPPERCASE.md for main docs (PHASE_1_REVIEW.md, not phase_1_review.md)
- ✅ Use underscore separator (PHASE_1, not PHASE-1 or Phase1)
- ✅ README.md (lowercase only) in each folder
- ❌ NO camelCase (TestPlan not valid)
- ❌ NO hyphens in file names
- ❌ NO numbers without underscore (PHASE3_ISSUES not PHASE3ISSUES)
- ❌ NO folders like docs/logs/, docs/technical/, etc.

---

## Tech Stack (Stable, Up-to-date)

- **Language**: Python 3.10+
- **GUI**: PySide6-Essentials 6.5.0+ (Qt6)
- **Global Hotkeys**: keyboard library (0.13.5+) - **replacing pynput** ⭐
- **HTTP**: requests 2.31.0+
- **LLM**: Ollama, OpenAI, Anthropic, OpenRouter (abstracted)
- **Build**: Nuitka 1.9+ (standalone exe)

## Tech Stack Issues & Resolutions

| Issue | Previous | Current | Fix |
|-------|----------|---------|-----|
| Global hotkeys | pynput (broken) | keyboard (active) | Replace lib |
| UI Threading | QApplication.processEvents() | QThread worker | Proper pattern |
| Chat freezing | Main thread blocking | Worker thread + signals | Implement |
| Settings crash | QWidget hierarchy | QDialog proper | Review closeEvent |
| Health check | Manual check | Automatic on change | Signal connection |

---

## Development Status

- ✅ Architecture: Mature
- ✅ Core Features: All 20 features coded
- ✅ Testing: 365 tests (89% coverage)
- ⏳ UI Polish: Blocked by 5 bugs (fixable, 1 week)
- ⏳ UAT: Ready after bug fixes
- ⏳ Production: Blocked by Path 1 completion

## Quick Links to Audit

1. **Start Here** (5 min): RESEARCH_EXECUTIVE_SUMMARY.md
2. **Decision Tree** (2 min): AUDIT_FINAL_RESUME.txt (lines 157-191)
3. **Day-by-Day Plan** (30 min): PLAN_ACTION_SEMAINE.md
4. **Code Ready** (copy-paste): PRACTICAL_SOLUTIONS_CODE_SNIPPETS.md
5. **Deep Analysis** (1+ hour): RESEARCH_REPORT_ARCHITECTURE_ALTERNATIVES.md
6. **Full Audit** (2 hours): AUDIT_TECHNOLOGIQUE_COMPLET.md
