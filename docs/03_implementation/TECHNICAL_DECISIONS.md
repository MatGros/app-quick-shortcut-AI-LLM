# ⚙️ Technical Decisions & Architecture

This document captures **key architectural and technical decisions** made during implementation of the Quick Shortcut AI LLM Assistant.

---

## 1. Framework Choice: PySide6 over PyQt5

**Decision**: Use **PySide6-Essentials** (Qt GUI framework)

**Rationale**:
- **Official Qt bindings** - Maintained by Qt Company (stable)
- **Modern API** - PySide6 has updated bindings vs PyQt5
- **Lighter weight** - Using Essentials only (~50MB vs full ~150MB)
- **Performance** - Native compilation possible with Nuitka

**Trade-offs**:
- Learning curve for Qt signals/slots
- Larger dependency than Tkinter (but modern UI worth it)

**Alternative considered**: PyQt5 (older, less maintained), Tkinter (too limited for modern UI)

---

## 2. Global Keyboard Hooks: pynput Library

**Decision**: Use **pynput** for keyboard/mouse hooks

**Rationale**:
- **Cross-platform capable** - Windows/Mac/Linux support
- **Well-maintained** - Active development and community
- **No admin rights needed** for basic hooks
- **Lightweight** - Single dependency, minimal overhead

**Implementation**:
- Hooks run in dedicated QThread (non-blocking)
- Trigger: Ctrl + Right-Click (release event)
- Latency target: < 100ms from action to menu display

**Alternative considered**: Win32 API directly (more complex, Windows-only)

---

## 3. LLM Provider Architecture: Factory Pattern + Abstract Base Class

**Decision**: **Abstract base class (ABC)** with **Factory pattern**

```python
class LLMProvider(ABC):
    @abstractmethod
    def stream_chat(...) -> Iterator[str]: ...
    @abstractmethod
    def get_models(...) -> List[str]: ...
    @abstractmethod
    def health_check(...) -> bool: ...

class OllamaProvider(LLMProvider): ...
class OpenAIProvider(LLMProvider): ...
class AnthropicProvider(LLMProvider): ...

class LLMFactory:
    @staticmethod
    def create(provider_type: str) -> LLMProvider: ...
```

**Rationale**:
- **Pluggable providers** - Easy to add new LLM services
- **Testable** - Mock providers for unit tests
- **Unified interface** - Code doesn't care which provider (Ollama/OpenAI/Anthropic)
- **Failover possible** - Switch providers if one fails

**Supported providers**:
- ✅ Ollama (local, no API key)
- ✅ OpenAI (GPT-4o, GPT-4 Turbo)
- ✅ Anthropic (Claude 3 series)
- ⏳ OpenRouter (planned)

---

## 4. Configuration Management: Singleton Pattern

**Decision**: **Singleton ConfigService** with JSON persistence

**Rationale**:
- **Single source of truth** - One config object across app
- **JSON format** - Human readable, no binary dependencies
- **Location**: `%APPDATA%\QuickShortcutAI\config.json`
- **Validation** - Schema validation on load

**Config structure**:
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

**Alternative considered**: SQLite (over-engineered), .env files (less user-friendly)

---

## 5. Chat Streaming: Token-by-Token with Buffering

**Decision**: **Collect tokens into 50ms windows** before UI update

**Rationale**:
- **Smooth UX** - Don't update UI 50+ times per second (wasted redraws)
- **CPU efficient** - Batch processing reduces overhead
- **60 FPS target** - Streaming renders smoothly (not jerky)
- **Thread safety** - QTimer ensures main thread updates

**Implementation**:
```python
def stream_response():
    token_buffer = []
    buffer_timer = QTimer()

    def on_token(token: str):
        token_buffer.append(token)

    def flush_buffer():
        if token_buffer:
            text = "".join(token_buffer)
            display_widget.append(text)
            token_buffer.clear()

    buffer_timer.timeout.connect(flush_buffer)
    buffer_timer.start(50)  # 50ms window
```

**Alternative considered**: Update per token (CPU intensive), update per sentence (choppy)

---

## 6. Markdown Rendering: markdown + Pygments

**Decision**: **markdown library** + **Pygments** for syntax highlighting

**Rationale**:
- **LLM responses often include code** - Syntax highlighting improves readability
- **Simple rendering** - Convert to HTML and display in QTextEdit
- **Performance** - Fast processing, minimal latency
- **Customizable** - Can theme colors per language

**Features**:
- ✅ Bold, italic, links
- ✅ Code blocks with language-specific highlighting
- ✅ Lists, tables, blockquotes
- ✅ Dark/light theme support

**Alternative considered**: Qt Markdown extensions (limited), raw text (unreadable for code)

---

## 7. UI Thread Protection: QThread Workers

**Decision**: **All I/O in QThread**, signals/slots for communication

**Rationale**:
- **No UI freezing** - Long operations (API calls, file I/O) in separate thread
- **Thread-safe signals** - Qt handles thread marshalling automatically
- **Responsive UI** - User can cancel/interact while operations run
- **Standard Qt pattern** - Proven, well-documented approach

