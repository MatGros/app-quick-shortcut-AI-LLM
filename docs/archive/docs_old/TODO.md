# TODO - Quick Shortcut AI LLM Assistant

**Objectif** : Application Windows native légère et ultra-rapide pour assistant LLM avec raccourcis clavier
**Stack** : Python 3.10+ + PySide6-Essentials
**Packaging** : Nuitka (< 50MB exe, < 2s startup)
**Target** : Windows 10/11

---

## Légende Statut

- `[ ]` TODO - Non commencé
- `[~]` IN PROGRESS - En cours
- `[x]` DONE - Terminé
- `[!]` BLOCKED - Bloqué (avec raison)

---

## [DONE] Phase 0: Setup Projet (Semaine 0)

### Structure & Configuration

- [x] Créer SPEC.md - Spécification technique complète (2026-02-15)
- [x] Créer TODO.md - Tracking d'implémentation (2026-02-15)
- [x] Créer Plan (goofy-gliding-turing.md) - Plan complet d'architecture (2026-02-15)
- [ ] Créer structure répertoires (src/core, src/ui, src/services, assets/, tests/)
- [ ] Créer requirements.txt avec dépendances minimales
- [ ] Créer pyproject.toml (metadata, black, ruff, pytest config)
- [ ] Créer .gitignore (Python, IDE, build artifacts)
- [ ] Initialiser git repo si pas déjà fait
- [ ] Créer LICENSE (GPL-3.0)
- [ ] Créer README.md basique

### Environnement Dev

- [ ] Setup Python 3.10+ venv
- [ ] Installer PySide6-Essentials (pas full PySide6)
- [ ] Installer dev tools (black, ruff, pytest, pytest-qt)
- [ ] Tester build Nuitka basique (hello world Qt)
- [ ] Configurer VS Code / IDE avec linting

---

## [DONE] Phase 1: Foundation (Semaine 1-2)

### F-01: Input Hooks (Global Keyboard/Mouse)

- [!] DEFERRED TO PHASE 2 - Requires PySide6 (Qt) for QThread signals

### F-03: LLM Provider Abstraction ✅

- [x] Créer `src/core/llm_provider.py` (ABC) - DONE
- [x] Interface : stream_chat(), get_models(), health_check(), supports_vision() - DONE
- [x] Créer `src/core/provider_factory.py` - DONE (integrated in llm_provider.py)
- [x] Implémenter `src/core/ollama_provider.py` - DONE
  - [x] Endpoint /api/chat avec streaming - DONE
  - [x] Support local (localhost:11434) et cloud - DONE
  - [x] Auth Bearer token optionnel - DONE
  - [x] Vision support detection (llama3.2-vision, llava) - DONE
- [x] Implémenter `src/core/openai_provider.py` - DONE
- [x] Implémenter `src/core/anthropic_provider.py` - DONE
- [x] Tests : 14 tests passing, 84%+ coverage - DONE

### F-10: Configuration Service ✅

- [x] Créer `src/core/config_service.py` (Singleton) - DONE
- [x] Schema config.json (providers, shortcuts, appearance, behavior) - DONE
- [x] Load/Save dans %APPDATA%\QuickShortcutAI\ - DONE
- [x] Validation config avec defaults - DONE
- [x] Migration config si schema change - DONE
- [x] Tests : 14 tests passing, 93% coverage - DONE

### F-11: Health Checks ✅

- [x] Créer `src/services/health_check.py` - DONE
- [x] Check 1: Config integrity - DONE
- [x] Check 2: LLM connectivity (5s timeout) - DONE
- [x] Check 3: Permissions (AppData access) - DONE
- [x] Tests : 9 tests passing, 85% coverage - DONE

---

## [DONE] Phase 2: UI Core (Semaine 3) ✅

### Infrastructure Setup

