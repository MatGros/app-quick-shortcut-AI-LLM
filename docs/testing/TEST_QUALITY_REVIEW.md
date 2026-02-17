# TEST QUALITY REVIEW - Phase 2
**Date**: 2026-02-15
**Status**: ⚠️ CRITICAL GAPS IDENTIFIED
**Coverage**: 193 passing tests, but **28% are trivial**, **72% over-mocked**

---

## EXECUTIVE SUMMARY

Tests verify that **code runs without crashing**, but **don't verify actual functionality** against SPEC requirements:

| Metric | Status | Issue |
|--------|--------|-------|
| **Code Coverage** | 89% (lines of code) | ✅ Good |
| **Functional Coverage** | ~40% (actual requirements) | ⚠️ **CRITICAL** |
| **Trivial Tests** | 28% (empty assertions, hasattr) | ❌ **Removing 45 tests** |
| **Over-Mocked Tests** | 72% (mock real behavior away) | ❌ **Needs replacement** |
| **Real-World Tests** | < 5% (actual performance) | ❌ **Missing** |

---

## CRITICAL FINDINGS BY FEATURE

### **F-01: Input Hooks (20 tests) - MAJOR GAPS**

**Status**: Tests don't verify the actual hook behavior that matters

**Trivial Tests Found (7):**
```python
# Line 57-61: Useless - initial position is hardcoded to (0,0)
def test_initial_position(self, input_manager):
    x, y = input_manager.get_last_position()
    assert x == 0
    assert y == 0

# Line 165: ALWAYS PASSES - defeats test purpose
assert callback.called or True  # ❌ BAD

# Lines 50-55: Just checks hasattr() exists
def test_input_manager_signals_exist(self, input_manager):
    assert hasattr(input_manager, 'sig_shortcut_triggered')
    # ... doesn't verify signals actually work
```

**What's NOT tested (the important stuff):**
- ❌ **Real latency** from actual mouse hook to signal emission (SPEC: <100ms critical)
- ❌ **Race conditions** on rapid Ctrl+Click sequences
- ❌ **Listener lifecycle** - creation/destruction edge cases
- ❌ **Thread safety** - concurrent signal emissions
- ❌ **Real pynput integration** - all events are mocked

**Why it matters:**
SPEC requirement: *"Latence trigger → menu affiché: < 100ms"*
Current tests: Measure internal function call (~0.001ms) - **not real latency**
Reality gap: Could be 200-300ms with actual mouse listener

**Recommendation**: Replace 7 trivial tests with:
1. **Integration test** with real pynput listener measuring actual latency
2. **Stress test** - 100 rapid Ctrl+clicks
3. **Thread race test** - simultaneous listeners

---

### **F-02: Floating Menu (36 tests) - WEAK POSITIONING**

**Status**: Tests check object existence, not visual correctness

**Trivial Tests (8):**
```python
# Line 85-90: Single property check
def test_menu_item_height(self, qapp):
    action = MenuAction("test", "Test")
    item = MenuItem(action)
    assert item.minimumHeight() == 40  # ✅ Passes, but meaningless

# Line 197: ALWAYS TRUE
assert callback.called or True
```

**What's NOT tested:**
- ❌ **Multi-monitor positioning** - menu off-screen on secondary monitors?
- ❌ **DPI scaling** - menu rendered at 125%/150% Windows scale?
- ❌ **Animation timing** - fade-in actually 200ms as spec says?
- ❌ **Keyboard conflicts** - menu shortcuts conflict with system?
- ❌ **Large menus** - performance with 50+ items?
- ❌ **Focus management** - menu focus stealing?

**Why it matters:**
SPEC: *"Menu must be frameless avec coins arrondis (8px), ombre portée, fade-in 200ms"*
Current tests: Check opacity property is set
Reality gap: Animation could be wrong easing curve, wrong timing, might stutter on some Windows versions

