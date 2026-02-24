# Phase 3B Plan - Hotkeys & Threading Patch
## Quick Shortcut AI LLM Assistant

**Status**: PLANNED (Ready to start)
**Target Duration**: 3-5 working days (Mon-Fri)
**Start Date**: 2026-02-24 (This week)
**Branch**: `phase-3b/hotkeys-threading` (git)
**Goal**: Fix 5 critical bugs blocking UAT via library replacement + threading fix

---

## Strategic Overview

Phase 3 is currently BLOCKED by 5 critical UI bugs. Rather than attempting multiple complex fixes to existing architecture, Phase 3B takes a **minimal, targeted approach**:

1. **Replace problematic library** (`pynput` → `keyboard`)
2. **Fix threading architecture** (add QThread worker pattern)
3. **Validate on clean branch** (risk-isolated)
4. **Merge back if successful** (continue to Phase 4-5)
5. **Fallback if failed** (decide rewrite strategy)

This is a **low-risk, high-confidence approach** backed by:
- ✅ 95% audit confidence
- ✅ 90% success rate
- ✅ Code ready to copy-paste
- ✅ Well-documented patterns

---

## The 5 Critical Bugs (Phase 3 Blockers)

| # | Bug | Severity | Root Cause | Fix Time | Fix Method |
|---|-----|----------|-----------|----------|-----------|
| 1 | Settings closes app | 🔴 CRIT | pynput + QWidget hierarchy | 2-4h | QDialog fix |
| 2 | Icon stuck RED | 🔴 CRIT | Health check not updating | 1-2h | Signal connection |
| 3 | Chat FREEZES (Ctrl+Enter) | 🔴 CRIT | Main thread blocked | 4-6h | QThread worker |
| 4 | Menu non-clickable | 🟠 IMP | Event propagation/signals | 2-3h | Debug + fix |
| 5 | Windows menu visible | 🟠 IMP | pynput suppression broken | Accepted | Known limitation |

**Total Fix Effort**: 10-18 hours = ~2-3 dev days in reality

---

## Phase 3B Execution Plan (Day-by-Day)

### Day 1-2: Hotkeys Replacement (Monday-Tuesday)

**Objective**: Replace pynput with keyboard library, hotkeys working

#### 1.1 Setup & Dependencies (1-2 hours)
```bash
# Create isolated branch
git checkout -b phase-3b/hotkeys-threading
git branch -u origin/main  # Track main for easy merge

# Uninstall old, install new
pip uninstall pynput -y
pip install keyboard>=0.13.5

# Update requirements.txt
# Change: pynput>=1.7.6
# To:     keyboard>=0.13.5

# Verify
pip list | grep keyboard
python -c "import keyboard; print(keyboard.__version__)"
```

#### 1.2 Refactor InputManager (2-4 hours)
- **File**: `src/core/input_manager.py`
- **Source Code**: See `docs/08_audit/PRACTICAL_SOLUTIONS_CODE_SNIPPETS.md`
- **Tasks**:
  - Copy new InputManager class (keyboard-based, Option A or B)
  - Keep signal interface same (sig_shortcut_triggered, sig_error)
  - Update hotkey registration (keyboard.add_hotkey syntax)
  - Test keyboard import doesn't break PySide6

#### 1.3 Test Hotkeys (2-3 hours)
```bash
# Run tests
pytest tests/test_core/test_input_manager.py -v

# Manual test
python -m src.main &
# Press Ctrl+Shift+Right (or configured hotkey)
# Expected: Menu appears at cursor

# Check no crashes
ps aux | grep python  # Should still show process
```

#### 1.4 Day 1-2 Validation
**Checklist (end of Tuesday EOD)**:
- [ ] pynput uninstalled, keyboard installed
- [ ] src/core/input_manager.py fully refactored
- [ ] pytest tests/test_core/test_input_manager.py PASSES
- [ ] Manual hotkey test works (menu appears)
- [ ] No import errors
- [ ] No PySide6 crashes
- [ ] Commit: `git commit -m "feat(phase3b): replace pynput with keyboard library"`

