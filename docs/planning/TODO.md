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

## [IN PROGRESS] Phase 2: UI Core (Semaine 3) 🚧

### Infrastructure Setup
- [~] Setup PySide6-Essentials + Qt plugins (Task #6)
- [~] Create main.py entry point (Task #8)
- [ ] Configure pytest-qt for UI testing

### F-01: Global Input Hooks ✅
- [~] Créer `src/core/input_manager.py` (Task #1)
- [~] Capture Ctrl+Right-Click globally
- [~] QThread for non-blocking hook listening
- [~] Signal-based event emission (thread-safe)
- [~] Tests: positioning, event filtering, signals

### F-02: Floating Menu (Context Menu) ✅
- [~] Créer `src/ui/floating_menu.py` (Task #2)
- [~] QWidget frameless (Qt.FramelessWindowHint, Qt.Tool)
- [~] Design : rounded corners (8px), shadow, fade-in 200ms
- [~] Layout : icon + text rows, separators
- [~] Actions : Summarize, Translate, Custom Prompt, Screenshot, Chat
- [~] Keyboard navigation (arrows, Enter, Esc)
- [~] Smart positioning (cursor, edge detection, multi-monitor)
- [~] Signal `sig_action_selected(action_id: str)`
- [~] Tests UI : positioning, keyboard nav, animations

### F-04: Response Window (Chat Streaming) ✅
- [~] Créer `src/ui/response_window.py` (Task #3)
- [~] Singleton pattern ou instance tracking
- [~] QTextEdit read-only pour chat area
- [~] Auto-scroll avec détection user scroll
- [~] Créer `src/ui/widgets/auto_expanding_text.py` (input area)
  - [~] Min 40px, max 200px
  - [~] Auto-expand on textChanged
- [~] Toolbar : Stop, Copy, Settings buttons
- [~] Status bar : provider + model info
- [~] Token buffering (50ms) pour smooth streaming
- [~] Tests UI : singleton, scroll, resize, streaming

### F-13: Keyboard Shortcuts ✅
- [~] Créer `src/core/shortcut_manager.py` (Task #4)
- [~] Enregistrement raccourcis globaux
- [~] Détection conflits
- [~] Defaults : Ctrl+Right Click, Ctrl+Shift+S, Esc, Ctrl+W
- [~] Customization via Settings
- [~] Persistence in config.json
- [~] Tests : conflict detection, registration

### F-14: System Tray Integration ✅
- [~] Créer `src/ui/tray_icon.py` (Task #5)
- [~] QSystemTrayIcon avec menu
- [~] États : Ready (vert), Busy (jaune), Error (rouge)
- [~] Menu : Quick Actions, Settings, Exit
- [~] Tooltip avec status
- [~] Notification fallback si toasts fail
- [~] Tests : state changes, menu actions

### Testing & Documentation
- [~] Phase 2 Tests: > 80% coverage (Task #7)
- [~] Phase 2 Documentation & Review (Task #9)

---

## [TODO] Phase 3: LLM Integration & Streaming (Semaine 3-4)

### Streaming Implementation
- [ ] Créer `src/core/llm_worker.py` (QThread)
- [ ] Stream tokens via signal `sig_token_received(str)`
- [ ] Token buffering (50ms window) pour perf UI
- [ ] Cancellation support (stop button)
- [ ] Error handling avec retry logic
- [ ] Tests : streaming, cancellation, errors

### Additional Providers
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

### Markdown Rendering
- [ ] Créer `src/utils/markdown_renderer.py`
- [ ] Markdown → HTML avec extensions (fenced_code, tables)
- [ ] Syntax highlighting avec Pygments
- [ ] Styling CSS pour dark/light themes
- [ ] Injection dans QTextEdit ou QWebEngineView (si size ok)
- [ ] Tests : rendering, code blocks

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
