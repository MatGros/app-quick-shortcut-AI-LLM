---
name: release
description: Prepare release with version bump, changelog, and validation
---

# Release Skill

Prepare a complete release with version updates, release notes, and final validation.

## What This Does

1. **Final Validation** - Run all tests and checks
2. **Update Version** - Bump version in pyproject.toml
3. **Generate Changelog** - Create/update RELEASE_NOTES.md
4. **Create Commit** - Version bump with tag
5. **Documentation** - Update UPDATED_SPEC.md

## Release Checklist

Before release, verify:

- [x] All tests pass (365/365)
- [x] Documentation validates
- [x] Code is formatted and linted
- [x] Known issues documented (PHASE3_ISSUES_INVENTORY.md)
- [x] UPDATED_SPEC.md is current
- [x] RELEASE_NOTES.md is complete

## Steps

### 1. Final Validation
```bash
# Run all quality checks
pytest tests/ -v --cov=src
python docs/verify_docs.py
ruff check src/ tests/
black --check src/ tests/
```

### 2. Update Version (in pyproject.toml)
```toml
[project]
version = "1.0.0"  # Bump from previous
```

### 3. Update Release Notes
Create/update `docs/06_release/RELEASE_NOTES.md`:
```markdown
# Release Notes - Version 1.0.0

**Date:** 2026-02-18
**Status:** Ready for Production

## What's New
- Feature A
- Feature B
- Bug fixes

## Known Issues
- Issue 1
- Issue 2

## Installation
...
```

### 4. Update UPDATED_SPEC.md
In `docs/06_release/UPDATED_SPEC.md`:
```markdown
# Updated Specification - Version 1.0.0

**Status:** Released

## Features Deployed
- ✅ Feature A
- ✅ Feature B
```

### 5. Create Release Commit
```bash
git add docs/06_release/RELEASE_NOTES.md
git add docs/06_release/UPDATED_SPEC.md
git add pyproject.toml
git commit -m "release: version 1.0.0"
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main --tags
```

## Version Numbering (Semantic Versioning)

```
MAJOR.MINOR.PATCH

1.0.0    = First release (MAJOR)
1.1.0    = New features (MINOR)
1.0.1    = Bug fixes (PATCH)
2.0.0    = Breaking changes (MAJOR)
```

## Release Types

### Major Release (Phase Complete)
```
From: 0.3.0
To:   1.0.0
When: Phase 3 bugs fixed, full UAT pass
```

### Minor Release (Features Added)
```
From: 1.0.0
To:   1.1.0
When: New features, no breaking changes
```

### Patch Release (Bug Fixes)
```
From: 1.0.0
To:   1.0.1
When: Critical bugs fixed
```

## GitHub Release Notes Template

```markdown
# Version X.Y.Z

**Release Date:** YYYY-MM-DD

## 📋 Summary
One sentence summary of this release

## ✨ New Features
- Feature A description
- Feature B description

## 🐛 Bug Fixes
- Bug fix description
- Another bug fix

## 📖 Documentation
- Documentation update description

## ⚠️ Known Issues
- Known issue and workaround

## 📊 Stats
- Tests: 365 passing
- Coverage: 89%
- Performance: Startup < 2s

## 🙏 Thanks
Contributors and acknowledgments
```

## Quality Gates (Must Pass Before Release)

- ✅ All 365 tests passing
- ✅ 89%+ code coverage maintained
- ✅ Documentation validates (27 tests)
- ✅ No new issues in PHASE3_ISSUES_INVENTORY.md
- ✅ Performance targets met (startup < 2s, memory < 150MB)
- ✅ Zero security issues

## When to Use

Use `/release` when:
- ✅ All Phase work is complete
- ✅ All tests passing
- ✅ All documentation updated
- ✅ Ready to create GitHub Release

## After Release

1. **Announce** - Update README.md with latest version
2. **Tag** - Git tag v1.0.0 for release
3. **GitHub Release** - Create GitHub release page
4. **Celebrate** 🎉 - You earned it!

## Important Notes

- Never release with failing tests
- Never release with known bugs (document them)
- Always update version numbers
- Always generate release notes
- Always tag releases in git

Each release is a milestone. Do it right!