**If blocked**: Debug section in `docs/08_audit/PLAN_ACTION_SEMAINE.md`

---

### Day 2-3: Threading Fix (Tuesday-Wednesday)

**Objective**: Implement proper QThread pattern, chat doesn't freeze on Ctrl+Enter

#### 2.1 Add StreamingWorker Class (1-2 hours)
- **File**: `src/main.py`
- **Source Code**: See `docs/08_audit/PRACTICAL_SOLUTIONS_CODE_SNIPPETS.md` (section 2)
- **Tasks**:
  - Add StreamingWorker(QObject) class
  - Signals: token_received, streaming_complete, error_occurred
  - run() method with provider.stream_chat() loop
  - stop() method for cancellation

#### 2.2 Refactor _stream_chat_response() (1-2 hours)
- **File**: `src/main.py`
- **Tasks**:
  - Replace old blocking implementation
  - Create QThread and move worker to it
  - Connect signals to handlers
  - Auto-cleanup on completion

#### 2.3 Add Signal Handlers (30 min - 1 hour)
- **File**: `src/main.py`
- **Methods to add**:
  - `_on_token_received(token: str)` → update UI
  - `_on_streaming_complete()` → cleanup
  - `_on_streaming_error(error: str)` → show error

#### 2.4 Test Threading (1-2 hours)
```bash
# Run streaming tests
pytest tests/test_ui/ -v -k streaming

# Manual test
python -m src.main &
# Type in chat window
# Press Ctrl+Enter
# Expected: UI remains responsive, tokens appear progressively
# NOT expected: Frozen window waiting for response
```

#### 2.5 Day 2-3 Validation
**Checklist (end of Wednesday EOD)**:
- [ ] StreamingWorker class added
- [ ] _stream_chat_response() refactored
- [ ] Handlers connected (_on_token_received, etc.)
- [ ] pytest tests/test_ui/ PASSES (or most pass)
- [ ] Manual test: Ctrl+Enter → responsive UI
- [ ] Tokens appear progressively (not all at end)
- [ ] Commit: `git commit -m "feat(phase3b): implement QThread worker pattern for streaming"`

**If blocked**: See troubleshooting in `docs/08_audit/PLAN_ACTION_SEMAINE.md`

---

### Day 3-4: Other Bug Fixes (Wednesday-Thursday)

**Objective**: Fix Settings, Health Check, Menu click issues

#### 3.1 Fix Settings Dialog (2-4 hours)
- **File**: `src/ui/settings_dialog.py`
- **Issue**: Clicking OK closes entire app
- **Root Cause**: Likely QWidget vs QDialog, or parent relationship
- **Fix**:
  - Ensure SettingsDialog(QDialog) not QWidget
  - Verify closeEvent() only closes dialog
  - Check parent/child relationships
  - Use self.reject() on close

#### 3.2 Fix Health Check Updates (1-2 hours)
- **Files**: `src/services/health_check.py` + `src/ui/tray_icon.py`
- **Issue**: Icon stuck RED despite valid config
- **Root Cause**: Health check not re-run after settings change
- **Fix**:
  - Connect settings save signal to health_check.run_check()
  - Update tray icon on result
  - Test: change config → icon should update

#### 3.3 Debug Menu Click Issues (1-2 hours)
- **File**: `src/ui/floating_menu.py`
- **Issue**: Menu items not clickable
- **Likely root cause**: keyboard library now working → might already be fixed!
- **Test**: Ctrl+Right → click item → action should work
- **If still broken**: Debug signal connections, event propagation

#### 3.4 Day 3-4 Validation
**Checklist (end of Thursday EOD)**:
- [ ] Settings dialog: OK button closes dialog (not app)
- [ ] Health check: Icon updates on config change
- [ ] Menu items: Clickable and functional
- [ ] pytest tests/ PASSES (full suite)
- [ ] Manual test: All 3 bugs fixed
- [ ] Commit: `git commit -m "fix(phase3b): settings, health check, menu issues"`