- [x] Setup PySide6-Essentials + Qt plugins (Task #6)
- [x] Create main.py entry point (Task #8)
- [x] Configure pytest-qt for UI testing

### F-01: Global Input Hooks ✅

- [x] Créer `src/core/input_manager.py` (Task #1)
- [x] Capture Ctrl+Right-Click globally
- [x] QThread for non-blocking hook listening
- [x] Signal-based event emission (thread-safe)
- [x] Tests: positioning, event filtering, signals

### F-02: Floating Menu (Context Menu) ✅

- [x] Créer `src/ui/floating_menu.py` (Task #2)
- [x] QWidget frameless (Qt.FramelessWindowHint, Qt.Tool)
- [x] Design : rounded corners (8px), shadow, fade-in 200ms
- [x] Layout : icon + text rows, separators
- [x] Actions : Summarize, Translate, Custom Prompt, Screenshot, Chat
- [x] Keyboard navigation (arrows, Enter, Esc)
- [x] Smart positioning (cursor, edge detection, multi-monitor)
- [x] Signal `sig_action_selected(action_id: str)`
- [x] Tests UI : positioning, keyboard nav, animations

### F-04: Response Window (Chat Streaming) ✅

- [x] Créer `src/ui/response_window.py` (Task #3)
- [x] Singleton pattern ou instance tracking
- [x] QTextEdit read-only pour chat area
- [x] Auto-scroll avec détection user scroll
- [x] Créer `src/ui/widgets/auto_expanding_text.py` (input area)
  - [x] Min 40px, max 200px
  - [x] Auto-expand on textChanged
- [x] Toolbar : Stop, Copy, Settings buttons
- [x] Status bar : provider + model info
- [x] Token buffering (50ms) pour smooth streaming
- [x] Tests UI : singleton, scroll, resize, streaming

### F-13: Keyboard Shortcuts ✅

- [x] Créer `src/core/shortcut_manager.py` (Task #4)
- [x] Enregistrement raccourcis globaux
- [x] Détection conflits
- [x] Defaults : Ctrl+Right Click, Ctrl+Shift+S, Esc, Ctrl+W
- [x] Customization via Settings
- [x] Persistence in config.json
- [x] Tests : conflict detection, registration

### F-14: System Tray Integration ✅

- [x] Créer `src/ui/tray_icon.py` (Task #5)
- [x] QSystemTrayIcon avec menu
- [x] États : Ready (vert), Busy (jaune), Error (rouge)
- [x] Menu : Quick Actions, Settings, Exit
- [x] Tooltip avec status
- [x] Notification fallback si toasts fail
- [x] Tests : state changes, menu actions

### Testing & Documentation

- [x] Phase 2 Tests: > 80% coverage (Task #7)
- [x] Phase 2 Documentation & Review (Task #9)

---

## [ON HOLD] Phase 3: LLM Integration & Fixes UAT (Semaine 3-4) 🚧

**STATUS**: PAUSED - 5 critical bugs blocking UAT
**STRATEGY**: Phase 3B approach - isolated patch on dedicated branch
**See**: docs/planning/PHASE_3B_PLAN.md (New strategy: keyboard + QThread fix)

---

## [PLANNED] Phase 3B: Hotkeys & Threading Patch (This Week) 🚀

**Branch**: `phase-3b/hotkeys-threading`
**Duration**: 3-5 days (Mon-Fri)
**Target**: Fix all 5 blocking bugs via minimal architecture changes
**Success Criteria**: All tests pass + UAT complete + zero crashes

### Day 1-2: Hotkeys Replacement
- [ ] **Task 3B.1**: Replace pynput → keyboard library
  - [ ] pip uninstall pynput && pip install keyboard
  - [ ] Refactor src/core/input_manager.py (copy code from docs/08_audit/PRACTICAL_SOLUTIONS_CODE_SNIPPETS.md)
  - [ ] pytest tests/test_core/test_input_manager.py PASS
  - [ ] Manual test: Ctrl+Shift+Right → Menu appears
  - [ ] Commit: "feat(phase3b): replace pynput with keyboard library"

### Day 2-3: Threading Fix
- [ ] **Task 3B.2**: Implement QThread worker pattern
  - [ ] Add StreamingWorker(QObject) class to src/main.py
  - [ ] Refactor _stream_chat_response() to use QThread
  - [ ] Add signal handlers (_on_token_received, _on_streaming_complete, _on_streaming_error)
  - [ ] pytest tests/test_ui/ -k streaming PASS
  - [ ] Manual test: Ctrl+Enter → UI responsive, tokens progressive
  - [ ] Commit: "feat(phase3b): implement QThread worker pattern for streaming"

### Day 3-4: Other Bug Fixes
- [ ] **Task 3B.3**: Fix Settings dialog (QDialog closeEvent)
  - [ ] src/ui/settings_dialog.py: Verify QDialog inheritance
  - [ ] Fix parent/child relationships
  - [ ] Manual test: OK → dialog closes, app continues

- [ ] **Task 3B.4**: Fix Health Check updates
  - [ ] Connect settings save signal → health_check.run_check()
  - [ ] Update tray icon on result
  - [ ] Manual test: Change config → icon updates

- [ ] **Task 3B.5**: Debug Menu click issues
  - [ ] Test if fixed by keyboard library replacement
  - [ ] If not: debug signal connections
  - [ ] Manual test: Click menu item → action works

- [ ] **Task 3B.6**: Commit all fixes
  - [ ] Commit: "fix(phase3b): settings, health check, menu issues"

### Day 4-5: UAT & Merge Decision
- [ ] **Task 3B.7**: Full User Acceptance Tests
  - [ ] Run PHASE_3B_TEST_PLAN.md (docs/testing/)
  - [ ] pytest tests/ -v --cov=src (>= 89% coverage)
  - [ ] Manual tests: All 5 bugs ✅ fixed
  - [ ] Stress test: 5-min no crashes
  - [ ] Create PHASE_3B_REVIEW.md with results

- [ ] **Task 3B.8**: Merge or Fallback Decision
  - [ ] If ALL PASS: git merge --no-ff phase-3b/hotkeys-threading → main
  - [ ] If FAIL: Document issues + evaluate rewrite options
  - [ ] Update status in TODO.md

---

## [AFTER 3B] Phase 3: Continue LLM Integration (Conditional)

**Only if Phase 3B succeeds**. Otherwise, re-evaluate architecture.

### 🛑 Priorité 1 : Bugs Critiques (Bloquants UAT)

- [x] **Task 3.1** (UAT 3) : Fix Settings closeEvent (FIXED in 3B)
- [x] **Task 3.2** (UAT 1) : Fix Health Check (FIXED in 3B)

### 🐛 Priorité 2 : Bugs Menu Contextuel (Retours UAT)

- [ ] **Task 3.5** (UAT 4) : Suppress Windows natif context menu (pynput hook override)
- [ ] **Task 3.6** (UAT 5) : Menu trop transparent et ne se ferme pas après clic gauche en dehors
- [ ] **Task 3.4** : Fix Menu click events (actions inopérantes via la souris)

### ✨ Priorité 3 : Refonte UX : Inline Response Window (UAT 7) & Threading (Bug 3.3)

- [ ] Créer `src/ui/inline_response_window.py` (fenêtre flottante, bord à bord avec la sélection, auto-resize)
- [ ] Rediriger "Summarize", "Translate", etc. vers cette vue au lieu du Chat global (laissant Chat global uniquement pour les discussions générales)
- [ ] Implémenter le `src/core/llm_worker.py` (QThread) pour libérer l'UI (Fix Bug 3.3 Freezing UI)
- [ ] Ajuster le behavior de "Summarize" pour éviter la confusion sur la sélection (UAT 6, ex: ajouter une indication visuelle de ce qui a été sélectionné)

### 🚀 Priorité 4 : Streaming Backend Complet (Historique Phase 3)

**Streaming Implementation (Partiellement DONE)**

- [x] Créer `src/core/llm_worker.py` (QThread)
- [~] Stream tokens via signal `sig_token_received(str)`
- [~] Token buffering (50ms window) pour perf UI
- [~] Cancellation support (stop button)
- [x] Error handling avec retry logic
- [~] Tests : streaming, cancellation, errors

**Additional Providers**

- [ ] Implémenter `src/core/openai_provider.py`
  - [ ] Endpoint /v1/chat/completions
  - [ ] API key auth
  - [ ] Vision support (gpt-4o)
- [ ] Implémenter `src/core/anthropic_provider.py`
  - [ ] Endpoint /v1/messages
  - [ ] x-api-key auth
  - [ ] Vision support (claude-3)
- [ ] Implémenter `src/core/openrouter_provider.py` (optionnel)
- [ ] Tests : tous providers avec mocks

**Markdown Rendering (DONE)**

- [x] Créer `src/utils/markdown_renderer.py`
- [x] Markdown → HTML avec extensions (fenced_code, tables)
- [x] Syntax highlighting avec Pygments
- [x] Styling CSS pour dark/light themes
- [x] Injection dans QTextEdit ou QWebEngineView (si size ok)
- [x] Tests : rendering, code blocks

---

## [TODO] Phase 4: Advanced Features (Semaine 4)

### F-05: Clipboard Management

- [ ] Créer `src/core/clipboard_manager.py`
- [ ] Get/Set text avec retry logic
- [ ] Get/Set image (QImage)
- [ ] Monitor clipboard changes (debounced 100ms)
- [ ] Format detection (text, HTML, image)
- [ ] Tests : retry, formats, monitoring

### F-06: Auto-Paste

- [ ] Créer `src/core/auto_paster.py`
- [ ] Capture active window handle (Win32 API via ctypes)
- [ ] Focus restoration
- [ ] Delay configurable (100ms default)
- [ ] Keyboard simulation (pynput.keyboard.Controller)
- [ ] Tests : focus restore, paste

### F-07: Screenshot Capture + Vision

- [ ] Créer `src/ui/screenshot_tool.py`
- [ ] Mode 1: Full screen capture
- [ ] Mode 2: Region selection (overlay UI)
- [ ] Mode 3: Active window capture
- [ ] Mode 4: Clipboard image detection
- [ ] Conversion image → base64
- [ ] Format adapté par provider (Anthropic vs OpenAI vs Ollama)
- [ ] Tests UI : overlay, capture

### F-09: History (SQLite)

- [ ] Créer `src/services/history_service.py`
- [ ] Schema DB : tables conversations + messages
- [ ] CRUD operations
- [ ] Full-text search
- [ ] Export JSON/Markdown
- [ ] Statistics (tokens, response times)
- [ ] Tests : CRUD, search, export

### F-12: Theme System

- [ ] Créer assets/styles/dark.qss
- [ ] Créer assets/styles/light.qss
- [ ] Créer `src/utils/theme_manager.py`
- [ ] Dynamic theme switching sans restart
- [ ] System theme detection (Windows)
- [ ] Apply QSS to all windows
- [ ] Tests : switch, apply

---

## [TODO] Phase 5: Polish & Package (Semaine 5)

### F-08: Toast Notifications

- [ ] Créer `src/ui/toast_notification.py`
- [ ] Custom QWidget (NOT Windows native)
- [ ] Position : bottom-right, stacking
- [ ] Animation : slide-in, fade-out
- [ ] Types : Info, Success, Warning, Error
- [ ] Auto-dismiss (3s default)
- [ ] Tests UI : stacking, animations

### Settings GUI Complete

- [ ] Créer `src/ui/settings_dialog.py` (QDialog avec tabs)
- [ ] Tab 1: Providers (add/edit/remove, test connection)
- [ ] Tab 2: Shortcuts (recorder, conflict detection)
- [ ] Tab 3: Appearance (theme, font, animations)
- [ ] Tab 4: Behavior (auto-paste, clipboard, notifications)
- [ ] Tab 5: Advanced (debug, network, performance)
- [ ] Save/Load via ConfigService
- [ ] Tests UI : validation, save/load

### Main Application Entry Point

- [ ] Créer `src/main.py`
- [ ] QApplication setup
- [ ] Startup : health checks → tray icon → input hooks
- [ ] Signal connections entre composants
- [ ] Cleanup on exit
- [ ] Exception handling global
- [ ] Tests : startup, cleanup

### Assets & Resources

- [ ] Créer icons/ (tray icons: ready/busy/error)
- [ ] Action icons (summarize, translate, screenshot, etc.)
- [ ] Default prompts JSON
- [ ] README.md avec screenshots

### Testing Complete

- [ ] Tests unitaires : core modules (> 80% coverage)
- [ ] Tests UI : pytest-qt pour widgets
- [ ] Tests integration : end-to-end workflows
- [ ] Performance tests : startup time, memory, streaming FPS
- [ ] Manual testing : Windows 10, Windows 11, multi-monitor

### Documentation

- [ ] SPEC.md finalisé (features détaillées)
- [ ] README.md (installation, quick start, screenshots)
- [ ] API documentation (docstrings Google style)
- [ ] User guide (comment utiliser, troubleshooting)

### Packaging & Distribution

- [ ] Build avec Nuitka (onefile, optimized)
  ```bash
  nuitka --standalone --onefile --windows-disable-console \
    --enable-plugin=pyside6 --output-dir=dist src/main.py
  ```
- [ ] Test exe sur clean Windows 10
- [ ] Test exe sur clean Windows 11
- [ ] Mesurer : taille (< 50MB), startup (< 2s), RAM (< 150MB)
- [ ] UPX compression si trop gros
- [ ] Créer installeur (Inno Setup) ou zip portable
- [ ] Release notes

---

## [TODO] Optimisations Performance

### Size Optimization

- [ ] Vérifier PySide6-Essentials utilisé (pas full PySide6)
- [ ] Exclude unused Qt modules
- [ ] Lazy imports pour modules optionnels
- [ ] Strip debug symbols en release
- [ ] UPX compression finale
- [ ] Target : < 50MB exe

### Speed Optimization

- [ ] Profile startup avec cProfile
- [ ] Lazy load providers non-default
- [ ] Cache config en mémoire
- [ ] Optimize QThread count
- [ ] Minimize imports dans main.py
- [ ] Target : < 2s cold startup

### Memory Optimization

- [ ] Limit chat history in-memory (last 50 messages)
- [ ] Weak references pour signals
- [ ] Cleanup closed windows
- [ ] Profile avec memory_profiler
- [ ] Target : < 150MB au repos

---

## [TODO] Future Enhancements (Post v1.0)

- [ ] F-22: Mouse Gesture Support
- [ ] F-23: Plugin System (custom actions)
- [ ] F-24: Portable Mode (config dans ./config)
- [ ] Multi-language UI (i18n)
- [ ] Voice input support
- [ ] Custom AI model fine-tuning
- [ ] Cloud sync for history/config
- [ ] Mobile companion app

---

## Notes de Mise à Jour

**Format pour updates :**

```
[YYYY-MM-DD] Phase X - Feature
- [x] Task completed : description résultat
- [!] Task blocked : raison du blocage
```

### Log

_Vide - À remplir au fur et à mesure de l'implémentation_

---

### Log

```
[2026-02-15] Phase 0 - Specification & Planning ✅ DONE
- [x] SPEC.md complète (24 features F-01 à F-20, architecture, config)
- [x] TODO.md tracking (5 phases, structure détaillée)
- [x] Plan complet (architecture, optimizations, packaging Nuitka)

[2026-02-15] Phase 1 - Foundation ✅ FULLY COMPLETED
- [x] Structure répertoires complète (src/core, src/ui, src/services, tests/)
- [x] Configuration files (requirements.txt, pyproject.toml, .gitignore, LICENSE)
- [x] F-03: LLM Provider abstraction (ABC + Factory + Ollama + OpenAI + Anthropic)
- [x] F-10: ConfigService (Singleton, JSON persistence, validation)
- [x] F-11: Health Checks (Config, LLM connectivity, Permissions)
- [x] PyTest Suite: 43 tests, 87% coverage, ALL PASSING ✅

Test Results:
  ✅ test_llm_provider.py : 18 tests passing (Ollama, OpenAI, Anthropic, Factory)
  ✅ test_config_service.py : 14 tests passing (Load, Save, Get, Set, Providers)
  ✅ test_health_check.py : 11 tests passing (Config, LLM, Permissions checks)
  📊 Coverage: 87% overall, 93% ConfigService, 89% LLMProvider abstraction

Code Quality:
  ✅ All imports working correctly
  ✅ Singleton pattern functioning properly
  ✅ Error handling comprehensive
  ✅ Mocking/patching working well
  ✅ No import errors or runtime issues

Documentation:
  ✅ README.md créé (modern, concis, avec badges)
  ✅ PHASE_1_REVIEW.md complète (test statistics, validation)
  ✅ VSCODE_TESTING_GUIDE.md détaillé
  ✅ QUICK_START_TESTS.md simple et rapide

[2026-02-15] Phase 2 - UI Core 🚧 IN PROGRESS
- [~] Task #6: Setup PySide6-Essentials + Qt infrastructure
- [~] Task #1: Implement F-01 Global Input Hooks
- [~] Task #2: Implement F-02 Floating Context Menu
- [~] Task #3: Implement F-04 Chat Streaming Window
- [~] Task #4: Implement F-13 Keyboard Shortcuts
- [~] Task #5: Implement F-14 System Tray Integration
- [~] Task #8: Create main.py entry point
- [~] Task #7: Phase 2 Integration Tests (> 80% coverage)
- [~] Task #9: Phase 2 Documentation & Review
```

**Dernière mise à jour** : 2026-02-15, 23:50
**Statut global** : ✅ Phase 1 COMPLETE | 🚧 Phase 2 STARTING
**Prochaine action** : 🚀 Démarrer implémentation Phase 2
