# Phase 2: UI Core - Implementation Plan 🚧

**Status**: Ready to Start
**Date Started**: 2026-02-15
**Target Completion**: End of Week (5 working days)

---

## 📋 Overview

Phase 2 focuses on building the **user-facing UI components** that integrate with the solid Phase 1 foundation:

| Feature | ID | Status | Priority |
|---------|-----|--------|----------|
| Global Input Hooks | F-01 | 🚧 | P0 |
| Floating Context Menu | F-02 | 🚧 | P0 |
| Chat Streaming Window | F-04 | 🚧 | P0 |
| Keyboard Shortcuts | F-13 | 🚧 | P1 |
| System Tray Icon | F-14 | 🚧 | P1 |
| Main Application | - | 🚧 | P0 |

---

## 🛠️ Prerequisites Before Starting

### ✅ Phase 1 Complete
- [x] LLM Provider abstraction (Phase 1)
- [x] ConfigService with JSON persistence (Phase 1)
- [x] Health checks framework (Phase 1)
- [x] 43 tests passing with 87% coverage

### ✅ Environment Ready
- [x] Python venv setup and active
- [x] requirements.txt with Phase 1 deps
- [x] pytest + pytest-cov working
- [x] VS Code configured for testing

### 🚧 Before Phase 2 Code Starts

**Task #6: Setup PySide6-Essentials**
```bash
# 1. Add to requirements.txt
echo "PySide6-Essentials>=6.5.0" >> requirements.txt

# 2. Install in venv
pip install PySide6-Essentials>=6.5.0

# 3. Verify Qt imports work
python -c "from PySide6.QtWidgets import QApplication; print('✅ Qt working')"

# 4. Install pytest-qt for UI testing
pip install pytest-qt>=4.2
```

---

## 📦 Task Breakdown

### **Priority P0 (Critical Path)**

#### Task #1: Global Input Hooks (F-01)
**File**: `src/core/input_manager.py`

**What**: Capture Ctrl+Right-Click globally anywhere on Windows

**Implementation**:
```python
class InputManager(QThread):
    sig_action_triggered = Signal(str, int, int)  # action, x, y

    def __init__(self):
        super().__init__()
        self.listener = None

    def run(self):
        """Run in separate thread - listen for hooks"""
        # Use pynput to listen for Ctrl+Right-Click
        # Emit signal to main thread when triggered

    def stop(self):
        """Gracefully stop listener"""
```

**Tests**:
- [ ] Hook captures event correctly
- [ ] Signal emitted to main thread
- [ ] Latency < 50ms
- [ ] Can stop listening cleanly
- [ ] Works with multiple monitors

**Acceptance**: Ctrl+Right-Click registered and emits signal

---

#### Task #2: Floating Context Menu (F-02)
**File**: `src/ui/floating_menu.py`

**What**: Modern frameless menu that appears at cursor position

**Implementation**:
```python
class FloatingMenu(QWidget):
    sig_action_selected = Signal(str)  # "summarize", "translate", etc

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def show_at_cursor(self):
        """Show menu at cursor position with animation"""

    def handle_keyboard(self, event: QKeyEvent):
        """Navigate with arrow keys"""

    def position_smart(self, pos: QPoint):
        """Avoid going off-screen (multi-monitor aware)"""
```