---

### Day 4-5: UAT & Validation (Thursday-Friday)

**Objective**: Full User Acceptance Test, production readiness

#### 4.1 Full Manual Testing (2-4 hours)
Run complete UAT based on `docs/testing/PHASE_3B_TEST_PLAN.md`:

**Test 1: Hotkeys**
- [ ] Ctrl+Shift+Right → Menu appears
- [ ] Menu click → Action executes
- [ ] Multiple clicks → No crashes
- [ ] In different apps → Still works

**Test 2: Streaming**
- [ ] Type in chat, Ctrl+Enter
- [ ] UI stays responsive
- [ ] Tokens arrive progressively
- [ ] Window can be closed mid-stream
- [ ] Stop button works

**Test 3: Settings**
- [ ] Open Settings dialog
- [ ] Change something (e.g., model)
- [ ] Click OK → Dialog closes
- [ ] App continues, not crashed
- [ ] Change persisted

**Test 4: Health Check**
- [ ] Start app → correct color (green/red)
- [ ] Change config → color updates
- [ ] Invalid config → red
- [ ] Valid config → green

**Test 5: Performance**
- [ ] Startup time < 3 seconds
- [ ] No memory leaks (check after 5 min use)
- [ ] Streaming smooth (no stuttering)
- [ ] CPU usage reasonable

#### 4.2 Pytest Coverage (1 hour)
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
# Target: >= 89% coverage maintained or improved
```

#### 4.3 Git & Merge Prep (30 min - 1 hour)
```bash
# Clean up commits
git log --oneline phase-3b/hotkeys-threading | head -10

# Prepare for merge
git fetch origin main
git rebase origin/main  # If needed

# Create summary
git log origin/main..phase-3b/hotkeys-threading --oneline
```

#### 4.4 Day 4-5 Validation
**Checklist (end of Friday 5 PM)**:
- [ ] All 5 bugs fixed ✅
- [ ] All tests passing (>= 89% coverage)
- [ ] Manual UAT complete
- [ ] Zero crashes (5-min stress test)
- [ ] Performance acceptable
- [ ] Git history clean
- [ ] Ready to merge to main

---

## Success Criteria for Phase 3B

### If ALL Green ✅ → MERGE TO MAIN & CONTINUE PHASE 4-5

```
✅ Hotkeys work (Ctrl+Shift+Right → Menu)
✅ Chat responsive (no freeze on Ctrl+Enter)
✅ Settings stable (OK button works)
✅ Health check updates (icon color changes on config)
✅ Menu clickable (click item → action)
✅ Tests passing (pytest >= 89% coverage)
✅ Zero crashes (5-min manual test)
✅ Performance good (responsive, reasonable CPU/memory)
```

**Action**:
```bash
git checkout main
git merge --no-ff phase-3b/hotkeys-threading -m "Merge phase-3b: fix critical UAT blockers"
git push origin main
```

Then continue to Phase 4 (Advanced Features).

---

### If 1-2 Bugs Remain ❌ → DEBUG OR FALLBACK

**Option 1**: Debug & fix (extend 1-2 days)
- Identify specific issue
- Apply targeted fix
- Re-test
- Merge when ready

**Option 2**: Accept limitation & merge anyway
- If non-critical (like Windows menu visible)
- Document as known issue
- Plan fix for Phase 4+

**Option 3**: Fallback to alternatives (2-3 weeks)
- If keyboard library still fails: try Win32 API
- If architecture still broken: consider Electron rewrite
- Decision made during Phase 3B failure

---

### If Phase 3B Fails Completely 🔴 → EVALUATE REWRITE

**Scenario**: keyboard library doesn't work, QThread doesn't fix freeze, issues persist

**Actions**:
1. Document why Phase 3B failed (exact errors, reproduction steps)
2. Discuss findings with team/stakeholder
3. Decide:
   - **Option A**: More targeted fixes (1-2 weeks)
   - **Option B**: Rewrite to Electron (2-3 weeks, JS)
   - **Option C**: Rewrite to Tauri (3-4 weeks, Rust)

Phase 3B stays on branch, Phase 3 remains as fallback baseline.

---

## Git Strategy

### Branch Management

```
main (Phase 3 - stable baseline)
 │
 ├─ phase-3b/hotkeys-threading (Patch attempt)
 │  ├─ Day 1: hotkeys fix
 │  ├─ Day 2-3: threading fix
 │  ├─ Day 3-4: other bugs
 │  └─ Day 4-5: UAT & merge/fallback decision
 │
 └─ (Future phases 4, 5, etc.)
