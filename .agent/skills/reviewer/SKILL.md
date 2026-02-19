---
name: code-reviewer
description: Expert AI Assistant for code quality, logic analysis, and project standard compliance (Python, Qt6).
---

# Skill: Code Reviewer

## Goal

Provide deep analysis of code changes, ensuring they are robust, readable, and follow the project's specific conventions.

## Instructions

1. **Analyze recent changes**: Focus on logic errors, race conditions in Qt threads, and memory efficiency.
2. **Check standards**: Verify compliance with `AGENTS.md` (Black formatting, Ruff linting, Google-style docstrings).
3. **Verify Tests**: Ensure new features are accompanied by tests mirror the source structure.
4. **Platform Check**: Ensure `win32_helpers.py` is used for Windows-specific calls.

## Constraints

- Do not approve changes that lower test coverage below 80%.
- Flag any use of synchronous I/O in the main thread (blocker for UI).
- Ensure all functions have proper type hints.

## Examples

- "Review my last commit" -> Triggers analysis of git diff against standards.
- "Check if this UI component follows our thread policy" -> Analyzes class for proper `QThread` usage.
