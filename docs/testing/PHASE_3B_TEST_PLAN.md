# Phase 3B Testing Plan - Hotkeys & Threading Patch Validation
## Quick Shortcut AI LLM Assistant

**Date**: 24 février 2026
**Target**: Validate all 5 critical bugs are fixed
**Duration**: Day 4-5 (Thursday-Friday)
**Status**: Ready to execute

---

## Overview

Phase 3B Testing validates that the keyboard library + QThread pattern fixes resolve the 5 critical bugs blocking Phase 3 UAT.

**Success = ALL tests pass + ZERO crashes**

---

## Test Environment

### Prerequisites
- Branch: `phase-3b/hotkeys-threading`
- Python: 3.10+
- Dependencies: `pip install -r requirements.txt` (updated with keyboard)
- OS: Windows 10 or 11

### Setup
```bash
cd /d/MGS/DEV/app-quick-shortcut-AI-LLM
python -m venv venv
source venv/Scripts/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python -m pytest tests/ -v --tb=short
```

---

## Test Categories

### 1. Unit Tests (Automated)

#### 1.1 InputManager Tests
**File**: `tests/test_core/test_input_manager.py`

```bash
pytest tests/test_core/test_input_manager.py -v
```

**Expected Results**:
- ✅ test_initialization (InputManager creates without error)
- ✅ test_hotkey_registration (keyboard.add_hotkey called correctly)
- ✅ test_hotkey_trigger (signal emitted on hotkey press)
- ✅ test_stop (thread stops gracefully)
- ✅ No import errors from `keyboard` library

**Pass/Fail**: Must be 100% passing

---

#### 1.2 Streaming Tests
**File**: `tests/test_ui/test_response_window.py` and `tests/test_core/` (if streaming worker tests exist)

```bash
pytest tests/test_ui/ -v -k streaming
pytest tests/test_core/ -v -k streaming
```

**Expected Results**:
- ✅ StreamingWorker initializes correctly
- ✅ Signals connected properly
- ✅ Tokens emitted progressively
- ✅ Error handling works
- ✅ Cancellation stops streaming

**Pass/Fail**: Must be >= 95% passing (allow minor test additions needed)

---

#### 1.3 Full Suite Coverage
**File**: All tests

```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

**Expected Results**:
- ✅ >= 89% code coverage maintained
- ✅ All Phase 1-2 tests still passing (regression check)
- ✅ New tests for Phase 3B components passing

**Pass/Fail**: >= 89% coverage, 0 failed tests

---

### 2. Manual Tests (Interactive)

#### 2.1 Hotkey Detection

**Test 2.1.1: Basic Hotkey**
```
Steps:
  1. python -m src.main
  2. Open any text editor (Notepad, Word, etc.)
  3. Press Ctrl+Shift+Right (or configured hotkey)
  4. Check: Context menu appears at cursor position

Expected:
  ✅ Menu appears at cursor
  ✅ Menu is visible and clickable
  ✅ No delays (< 100ms response)

Pass/Fail: [ ] PASS [ ] FAIL
Notes: ___________
```

**Test 2.1.2: Multiple Hotkey Presses**
```
Steps:
  1. Keep app running from Test 2.1.1
  2. Press Ctrl+Shift+Right again (5 times)
  3. Each time, menu should appear

Expected:
  ✅ Menu appears each time
  ✅ No cumulative delays
  ✅ No memory growth
  ✅ No crashes

Pass/Fail: [ ] PASS [ ] FAIL
Notes: ___________
```

**Test 2.1.3: Hotkey in Different Apps**
```
Steps:
  1. Keep app running
  2. Open multiple apps (browser, IDE, terminal, etc.)
  3. In each app, press Ctrl+Shift+Right
  4. Check: Menu appears in each

Expected:
  ✅ Menu works in all apps
  ✅ Quick response (< 100ms)
  ✅ No crashes

Pass/Fail: [ ] PASS [ ] FAIL
Notes: ___________
```

---

#### 2.2 Chat Streaming (Threading)

**Test 2.2.1: Basic Streaming**
```
Steps:
  1. python -m src.main
  2. Focus chat window (if available) or trigger via menu
  3. Type: "What is 2+2?"
  4. Press Ctrl+Enter
  5. Observe: Response should arrive progressively

Expected:
  ✅ UI stays responsive (not frozen)
  ✅ Tokens appear as they arrive
  ✅ Response completes normally
  ✅ No UI lag

