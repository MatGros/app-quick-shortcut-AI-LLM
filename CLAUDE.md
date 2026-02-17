# CLAUDE.md - Project Context & Guidelines

**Last Updated:** 2026-02-17
**Project:** Quick Shortcut AI LLM Assistant
**Status:** Phase 3 Complete (5 known bugs)

---

## 📍 Project Overview

Quick Shortcut AI is a **modern, native Windows application** that provides instant access to multiple LLM providers (Ollama, OpenAI, Anthropic, OpenRouter) via global hotkeys and a floating context menu.

**Key Stats:**
- 🐍 Language: Python 3.11+
- 🎨 UI: PySide6-Essentials (Qt6)
- 🪟 Platform: Windows 10 (1809+) / Windows 11 only
- ⚡ Performance: < 2s startup, < 150MB memory
- ✅ Test Coverage: 89% (365 tests)

---

## 📁 Project Structure (CRITICAL)

```
.
├── src/                          # Application source code
│   ├── main.py                   # Entry point
│   ├── core/                     # Core services
│   │   ├── config_service.py     # Settings management
│   │   ├── input_manager.py      # Global hotkeys (pynput)
│   │   ├── clipboard_manager.py  # Clipboard operations
│   │   ├── auto_paster.py        # Win32 window focus + paste
│   │   └── llm_provider.py       # Abstract provider interface
│   ├── ui/                       # UI components (PySide6)
│   │   ├── floating_menu.py      # Context menu (frameless)
│   │   ├── response_window.py    # Chat streaming window
│   │   ├── settings_dialog.py    # Configuration dialog
│   │   ├── screenshot_tool.py    # Region selection overlay
│   │   ├── tray_icon.py          # System tray integration
│   │   └── widgets/              # Reusable Qt components
│   ├── services/                 # Business logic
│   │   ├── providers/            # LLM provider implementations
│   │   │   ├── ollama_provider.py
│   │   │   ├── openai_provider.py
│   │   │   ├── anthropic_provider.py
│   │   │   └── openrouter_provider.py
│   │   ├── history_service.py    # SQLite conversation storage
│   │   └── notification_service.py
│   └── utils/                    # Helpers
│       ├── win32_helpers.py      # Windows API wrappers
│       └── markdown_renderer.py  # Markdown + syntax highlighting
│
├── tests/                        # Test suite
│   ├── test_core/                # Core module tests
│   ├── test_ui/                  # UI component tests
│   ├── test_services/            # Service tests
│   └── test_docs/                # Documentation tests
│       └── test_documentation.py # 27 tests for docs structure
│
├── docs/                         # Documentation (7-step workflow)
│   ├── 01_input/                 # Requirements & specifications
│   ├── 02_planning/              # Tasks & plans (TODO.md is source of truth)
│   ├── 03_implementation/        # Technical decisions
│   ├── 04_testing/               # Test guides & UAT
│   ├── 05_review/                # Issues & reviews (PHASE3_ISSUES_INVENTORY.md)
│   ├── 06_release/               # Release notes & updated spec
│   ├── 07_archive/               # Historical context only
│   └── README.md                 # Maintenance checklist
│
├── assets/                       # Static resources
│   ├── icons/                    # Application icons
│   └── styles/                   # QSS stylesheets (dark.qss, light.qss)
│
├── .github/
│   └── workflows/                # GitHub Actions CI/CD
│       ├── tests.yml             # Run pytest + coverage
│       ├── lint.yml              # Code quality (ruff, black)
│       └── docs.yml              # Documentation validation
│
├── .claude/
│   └── commands/                 # Slash command skills
│       ├── test.md               # /test
│       ├── docs.md               # /docs
│       ├── commit.md             # /commit
│       └── release.md            # /release
│
├── .githooks/
│   └── pre-commit                # Git hook to remind docs update
│
├── CLAUDE.md                     # This file - Claude Code context
├── AGENTS.md                     # GitHub Copilot + other AI context
├── README.md                     # User-facing project overview
├── CONTRIBUTING.md               # Contribution guidelines
├── LICENSE                       # MIT License
├── requirements.txt              # Python dependencies
├── pyproject.toml                # Project metadata & build config
└── pytest.ini                    # Pytest configuration
```

---

## 📋 Naming Conventions (STRICT)

### Python Files & Folders
- ✅ `snake_case.py` for files and folders
- ✅ `ClassName` for class names
- ❌ No spaces, no hyphens, no camelCase in filenames

### Documentation
- ✅ `UPPERCASE.md` for main documents (SPEC.md, TODO.md, TECHNICAL_DECISIONS.md)
- ✅ `README.md` (lowercase) for folder intros
- ❌ No numbers in filenames (numbered folders only: 01_input, 02_planning, etc.)

