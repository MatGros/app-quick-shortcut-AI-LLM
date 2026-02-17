# 📚 Documentation Project - Structure & Maintenance

Welcome to the Quick Shortcut AI LLM Assistant documentation hub. This folder is organized into **7 workflow steps** that mirror the development process.

---

## 🎯 Quick Navigation

```
docs/
├── 01_input/           ← Requirements, specifications (INPUT)
├── 02_planning/        ← Tasks, plans, TODO.md (PLANNING)
├── 03_implementation/  ← Technical decisions (IMPLEMENTATION)
├── 04_testing/         ← Test guides, UAT (TESTING)
├── 05_review/          ← Issues, reviews, feedback (REVIEW)
├── 06_release/         ← Release notes, updated specs (RELEASE)
└── 07_archive/         ← Old versions, historical context (ARCHIVE)
```

---

## 📖 What's In Each Folder?

| Step | Folder | Purpose | Key Files |
|------|--------|---------|-----------|
| 1️⃣ | `01_input/` | **What should we build?** | CAHIER_DES_CHARGES.md, SPEC.md, PROJECT_DEFINITION.md |
| 2️⃣ | `02_planning/` | **What will we do?** | TODO.md (source of truth), PHASE_X_PLAN.md |
| 3️⃣ | `03_implementation/` | **How will we build it?** | TECHNICAL_DECISIONS.md |
| 4️⃣ | `04_testing/` | **How do we verify?** | TEST guides, VSCODE_TESTING_GUIDE.md, UAT_DETAILED_GUIDE.md |
| 5️⃣ | `05_review/` | **What did we find?** | PHASE3_ISSUES_INVENTORY.md, PHASE_X_REVIEW.md |
| 6️⃣ | `06_release/` | **What changed?** | UPDATED_SPEC.md, RELEASE_NOTES.md (after approval) |
| 7️⃣ | `07_archive/` | **What was old?** | Historical versions, lessons learned |

---

## ✅ Documentation Maintenance Checklist

Run this checklist **weekly** to keep documentation healthy:

### 1️⃣ Structure Verification
- [ ] Only **7 numbered folders** exist (01_input ... 07_archive)
- [ ] No extra folders like `docs/logs/`, `docs/technical/`, etc.
- [ ] Each folder has a **README.md**
- [ ] No `.py`, `.json`, or code files in docs/

### 2️⃣ File Placement Validation
- [ ] `01_input/` contains: CAHIER_DES_CHARGES.md, SPEC.md, PROJECT_DEFINITION.md
- [ ] `02_planning/` contains: TODO.md, PHASE_*_PLAN.md, IMPLEMENTATION_PLAN.md
- [ ] `03_implementation/` contains: TECHNICAL_DECISIONS.md
- [ ] `04_testing/` contains: TEST guides and UAT documents
- [ ] `05_review/` contains: PHASE_*_REVIEW.md, PHASE3_ISSUES_INVENTORY.md
- [ ] `06_release/` is empty OR contains UPDATED_SPEC.md (after approval)
- [ ] `07_archive/` contains ONLY README.md (no .archived files)

### 3️⃣ File Placement Rules (Critical!)
- [ ] ✅ PHASE_1_REVIEW.md is in `05_review/` (NOT planning)
- [ ] ✅ PHASE3_ISSUES_INVENTORY.md is in `05_review/` (NOT testing)
- [ ] ✅ TECHNICAL_DECISIONS.md is in `03_implementation/`
- [ ] ✅ TODO.md is in `02_planning/` (source of truth)

### 4️⃣ Reference Integrity
- [ ] No broken links in any README.md
- [ ] All cross-references use `docs/0X_` format (NOT `docs/old-name/`)
- [ ] Each folder README points to prev/next step
- [ ] Root README.md points to 02_planning/TODO.md, 05_review/PHASE3_ISSUES_INVENTORY.md

### 5️⃣ Workflow Coherence
- [ ] 01_input/ README → points to 02_planning/ ✓
- [ ] 02_planning/ README → points to 01_input/ + 03_implementation/ ✓
- [ ] 03_implementation/ README → points to 02_planning/ + 04_testing/ ✓
- [ ] 04_testing/ README → points to 03_implementation/ + 05_review/ ✓
- [ ] 05_review/ README → points to 04_testing/ + 06_release/ ✓
- [ ] 06_release/ README → points to 05_review/ + 07_archive/ ✓
- [ ] 07_archive/ README → points to 06_release/ ✓

