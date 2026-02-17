# Project Definition - Phase Boundaries & Scope
**Version**: 2.0
**Date**: 2026-02-16
**Status**: ACTIVE - Phases 1-3 in progress

---

## 📋 PHASE DEFINITIONS (REVISED)

### PHASE 1: Foundation (COMPLETE ✅)
**Scope**: Core services and provider abstraction
**Duration**: Session 1
**Status**: ✅ 100% Complete

**Deliverables**:
- LLM Provider abstraction (4 files)
- Configuration Service (Singleton)
- Health check framework
- Unit tests (43 tests, 87% coverage)

**Testing**: Unit tests ONLY (mocked providers)

**Output**:
- Ready for UI layer (Phase 2)

---

### PHASE 2: UI Core Implementation (IN PROGRESS ✅)
**Scope**: Complete UI layer with component integration and unit tests
**Duration**: Session 2
**Status**: 🟢 Code 100%, Unit Tests 100%

**Deliverables**:

#### Features (F-01 to F-14)
| ID | Feature | Component | Status |
|:---|---------|-----------|--------|
| F-01 | Global Input Hooks | input_manager.py | ✅ |
| F-02 | Floating Menu | floating_menu.py | ✅ |
| F-04 | Chat Streaming Window | response_window.py | ✅ |
| F-13 | Keyboard Shortcuts | shortcut_manager.py | ✅ |
| F-14 | System Tray Icon | tray_icon.py | ✅ |
| F-11 | Health Checks | (Phase 1) | ✅ |
| Main | App Orchestration | main.py | ✅ |

#### Testing - Phase 2
✅ Unit tests for each component (isolated)
✅ Signal/slot verification (Qt testing)
✅ Configuration persistence
✅ Error handling paths
❌ Integration tests (MOVED TO PHASE 3)
❌ User acceptance testing (MOVED TO PHASE 3)
❌ Real provider calls (MOVED TO PHASE 3)

**Tests by Component**:
- InputManager: 17 tests (63% coverage)
- FloatingMenu: 28 tests (91% coverage)
- ResponseWindow: 33 tests (98% coverage)
- ShortcutManager: 31 tests (100% coverage)
- TrayIcon: 22 tests (92% coverage)
- Main: 21 tests (85% coverage)
- ClipboardManager: 18 tests (90% coverage)
- **Total**: 213 tests, 89% overall coverage

**Testing Strategy**: Mocks for all external dependencies (pynput, Qt events, clipboard, LLM)

**What Phase 2 DOES**:
- ✅ Implement all UI components
- ✅ Create unit tests
- ✅ Verify signal connectivity
- ✅ Confirm basic functionality

**What Phase 2 DOES NOT DO**:
- ❌ Test with real mouse/keyboard input
- ❌ Test with real LLM providers
- ❌ Validate visual appearance
- ❌ Test error scenarios with real inputs
- ❌ Measure actual performance

---

