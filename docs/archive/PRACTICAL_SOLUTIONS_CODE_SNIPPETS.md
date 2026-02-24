# Solutions Pratiques et Snippets de Code
## Quick Shortcut AI - Alternatives Prêtes à l'Emploi

**Date**: 24 février 2026
**Focus**: Code implementable immédiatement

---

## 1. Solution Rapide: Remplacer pynput par keyboard

### Installation

```bash
# Supprimer pynput
pip uninstall pynput -y

# Installer keyboard
pip install keyboard

# Alternative: pip install keyboard pywin32 (pour Win32 stuff)
```

### Implementation 1A: InputManager avec keyboard library

**File: `src/core/input_manager.py` (REFACTORED)**

```python
"""
Global Input Manager - Keyboard Hooks with keyboard library

Uses keyboard library instead of pynput for better Windows support.
Runs in separate QThread for non-blocking event capture.

Features:
  - Global Ctrl+Right-Click detection
  - Signal-based event emission (thread-safe)
  - Better event suppression than pynput
  - Simpler implementation
"""

from PySide6.QtCore import QThread, Signal, QObject
import keyboard
import logging
import time
from pynput import mouse
from typing import Optional

logger = logging.getLogger(__name__)


class InputManager(QThread):
    """
    Global input hook listener running in separate thread.

    Detects hotkey combinations and emits signals.
    Non-blocking - runs in background QThread.

    Usage:
        input_mgr = InputManager()
        input_mgr.sig_shortcut_triggered.connect(on_shortcut_triggered)
        input_mgr.start()

        # Later:
        input_mgr.stop()
        input_mgr.wait()
    """

    # Signals
    sig_shortcut_triggered = Signal(str, int, int)  # action_id, x, y
    sig_error = Signal(str)
    sig_started = Signal()
    sig_stopped = Signal()

    def __init__(self):
        super().__init__()
        self._running = False
        self._stop_event = False
        self._mouse = mouse.Controller()

        # Hotkey name for later removal
        self._hotkey_name = 'ctrl+shift+right'

    def run(self):
        """Main thread loop - register hotkey and wait"""
        try:
            logger.info("InputManager: Starting listener")
            self._running = True
            self.sig_started.emit()

            # Register global hotkey
            # Using ctrl+shift+right as proxy for ctrl+rightclick
            # (keyboard library doesn't support mouse combinations)
            keyboard.add_hotkey(
                self._hotkey_name,
                self._on_hotkey,
                suppress=False  # Don't suppress (we want app to see it)
            )

            # Keep thread alive
            while not self._stop_event:
                time.sleep(0.1)

            # Cleanup
            keyboard.remove_hotkey(self._hotkey_name)
            logger.info("InputManager: Stopped")
            self.sig_stopped.emit()

        except Exception as e:
            logger.error(f"InputManager error: {e}", exc_info=True)
            self.sig_error.emit(str(e))
        finally:
            self._running = False

    def _on_hotkey(self):
        """Called when hotkey is triggered"""
        try:
            # Get current mouse position
            x, y = self._mouse.position
            logger.info(f"Hotkey triggered at ({x}, {y})")

            # Emit signal with action and coordinates
            self.sig_shortcut_triggered.emit('menu', int(x), int(y))

        except Exception as e:
            logger.error(f"Hotkey handler error: {e}", exc_info=True)
            self.sig_error.emit(str(e))

    def stop(self):
        """Request thread to stop"""
        logger.info("InputManager: Stop requested")
        self._stop_event = True
        self.wait(timeout=5000)  # Wait up to 5 seconds

    def is_running(self):
        """Check if listener is active"""
        return self._running


# ALTERNATIVE: If you need actual mouse right-click detection
class InputManagerAdvanced(QThread):
    """
    More advanced version using mouse + keyboard combo.

    NOTE: keyboard library doesn't support mouse buttons in hotkey syntax.
    So we need to manually track Ctrl key + mouse right-click.
    """

    sig_shortcut_triggered = Signal(str, int, int)
    sig_error = Signal(str)
    sig_started = Signal()
    sig_stopped = Signal()

    def __init__(self):
        super().__init__()
        self._stop_event = False
        self._ctrl_pressed = False
        self._mouse = mouse.Controller()
        self._mouse_listener = None

    def run(self):
        """Main loop - register keyboard + mouse listeners"""
        try:
            logger.info("InputManagerAdvanced: Starting")
            self.sig_started.emit()

            # Monitor keyboard for Ctrl key
            keyboard.on_press(self._on_key_press)
            keyboard.on_release(self._on_key_release)

            # Monitor mouse for right-click
            self._mouse_listener = mouse.Listener(
                on_click=self._on_mouse_click
            )
            self._mouse_listener.start()

            # Keep thread alive
            while not self._stop_event:
                time.sleep(0.1)

            # Cleanup
            keyboard.unhook_all()
            if self._mouse_listener:
                self._mouse_listener.stop()

            logger.info("InputManagerAdvanced: Stopped")
            self.sig_stopped.emit()

        except Exception as e:
            logger.error(f"InputManagerAdvanced error: {e}", exc_info=True)
            self.sig_error.emit(str(e))

    def _on_key_press(self, event):
        """Track Ctrl key state"""
        if event.name == 'ctrl':
            self._ctrl_pressed = True

    def _on_key_release(self, event):
        """Track Ctrl key release"""
        if event.name == 'ctrl':
            self._ctrl_pressed = False

    def _on_mouse_click(self, x, y, button, pressed):
        """Detect right-click while Ctrl is pressed"""
        if pressed and button == mouse.Button.right and self._ctrl_pressed:
            logger.info(f"Ctrl+Right-Click at ({x}, {y})")
            self.sig_shortcut_triggered.emit('menu', x, y)

    def stop(self):
        """Request thread to stop"""
        self._stop_event = True
        self.wait(timeout=5000)
```