**Pattern**:
```python
class LLMWorker(QThread):
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def run(self):
        try:
            response = llm.stream_chat(...)  # Blocking, but in separate thread
            self.response_ready.emit(response)
        except Exception as e:
            self.error_occurred.emit(str(e))

# Main thread:
worker = LLMWorker()
worker.response_ready.connect(ui_widget.display_response)
worker.error_occurred.connect(ui_widget.show_error)
worker.start()
```

---

## 8. Auto-Paste: Win32 API for Window Focus

**Decision**: Use **ctypes + Win32 API** to capture/restore window focus

**Rationale**:
- **Precise control** - Get exact window handle before paste
- **No external dependencies** - ctypes is built-in to Python
- **Reliable** - Proven Win32 approach, used in many automation tools
- **Configurable delay** - User can set pause before paste

**Implementation**:
```python
import ctypes
import time

def paste_to_active_window(text: str, delay_ms: int = 100):
    # Get current window
    hwnd = ctypes.windll.user32.GetForegroundWindow()

    # Put text in clipboard
    copy_to_clipboard(text)

    # Wait and restore focus
    time.sleep(delay_ms / 1000)
    ctypes.windll.user32.SetForegroundWindow(hwnd)

    # Simulate Ctrl+V
    keyboard.press_and_release('ctrl+v')
```

---

## 9. Testing Strategy: pytest + pytest-qt

**Decision**: **pytest** for unit tests, **pytest-qt** for UI tests

**Metrics**:
- ✅ **365 tests passing** (Phase 3 integration tests complete)
- ✅ **89% code coverage** (core modules > 85%)
- ✅ **Unit tests** - Every major component tested
- ✅ **Integration tests** - Real LLM calls, streaming, markdown rendering

**Test organization**:
```
tests/
├── test_core/
│   ├── test_llm_provider.py
│   ├── test_config_service.py
│   └── test_ollama_provider.py
├── test_ui/
│   ├── test_floating_menu.py
│   ├── test_response_window.py
│   └── test_settings_dialog.py
└── test_services/
    ├── test_clipboard_manager.py
    └── test_health_check.py
```

**Alternative considered**: unittest (verbose), nose (abandoned project)

---

## 10. Packaging Strategy: Nuitka over PyInstaller

**Decision**: **Nuitka** for compilation to native executable

**Rationale**:
- **Faster execution** - Compiled to C++, 20-40% performance gain
- **Smaller size** - Better optimization, dead code elimination
- **Faster startup** - < 2 seconds (vs 3-5s with PyInstaller)
- **Future-proof** - Better for performance-critical apps

**Build command**:
```bash
python -m nuitka --standalone --onefile \
  --windows-disable-console \
  --windows-icon-from-ico=assets/icon.ico \
  --enable-plugin=pyside6 \
  --output-dir=dist \
  src/main.py
```

**Targets**:
- Exe size: < 50MB (with PySide6-Essentials)
- Startup: < 2 seconds
- Memory idle: < 150MB

**Alternative considered**: PyInstaller (simpler but slower/larger)

---

## 11. File Structure: src/ + tests/ Separation

**Decision**: Clear separation - **src/** for application, **tests/** for tests

**Structure**:
```
src/
├── core/              # Business logic
│   ├── llm_provider.py
│   ├── config_service.py
│   └── ollama_provider.py
├── ui/                # PySide6 widgets
│   ├── floating_menu.py
│   ├── response_window.py
│   └── settings_dialog.py
├── services/          # Background tasks
│   ├── clipboard_manager.py
│   └── health_check.py
├── utils/             # Helper functions
│   ├── win32_helpers.py
│   └── markdown_renderer.py
└── main.py            # Application entry point

tests/
├── test_core/
├── test_ui/
└── test_services/
```

**Rationale**:
- **Clear boundaries** - Testing doesn't mix with application code
- **Easier distribution** - Include only src/ in final exe
- **Maintainability** - Easy to find code vs tests
- **Standard convention** - Follows Python best practices

---

## 12. Phase 3 Critical Issues (Known Limitations)

**Current blockers** (being fixed):

1. **Settings dialog closes app** - Window lifecycle issue in PySide6
2. **Chat freezes during streaming** - Need better thread synchronization
3. **Tray icon stays red** - Status update not triggering properly
4. **Menu items unclickable** - Event propagation issue with frameless menu
5. **Windows context menu visible** - Need to suppress system menu

**Status**: Fixes in progress (Tasks 3.1-3.5)

---

## 13. Code Style & Quality

**Standards**:
- **Formatter**: `black` (auto-formatted)
- **Linter**: `ruff` (strict PEP 8 compliance)
- **Type hints**: Required for function signatures
- **Docstrings**: Google style, required for all classes/methods

**CI/CD**:
- Pre-commit hooks check formatting
- All tests must pass before merge
- Coverage > 85% required

---

## Future Considerations (Phase 4+)

- [ ] **History SQLite** - Persistent conversation storage
- [ ] **Toast notifications** - Custom toast widget (not system)
- [ ] **Dark/Light themes** - QSS stylesheets
- [ ] **Vision API support** - Screenshot + LLM analysis
- [ ] **Custom prompts** - User-defined prompt templates
- [ ] **Rate limiting** - Throttle API calls per provider

---

**Last Updated**: 2026-02-17 (Phase 3 - Code Complete)
**Next Review**: When fixing critical UI bugs (Phase 3 Tasks 3.1-3.5)