**Design**:
- Rounded corners: 8px border-radius
- Shadow: QGraphicsDropShadowEffect
- Animation: QPropertyAnimation (fade-in 200ms)
- Colors: Dark theme (#1a1a1a) with accent (#0066ff)

**Tests**:
- [ ] Menu appears at cursor
- [ ] Keyboard navigation works
- [ ] Smart positioning (no off-screen)
- [ ] Animation smooth
- [ ] Actions emitted correctly

**Acceptance**: User presses Ctrl+Right-Click → menu appears < 100ms

---

#### Task #3: Chat Streaming Window (F-04)
**File**: `src/ui/response_window.py` + `src/ui/widgets/auto_expanding_text.py`

**What**: Singleton window showing streamed LLM responses

**Implementation**:
```python
class ResponseWindow(QMainWindow):
    _instance = None
    sig_stop_requested = Signal()

    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def stream_response(self, tokens: Iterator[str]):
        """Buffer tokens (50ms window) then update display"""

    def on_user_scroll(self):
        """Detect if user scrolled - stop auto-scroll"""
```

**Components**:
- Chat display: QTextEdit (read-only) with markdown
- Input area: AutoExpandingText (40px min, 200px max)
- Toolbar: Stop, Copy, Settings buttons
- Status: Provider name + model name

**Tests**:
- [ ] Singleton works (same instance reused)
- [ ] Streaming smooth (token buffering)
- [ ] Auto-scroll works (with user override)
- [ ] Input expands correctly
- [ ] Stop button cancels streaming

**Acceptance**: Real-time streaming appears smooth without lag

---

#### Task #8: Main Application (main.py)
**File**: `src/main.py`

**What**: Entry point orchestrating all components

**Implementation**:
```python
class QuickShortcutApp(QApplication):
    def __init__(self):
        super().__init__()
        self.config = ConfigService()
        self.health = HealthCheckManager()
        self.input_mgr = InputManager()
        self.menu = FloatingMenu()
        self.chat = ResponseWindow()
        self.tray = TrayIcon()

    def startup(self):
        """Run health checks → setup UI → start listening"""

    def connect_signals(self):
        """Connect all component signals/slots"""

if __name__ == "__main__":
    app = QuickShortcutApp()
    sys.exit(app.exec())
```

**Tests**:
- [ ] App starts without errors
- [ ] Health checks run
- [ ] Components initialized
- [ ] Signals connected properly
- [ ] Graceful shutdown

**Acceptance**: `python src/main.py` runs without errors

---

### **Priority P1 (Important)**

#### Task #4: Keyboard Shortcuts (F-13)
**File**: `src/core/shortcut_manager.py`

**Defaults**:
- `Ctrl+Right-Click` → Show menu
- `Ctrl+Shift+S` → Screenshot
- `Esc` → Close menu/window
- `Ctrl+W` → Close chat window

#### Task #5: System Tray (F-14)
**File**: `src/ui/tray_icon.py`

**Status Indicators**:
- 🟢 Green: Ready
- 🟡 Yellow: Processing
- 🔴 Red: Error

---

## 📊 Task Dependencies

```
Phase 1 Complete ✅
        ↓
Task #6: Setup Qt ─────┐
        ↓              ↓
Task #1: Hooks ──────┬─→ Task #8: main.py
        ↓            │
Task #2: Menu ───────┤
        ↓            │
Task #3: Chat ───────┤
        ↓            │
Task #4: Shortcuts ──┤
        ↓            │
Task #5: Tray ───────┴─→ Task #7: Tests
        ↓
Task #9: Documentation
```

**Execution Order**:
1. Task #6 (Setup) - must be first
2. Task #1, #2, #3, #4, #5 - can be parallel after setup
3. Task #8 (main.py) - after components exist
4. Task #7 (Tests) - throughout, finalize after components
5. Task #9 (Docs) - last

---

## ✅ Completion Criteria

### Code Quality
- [ ] All Phase 2 modules have docstrings
- [ ] Type hints on public methods
- [ ] No import errors
- [ ] Black formatted + ruff clean

### Testing
- [ ] > 80% code coverage for Phase 2 modules
- [ ] All tests passing
- [ ] Tests for normal paths + error paths + edge cases
- [ ] Integration tests between components

### Performance
- [ ] Menu appears < 100ms after trigger
- [ ] Streaming smooth (60 FPS target)
- [ ] App startup < 3 seconds
- [ ] No UI freezes during operations

### Documentation
- [ ] README.md updated with Phase 2 features
- [ ] SPEC.md matches implementation
- [ ] PHASE_2_REVIEW.md created
- [ ] User guide for Phase 2 features

---

## 🚀 Getting Started

### Step 1: Setup Qt
```bash
# Activate venv
.\venv\Scripts\activate

# Install PySide6-Essentials
pip install PySide6-Essentials>=6.5.0 pytest-qt>=4.2

# Verify
python -c "from PySide6.QtWidgets import QApplication; print('✅')"
```

### Step 2: Create Qt Application Structure
```bash
mkdir -p src/ui/widgets
touch src/ui/__init__.py
touch src/ui/floating_menu.py
touch src/ui/response_window.py
touch src/ui/widgets/__init__.py
touch src/ui/widgets/auto_expanding_text.py
```

### Step 3: Start Task #1 (Hooks)
```bash
# Read documentation in SPEC.md for F-01
# Implement src/core/input_manager.py
# Create tests/test_ui/test_input_manager.py
```

### Step 4: Run Tests
```bash
# Test Task #1 implementation
pytest tests/test_ui/test_input_manager.py -v

# Check overall coverage
pytest tests/ -v --cov=src
```

---

## 📝 Daily Checklist

Each day before working:

- [ ] Venv activated: `.\venv\Scripts\activate`
- [ ] Tests passing: `pytest tests/ -v`
- [ ] Coverage OK: `--cov=src` shows > 80%
- [ ] No import errors: Each file imports clean
- [ ] Documentation updated

---

## 🎯 Next Steps After Phase 2

Once Phase 2 complete:
- **Phase 3**: Streaming, Markdown rendering, Additional providers
- **Phase 4**: Advanced features (clipboard, screenshot, history)
- **Phase 5**: Polish, packaging, release

---

**Ready to start Phase 2? Let's go! 🚀**