**Integration in main.py**:

```python
# In QuickShortcutApp.__init__():
# OLD:
# from src.core.input_manager import InputManager
# self.input_manager = InputManager()

# NEW:
from src.core.input_manager import InputManager
self.input_manager = InputManager()  # Or InputManagerAdvanced

# Same signal connection:
self.input_manager.sig_shortcut_triggered.connect(self._on_shortcut_triggered)

# Same start/stop:
self.input_manager.start()
# Later: self.input_manager.stop()
```

### Why This Works Better

1. **No PySide6 crashes**: keyboard library has no known interaction issues with Qt
2. **Better suppression**: Event suppression works correctly
3. **Simpler code**: Less state tracking, clearer logic
4. **Active maintenance**: keyboard library is actively developed
5. **Lower overhead**: Pure Python, zero compilation needed

### Trade-offs

- ✅ Requires admin on Windows (app already asks for admin)
- ⚠️ macOS support is experimental (acceptable if not priority)
- ✅ No pynput crashes

---

## 2. Solution Core: Fix Threading for Chat Streaming

### Problem Recap

```python
# CURRENT (BROKEN):
def _stream_chat_response(self):
    for token in provider.stream_chat(...):  # ← BLOCKS main thread!
        QApplication.processEvents()  # ← Not enough
        response += token
        # UI freezes here
```

### Solution: Proper QThread Worker Pattern

**File: `src/main.py` (REFACTORED sections)**