Pass/Fail: [ ] PASS [ ] FAIL
Response Time: _____ seconds
Notes: ___________
```

**Test 2.2.2: Streaming Responsiveness**
```
Steps:
  1. Start streaming (same as Test 2.2.1)
  2. While streaming, try to:
     - Click on menu buttons (Stop, Copy, etc.)
     - Move window
     - Resize window
  3. Check: All interactions responsive

Expected:
  ✅ All interactions work mid-stream
  ✅ Window moves smoothly
  ✅ Buttons respond immediately
  ✅ NOT frozen/laggy

Pass/Fail: [ ] PASS [ ] FAIL
Notes: ___________
```

**Test 2.2.3: Long Response**
```
Steps:
  1. Start streaming with longer prompt
     Example: "Write a 500-word essay on AI ethics"
  2. Let it stream for 30+ seconds
  3. Check: UI remains responsive

Expected:
  ✅ Window still moveable
  ✅ Stop button works if clicked
  ✅ No memory spike
  ✅ No CPU spike (reasonable)

Pass/Fail: [ ] PASS [ ] FAIL
Response Time: _____ seconds
Notes: ___________
```

---

#### 2.3 Settings Dialog

**Test 2.3.1: Settings Open/Close**
```
Steps:
  1. python -m src.main
  2. Right-click tray icon → Settings
  3. Settings dialog opens
  4. Click OK

Expected:
  ✅ Dialog opens without error
  ✅ Dialog closes when OK clicked
  ✅ App continues running (NOT closed)
  ✅ No crashes

Pass/Fail: [ ] PASS [ ] FAIL
Notes: ___________
```

**Test 2.3.2: Settings Change & Persist**
```
Steps:
  1. Open Settings (Test 2.3.1)
  2. Change a setting (e.g., model dropdown)
  3. Click OK
  4. Reopen Settings
  5. Check: Change is still there

Expected:
  ✅ Setting persisted to config
  ✅ Change visible on reopen
  ✅ No data loss

Pass/Fail: [ ] PASS [ ] FAIL
Notes: ___________
```

---

#### 2.4 Health Check & Tray Icon

**Test 2.4.1: Icon Color**
```
Steps:
  1. python -m src.main
  2. Right-click tray icon
  3. Observe icon color

Expected (if config valid):
  ✅ Icon is GREEN or appropriate color
  ✅ Tray menu shows "Ready"

Expected (if config invalid):
  ✅ Icon is RED
  ✅ Tray menu shows "Error"

Pass/Fail: [ ] PASS [ ] FAIL
Notes: ___________
```

**Test 2.4.2: Icon Update on Config Change**
```
Steps:
  1. Start app (note icon color)
  2. Invalidate config (wrong LLM endpoint)
  3. Change Settings → invalid config
  4. Click OK
  5. Observe icon

Expected:
  ✅ Icon changes to RED quickly (< 2 seconds)
  ✅ Reflects config change

Pass/Fail: [ ] PASS [ ] FAIL
Notes: ___________
```

---

#### 2.5 Menu Click Functionality

**Test 2.5.1: Menu Item Click**
```
Steps:
  1. python -m src.main
  2. In text editor, select some text
  3. Press Ctrl+Shift+Right → Menu appears
  4. Click on menu item (e.g., "Summarize")
  5. Check: Action executes

Expected:
  ✅ Menu closes
  ✅ Action starts (e.g., LLM call for summary)
  ✅ Response window shows result
  ✅ No crashes

Pass/Fail: [ ] PASS [ ] FAIL
Notes: ___________
```

**Test 2.5.2: Menu Close on Click Outside**
```
Steps:
  1. Open menu (Ctrl+Shift+Right)
  2. Click outside menu (somewhere in app or other window)
  3. Check: Menu closes

Expected:
  ✅ Menu disappears
  ✅ No error

Pass/Fail: [ ] PASS [ ] FAIL
Notes: ___________
```

---

### 3. Performance Tests (Observation)

#### 3.1 Startup Time
```
Steps:
  1. Time how long it takes to start the app
  2. python -m src.main
  3. Record: Time until tray icon appears + menu responsive

Expected:
  ✅ < 3 seconds from command to ready

Pass/Fail: [ ] PASS [ ] FAIL
Startup Time: _____ seconds
Notes: ___________
```

#### 3.2 Memory Usage
```
Steps:
  1. Start app
  2. Use it for 5 minutes:
     - Press hotkey 10 times
     - Stream 3 responses
     - Open/close settings
  3. Observe: Memory usage stable?

Expected:
  ✅ No memory leaks (usage stable)
  ✅ < 200 MB baseline
  ✅ < 300 MB during streaming