### PHASE 3: LLM Integration & Testing (CURRENT)
**Scope**: Real provider integration + comprehensive testing + user validation
**Duration**: Sessions 3-4
**Status**: 🟡 In Progress (Task #1 partially done, now resuming full scope)

**Deliverables**:

#### Features (F-03, F-05-F-09, F-12, F-15-F-19)
| ID | Feature | Component | Status |
|:---|---------|-----------|--------|
| F-03 | LLM Provider Integration | ollama/openai/anthropic providers | 🚧 |
| F-05 | Clipboard Management | clipboard_manager.py | 🚧 |
| F-06 | Auto-Paste | auto_paster.py | 📋 |
| F-07 | Vision API Integration | vision_manager.py | 📋 |
| F-16 | Markdown Rendering | markdown support | 📋 |
| F-12 | Theme System | Dark/Light mode | 📋 |
| Settings | Configuration Dialog | settings_dialog.py | 📋 |

#### Testing - Phase 3 (NEW EMPHASIS)
🆕 **Integration Tests**: Test full workflows
- Ctrl+Click → menu → select → stream → display
- Clipboard read → LLM call → streaming → display
- Settings → provider change → streaming with new provider

🆕 **User Acceptance Tests**: With real inputs/outputs
- Real mouse/keyboard detection
- Real LLM provider calls (Ollama local/cloud, OpenAI)
- Visual validation (animations, positioning, rendering)
- Performance measurement (latency, throughput)
- Error scenario handling

🆕 **E2E Tests**: Full workflows
- End-to-end user scenarios
- Real clipboard content
- Real LLM responses
- Actual system state

#### Testing Strategy - Phase 3
✅ Real provider calls (Ollama, OpenAI, Anthropic optional)
✅ Real system input (mouse, keyboard)
✅ Real clipboard operations
✅ User participation in testing
✅ Performance profiling
✅ Visual validation

**What Phase 3 DOES**:
- ✅ Integrate with real LLM providers
- ✅ Create integration tests (component chains)
- ✅ Create user acceptance tests
- ✅ Test real workflows end-to-end
- ✅ Validate performance
- ✅ Add remaining UI features

**What Phase 3 DOES NOT Do**:
- ❌ Change Phase 2 code (only extend)
- ❌ Add new components (only integrate existing)
- ❌ Modify unit test structure

---

## 🎯 KEY DIFFERENCES

### Unit Tests (Phase 2)
```python
# WHAT WE DO:
- Mock all external dependencies
- Test component in isolation
- Verify logic and signal connectivity
- Fast execution

# EXAMPLE:
with patch('pynput.mouse.Listener'):
    input_mgr = InputManager()
    input_mgr._on_mouse_click(100, 200, Button.right, False)
    assert callback.called  # Logic works ✓
```

### Integration Tests (Phase 3)
```python
# WHAT WE DO:
- Test components working together
- Still mock external APIs (but verify calls)
- Test signal flow between components
- Medium execution time

# EXAMPLE:
main_app = QuickShortcutApp()
main_app.startup()
main_app._on_shortcut_triggered("show_menu", 100, 100)
# Verify: FloatingMenu opened via signal ✓
```

### User Acceptance Tests (Phase 3)
```python
# WHAT WE DO:
- Test with real system input
- Test with real LLM providers (if available)
- Measure actual performance
- Validate visual behavior
- Slow execution, requires real setup

# EXAMPLE:
1. Start app
2. Ctrl+Click (real mouse event)
3. Verify: Menu appears at exact cursor position
4. Arrow down (real keyboard)
5. Verify: Selection changes (blue highlight)
```

---

## 📊 PROJECT ROADMAP

```
Phase 1: Foundation (Core Services)
    ✅ COMPLETE - 43 tests
    └─→ Phase 2

Phase 2: UI Core (Components + Unit Tests)
    🟢 COMPLETE - 213 tests (unit-level)
    └─→ Phase 3

Phase 3: LLM Integration + Testing (Real Providers + Integration/UAT)
    🟡 IN PROGRESS
    ├─ Task #1: Real LLM Streaming (DONE - need resume)
    ├─ Task #2: Clipboard Manager (DONE)
    ├─ Task #3: Markdown Rendering (TODO)
    ├─ Task #4: Settings Dialog (TODO)
    ├─ Task #5: Auto-Paste (TODO)
    ├─ Task #6: Integration Tests (TODO)
    ├─ Task #7: User Acceptance Tests (TODO)
    ├─ Task #8: Performance Profiling (TODO)
    └─→ Phase 4 or MVP Release

Phase 4+: Advanced Features (Optional)
    📋 PLANNED
    ├─ Vision API
    ├─ Advanced Settings
    ├─ Plugin System
    └─ Package as .exe
```

---

## 🔄 WORKFLOW SUMMARY

| Phase | Code | Unit Tests | Integration Tests | UAT | Provider Calls |
|-------|------|------------|-------------------|-----|----------------|
| **1** | ✅ | ✅ | - | - | Mocked |
| **2** | ✅ | ✅ | - | - | Simulated |
| **3** | ✅ | ✅ | ✅ | ✅ | Real |

---

## 📝 DOCUMENTATION ORGANIZATION

### Core Docs
- **PROJECT_DEFINITION.md** (THIS FILE) - Phase boundaries, scope
- **SPEC.md** - Complete feature specifications
- **README.md** - User-facing project overview

### Implementation Docs
- **PHASE_2_REVIEW.md** - Phase 2 final status (updated)
- **PHASE_3_PLAN.md** - Phase 3 tasks and planning (updated)
- **STATUS.md** - Current project status (updated)

### Testing Docs
- **TEST_QUALITY_REVIEW.md** - Analysis of test weaknesses (reference only)
- **QUICK_START_TESTS.md** - How to run pytest

### Setup Docs
- **ENVIRONMENT.md** - Python venv setup
- **VSCODE_TESTING_GUIDE.md** - VS Code pytest configuration

### Deprecated (Remove Later)
- ❌ PHASE_2_REALITY_CHECK.md (superseded by this definition)
- ❌ PHASE_2_TEST_PLAN.md (superseded - tests move to Phase 3)

---

## ✅ APPROVAL CRITERIA

### Phase 2 Approved When
- [x] All 7 components code complete
- [x] 200+ unit tests written
- [x] All tests passing
- [x] Components signal-connected
- [x] Documentation complete

**Status**: ✅ APPROVED - Moving to Phase 3

### Phase 3 Approved When (In Progress)
- [ ] Real LLM provider integration done
- [ ] Integration tests for component chains (5+)
- [ ] User acceptance tests (5+)
- [ ] Performance targets met (latency <100ms)
- [ ] Visual validation complete
- [ ] Documentation updated
- [ ] Ready for Phase 4 or MVP release

---

## 🎯 SUCCESS METRICS

### Phase 2 Success
✅ Code compiles and runs
✅ Unit tests all pass
✅ Coverage >85%
✅ No crashes in isolation

### Phase 3 Success
✅ Real LLM responses appear in chat
✅ Full workflows tested (clipboard→LLM→display)
✅ Performance <100ms trigger latency
✅ User can manually validate visuals
✅ All components work together
✅ Ready for production

---

**Next Step**: Resume Phase 3 Task #1+ with clear integration/UAT focus