### Git & Commits
- ✅ Conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`
- ✅ Lowercase descriptions
- ✅ Example: `feat: add screenshot tool with region selection`

### Variables & Constants
- ✅ `snake_case` for variables
- ✅ `UPPER_SNAKE_CASE` for constants
- ✅ No single letters except loop indexes

---

## 🔧 Development Tools & Dependencies

### Core Libraries (MINIMAL - targeting < 50MB exe)
```
PySide6-Essentials>=6.5.0  # Qt6 minimal (NOT full PySide6)
pynput>=1.7.6              # Global keyboard/mouse hooks
requests>=2.31.0           # HTTP client
markdown>=3.5              # Markdown parsing
Pygments>=2.16             # Syntax highlighting
Pillow>=10.0               # Image handling
```

### Development Tools
```
pytest>=7.4                # Testing framework
pytest-qt>=4.2             # Qt testing
pytest-cov>=7.0            # Coverage reporting
black>=23.0                # Code formatter
ruff>=0.1.0                # Linter
mypy>=1.5                  # Type checking (optional)
```

### Build Tools
```
nuitka>=1.9                # Preferred: compile to native exe
pyinstaller>=6.0           # Alternative: if Nuitka issues
```

---

## 📖 Single Source of Truth

### `docs/02_planning/TODO.md`
- **This is THE authoritative task list**
- Update every session before committing
- Format: Simple markdown with checkboxes
- Claude will reference this when planning work

### `docs/05_review/PHASE3_ISSUES_INVENTORY.md`
- Current bugs and their status
- Updated when new issues found
- 5 known critical bugs documented

---

## 🔄 Workflow & Process

### Before Starting Work
1. Read `docs/02_planning/TODO.md` (what needs doing)
2. Read `docs/05_review/PHASE3_ISSUES_INVENTORY.md` (known blockers)
3. Update CLAUDE.md context if needed (rare)

### During Development
1. Make small, focused commits
2. Use conventional commit messages
3. Run: `pytest tests/ -v` before committing
4. Ensure new code has tests (maintain 80%+ coverage)

### Before Committing
```bash
# 1. Run all quality checks
pytest tests/ -v --cov=src --cov-report=term-missing

# 2. Check documentation
python docs/verify_docs.py

# 3. Lint code
ruff check src/ tests/
black --check src/ tests/

# 4. Update TODO.md with your changes
# 5. Create commit with conventional message
git add .
git commit -m "feat: add screenshot region selection"
```

### After Committing
- GitHub Actions will run automatically (tests, lint, docs)
- Check status at: https://github.com/YOUR_USERNAME/app-quick-shortcut-AI-LLM/actions
- Failures block future merges

---

## 🧪 Testing Requirements

### Pytest Configuration
- Location: `pytest.ini`
- Run: `pytest tests/` (auto-discovers tests)
- Coverage target: > 80% for new code
- Report format: JUnit XML + HTML

### Test Organization
```
tests/
├── test_core/           # Core services (config, input, clipboard)
├── test_ui/             # UI components
├── test_services/       # LLM providers, history
└── test_docs/           # Documentation structure (27 tests)
```

### Running Tests
```bash
pytest tests/                                    # All tests
pytest tests/test_core/ -v                       # Specific module
pytest tests/ --cov=src --cov-report=html       # With coverage
```

---

## 📚 Documentation Standards

### Docstrings (Google Style)
```python
def process_response(text: str, provider: str) -> str:
    """Process LLM response with formatting and caching.

    Args:
        text: Raw response from LLM provider
        provider: Provider name (ollama, openai, etc)

    Returns:
        Formatted response ready for display

    Raises:
        ValueError: If text is empty
    """
```

### Comments
- Explain WHY, not WHAT (code shows what)
- Use comments for complex logic, edge cases
- Keep comments near relevant code

### Type Hints
- Add type hints to all function signatures
- Use `from typing import Optional, List, Dict` as needed
- Run mypy for static type checking (optional but recommended)

---

## 🐛 Phase 3 Known Issues

**5 Critical Bugs** (to fix in Phase 4):

1. **Settings Dialog Closes App** - Closing settings exits entire application
2. **Tray Icon Not Syncing** - Icon doesn't update after settings change
3. **Chat Freeze on Long Messages** - UI unresponsive with 2000+ tokens
4. **Menu Click Events Broken** - Menu items don't respond to clicks (keyboard works)
5. **Windows Context Menu Overlay** - System menu still appears alongside app menu

**Do NOT work on features until these are fixed.**

---

## 🔒 Security & Privacy Guidelines

- ❌ Never commit API keys or secrets
- ✅ Use environment variables for sensitive data
- ✅ Validate all user input
- ✅ No telemetry or data collection
- ✅ Screenshot data stays local

---

## 🚀 Key Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| Startup time | < 2s | ~1.5s ✅ |
| Memory (idle) | < 150MB | ~140MB ✅ |
| First token | < 200ms | ~180ms ✅ |
| Menu trigger latency | < 100ms | ~95ms ✅ |
| Exe size | < 50MB | ~45MB ✅ |

Keep these in mind when optimizing!

---

## 💡 Architecture Decisions

See `docs/03_implementation/TECHNICAL_DECISIONS.md` for:
- Why PySide6-Essentials (not PyQt5/Tkinter)
- Why pynput for hooks
- Why Abstract Factory for LLM providers
- Why QThread for all I/O
- Why Nuitka for compilation

---

## 🛠️ Common Commands

```bash
# Development
python -m src.main                              # Run app

# Testing
pytest tests/ -v                                # All tests
pytest tests/ --cov=src                         # With coverage
python docs/verify_docs.py                      # Doc validation

# Code Quality
ruff check src/ tests/                          # Linting
black src/ tests/                               # Formatting

# Git Hooks
git config core.hooksPath .githooks             # Enable pre-commit hook
```

---

## 📞 When to Update CLAUDE.md

Update this file when:
- ✅ Project structure changes (new folders, renamed modules)
- ✅ New development standards adopted
- ✅ New critical context Claude needs to know
- ✅ Build/deployment process changes

Don't update for:
- ❌ Bug fixes (use git commits instead)
- ❌ Small code changes (CLAUDE.md is for meta-level context)
- ❌ Temporary experimental code

---

## 🎯 Claude Code Integration

Claude Code will:
- ✅ Read this CLAUDE.md automatically
- ✅ Understand your project structure
- ✅ Apply your naming conventions
- ✅ Reference TODO.md for task status
- ✅ Check PHASE3_ISSUES_INVENTORY.md for blockers
- ✅ Run pytest before suggesting commits
- ✅ Validate documentation changes

**This makes Claude more effective and reduces errors.**

---

**Remember:** Keep this file updated. It's the instruction manual for working efficiently with Claude Code. 🚀