Pass/Fail: [ ] PASS [ ] FAIL
Baseline Memory: _____ MB
Peak Memory: _____ MB
Notes: ___________
```

#### 3.3 CPU Usage
```
Steps:
  1. At rest (idle), check CPU
  2. During streaming, check CPU
  3. After stream completes, check CPU

Expected:
  ✅ At rest: near 0%
  ✅ Streaming: moderate (not pegged at 100%)
  ✅ After: back to near 0%

Pass/Fail: [ ] PASS [ ] FAIL
Idle CPU: _____ %
Streaming CPU: _____ %
Post-Stream CPU: _____ %
Notes: ___________
```

---

### 4. Regression Tests (Ensure Phase 1-2 still work)

#### 4.1 Phase 1 Components
```bash
pytest tests/test_core/test_llm_provider.py -v
pytest tests/test_core/test_config_service.py -v
pytest tests/test_services/test_health_check.py -v
```

**Expected**: All Phase 1 tests still pass (no regression)

Pass/Fail: [ ] PASS [ ] FAIL
Notes: ___________

#### 4.2 Phase 2 Components
```bash
pytest tests/test_ui/test_floating_menu.py -v
pytest tests/test_ui/test_response_window.py -v
pytest tests/test_ui/test_tray_icon.py -v
```

**Expected**: All Phase 2 tests still pass (no regression)

Pass/Fail: [ ] PASS [ ] FAIL
Notes: ___________

---

### 5. Crash Test (Stress)

**Test 5.1: 5-Minute Stress Test**
```
Steps:
  1. python -m src.main
  2. Perform rapid actions for 5 minutes:
     - Hotkey (Ctrl+Shift+Right): Press every 3 seconds
     - Streaming: Ctrl+Enter every 10 seconds
     - Settings: Open/close every 30 seconds
  3. Observe: Any crashes?

Expected:
  ✅ No crashes in 5 minutes
  ✅ No hangs
  ✅ No memory spike
  ✅ All features still responsive

Pass/Fail: [ ] PASS [ ] FAIL
Crashes: 0
Hangs: 0
Errors: ___________
Notes: ___________
```

---

## Test Results Summary

### Unit Tests
- [ ] InputManager tests: PASS/FAIL
- [ ] Streaming tests: PASS/FAIL
- [ ] Full coverage >= 89%: PASS/FAIL

### Manual Tests
- [ ] Hotkey detection: PASS/FAIL
- [ ] Chat streaming (responsive): PASS/FAIL
- [ ] Settings dialog: PASS/FAIL
- [ ] Health check/icon: PASS/FAIL
- [ ] Menu click: PASS/FAIL

### Performance
- [ ] Startup < 3s: PASS/FAIL
- [ ] Memory stable: PASS/FAIL
- [ ] CPU reasonable: PASS/FAIL

### Regression
- [ ] Phase 1 tests: PASS/FAIL
- [ ] Phase 2 tests: PASS/FAIL

### Stress
- [ ] 5-min test zero crashes: PASS/FAIL

---

## Overall Phase 3B Status

### Success Criteria (ALL must be green)

```
✅ All 5 bugs fixed
✅ All tests passing (>= 89% coverage)
✅ Manual UAT complete (PASS)
✅ Regression tests pass (no breakage)
✅ Performance acceptable
✅ Zero crashes (stress test)

RESULT: [  ] PASS → Merge to main
        [  ] FAIL → Debug or fallback
```

---

## If PASS → Merge Decision

```
1. Document results in PHASE_3B_REVIEW.md
2. Run: git log --oneline phase-3b/hotkeys-threading
3. Run: git merge --no-ff phase-3b/hotkeys-threading
4. Continue to Phase 4 (Advanced Features)
```

---

## If FAIL → Debug Steps

1. **Identify failing test** (unit or manual)
2. **Review error message** carefully
3. **Check troubleshooting** in `docs/08_audit/PLAN_ACTION_SEMAINE.md`
4. **Fix targeted issue** (extend Day 5-6)
5. **Re-test** specific component
6. **Merge when ready** OR **fallback to Plan B**

---

## Questions During Testing?

1. Check `docs/08_audit/PLAN_ACTION_SEMAINE.md` (troubleshooting)
2. Check `docs/08_audit/AUDIT_TECHNOLOGIQUE_COMPLET.md` (technical)
3. Review `docs/08_audit/PRACTICAL_SOLUTIONS_CODE_SNIPPETS.md` (code)

---

**Ready to test? Run on Day 4-5 (Thursday-Friday)! 🚀**
