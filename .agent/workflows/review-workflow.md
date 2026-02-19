---
description: Run a comprehensive code review using the code-reviewer skill.
---

# Workflow: Code Review (/review)

1. **Self-Check**: Run `pytest` and `ruff check` to ensure basic quality.
2. **Skill Activation**: Activate the `code-reviewer` skill.
3. **Deep Analysis**:
   - Analyze current changes (unstaged and staged).
   - Compare against `AGENTS.md` and `CLAUDE.md`.
4. **Report**:
   - List critical issues (logic, bugs).
   - List style issues (linting, docs).
   - Provide a "Pass/Fail" recommendation.