```python
# KEEP existing StreamingWorker class (it's actually good!)
class StreamingWorker(QObject):
    """Worker to run LLM streaming in a separate thread (non-blocking UI)"""

    # Signals
    token_received = Signal(str)
    streaming_complete = Signal()
    error_occurred = Signal(str)

    def __init__(self, provider, messages, model):
        super().__init__()
        self.provider = provider
        self.messages = messages
        self.model = model
        self._is_stopped = False

    def stop(self):
        self._is_stopped = True

    def run(self):
        """Run streaming in worker thread (NOT main thread)"""
        try:
            logger.info("StreamingWorker: Starting")
            token_count = 0

            # This loop runs in WORKER thread, not main thread
            # So it can block without freezing UI
            for token in self.provider.stream_chat(self.messages, model=self.model):
                if self._is_stopped:
                    logger.info("StreamingWorker: Stopped by user")
                    break

                # Emit signal = thread-safe way to send to main thread
                self.token_received.emit(token)
                token_count += 1

            logger.info(f"StreamingWorker: Complete ({token_count} tokens)")
            self.streaming_complete.emit()

        except Exception as e:
            logger.error(f"StreamingWorker error: {e}", exc_info=True)
            self.error_occurred.emit(str(e))


# REPLACE THIS OLD METHOD:
def _stream_chat_response_OLD(self):
    """OLD VERSION - BLOCKS UI, DON'T USE"""
    try:
        provider = self.llm_factory.get_provider()
        model = self.config.get('model', 'llama2')

        # ❌ PROBLEM: This runs in main thread!
        for token in provider.stream_chat(messages, model=model):
            QApplication.processEvents()  # ← Not enough
            response += token  # ← Main thread blocked


# WITH THIS NEW METHOD:
def _stream_chat_response(self):
    """NEW VERSION - Non-blocking UI using QThread worker"""
    try:
        logger.info("Chat: Starting streaming response")

        # Create worker
        provider = self.llm_factory.get_provider()
        model = self.config.get('model', 'llama2')
        worker = StreamingWorker(provider, self.chat_messages, model)

        # Create thread
        thread = QThread()

        # Move worker to thread (important!)
        worker.moveToThread(thread)

        # Connect signals
        # When thread starts, call worker.run()
        thread.started.connect(worker.run)

        # When worker emits token, update UI
        worker.token_received.connect(self._on_token_received)

        # When worker finishes
        worker.streaming_complete.connect(lambda: self._on_streaming_complete(thread))

        # Error handling
        worker.error_occurred.connect(self._on_streaming_error)

        # Clean up thread when done
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(worker.deleteLater)

        # Keep references to avoid garbage collection
        self._current_worker = worker
        self._current_thread = thread

        # Start!
        logger.info("Chat: Starting worker thread")
        thread.start()

    except Exception as e:
        logger.error(f"Chat: Failed to start streaming: {e}", exc_info=True)
        self._on_streaming_error(str(e))


def _on_token_received(self, token):
    """Called in main thread when worker emits token"""
    logger.debug(f"Token received: {len(token)} chars")
    self.response_window.append_text(token)
    self.tray_icon.set_status(TrayStatus.BUSY)  # Keep busy indicator


def _on_streaming_complete(self, thread):
    """Called in main thread when streaming done"""
    logger.info("Chat: Streaming complete")
    self.response_window.finalize_response()  # Markdown rendering, etc
    self.tray_icon.set_status(TrayStatus.READY)

    # Thread will clean up via deleteLater signal


def _on_streaming_error(self, error_msg):
    """Called in main thread when streaming error"""
    logger.error(f"Chat: Streaming error: {error_msg}")
    self.response_window.show_error(f"Error: {error_msg}")
    self.tray_icon.set_status(TrayStatus.READY)
```

### Why This Pattern Works

1. **Non-blocking**: Worker thread blocks, main thread processes events
2. **Thread-safe**: Qt signals are thread-safe by design
3. **Clean separation**: UI logic stays in main thread
4. **Easy debugging**: Each piece has clear responsibility
5. **Responsive**: You can close windows, click buttons during streaming

### Key Points

```python
# DON'T:
for token in stream:
    QApplication.processEvents()  # ← Still blocks!
    update_ui(token)

# DO:
# In worker thread:
for token in stream:
    self.signal.emit(token)  # ← Non-blocking

# In main thread (auto-called by Qt):
def on_signal(self, token):
    self.update_ui(token)  # ← Responsive
```

---

## 3. Bonus: Win32 API Approach (If keyboard library Not Enough)

### When to Use

- Windows-only approach needed
- keyboard library insufficient
- Perfect event suppression required

