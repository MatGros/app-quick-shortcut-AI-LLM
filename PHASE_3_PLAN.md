# Phase 3 Plan - LLM Integration & Streaming
**Status**: PLANNING
**Target Duration**: 3-4 sessions (intensive)
**Start Date**: 2026-02-15
**Goal**: Replace simulated responses with real LLM streaming + Markdown rendering

---

## Overview

Phase 2 completed the **UI layer** with all components in place. Phase 3 adds the **LLM layer** - real API calls, streaming, and content rendering.

### What Works (from Phase 2)
✅ Global input hooks (Ctrl+Right-Click)
✅ Floating menu (6 actions with selection)
✅ Response window (singleton, token buffering ready)
✅ Shortcuts management system
✅ System tray with status indicators
✅ Main app orchestration

### What's Missing (Phase 3)
- Real LLM API calls (not simulated)
- Clipboard content capture (text + images)
- Markdown rendering in response window
- Vision API integration
- Settings dialog for provider configuration
- Auto-paste responses to active window

---

## Phase 3 Tasks

### Task #1: Real LLM Integration (Priority: CRITICAL)
**Duration**: 1.5-2 hours
**Files to Modify**:
- `src/core/ollama_provider.py` - Already has stream_chat(), verify works with real endpoint
- `src/main.py` - Replace _simulate_response() with real calls
- `src/ui/response_window.py` - Handle real token streaming (already supports it)

**What to Do**:
1. Test OllamaProvider.stream_chat() with real Ollama instance
   - Start local Ollama on localhost:11434
   - Test with llama2 or mistral model
   - Verify token streaming works
   - Measure latency to first token

2. Replace `_simulate_response()` in main.py:
   ```python
   # OLD:
   for token in response.split():
       self.response_window.append_token(token + " ")

   # NEW:
   provider = self.config.get_default_provider()
   for token in provider.stream_chat(clipboard_content, action_id):
       self.response_window.append_token(token)
   ```

3. Add error handling:
   - Provider not available → show toast "Ollama not running"
   - Clipboard empty → show warning
   - Streaming timeout → stop and show error

4. Test with real responses (100+ tokens) - verify:
   - Token buffering still smooth
   - No memory leaks
   - Scrolling responsive

**Tests to Create**:
- Integration test: real Ollama call (if available)
- Timeout test: mock slow provider
- Large response test: 1000+ tokens

---

### Task #2: Clipboard Integration (Priority: HIGH)
**Duration**: 1 hour
**Files to Create**:
- `src/core/clipboard_manager.py` - Text + image clipboard access

**What to Do**:
1. Create ClipboardManager class:
   ```python
   class ClipboardManager:
       def get_text() -> str
       def get_image() -> Optional[bytes]  # PNG bytes
       def set_text(text: str) -> bool
       def set_rich_text(html: str) -> bool
   ```

2. Implement thread-safe clipboard access:
   - Use QApplication.clipboard()
   - Retry logic for concurrent access (100ms timeout)
   - Handle Unicode/RTL text properly

3. Integrate with main.py:
   - On "summarize": `text = clipboard_mgr.get_text()`
   - Send to LLM provider instead of hardcoded text

4. Tests:
   - Read/write text
   - Read/write with special chars (emoji, RTL)
   - Concurrent access handling

---

### Task #3: Markdown Rendering (Priority: HIGH)
**Duration**: 2 hours
**Files to Modify**:
- `src/ui/response_window.py` - Add markdown → HTML rendering
- Possibly create: `src/ui/widgets/markdown_editor.py`

**What to Do**:
1. Add markdown rendering to ResponseWindow:
   ```python
   from markdown import markdown
   from pygments.formatters import HtmlFormatter

   # In response_window, convert response text to HTML:
   html = markdown(response_text, extensions=['fenced_code', 'tables'])
   ```

2. Syntax highlighting for code blocks:
   - Use Pygments for language detection
   - Add CSS styling for dark/light mode
   - Test with Python, JavaScript, SQL, bash blocks

3. Update response display:
   - Keep QTextEdit but set as read-only rich text
   - Or migrate to QTextBrowser if needed
   - Verify scrolling still smooth with HTML

4. Tests:
   - Markdown headers, bold, italic, links
   - Code blocks with language detection
   - Tables, lists, blockquotes
   - Mixed content (text + code + lists)

**Example Response Display**:
```
# Summary
This is **bold** and *italic*

## Key Points
- Point 1
- Point 2

## Code Example
```python
def hello():
    print("world")
```
```

---

### Task #4: Settings Dialog (Priority: MEDIUM)
**Duration**: 1.5 hours
**Files to Create**:
- `src/ui/settings_dialog.py`

**What to Do**:
1. Create QDialog with tabs:
   - **Providers Tab**: Select active provider, test connection
   - **Shortcuts Tab**: View/edit keyboard shortcuts
   - **Appearance Tab**: Dark/light theme toggle
   - **About Tab**: Version, links

2. Providers Tab Implementation:
   - ComboBox listing: Ollama (local), OpenAI, Anthropic, OpenRouter
   - For each: URL input field, API key input (password field)
   - "Test Connection" button → calls provider.health_check()
   - Shows: ✅ Connected or ❌ Failed with error

3. Shortcuts Tab:
   - List current shortcuts (Ctrl+Right, Ctrl+Shift+S, etc.)
   - Button to record new shortcut: "Click to record..."
   - Shows conflicts if any (red background)
   - "Restore Defaults" button