### 6️⃣ Content Quality
- [ ] `02_planning/TODO.md` is up-to-date (updated every session)
- [ ] `05_review/PHASE3_ISSUES_INVENTORY.md` reflects current bugs
- [ ] No contradictory status messages (e.g., "ready for UAT" but bugs block it)
- [ ] No misleading documents (archive should have no conflicting info)

### 7️⃣ Optional Files Tracking
- [ ] `05_review/REVIEW_DECISION.md` exists? (For Phase 3 approval)
- [ ] `05_review/REVIEW_FEEDBACK.md` exists? (For Phase 3 comments)
- [ ] `04_testing/TEST_PLAN.md` exists? (Optional: test documentation)
- [ ] `06_release/UPDATED_SPEC.md` exists? (After Phase 3 approval)

### 8️⃣ Root-Level Files
- [ ] `README.md` (root) points to docs/0X_/ paths
- [ ] `CONTRIBUTING.md` explains 7-step workflow
- [ ] `.githooks/pre-commit` references 02_planning/TODO.md

---

## 🚨 Common Issues & Fixes

### ❌ Problem: Files in wrong folder
**Example**: PHASE_1_REVIEW.md in `02_planning/` instead of `05_review/`

**Fix**: Move to correct folder
```bash
mv docs/02_planning/PHASE_1_REVIEW.md docs/05_review/PHASE_1_REVIEW.md
```

### ❌ Problem: Broken references (old paths)
**Example**: Reference to `docs/technical/SPEC.md` or `docs/testing/PHASE3_ISSUES_INVENTORY.md`

**Fix**: Update to numbered folders
```bash
grep -r "docs/technical\|docs/testing\|docs/planning\|docs/input\|docs/archive" docs/ --include="*.md"
# Then update all matches to docs/0X_/ format
```

### ❌ Problem: Extra folders appeared
**Example**: `docs/logs/`, `docs/technical/`, etc.

**Fix**: Delete them
```bash
rm -rf docs/logs docs/technical
```

### ❌ Problem: Archive contains misleading files
**Example**: `FINAL_UAT_FIXES.md` in archive but bugs still exist

**Fix**: Delete misleading files, keep only historical context
```bash
rm docs/07_archive/*.archived  # Remove all archived docs with conflicting info
```

---

## 📝 Naming Conventions (STRICT)

All documentation files must follow these naming rules to maintain clarity:

### Folder Naming
- **Format**: `XX_name/` (two digits + underscore + lowercase name)
- **Example**: `01_input/`, `02_planning/`, `03_implementation/`
- **Rule**: ✅ MUST use numbers 01-07 in order
- **Rule**: ❌ NO old names like `input/`, `planning/`, `testing/`, `technical/`

### File Naming by Folder

#### `01_input/` - Requirements Files
- `CAHIER_DES_CHARGES.md` - Original requirements (French)
- `SPEC.md` - Technical specification
- `PROJECT_DEFINITION.md` - Phase scope definitions
- **Rule**: UPPERCASE.md for requirements documents

#### `02_planning/` - Planning Files
- `TODO.md` - Task tracking (source of truth) - **MUST be updated every session**
- `PHASE_X_PLAN.md` - Phase implementation plans (where X = 1, 2, 3...)
- `IMPLEMENTATION_PLAN.md` - Overall implementation strategy
- **Rule**: PHASE_1_PLAN.md (not phase_1_plan.md or PHASE-1-PLAN.md)
- **Rule**: Snake_case or UPPERCASE.md, NOT camelCase

#### `03_implementation/` - Technical Files
- `TECHNICAL_DECISIONS.md` - Architecture & design decisions
- `(Add more as needed)` - Other technical docs
- **Rule**: UPPERCASE for main technical documents

#### `04_testing/` - Testing & Verification Files
- `TEST_PLAN.md` - What tests exist and coverage (optional)
- `TEST_QUALITY_REVIEW.md` - Test coverage analysis
- `QUICK_START_TESTS.md` - How to run tests quickly
- `VSCODE_TESTING_GUIDE.md` - Debug tests in VS Code
- `UAT_DETAILED_GUIDE.md` - User Acceptance Testing guide
- **Rule**: Descriptive UPPERCASE.md for guides
- **Rule**: Use underscore for multi-word names (TEST_QUALITY_REVIEW.md not TestQualityReview.md)