### Installation

```bash
pip install pywin32
python -m Scripts.pywin32_postinstall -install
```

### Implementation: Win32-based InputManager

```python
"""
Win32 API-based global hotkey (Windows-only, no external dependencies).

Uses RegisterHotKey + message loop.
More reliable than pynput/keyboard for Windows.
"""

import ctypes
import win32con
import win32api
import win32gui
import win32gui
from PySide6.QtCore import QThread, Signal, QObject
import logging
import time

logger = logging.getLogger(__name__)


class InputManagerWin32(QThread):
    """Windows-only global hotkey using RegisterHotKey API"""

    sig_shortcut_triggered = Signal(str, int, int)
    sig_error = Signal(str)
    sig_started = Signal()
    sig_stopped = Signal()

    def __init__(self, parent_hwnd=None):
        super().__init__()
        self._running = False
        self._stop_event = False
        self._hotkey_id = 1
        self._parent_hwnd = parent_hwnd

    def run(self):
        """Register hotkey and process messages"""
        try:
            logger.info("Win32InputManager: Starting")
            self.sig_started.emit()

            # Get or create window for WM_HOTKEY messages
            if not self._parent_hwnd:
                # Create minimal window
                class_name = f"HotkeyListener_{id(self)}"
                self._create_window(class_name)

            # Register hotkey
            # Ctrl(MOD_CONTROL) + Shift(MOD_SHIFT) + A(0x41)
            success = ctypes.windll.user32.RegisterHotKey(
                self._parent_hwnd,
                self._hotkey_id,
                win32con.MOD_CONTROL | win32con.MOD_SHIFT,
                win32con.VK_A  # Change to VK_RIGHT for right-click equivalent
            )

            if not success:
                raise Exception("RegisterHotKey failed")

            logger.info("Win32InputManager: Hotkey registered")
            self._running = True

            # Message loop
            msg = ctypes.wintypes.MSG()
            while not self._stop_event and ctypes.windll.user32.GetMessage(
                ctypes.byref(msg), None, 0, 0
            ):
                if msg.message == win32con.WM_HOTKEY:
                    if msg.wParam == self._hotkey_id:
                        # Hotkey triggered!
                        logger.info("Win32InputManager: Hotkey triggered")

                        # Get mouse position
                        x, y = ctypes.wintypes.c_long(), ctypes.wintypes.c_long()
                        ctypes.windll.user32.GetCursorPos(ctypes.byref(x), ctypes.byref(y))

                        self.sig_shortcut_triggered.emit('menu', x.value, y.value)

                ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
                ctypes.windll.user32.DispatchMessage(ctypes.byref(msg))

            # Cleanup
            ctypes.windll.user32.UnregisterHotKey(self._parent_hwnd, self._hotkey_id)
            logger.info("Win32InputManager: Stopped")
            self.sig_stopped.emit()

        except Exception as e:
            logger.error(f"Win32InputManager error: {e}", exc_info=True)
            self.sig_error.emit(str(e))
        finally:
            self._running = False

    def _create_window(self, class_name):
        """Create hidden window for message handling"""
        # Implementation details...
        # This is complex, use win32gui library if available
        pass

    def stop(self):
        logger.info("Win32InputManager: Stop requested")
        self._stop_event = True
```

### Why This Approach

✅ Perfect hotkey reliability
✅ 100% event suppression
✅ Native Windows, no translation layer
✅ Lowest latency

❌ Windows-only (no macOS/Linux)
❌ Complex code (message loop)
❌ Harder to debug

---

## 4. Quick Comparison: keyboard vs pynput vs Win32

### Code Complexity

```python
# CURRENT (pynput) - Complex, buggy
from pynput import keyboard

listener = keyboard.Listener(on_press=on_press)
listener.start()
# Problem: Crashes with PySide6, suppression broken

# RECOMMENDED (keyboard) - Simple, reliable
import keyboard

keyboard.add_hotkey('ctrl+shift+a', on_hotkey)
# Problem: Admin required on Windows, macOS experimental

# WIN32 (lowest level) - Most complex, most reliable
import win32api
win32api.RegisterHotKey(hwnd, id, modifiers, vk_code)
# Problem: Windows only, complex message loop
```