4. Theme Tab:
   - Radio buttons: Dark / Light / System
   - Preview of current theme
   - Apply immediately without restart

5. Integration with main.py:
   - Open from tray menu: "Settings" action
   - Settings saved to config.json
   - Changes applied immediately

**Tests**:
- Dialog initialization
- Provider validation
- Theme switching
- Shortcut editing

---

### Task #5: Auto-Paste (Priority: MEDIUM)
**Duration**: 1.5 hours
**Files to Create**:
- `src/core/auto_paster.py`

**What to Do**:
1. Create AutoPaster class:
   ```python
   class AutoPaster:
       def paste_to_active_window(text: str) -> bool
       # Uses Win32 API to:
       # 1. Get current foreground window
       # 2. Paste text using keyboard simulation
       # 3. Restore original window focus
   ```

2. Implementation:
   - Get active window handle using ctypes/Win32
   - Simulate Ctrl+V after copying to clipboard
   - Add delay (100-200ms) for window to be ready
   - Restore focus to original window

3. Add to response window:
   - "Paste to Active Window" button
   - Copies response to clipboard
   - Pastes into focused app
   - Shows success/failure notification

4. Tests:
   - Window focus restoration
   - Paste into different apps (Notepad, Word, browser)
   - Special characters handling

---

### Task #6: Vision API Integration (Priority: LOW - Phase 3B)
**Duration**: 2 hours
**Files to Create**:
- `src/ui/screenshot_tool.py` - Region selection overlay
- `src/core/vision_manager.py` - Screenshot + API call

**What to Do**:
1. Screenshot selection overlay:
   - Show semi-transparent overlay on full screen
   - Let user drag rectangle to select region
   - Show crosshair cursor
   - Preview of selected region

2. Vision integration:
   - Capture selected region to PNG
   - Send to LLM provider (if supports vision)
   - Display response in chat window

3. Tests:
   - Region selection accuracy
   - Screenshot capture quality
   - Vision API call with image

---

## Implementation Order

### Session 1 (Today/Tomorrow) - Foundation
1. ✅ Task #1: Real LLM streaming (test with local Ollama)
2. ✅ Task #2: Clipboard manager (text + error handling)
3. ✅ Task #3: Markdown rendering (basic + code blocks)

**Result**: Real responses with formatting!

### Session 2 - Polish
4. Task #4: Settings dialog (provider config)
5. Task #5: Auto-paste (paste to active window)

**Result**: Full configuration + response delivery!

### Session 3 - Advanced (if time)
6. Task #6: Vision API (screenshots)

---

## Testing Strategy for Phase 3

Since Phase 2 tests were weak on integration, Phase 3 will:

1. **Create `tests/test_integration/` folder** for real tests:
   - `test_ollama_streaming.py` - Real Ollama calls (skip if not available)
   - `test_markdown_rendering.py` - Markdown → HTML verification
   - `test_clipboard_flow.py` - Full clipboard read → LLM → paste flow
   - `test_e2e_workflow.py` - User trigger → response → result

2. **Keep Phase 2 tests** as baseline (don't modify)

3. **Add performance benchmarks**:
   - First token latency (should be <500ms with local Ollama)
   - Streaming throughput (tokens/sec)
   - Memory usage during streaming

---

## Dependencies to Add

```bash
# Already have:
pynput>=1.7.6
requests>=2.31.0

# Add for Phase 3:
markdown>=3.5              # Markdown rendering
Pygments>=2.16            # Syntax highlighting
python-docx>=0.8.11       # Optional: Rich text export

# Windows-specific:
pywin32>=305              # Win32 API for auto-paste
# or use ctypes (stdlib, preferred)
```

---

## Success Criteria

Phase 3 is complete when:

- ✅ Real LLM responses appear in chat window
- ✅ Responses formatted with Markdown (headers, code, bold, etc.)
- ✅ Clipboard content used as input (not hardcoded text)
- ✅ Settings dialog allows provider configuration
- ✅ Auto-paste works (responses pasted to active window)
- ✅ 10+ new integration tests added
- ✅ Performance: first token <500ms, smooth streaming
- ✅ No crashes on: empty clipboard, missing provider, network errors

---

## Known Risks

1. **Ollama not installed** - Tests will skip if not available
2. **Network latency** - First token might be slow over internet
3. **Markdown rendering complexity** - Some edge cases with HTML
4. **Auto-paste in different apps** - Behavior varies by window focus

---

## Estimated Timeline

| Task | Hours | Difficulty |
|------|-------|-----------|
| Task #1: Real LLM | 1.5 | Medium |
| Task #2: Clipboard | 1 | Easy |
| Task #3: Markdown | 2 | Medium |
| Task #4: Settings | 1.5 | Medium |
| Task #5: Auto-paste | 1.5 | Hard |
| Task #6: Vision | 2 | Hard |
| **Tests** | 2 | Medium |
| **TOTAL** | **11.5 hours** | - |

**Realistic timeline**: 2-3 intensive sessions (~4-5 hours each)

---

## Next Immediate Action

Start **Task #1** (Real LLM Integration):

1. Check if Ollama is available locally
2. Modify `main.py._simulate_response()` to use real provider
3. Test streaming with actual LLM
4. Create integration test

Ready to proceed? 🚀