#### `05_review/` - Review & Validation Files
- `PHASE_X_REVIEW.md` - Phase review results (X = 1, 2, 3...)
- `PHASE3_ISSUES_INVENTORY.md` - Current bugs and their status
- `REVIEW_DECISION.md` - Approval/rejection decision (optional)
- `REVIEW_FEEDBACK.md` - Reviewer comments (optional)
- **Rule**: PHASE3_ISSUES_INVENTORY.md (not PHASE-3 or phase3)
- **Rule**: UPPERCASE_WITH_UNDERSCORE for issue tracking

#### `06_release/` - Release Files
- `UPDATED_SPEC.md` - Updated SPEC with deployed features marked
- `RELEASE_NOTES.md` - Changelog for this release
- **Rule**: UPPERCASE.md for release documents
- **Rule**: Empty folder until after review approval

#### `07_archive/` - Historical Files
- Only `README.md` (explains why files are archived)
- No `.archived` extension on files anymore
- **Rule**: Archive folder must stay CLEAN (no misleading files)
- **Rule**: If file contradicts current truth, DELETE it (don't archive)

### README.md Naming
- Each folder MUST have `README.md` (lowercase)
- Explains: Purpose, files, when to use, next step
- **Rule**: Same for all folders (01_input/README.md, 02_planning/README.md, etc.)

### General Rules
- ✅ **Case**: UPPERCASE.md for main docs, lowercase for README.md
- ✅ **Separators**: Use underscore `_` (not hyphen or camelCase)
- ✅ **Numbers**: Use format like PHASE_1, PHASE_2 (not phase-1 or Phase1)
- ✅ **Format**: Always .md (Markdown)
- ❌ **Avoid**: Special characters, spaces, UPPERCASE_underscore MIX
- ❌ **Avoid**: Creating new files without checking folder conventions first

### Forbidden Patterns
```
❌ docs/logs/              → No standalone status folders
❌ docs/technical/         → No old folder names
❌ Phase_1_Review.md       → No camelCase
❌ phase-1-review.md       → No hyphens for numbered items
❌ PHASE1REVIEW.md         → Underscore required for readability
❌ MyDocument.pdf          → Only .md files in docs/
❌ temp_notes.md           → Only formal documents
```

---

## 📋 Maintenance Workflow

### Daily (Each Session)
1. ✏️ Update `docs/02_planning/TODO.md` with task status
2. ✏️ Update `docs/05_review/PHASE3_ISSUES_INVENTORY.md` if bugs found
3. ✓ Check no files are in wrong folders

### Weekly
1. Run **Section 1-3** of checklist above
2. Fix any broken references
3. Verify README.md cross-references

### Before Each Release/Phase Completion
1. Run **entire checklist** above
2. Move review docs from `05_review/` to `07_archive/` (if phase complete)
3. Create `06_release/UPDATED_SPEC.md` with deployed features
4. Update root README.md with latest status

---

## 🔧 Quick Maintenance Commands

### Check structure integrity
```bash
cd docs
ls -d */ | grep "^[0-9][0-9]_" || echo "All folders correctly numbered"
```

### Find broken doc references
```bash
grep -r "docs/technical\|docs/testing\|docs/planning\|docs/input\|docs/archive" --include="*.md"
```

### List all files by folder
```bash
for dir in 01_input 02_planning 03_implementation 04_testing 05_review 06_release 07_archive; do
  echo "$dir:"; ls -1 "$dir" | grep -v README.md
done
```

### Verify each folder has README.md
```bash
for dir in 01_input 02_planning 03_implementation 04_testing 05_review 06_release 07_archive; do
  [ -f "$dir/README.md" ] && echo "✓ $dir" || echo "❌ $dir MISSING README"
done
```

---

## 📞 Key Principles

1. **Single Source of Truth**: `docs/02_planning/TODO.md` - Update every session
2. **Workflow Alignment**: Folder order = development process
3. **No Contradictions**: Archive has no conflicting status files
4. **Clear References**: All links use `docs/0X_/` format (numbered)
5. **Self-Documenting**: Each folder README explains its purpose

---

## 🎯 Goal

Keep documentation **organized, coherent, and maintainable** so:
- ✅ No confusion about where things belong
- ✅ No contradictory status documents
- ✅ Single source of truth for all project info
- ✅ Easy to find what you need (input → release → archive)

---

**Last Updated**: 2026-02-17
**Status**: Documentation structure finalized
**Next**: Create missing Phase 3 review documents (REVIEW_DECISION.md, REVIEW_FEEDBACK.md)