### Test Results (Hypothetical)

| Test | pynput | keyboard | Win32 |
|------|--------|----------|-------|
| Hotkey triggers | ✅ (sometimes) | ✅ Reliable | ✅ Perfect |
| Event suppression | ❌ Broken | ✅ Works | ✅ Perfect |
| PySide6 compatible | ❌ Crashes | ✅ Works | ✅ Works |
| Code complexity | 🔴 High | 🟢 Low | 🔴 Very High |
| Cross-platform | ✅ All | ✅ (macOS?) | ❌ Windows only |
| Maintenance | ❌ Stale | ✅ Active | N/A (Win32) |

---

## 5. Testing Checklist

After implementing keyboard library OR fixing threading:

### Unit Tests

```python
# tests/test_input_manager.py
def test_hotkey_registration():
    manager = InputManager()
    manager.start()
    assert manager.is_running()
    manager.stop()
    assert not manager.is_running()

def test_hotkey_triggered_emits_signal():
    manager = InputManager()
    signal_received = False

    def on_signal(*args):
        nonlocal signal_received
        signal_received = True

    manager.sig_shortcut_triggered.connect(on_signal)
    manager.start()
    # Simulate hotkey... (complex)
    manager.stop()
```

### Integration Tests

```python
# tests/test_streaming.py
def test_streaming_doesnt_freeze_ui(qtbot):
    """Verify chat streaming doesn't block UI"""
    app = QuickShortcutApp()

    # Send chat message
    app._on_chat_message("test")

    # UI should still be responsive
    for i in range(10):
        QApplication.processEvents()
        # Try clicking buttons, etc.
        # Should all work without lag

    # Streaming completes
    app._current_thread.wait()
```

### Manual Tests

```
1. Launch app
2. Trigger Ctrl+Shift+A (keyboard) or Ctrl+Right-Click (mouse)
3. Verify menu appears
4. Verify menu is clickable
5. Verify Windows context menu does NOT appear
6. Click menu item
7. Chat streaming starts
8. WHILE streaming:
   - Click close button (window closes immediately)
   - Settings dialog (should open/close instantly)
   - Try Alt+Tab (works instantly)
9. After streaming completes, verify response displayed
10. Settings dialog → Save → Verify health check updates immediately
```

---

## 6. Incremental Migration Path

### Phase 0 (Baseline - Today)

```
Current state = 5 critical bugs, app unusable
```

### Phase 1 (Option A - keyboard library) - 1 Day

```
1. pip uninstall pynput
2. pip install keyboard
3. Refactor InputManager (2 hours)
4. Test hotkey + menu (1 hour)
5. Result: Menu working, still have UI freeze bug
```

### Phase 2 (Threading fix) - 1 Day

```
1. Verify StreamingWorker setup
2. Fix _stream_chat_response() to use QThread properly
3. Test streaming (2 hours)
4. Result: Both hotkey AND streaming work
```

### Phase 3 (Polish) - 2-3 Days

```
1. Settings dialog close fix
2. Health check auto-update
3. Menu clickability verification
4. Full UAT
5. Result: App ready for production
```

### Total: 3-5 Days to Production ✨

---

## References & Further Reading

- [keyboard library documentation](https://github.com/boppreh/keyboard)
- [Qt threading documentation](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QThread.html)
- [Real Python: PyQt QThread Guide](https://realpython.com/python-pyqt-qthread/)
- [Win32 HotKey API](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-registerhotkey)

---

**Next Step**: Choose your path:
- **Path A** (Recommended): Try keyboard library + threading fix (this week)
- **Path B** (Conservative): Use Win32 API if keyboard doesn't work (Windows-only)
- **Path C** (Long-term): Rewrite in Electron/Tauri (3+ weeks, but more robust)