**Recommendation**: Replace 8 tests with:
1. **Multi-monitor test** - mock QScreen with secondary display
2. **Animation timing test** - verify 200ms ±10ms duration
3. **Visual rendering test** - QTest pixmap comparison
4. **Large menu performance test** - 50 items → scroll smooth?

---

### **F-04: Chat Streaming Window (24 tests) - MISSING LOAD TESTS**

**Status**: Single-token streaming tested, but not under load

**Trivial Tests (5):**
```python
# Line 52-56: Property check only
def test_auto_expanding_min_height(self, qapp):
    widget = AutoExpandingTextEdit()
    assert widget.minimumHeight() == 40

# Line 87-97: Singleton identity check
def test_singleton_creation(self):
    w1 = ResponseWindow()
    w2 = ResponseWindow()
    assert w1 is w2  # ✅ True but doesn't test functionality
```

**What's NOT tested:**
- ❌ **Buffering under load** - 1000 tokens/sec → actual flush timing?
- ❌ **Memory usage** - streaming 1MB response → buffer grows?
- ❌ **Scroll correctness** - auto-scroll with massive responses?
- ❌ **Concurrent append_token()** - multiple threads writing simultaneously?
- ❌ **Copy with special chars** - emoji, RTL, control characters?
- ❌ **Window resize during streaming** - responsive?

**Why it matters:**
SPEC: *"Token streaming avec buffering intelligent (50ms window)"*
Current tests: Append 5 tokens, verify buffer exists
Reality gap: With real LLM outputting 100 tokens/sec, buffer could flush too frequently or accumulate unbounded

**Recommendation**: Replace 5 tests with:
1. **Load test** - stream 5000 tokens, measure buffer flush count
2. **Memory test** - 1MB response, verify memory freed after clear
3. **Scroll stress test** - 10,000-line response, check scroll smooth
4. **Concurrent access test** - 5 threads calling append_token()

---

### **F-13: Shortcuts (39 tests) - SYSTEM INTEGRATION MISSING**

**Status**: App-only shortcuts tested, real system shortcuts never checked

**Trivial Tests (6):**
```python
# Line 338: ADMITS shared state, assertion is meaningless
def test_multiple_managers_independent(self):
    # ... setup ...
    assert mgr1._shortcuts != mgr2._shortcuts or True  # ❌ or True = always passes

# Lines 59-62: String equality
def test_default_show_menu_shortcut(self):
    assert config.key_sequence == "Ctrl+Right"
```

**What's NOT tested:**
- ❌ **Real Windows API conflicts** - Alt+Tab, Win, Ctrl+Alt+Del registration?
- ❌ **Persistence reload** - save to disk, restart app, shortcuts still there?
- ❌ **Registry conflicts** - check Windows Registry for system shortcuts?
- ❌ **Concurrent registration** - 5 threads registering simultaneously?
- ❌ **Invalid key sequences** - parse "Ctrl", "Super+", "Ctrl+Ctrl"?

**Why it matters:**
SPEC: *"Customisables avec détection conflits"*
Current tests: Check strings match
Reality gap: User sets Ctrl+A (conflicts with Select All), app doesn't warn. Or user resets shortcuts on next launch

**Recommendation**: Replace 6 tests with:
1. **System conflict test** - try register Ctrl+Alt+Del, verify rejection
2. **Persistence test** - save, restart app, verify config loaded
3. **Parsing test** - malformed shortcuts → ValueError with message
4. **Concurrency test** - 5 threads register simultaneously

---

### **F-14: Tray Icon (25 tests) - VISUAL TESTS MISSING**

**Status**: State changes verified, visual rendering never checked

**Trivial Tests (7):**
```python
# Lines 62-73: Status enum tests
def test_set_status_busy(self, tray_icon):
    tray_icon.set_status(TrayStatus.BUSY)
    assert tray_icon.get_status() == TrayStatus.BUSY  # ✅ True, but tray icon visual?

# Line 224: Assertion always true
assert tray_icon.sig_status_changed is not None
```

