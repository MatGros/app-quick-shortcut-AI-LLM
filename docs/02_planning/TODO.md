# TODO - Quick Shortcut AI LLM Assistant

**Objectif** : Application Windows native légère et ultra-rapide pour assistant LLM avec raccourcis clavier
**Stack** : Python 3.10+ + PySide6-Essentials
**Packaging** : Nuitka (< 50MB exe, < 2s startup)
**Target** : Windows 10/11

**Last Updated**: 2026-02-17 (Synchronized with STATUS.md)

---

## Légende Statut
- `[ ]` TODO - Non commencé
- `[~]` IN PROGRESS - En cours
- `[x]` DONE - Terminé
- `[!]` BLOCKED - Bloqué (avec raison)

---

## [x] Phase 0: Setup Projet

### Structure & Configuration
- [x] Créer SPEC.md
- [x] Créer TODO.md
- [x] Créer architecture plan
- [x] Créer structure répertoires (src/core, src/ui, src/services, etc.)
- [x] Créer requirements.txt avec dépendances minimales
- [x] Créer pyproject.toml
- [x] Créer .gitignore
- [x] Initialiser git repo
- [x] Créer LICENSE (GPL-3.0)
- [x] Créer README.md

### Environnement Dev
- [x] Setup Python 3.10+ venv
- [x] Installer PySide6-Essentials
- [x] Installer dev tools (black, ruff, pytest, pytest-qt)
- [x] Configurer VS Code / IDE avec linting

---

## [x] Phase 1: Foundation (Complete)

### F-03: LLM Provider Abstraction ✅
- [x] Créer `src/core/llm_provider.py` (ABC)
- [x] Implémenter `src/core/ollama_provider.py`
- [x] Implémenter `src/core/openai_provider.py`
- [x] Implémenter `src/core/anthropic_provider.py`
- [x] Tests : 43 unit tests passing, coverage 87%+

### F-10: Configuration Service ✅
- [x] Créer `src/core/config_service.py` (Singleton)
- [x] Schema config.json (providers, shortcuts, appearance)
- [x] Load/Save dans %APPDATA%\QuickShortcutAI\
- [x] Tests : 14 tests passing, 93% coverage

### F-11: Health Checks ✅
- [x] Créer `src/services/health_check.py`
- [x] Check 1: Config integrity
- [x] Check 2: LLM connectivity (5s timeout)
- [x] Check 3: Permissions (AppData access)
- [x] Tests : 9 tests passing, 85% coverage

---

## [x] Phase 2: UI Core (Complete)

### F-01: Global Input Hooks ✅
- [x] Créer `src/core/input_manager.py`
- [x] Capture Ctrl+Right-Click globally
- [x] QThread for non-blocking hook listening
- [x] Signal-based event emission (thread-safe)
- [x] Tests: 28 tests passing

### F-02: Floating Menu (Context Menu) ✅
- [x] Créer `src/ui/floating_menu.py`
- [x] QWidget frameless (Qt.FramelessWindowHint, Qt.Tool)
- [x] Design : rounded corners, shadow, fade-in 200ms
- [x] Keyboard navigation (arrows, Enter, Esc)
- [x] Smart positioning (cursor, edge detection, multi-monitor)
- [x] Signal `sig_action_selected(action_id: str)`
- [x] Tests UI : 28 tests passing

### F-04: Response Window (Chat Streaming) ✅
- [x] Créer `src/ui/response_window.py`
- [x] Singleton pattern
- [x] QTextEdit read-only pour chat area
- [x] Auto-scroll avec détection user scroll
- [x] Auto-expanding text input
- [x] Toolbar : Copy, Settings buttons
- [x] Status bar : provider + model info
- [x] Tests UI : 47 tests passing

### F-13: Keyboard Shortcuts ✅
- [x] Créer `src/core/shortcut_manager.py`
- [x] Enregistrement raccourcis globaux
- [x] Defaults : Ctrl+Right Click, Ctrl+Shift+S, Esc, Ctrl+W
- [x] Customization via Settings
- [x] Persistence in config.json
- [x] Tests : conflict detection, registration

### F-14: System Tray Integration ✅
- [x] Créer `src/ui/tray_icon.py`
- [x] QSystemTrayIcon avec menu
- [x] États : Ready (vert), Busy (jaune), Error (rouge)
- [x] Menu : Quick Actions, Settings, Exit
- [x] Tooltip avec status

### Main Application
- [x] Créer `src/main.py` (entry point)
- [x] QApplication setup
- [x] Startup : health checks → tray icon → input hooks
- [x] Signal connections entre composants

**Phase 2 Total: 153 tests passing, 89% coverage**

---

## [~] Phase 3: LLM Integration & Testing (In Progress - UAT Paused)

### Task #1: Real LLM Streaming ✅
- [x] ClipboardManager (text + images)
- [x] Real LLM calls (Ollama, OpenAI, Anthropic)
- [x] Stream tokens via signals
- [x] Error handling

### Task #2: Markdown Rendering ✅
- [x] Créer `src/ui/markdown_renderer.py`
- [x] Markdown → HTML avec Pygments
- [x] Dark/Light mode CSS theming
- [x] Tests : 30+ tests passing

