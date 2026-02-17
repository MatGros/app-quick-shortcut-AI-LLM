# AGENTS.md - AI Assistant Context

**Format:** AGENTS.md Standard v1.0
**Last Updated:** 2026-02-17
**Supported Tools:** GitHub Copilot, Cursor, Windsurf, Google Jules, Aider, and other AI coding assistants

---

## Project Information

**Project:** Quick Shortcut AI LLM Assistant
**Type:** Windows Native Desktop Application
**Language:** Python 3.11+
**Framework:** PySide6 (Qt6)
**Status:** Phase 3 Complete (5 known bugs, awaiting fixes)

---

## Directory Structure

```
.
├── src/                    # Application source code
│   ├── main.py             # Entry point - starts app
│   ├── core/               # Core functionality
│   ├── ui/                 # User interface components
│   ├── services/           # Business logic & providers
│   └── utils/              # Helper utilities
├── tests/                  # Test suite (365 tests, 89% coverage)
├── docs/                   # 7-step workflow documentation
├── assets/                 # Icons, stylesheets
├── .github/workflows/      # CI/CD automation
├── .claude/commands/       # Claude Code slash commands
└── .githooks/              # Git hooks for automation
```

---

## Key Conventions

### Code Style
- **Language:** Python 3.11+
- **Naming:** snake_case for functions/variables, CamelCase for classes
- **Formatting:** Black formatter (line length: 88)
- **Linting:** Ruff for code quality
- **Type Hints:** Required for all function signatures

### Documentation
- **Main Docs:** UPPERCASE.md (SPEC.md, TODO.md, TECHNICAL_DECISIONS.md)
- **Folder Intros:** README.md (lowercase)
- **Docstrings:** Google style
- **Comments:** Explain WHY, not WHAT

### File Organization
- **Numbered Folders:** docs/01_input through docs/07_archive (7-step workflow)
- **Source Code:** Organized by layer (core, ui, services, utils)
- **Tests:** Mirrored structure (test_core, test_ui, test_services, test_docs)

---

## Development Standards

### Before Starting Work
1. Check `docs/02_planning/TODO.md` for current tasks
2. Check `docs/05_review/PHASE3_ISSUES_INVENTORY.md` for known bugs
3. Read `docs/03_implementation/TECHNICAL_DECISIONS.md` for architecture decisions

### Testing
- **Framework:** pytest
- **Coverage Target:** > 80%
- **Run:** `pytest tests/ -v --cov=src`
- **Documentation Tests:** `python docs/verify_docs.py`

### Commits
- **Style:** Conventional commits (feat:, fix:, docs:, test:)
- **Message Format:** `feat: brief description of what changed`
- **Example:** `feat: add screenshot region selection tool`

### Quality Gates
- ✅ Tests must pass (pytest)
- ✅ Code must be formatted (black)
- ✅ Linting must pass (ruff)
- ✅ Documentation must validate (verify_docs.py)

---

## Source of Truth Documents

### `docs/02_planning/TODO.md`
- Primary task tracking document
- Update before committing changes
- Format: Simple markdown with checkboxes
- **This is what drives development decisions**

### `docs/05_review/PHASE3_ISSUES_INVENTORY.md`
- Current bugs and blockers
- 5 critical issues documented
- Don't start features until bugs are fixed

### `docs/03_implementation/TECHNICAL_DECISIONS.md`
- Architecture decisions and rationale
- Why we chose specific libraries
- Design patterns used

---

## Project Phases

### Phase 3 (Current - COMPLETE)
- ✅ Full LLM provider integration
- ✅ Complete UI implementation
- ✅ 365 tests (89% coverage)
- ⚠️ 5 known critical bugs
- 📋 Awaiting Phase 4 bug fixes

### Phase 4 (Next)
- [ ] Fix 5 critical bugs
- [ ] Re-run UAT suite
- [ ] Performance validation

---

## Critical Known Issues

**DO NOT ignore these.** They block feature development:

1. **Settings Dialog Closes Application**
   - Symptom: Closing settings closes entire app
   - Impact: HIGH - blocks UAT
   - Status: Documented, awaiting fix

2. **Tray Icon State Not Syncing**
   - Symptom: Icon doesn't update after settings change
   - Impact: HIGH - blocks UAT
   - Workaround: Restart app

3. **Chat Window Freezes**
   - Symptom: UI unresponsive with 2000+ token responses
   - Impact: HIGH - blocks UAT
   - Workaround: Send shorter prompts

4. **Menu Click Events Broken**
   - Symptom: Menu items don't respond to clicks
   - Impact: HIGH - keyboard navigation works
   - Workaround: Use arrow keys + Enter

5. **Windows Context Menu Still Appears**
   - Symptom: System menu overlays app menu
   - Impact: MEDIUM - UX degradation
   - Workaround: None yet

---

## Build & Run Commands