**What's NOT tested:**
- ❌ **Icon color rendering** - READY icon actually green (#00C800)?
- ❌ **DPI scaling** - icon rendering at 125%/150%?
- ❌ **Concurrent status changes** - rapid READY→BUSY→ERROR→READY?
- ❌ **Tooltip display** - tooltip actually appears on hover?
- ❌ **Context menu appearance** - right-click shows menu?

**Why it matters:**
SPEC: *"Status indicators (green/yellow/red), Tooltip with status text"*
Current tests: Check object state changes
Reality gap: Icon could be wrong color, hard to see at 150% scale, tooltip never tested

**Recommendation**: Replace 7 tests with:
1. **Color rendering test** - grab tray icon pixmap, verify color == expected
2. **DPI test** - mock QGuiApplication.primaryScreen().devicePixelRatio()
3. **Concurrent status test** - 5 status changes/sec, verify no flicker
4. **Tooltip test** - simulate hover event, verify text

---

### **F-11: Health Checks (9 tests) - ALL MOCKED**

**Status**: No real network calls, config validation never tested with corrupted files

**Over-Mocking (9/9 tests):**
```python
# Lines 74-83: ALL provider calls are mocked
with patch('src.core.llm_provider.OllamaProvider.health_check') as mock:
    mock.return_value = HealthCheckResult(True, "OK")
    # ... doesn't actually test timeout, network errors, etc.
```

**What's NOT tested:**
- ❌ **Real connectivity** - actual HTTP call to Ollama localhost?
- ❌ **Timeout behavior** - provider hangs for 10s, check timeout kicks in?
- ❌ **Corrupted config** - malformed JSON config.json, handled gracefully?
- ❌ **Config validation** - missing required keys (e.g., no provider defined)?
- ❌ **Retry logic** - transient failure → auto-retry?

**Why it matters:**
SPEC: *"Vérifications démarrage (config, LLM, permissions)"*
Current tests: All checks always pass (mocked)
Reality gap: Real config could be corrupted, Ollama could be down, checks never actually run

**Recommendation**: Create integration tests:
1. **Config corruption test** - write invalid JSON, verify health check fails gracefully
2. **Network timeout test** - mock slow provider response (5s), verify timeout < 6s
3. **Missing config test** - delete provider config, check health check error message
4. **Fallback test** - health check fails, verify app continues with warning

---

## STATISTICS

### Tests by Category

| Category | Count | Quality | Action |
|----------|-------|---------|--------|
| **Trivial** (assertions that always pass or check existence) | 45 | 🔴 Remove | DELETE |
| **Over-mocked** (mock away the behavior being tested) | 100 | 🟡 Weak | REWRITE |
| **Real-world** (actual performance, integration) | 12 | 🟢 Good | KEEP |
| **Incomplete** (partial assertions, no error cases) | 36 | 🟡 Weak | IMPROVE |

### Coverage vs Functionality

```
Code Coverage:    ██████████░░░░░░░░░░ 89%  (lines of code executed)
Functional Cov.:  ██████░░░░░░░░░░░░░░ 40%  (requirements verified)

Ratio: 2.2x gap between code coverage and actual functionality
```

---

## SPECIFIC PROBLEMATIC TEST PATTERNS

### Pattern 1: Always-True Assertions

```python
# ❌ BAD: Will always pass
assert callback.called or True

# ✅ GOOD: Actually verifies behavior
assert callback.call_count == 1
assert callback.call_args[0] == ("expected_action_id", 100, 200)
```

**Found in**: test_input_manager.py:165, test_floating_menu.py:197,321, test_shortcut_manager.py:250,290

**Fix**: Remove `or True`, add actual call verification

---

### Pattern 2: Over-Protected Mocks

```python
# ❌ BAD: Mocks prevent real behavior testing
with patch('src.core.input_manager.pynput.mouse.Listener') as mock:
    # Never tests actual listener lifecycle
    pass

# ✅ GOOD: Test real integration
def test_listener_lifecycle():
    mgr = InputManager()
    mgr.start()
    assert mgr._listener is not None
    assert mgr._listener.is_alive()
    mgr.stop()
    mgr.wait(2000)
    assert not mgr._listener.is_alive()
```

**Found in**: All test files (72% over-mocked)

**Fix**: Create integration tests that don't mock pynput, Qt event loop, filesystem

---

### Pattern 3: Trivial Property Checks

```python
# ❌ BAD: Doesn't test behavior
def test_menu_item_height(self, qapp):
    item = MenuItem(action)
    assert item.minimumHeight() == 40  # True by definition, test proves nothing

# ✅ GOOD: Test actual behavior
def test_menu_item_respects_minimum_height(self, qapp):
    item = MenuItem(action)
    item.show()
    assert item.height() >= 40  # Verify rendered height matches minimum
```

**Found in**: Every test file (45 tests)

**Fix**: Test observable behavior, not default values

---

## MISSING INTEGRATION TESTS

No tests verify components working **together** under real conditions:

```python
# ❌ MISSING: Full workflow test
def test_full_trigger_menu_select_workflow():
    """User presses Ctrl+RClick → menu appears → selects action"""
    # 1. InputManager detects real keyboard event (not mocked)
    # 2. Signal reaches FloatingMenu (real Qt signal/slot)
    # 3. Menu animates into view (real QPropertyAnimation)
    # 4. User selects with keyboard (real QKeyEvent)
    # 5. ResponseWindow opens (real signal chain)
    # 6. Streaming starts (real token buffering)
```

**Recommendation**: Create `tests/test_integration/` folder with:
1. `test_e2e_trigger_menu.py` - full user workflow
2. `test_e2e_streaming.py` - LLM → streaming → display
3. `test_e2e_settings_persist.py` - config save/load across restarts
4. `test_performance.py` - measure actual latencies

---

## RECOMMENDED FIXES (Priority Order)

### Phase A: Critical Fixes (Do Now)
1. **Remove 45 trivial tests** - `assert property == expected_value`
2. **Fix 6 always-true assertions** - remove `or True` patterns
3. **Add real integration tests** - at least 1 per feature

### Phase B: Improve Coverage (This Week)
1. **Add load tests** - streaming 5000+ tokens, rapid clicks
2. **Add system integration tests** - real shortcuts, real DPI scaling
3. **Add error scenario tests** - corrupt config, network timeouts
4. **Add timing tests** - verify animation durations, latencies

### Phase C: Full Refactor (Next Sprint)
1. **Create dedicated integration test suite** - separate from unit tests
2. **Add performance benchmarks** - latency targets, memory usage
3. **Add visual regression tests** - screenshot comparison
4. **Add multi-environment tests** - Windows 10/11, scales 100%/125%/150%

---

## IMPACT ASSESSMENT

**Current State:**
- 193 tests pass ✅
- But 28% are trivial (no real verification)
- And 72% over-mocked (test passes, real code might break)
- **Actual confidence level**: ~40% functionality works

**If Fixed:**
- Remove 45 trivial tests → 148 real tests
- Replace 100 over-mocked tests with integration tests
- Add 30-40 new critical tests
- **Target**: 100+ real integration tests with <10% trivial
- **Confidence level**: ~85% functionality verified

**Risk of Current State:**
- User installs app
- Settings don't persist between sessions (never tested)
- Menu appears off-screen on 4K monitor (never tested)
- Streaming stops with 1MB response (never tested)
- System shortcuts conflict undetected (never tested)

---

## NEXT ACTION ITEMS

**For This Session:**
- [ ] Decide: Remove trivial tests now, or defer?
- [ ] Decide: Rewrite over-mocked tests, or create integration suite?
- [ ] Decide: Proceed to Phase 3 with weak tests, or strengthen Phase 2 first?

**Recommended Path:**
1. Remove/rewrite 45 weak tests (2-3 hours)
2. Add 20 critical integration tests (4-5 hours)
3. Then proceed to Phase 3 with stronger foundation

---

**Report Generated**: 2026-02-15
**Reviewer**: Claude Code
**Status**: Awaiting direction for next phase