### Task #3: Settings Dialog ✅
- [x] Créer `src/ui/settings_dialog.py`
- [x] Tab: Providers (add/edit, test connection)
- [x] Tab: Shortcuts (customization)
- [x] Tab: Appearance (theme)
- [x] Tab: Behavior (auto-paste, clipboard)
- [x] Save/Load via ConfigService
- [x] Tests UI : 30 tests passing

### Task #4: Auto-Paste ✅
- [x] Créer `src/core/auto_paster.py`
- [x] Capture active window handle (Win32 API)
- [x] Focus restoration
- [x] Keyboard simulation (pynput)
- [x] Tests : 15+ tests passing

### Task #5: Integration Tests ✅
- [x] Test workflows : Clipboard → LLM → Display
- [x] Test error scenarios
- [x] Real provider mocking
- [x] Tests : 150+ tests passing

**Phase 3 Code Complete: 365/365 tests passing, 89% coverage**

---

## [!] Phase 3 Critical Fixes (BLOCKING UAT)

### Task 3.1: Fix Settings Dialog Closing App [!] BLOCKED
- [ ] Investigate closeEvent / parent-child relationships
- [ ] Ensure settings close ≠ app shutdown
- [ ] **Status**: CRITICAL - User cannot save configuration
- **Target**: Fix before resuming UAT

### Task 3.2: Fix Status Icon Staying Red [!] BLOCKED
- [ ] Health check must update after settings change
- [ ] Icon must become green if health check passes
- [ ] **Status**: CRITICAL - User confused, thinks app broken
- **Target**: Fix before resuming UAT

### Task 3.3: Fix Chat Freeze During Streaming [!] BLOCKED
- [ ] Implement proper QThread for streaming
- [ ] Non-blocking UI during LLM response
- [ ] Tokens arrive progressively without freeze
- [ ] **Status**: CRITICAL - App unresponsive during use
- **Target**: Fix before resuming UAT (Priority 1)

### Task 3.4: Fix Floating Menu Click Events [!] BLOCKED
- [ ] Debug signal/slot connections
- [ ] Ensure MenuItem clicks register properly
- [ ] Verify event propagation
- [ ] **Status**: IMPORTANT - Primary feature broken
- **Target**: Fix before completing UAT

### Task 3.5: Suppress Windows Context Menu [!] BLOCKED
- [ ] Block Windows system menu appearance
- [ ] Options: pynput event suppression, Windows API, other
- [ ] **Status**: COSMETIC - Interface confusion
- **Target**: Fix for polish (lower priority)

**Phase 3 Status: Code Complete but UAT Paused - 5 Critical Fixes Needed**

---

## [ ] Phase 4: Advanced Features (PLANNED)

### F-05: Clipboard Management (Enhanced)
- [ ] Get/Set text avec retry logic
- [ ] Get/Set image (QImage)
- [ ] Monitor clipboard changes
- [ ] Format detection

### F-07: Screenshot Capture + Vision
- [ ] Créer `src/ui/screenshot_tool.py`
- [ ] Mode 1: Full screen capture
- [ ] Mode 2: Region selection
- [ ] Mode 3: Active window capture
- [ ] Vision API integration

### F-09: History (SQLite)
- [ ] Créer `src/services/history_service.py`
- [ ] Schema DB : conversations + messages
- [ ] Full-text search
- [ ] Export JSON/Markdown

### F-12: Theme System
- [ ] Dark/Light QSS stylesheets
- [ ] Dynamic theme switching
- [ ] System theme detection

### F-08: Toast Notifications
- [ ] Custom QWidget notifications
- [ ] Position: bottom-right, stacking
- [ ] Auto-dismiss (3s default)

---

## [ ] Phase 5: Polish & Package (PLANNED)

### Performance Optimization
- [ ] Profile startup time
- [ ] Profile memory usage
- [ ] Optimize hot paths

### Packaging
- [ ] Build with Nuitka (< 50MB exe)
- [ ] Test on Windows 10/11
- [ ] Create installer

### Documentation & Release
- [ ] Final documentation
- [ ] User guide
- [ ] Release on GitHub

---

## 📊 Test Metrics Summary

| Phase | Unit Tests | Integration Tests | Total | Status |
|-------|-----------|------------------|-------|--------|
| **Phase 0** | - | - | - | ✅ Complete |
| **Phase 1** | 43 | - | 43 | ✅ Complete |
| **Phase 2** | 153 | - | 153 | ✅ Complete |
| **Phase 3** | 169 | 150+ | **365** | 🟠 Code Complete, UAT Paused |
| **TOTAL** | **365** | **365** | **365** | 🟠 5 Critical Bugs Blocking |

---

## 🎯 Next Steps

**Immediate (Next Session)**:
1. Fix Task 3.1 - Settings dialog closeEvent
2. Fix Task 3.3 - Chat freeze with threading
3. Fix Task 3.2 - Health check icon update
4. Fix Task 3.4 - Menu click events
5. Fix Task 3.5 - Windows menu suppression

**Then**: Resume manual UAT, verify fixes, complete Phase 3

**See**: [STATUS.md](../../STATUS.md) for detailed priority and status

---

**Last Synchronized**: 2026-02-17 with STATUS.md
**Synchronization Note**: When STATUS changes, this file MUST be updated (see DOCUMENTATION_SYNC.md)