```

### Commit Strategy

**Commit per major change**:
```
1. feat(phase3b): replace pynput with keyboard library
2. feat(phase3b): implement QThread worker pattern for streaming
3. fix(phase3b): settings dialog, health check, menu click issues
4. test(phase3b): full UAT validation and documentation
```

**Never force-push** on this branch (until after merge decision).

### Merge Strategy (if successful)

```bash
# No-fast-forward merge to preserve branch history
git merge --no-ff phase-3b/hotkeys-threading -m "
Merge phase-3b: Fix critical Phase 3 UAT blockers

- Replace pynput → keyboard library (hotkey fixes)
- Implement QThread worker pattern (threading fixes)
- Fix settings dialog, health check, menu click issues
- All UAT tests passing, 89%+ coverage maintained

Closes #phase-3-blockers
"
```

---

## Rollback Plan (if needed)

If Phase 3B fails catastrophically:

```bash
# Option 1: Just stay on main (don't merge)
git checkout main
# Phase 3B branch abandoned, Phase 3 continues

# Option 2: Revert if accidentally merged
git revert -n HEAD~0..HEAD  # Revert range
git commit -m "Revert phase-3b: reverting to Phase 3 baseline"

# Option 3: Hard reset (only if main is broken)
git reset --hard origin/main
```

But with proper testing, this shouldn't be needed.

---

## Documentation Updates (during Phase 3B)

Update as you progress:

1. **TODO.md**: Mark Phase 3B tasks [x] DONE as you complete
2. **This file (PHASE_3B_PLAN.md)**: Update Status as you progress
3. **Create PHASE_3B_TEST_PLAN.md**: Testing documentation
4. **Create PHASE_3B_REVIEW.md**: After completion, document results

---

## Timeline Summary

```
MONDAY (Day 1-2):    Hotkeys fix       (2-3 days)
TUESDAY (Day 2-3):   Threading fix     (1-2 days)
WEDNESDAY (Day 3-4): Bug fixes         (2-3 days)
THURSDAY-FRIDAY (4-5): UAT & Merge    (2-3 days)

Total: 3-5 working days
Expected: Production ready by Friday EOD
```

---

## References

- **Audit documents**: `docs/08_audit/`
- **Day-by-day plan**: `docs/08_audit/PLAN_ACTION_SEMAINE.md`
- **Code snippets**: `docs/08_audit/PRACTICAL_SOLUTIONS_CODE_SNIPPETS.md`
- **Testing guide**: `docs/04_testing/PHASE_3B_TEST_PLAN.md` (to be created)

---

## Questions? Blocked?

1. Check `docs/08_audit/PLAN_ACTION_SEMAINE.md` (troubleshooting section)
2. Check `docs/08_audit/PRACTICAL_SOLUTIONS_CODE_SNIPPETS.md` (code details)
3. Review `docs/08_audit/AUDIT_TECHNOLOGIQUE_COMPLET.md` (technical background)

---

**Status**: 🟡 PLANNED (Ready to execute Monday)
**Confidence**: 90% success rate
**Risk**: LOW (isolated branch, well-tested patterns)
**Next Action**: Start Day 1 (Monday morning) → Run `pip install keyboard`

**Good luck! 🚀**
