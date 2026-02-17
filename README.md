# ⚡ Quick Shortcut AI LLM Assistant

> A lightweight, ultra-fast Windows native application for AI-powered text assistance with global keyboard shortcuts.

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Tests Passing](https://img.shields.io/badge/Tests-365%2F365%20passing-brightgreen)](./docs/04_testing/PHASE3_ISSUES_INVENTORY.md)
[![Coverage](https://img.shields.io/badge/Coverage-89%25-brightgreen)](#test-coverage)
[![License](https://img.shields.io/badge/License-GPL--3.0-blue)](LICENSE)

---

## 🎯 What is This?

A modern Windows assistant that brings AI to your fingertips with **one keyboard shortcut**:

1. **Ctrl + Right-Click** anywhere
2. Choose an action (Summarize, Translate, Custom Prompt, etc.)
3. Get AI response instantly with streaming

**Supports:** Ollama (local), OpenAI, Anthropic Claude, and more.

---

## ✨ Key Features

| Feature                    | Status     | Details                               |
| -------------------------- | ---------- | ------------------------------------- |
| **🔌 Multi-LLM Support**   | ✅ Phase 1 | Ollama, OpenAI, Anthropic (pluggable) |
| **⌨️ Global Shortcuts**    | 🚧 Phase 2 | Ctrl+Right-Click menu system          |
| **💬 Streaming Chat**      | 🚧 Phase 2 | Real-time token streaming             |
| **📸 Screenshot + Vision** | 📋 Phase 3 | AI analyze images natively            |
| **💾 History**             | 📋 Phase 4 | SQLite-based conversation storage     |
| **🎨 Modern UI**           | 🚧 Phase 2 | Dark/Light themes, smooth animations  |
| **⚡ Ultra-Fast**          | 🎯 Target  | < 2s startup, < 100ms menu latency    |

---

## 🚀 Quick Start

### Prerequisites

- **Windows 10** (1809+) or **Windows 11**
- **Python 3.10+**
- One LLM: Ollama (local) OR OpenAI/Anthropic API key

### Installation (Development)

```bash
# 1. Clone repo
git clone <repo-url>
cd app-quick-shortcut-AI-LLM

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run tests to verify setup
pytest tests/ -v
```

### First Run

```bash
# Coming in Phase 2 - For now, tests only
python -m pytest tests/ -v
```

---

## 📋 Project Status

### ✅ Phase 1: Foundation (COMPLETE)

- [x] LLM Provider abstraction (Ollama, OpenAI, Anthropic)
- [x] Configuration service (JSON persistence)
- [x] Health checks (startup validation)
- [x] **43 unit tests (87% coverage)**
- [x] Ready for UI layer

### ✅ Phase 2: UI Core (COMPLETE - Unit Tests)

- [x] Global keyboard hooks (Ctrl+Right-Click) - unit tested
- [x] Floating context menu (6 actions) - unit tested
- [x] Response streaming window - unit tested
- [x] Keyboard shortcuts manager - unit tested
- [x] System tray icon - unit tested
- [x] Main app orchestration - unit tested
- [x] **213 unit tests (89% coverage)**
- [x] Components signal-connected
- ⚠️ No integration/visual tests yet (moved to Phase 3)

### 🚧 Phase 3: LLM Integration & Testing (IN PROGRESS - UAT PAUSED)

**Status**: Code complete (365 tests passing) but **critical UI bugs blocking UAT**

- [x] Real LLM streaming (Task #1 - done)
- [x] Clipboard manager (Task #1 - done)
- [x] Markdown rendering (Task #3 - done)
- [x] Settings dialog (Task #4 - done, but closes app ❌)
- [x] Auto-paste (Task #5 - done)
- [x] Integration Tests (Task #6 - 365 tests passing ✅)
- 🔴 Chat streaming (works but freezes UI ❌)
- 🔴 Floating context menu (appears but unclickable ❌)
- 🔴 Status icon (shows wrong state ❌)

**Blocking Issues** ([Details here](docs/05_review/PHASE3_ISSUES_INVENTORY.md)):
1. Settings dialog closes entire app
2. Status icon stays red with valid config
3. Chat UI freezes during LLM response
4. Menu items not clickable
5. Windows system menu appears alongside app menu

**Next**: Fix 5 critical issues before continuing UAT

### 📋 Phase 4: Polish (PLANNED)

- [ ] SQLite history with search
- [ ] Toast notifications
- [ ] Dark/Light theme system (QSS)
- [ ] Performance profiling and optimization

### 📋 Phase 5: Release (PLANNED)

- [ ] Packaging with Nuitka (< 50MB exe, < 2s startup)
- [ ] Final documentation & user guide
- [ ] Release on GitHub

---

## 🧪 Testing

### Run All Tests

```bash
# With coverage report
pytest tests/ -v --cov=src --cov-report=term-missing

# Summary
pytest tests/ -v
```

### Expected Output

```
✅ test_llm_provider.py     : 18 tests passing
✅ test_config_service.py   : 14 tests passing
✅ test_health_check.py     : 11 tests passing
======================== 43 passed in 0.56s ========================
Coverage: 87% ⭐
```

### Test Coverage by Module

```
llm_provider.py    : 89% ⭐
config_service.py  : 93% ⭐
health_check.py    : 85% ⭐
```

For more details, see [PHASE_1_REVIEW.md](PHASE_1_REVIEW.md) and [VSCODE_TESTING_GUIDE.md](VSCODE_TESTING_GUIDE.md).

---

## 📁 Project Structure

```
app-quick-shortcut-ai-llm/
├── src/                          # Application code
│   ├── core/                      # Core logic
│   │   ├── llm_provider.py        # Abstract LLM interface + Factory
│   │   ├── ollama_provider.py     # Ollama implementation
│   │   ├── openai_provider.py     # OpenAI implementation
│   │   ├── anthropic_provider.py  # Anthropic implementation
│   │   └── config_service.py      # Configuration (Singleton)
│   ├── ui/                        # UI components (Phase 2+)
│   ├── services/                  # Services
│   │   └── health_check.py        # Startup validation
│   └── utils/                     # Utilities
├── tests/                         # Test suite
│   ├── test_core/                 # Core tests
│   └── test_services/             # Service tests
├── assets/                        # Icons, styles (Phase 2+)
├── docs/                          # Documentation
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Project metadata
├── pytest.ini                     # Pytest configuration
├── SPEC.md                        # Technical specification
├── TODO.md                        # Implementation roadmap
├── LICENSE                        # GPL-3.0
└── README.md                      # This file
```

---

## ⚙️ Configuration

### Location

```
%APPDATA%\QuickShortcutAI\config.json
```

### Example Config

```json
{
  "providers": [
    {
      "id": "ollama-local",
      "type": "ollama",
      "base_url": "http://localhost:11434",
      "enabled": true
    }
  ],
  "appearance": {
    "theme": "dark",
    "font_family": "Segoe UI",
    "font_size": 11
  },
  "behavior": {
    "auto_paste_enabled": false,
    "auto_paste_delay_ms": 100
  }
}
```

See [SPEC.md](docs/01_input/SPEC.md) for complete configuration schema.

---

## 📚 Documentation

Documentation follows a **7-step workflow** matching the development process:

**Quick Navigation**:
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development workflow, checklists, git hooks
- **[TODO.md](docs/02_planning/TODO.md)** - **SOURCE OF TRUTH** for task status
- **[SPEC.md](docs/01_input/SPEC.md)** - Technical specification & features
- **[PHASE3_ISSUES_INVENTORY.md](docs/05_review/PHASE3_ISSUES_INVENTORY.md)** - Current Phase 3 bugs

**By Workflow Step**:
| Step | Folder | Purpose |
|------|--------|---------|
| 1️⃣ Input | [docs/01_input/](docs/01_input/) | Requirements, specs, definitions |
| 2️⃣ Planning | [docs/02_planning/](docs/02_planning/) | Plans, scope, TODO.md |
| 3️⃣ Implementation | [docs/03_implementation/](docs/03_implementation/) | Technical decisions, architecture |
| 4️⃣ Testing | [docs/04_testing/](docs/04_testing/) | Tests, guides, UAT |
| 5️⃣ Review | [docs/05_review/](docs/05_review/) | Issues, feedback, validation |
| 6️⃣ Release | [docs/06_release/](docs/06_release/) | Release notes, updated specs |
| 7️⃣ Archive | [docs/07_archive/](docs/07_archive/) | Historical versions, obsolete docs |

**Additional Resources**:
- **[VSCODE_TESTING_GUIDE.md](docs/04_testing/VSCODE_TESTING_GUIDE.md)** - Run tests in VS Code
- **[QUICK_START_TESTS.md](docs/04_testing/QUICK_START_TESTS.md)** - 3-minute test guide

---

## 🔧 Development

### Code Style

- **Formatter**: `black` (auto-formatted)
- **Linter**: `ruff`
- **Type Hints**: Where relevant (not strict)
- **Docstrings**: Google style

### VS Code Setup

```
Recommended extensions:
- Python (Microsoft)
- Pylance (Microsoft)
- Python Test Explorer (Little Fox Team)
```

Open command palette (`Ctrl+Shift+P`):

```
"Python: Select Interpreter" → Choose venv interpreter
"Test: Focus on Test Explorer View" → See all tests
```

---

## 🎯 Performance Targets

| Metric             | Target       | Current       |
| ------------------ | ------------ | ------------- |
| App startup        | < 2s         | TBD (Phase 2) |
| Menu latency       | < 100ms      | TBD (Phase 2) |
| Streaming response | Smooth 60fps | TBD (Phase 2) |
| Memory (idle)      | < 150MB      | TBD (Phase 2) |
| Exe size           | < 50MB       | TBD (Phase 5) |

---

## 🐛 Troubleshooting

### Tests not found in VS Code?

```bash
# 1. Refresh test explorer (icon in VS Code)
# 2. Ensure pytest installed in venv:
pip install pytest pytest-cov
# 3. Restart VS Code
```

### Import errors?

```bash
# Verify PYTHONPATH includes src/
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python -m pytest tests/ -v
```

### Need more details?

See [VSCODE_TESTING_GUIDE.md](VSCODE_TESTING_GUIDE.md) for comprehensive troubleshooting.

---

## 🤝 Contributing

This is a personal project, but improvements are welcome:

1. Fork the repo
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Add tests for your changes
4. Ensure all tests pass (`pytest tests/ -v`)
5. Submit pull request

---

## 📄 License

This project is licensed under **GPL-3.0** - see [LICENSE](LICENSE) file for details.

---

## 🚦 Next Steps

### For Users

1. ✅ Read this README
2. ✅ Check [SPEC.md](SPEC.md) for features
3. 🚧 Phase 2: Download exe and try it (coming soon)

### For Developers

1. ✅ Run tests: `pytest tests/ -v`
2. ✅ Read [PHASE_1_REVIEW.md](PHASE_1_REVIEW.md)
3. 🚧 Phase 2: Begin UI implementation
4. 📋 See [TODO.md](TODO.md) for detailed roadmap

---

## 📞 Support

- **Issues**: Check [TODO.md](TODO.md) roadmap
- **Questions**: See documentation files above
- **Test Help**: [VSCODE_TESTING_GUIDE.md](VSCODE_TESTING_GUIDE.md)

---

**Built with ❤️ using Python + PySide6 + pytest**

_Last updated: 2026-02-17 | Phase 3 Code Complete | UAT Paused - 5 Critical Bugs Blocking | See [TODO.md](docs/02_planning/TODO.md) for status_
