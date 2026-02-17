# Contributing to Quick Shortcut AI LLM Assistant

Thank you for your interest in contributing! This document outlines the standards and workflows for this project to ensure a clean, fluid, and high-quality codebase.

## Development Workflow

We follow a strict **Task -> Plan -> Implementation -> Verification** cycle for all significant changes.

### 1. Task Definition

- **Analyze**: Understand the goal deeply.
- **Checklist**: Break down the work into atomic steps in `task.md` (or a temporary task file).
- **Context**: Ensure you have the latest state (git pull, check `STATUS.md`).

### 2. Planning (Phase Planning)

- **Create a Plan**: For complex features, create a plan in `docs/planning/` (e.g., `PHASE_X_PLAN.md`).
- **Review**: If working with an AI assistant or team, get approval on the plan before writing code.
- **Technical Design**: Update `docs/technical/SPEC.md` if architectural changes are needed.

### 3. Implementation

- **Clean Code**: Follow Python PEP 8 standards. Used `black` for formatting and `ruff` for linting.
- **Type Hints**: Use type hints for function arguments and return values.
- **Documentation**: Add docstrings to all modules, classes, and functions (Google style).
- **Separation of Concerns**:
  - `src/core`: Business logic, interfaces, data models.
  - `src/ui`: PySide6 widgets and windows.
  - `src/services`: Background agents, OS integration.
  - `src/utils`: Helper functions.

### 4. Verification & Testing

- **Unit Tests**: Write tests in `tests/` for every new component.
- **Run Tests**:
  ```bash
  pytest tests/ -v
  ```
- **Coverage**: Ensure strict coverage standards (>85%).
  ```bash
  pytest --cov=src tests/
  ```
- **Manual Verification**: Run the app and verify the UX manually if applicable.

## Project Structure

- **`src/`**: Source code.
- **`tests/`**: Test suite (unit and integration tests).
- **`docs/`**: Documentation (organized by type).
  - **`planning/`**: Phase plans, reviews, roadmaps
  - **`technical/`**: Specifications, technical details, definitions
  - **`testing/`**: Test guides, UAT reports, issue inventory
  - **`logs/`**: Operational logs (current session status)
  - **`archive/`**: **Obsolete/consolidated documents** (historical reference only)
- **`assets/`**: Images, icons, styles.

## Documentation Standards

### Authoritative Sources

- **Current Status**: Update **`STATUS.md`** after every major session
- **Project Overview**: Update **`README.md`** if features or phases change
- **Phase 3 Issues**: See **`docs/testing/PHASE3_ISSUES_INVENTORY.md`** (authoritative for current bugs)
- **Logs**: Update **`docs/logs/`** with operational notes

### Consolidation Rules

- **Do NOT create new status documents** if one exists (avoid duplication)
- **Consolidate information** from multiple sources into single authoritative file
- **Archive outdated docs** in `docs/archive/` with `.archived` suffix
- **Never contradict** - if multiple docs exist for same topic, consolidate into one

## Asking for Help

See `docs/testing/VSCODE_TESTING_GUIDE.md` for debugging tips.
