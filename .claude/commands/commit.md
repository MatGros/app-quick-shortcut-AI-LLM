---
name: commit
description: Create a conventional commit with proper validation and formatting
---

# Commit Skill

Create properly formatted conventional commit messages that follow project standards.

## What This Does

1. **Validate Changes** - Run tests and linting
2. **Format Message** - Create conventional commit (feat:, fix:, docs:, etc)
3. **Update TODO.md** - Remind to update task status
4. **Create Commit** - Stage and commit with clean message

## Commit Types

```
feat:     New feature
fix:      Bug fix
docs:     Documentation changes only
test:     Test additions/modifications
refactor: Code refactoring without feature change
perf:     Performance improvement
chore:    Build, deps, tooling (no code change)
```

## Format Rules

```
✅ feat: add screenshot region selection
✅ fix: resolve settings dialog closing app
✅ docs: update TECHNICAL_DECISIONS.md
✅ test: add tests for clipboard manager

❌ Add feature (no type)
❌ FIX (uppercase)
❌ feat: Add feature (capitalized)
❌ feat: add screenshot region selection for better UX (too long)
```

## Steps

1. **Check status:**
   ```bash
   git status  # See what's changed
   ```

2. **Validate quality:**
   ```bash
   pytest tests/ -v --cov=src
   python docs/verify_docs.py
   ruff check src/ tests/
   black --check src/ tests/
   ```

3. **Update tracking:**
   - Edit docs/02_planning/TODO.md
   - Mark tasks as done/in-progress
   - Add new discoveries

4. **Stage files:**
   ```bash
   git add src/...  # Specific files
   git add docs/... # Documentation
   ```

5. **Create commit:**
   ```bash
   git commit -m "feat: brief description here"
   ```

## When to Use

Use `/commit` when you have:
- ✅ Completed a feature or fix
- ✅ All tests passing
- ✅ Updated documentation
- ✅ Updated TODO.md

## Scope Examples

### Small Fix
```
fix: correct typo in SPEC.md
```

### New Feature
```
feat: add screenshot region selection tool
```

### Multiple Changes (Multiple Commits Better)
```
# Split into separate commits:
git commit -m "feat: add screenshot tool"
git commit -m "docs: update SPEC with screenshot feature"
git commit -m "test: add screenshot tests"
```

## TODO.md Update

Before committing, update `docs/02_planning/TODO.md`:

```markdown
- [x] ✅ Add screenshot tool
- [x] ✅ Write screenshot tests
- [ ] ⏳ Handle region selection edge cases
- [ ] 📋 Add to SPEC.md
```

## Important Notes

- Keep commits small and focused
- One logical change per commit
- If fixing multiple things, use multiple commits
- Reference issue numbers if applicable: `fix: resolve #123`

## Verification

Before suggesting commit:
1. ✅ Tests pass (pytest)
2. ✅ Docs validate (verify_docs.py)
3. ✅ Code formatted (black)
4. ✅ Linting passes (ruff)
5. ✅ TODO.md updated

If any fail, show error and help fix before committing.