### Development
```bash
python -m src.main                    # Run application
```

### Testing
```bash
pytest tests/ -v                      # Run all tests
pytest tests/test_core/ -v            # Run specific test module
pytest tests/ --cov=src               # Run with coverage report
python docs/verify_docs.py            # Validate documentation
```

### Code Quality
```bash
black src/ tests/                     # Format code
ruff check src/ tests/                # Lint code
black --check src/ tests/             # Check formatting
```

---

## Dependencies

### Core (MINIMAL - optimize for < 50MB exe)
- **PySide6-Essentials** (Qt6 minimal)
- **pynput** (keyboard/mouse hooks)
- **requests** (HTTP client)
- **markdown** (Markdown parsing)
- **Pygments** (syntax highlighting)
- **Pillow** (image handling)

### Development
- **pytest** (testing)
- **pytest-qt** (Qt testing)
- **black** (formatting)
- **ruff** (linting)

### Build
- **nuitka** (compile to native exe - preferred)
- **pyinstaller** (alternative)

---

## LLM Provider Support

### Implemented Providers
1. **Ollama** - Local LLMs (Llama2, Mistral, etc.)
2. **OpenAI** - GPT-3.5-turbo, GPT-4, GPT-4o
3. **Anthropic** - Claude 3 (Sonnet, Opus)
4. **OpenRouter** - Multi-model aggregation

### Adding New Provider
1. Create file: `src/services/providers/new_provider.py`
2. Implement `LLMProvider` abstract interface
3. Add tests in `tests/test_services/test_providers/`
4. Update `docs/03_implementation/TECHNICAL_DECISIONS.md`

---

## Performance Targets

These should be maintained during development:

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Startup | < 2s | ~1.5s | ✅ Pass |
| Memory | < 150MB | ~140MB | ✅ Pass |
| First Token | < 200ms | ~180ms | ✅ Pass |
| Menu Latency | < 100ms | ~95ms | ✅ Pass |
| Exe Size | < 50MB | ~45MB | ✅ Pass |

Don't make changes that degrade these metrics.

---

## Common Tasks

### Add New Feature
1. Update `docs/02_planning/TODO.md`
2. Check `docs/05_review/PHASE3_ISSUES_INVENTORY.md` for blockers
3. Create feature branch
4. Write tests first (TDD recommended)
5. Implement feature
6. Update `docs/` if architecture changed
7. Run all quality checks
8. Create pull request

### Fix a Bug
1. Create issue/task in TODO.md
2. Add test that reproduces bug
3. Fix bug
4. Verify test now passes
5. Update PHASE3_ISSUES_INVENTORY.md
6. Commit with message: `fix: brief description`

### Update Documentation
1. Edit relevant file in docs/0X_*/
2. Run: `python docs/verify_docs.py`
3. Ensure all 27 tests pass
4. Commit with message: `docs: update XXXX`

---

## Git Workflow

```bash
# Setup
git config core.hooksPath .githooks    # Enable pre-commit hook

# Feature development
git checkout -b feature/short-name
git add .
git commit -m "feat: description"
git push

# After tests pass
# Create pull request on GitHub
# All checks must pass before merge
```

---

## Configuration

### Settings Storage
- Location: `%APPDATA%\QuickShortcutAI\config.json`
- Format: JSON
- Schema: See `docs/06_release/UPDATED_SPEC.md`

### Environment Variables
- Use for API keys (never commit)
- Example: `OPENAI_API_KEY=sk-...`

---

## Documentation Rules

### When to Update docs/
- ✅ Architecture changes
- ✅ New features (document in SPEC.md)
- ✅ Process changes
- ❌ Regular bug fixes (just commit message)
- ❌ Small code tweaks

### Quality Gate
- All documentation tests must pass
- Run: `python docs/verify_docs.py`
- Failing tests block commits

---

## Windows-Specific Notes

### Supported Versions
- Windows 10 (1809+)
- Windows 11

### Platform-Specific Code
- Use `win32_helpers.py` for Windows API calls
- Test on both Windows 10 and 11
- Use platform-agnostic paths where possible

---

## Getting Help

- **Architecture Questions:** See `docs/03_implementation/TECHNICAL_DECISIONS.md`
- **Tasks & Status:** Check `docs/02_planning/TODO.md`
- **Known Issues:** See `docs/05_review/PHASE3_ISSUES_INVENTORY.md`
- **Specification:** Read `docs/06_release/UPDATED_SPEC.md`

---

## Tools This File Supports

This AGENTS.md file is read by:
- ✅ GitHub Copilot (Visual Studio Code)
- ✅ Cursor IDE
- ✅ Windsurf IDE
- ✅ Google Jules
- ✅ Aider
- ✅ Other AI coding assistants supporting AGENTS.md standard

---

**Note:** This file complements CLAUDE.md (for Claude Code). Keep both updated.

For questions about conventions or standards, check this file first.
