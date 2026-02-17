---
name: docs
description: Validate and maintain project documentation structure
---

# Docs Skill

Validate documentation structure, naming conventions, and cross-references.

## What This Does

1. **Structure Check** - Verify 7 folders (01_input...07_archive) exist
2. **Naming Validation** - Check file naming conventions
3. **Reference Integrity** - Ensure links use correct docs/0X_/ format
4. **Workflow Coherence** - Verify README cross-references
5. **Optional Files** - Check Phase 3 completion files

## Steps

```bash
# 1. Run documentation tests
pytest tests/test_docs/ -v

# 2. Run PowerShell verification (if Windows)
# pwsh docs/verify_docs.ps1

# 3. Run Python verification
python docs/verify_docs.py

# 4. Report results
```

## Expected Output

```
========== VERIFICATION REPORT ==========
Checks Passed: 26
Warnings:      1 (optional files)
Errors:        0

✓ READY FOR RELEASE
```

## Naming Rules

When creating or updating documentation:

### Main Documents (UPPERCASE)
```
✅ SPEC.md
✅ TODO.md
✅ TECHNICAL_DECISIONS.md
✅ PHASE3_ISSUES_INVENTORY.md
```

### Folder Intros (lowercase)
```
✅ README.md (in each folder)
```

### Folder Names (Numbered)
```
✅ 01_input/        (never: docs/input/)
✅ 02_planning/     (never: docs/planning/)
✅ 03_implementation/
✅ 04_testing/
✅ 05_review/
✅ 06_release/
✅ 07_archive/
```

## Cross-Reference Format

✅ Correct:
```
See [docs/02_planning/TODO.md](docs/02_planning/TODO.md)
Refer to docs/05_review/PHASE3_ISSUES_INVENTORY.md
```

❌ Wrong:
```
See docs/planning/TODO.md (old folder name)
Refer to docs/testing/... (should be docs/04_testing/)
```

## When to Use

- Before committing documentation changes: `/docs`
- After adding new documentation files
- When referencing other docs in code/README
- Before releasing/merging

## Common Issues Fixed

- **Old paths:** docs/technical/ → docs/03_implementation/
- **Wrong cases:** phase3_issues.md → PHASE3_ISSUES_INVENTORY.md
- **Missing refs:** Add cross-references to previous/next step
- **Wrong placement:** Move files to correct numbered folder

## Failure Handling

If documentation validation fails:
1. Show which rule was violated
2. Suggest correct format
3. Fix it if possible
4. Explain the rule for future reference
