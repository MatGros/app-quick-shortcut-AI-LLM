# 🐛 Issues Found During UAT - 2026-02-17

**Status**: Documenting issues for fixes

---

## 🔴 CRITICAL BUGS (Block Usage)

### Issue #1: Chat Messages Don't Get Responses
**Severity**: CRITICAL
**User Report**: "J'envoie un message il s'efface quand j'appuie sur send, mais je n'ai pas de réponse"

**Root Cause**:
- Response window emits signal `sig_input_submitted` when Send clicked
- **BUT NO ONE LISTENS TO THIS SIGNAL in main.py**
- Message is erased but no LLM request is made

**Current Code Flow**:
```python
# response_window.py - _on_send_clicked()
self.sig_input_submitted.emit(text)  # Signal emitted
self.text_input.clear()               # Text erased
# ↓
# main.py - NOTHING CONNECTED!  ← BUG
```

**Fix Required**:
- Connect `sig_input_submitted` to handler in main.py
- Handler should: get message → send to LLM → stream response

---

### Issue #2: Floating Menu Unclickable
**Severity**: CRITICAL
**User Report**: "le menu contextuel est grisé, peu visible et pas cliquable"
**Also**: "on voit le menu contextuel Windows en même temps"

**Problems**:
1. Menu items are QLabel widgets - may not handle clicks properly
2. System context menu appears on top
3. Items appear grayed out / low contrast

**Fix Required**:
- Make menu items properly clickable (use custom widget or enhance QLabel)
- Hide Windows context menu when Ctrl+Right-Click pressed
- Improve visual contrast and styling

---

### Issue #3: Settings Dialog Closes Entire Application
**Severity**: CRITICAL
**User Report**: "l'application ferme les paramètres ou la config l'application alors qu'elle devrait tourner en fond"

**Expected**: Settings dialog closes, app stays running in tray
**Actual**: Settings dialog closes = app closes entirely

**Root Cause**: Likely an issue with window close behavior or parent-child relationship

**Fix Required**:
- Settings should be modal but NOT close main app
- App should continue running in background

---

## 🟠 IMPORTANT UX ISSUES

### Issue #4: Keyboard Input in Chat (Ctrl+Enter)
**User Report**: "il serait bien d'avoir la commande Ctrl plus Enter pour faire send"

**Current**: Only "Send" button works
**Desired**: Ctrl+Enter or just Enter sends message

**Fix Required**:
- Handle key press event in response_window
- Ctrl+Enter (or Enter) sends message

---

### Issue #5: Settings Button Clarity
**User Report**: "Il y a des boutons comme Apply et Save Provider... peut-être mettre une petite disquette icône"

**Problem**: Confusion between:
- "Apply" (general settings)
- "Save Provider" (provider-specific)
- "OK" (save and close)

**Fix Required**:
- Add icons to buttons
- Simplify button logic or better labels

---

### Issue #6: Icon Color at Startup
**User Report**: "L'icône peut être ROUGE ou JAUNE... cependant l'icône est toujours vert même après supprimer config"

**Expected**: Red/Yellow if no config → Green if configured
**Actual**: Always green

**Root Cause**: Health check may be passing even without config

**Fix Required**:
- Improve health check logic
- Show RED icon if no provider configured
- Show YELLOW while checking
- Show GREEN if ready

---

## 🟡 MISSING FEATURES / SHORTCUTS

### Issue #7: Ctrl+H (History) Not Working
**User Report**: "Le CTRL H Pour voir l'historique ne fonctionne pas"

**Status**: Feature not implemented yet
**Fix Required**: Implement history view (future phase)

---

### Issue #8: Replace Ctrl+, Shortcut
**User Report**: "le contrôle coma faudra le remplacer par une autre touche parce que je sais pas ce que c'est"

**Current**: Ctrl+, (comma) is bound to something unclear
**Fix Required**:
- Document or change this shortcut
- Suggest: Ctrl+M (for menu), Ctrl+C (for config), etc.

---

## 📊 Fix Priority Order

1. **CRITICAL - Fix Chat Input Handler** (Issue #1)
   - Without this, chat is completely broken

2. **CRITICAL - Fix Floating Menu Click** (Issue #2)
   - Without this, menu can't be used

3. **CRITICAL - Fix Settings Dialog Closing App** (Issue #3)
   - Without this, can't change settings

4. **IMPORTANT - Keyboard Input (Ctrl+Enter)** (Issue #4)
   - Better UX for chat

5. **IMPORTANT - Settings Buttons Clarity** (Issue #5)
   - UX improvement

6. **IMPORTANT - Health Check Logic** (Issue #6)
   - Better startup feedback

7. **FUTURE - History Feature** (Issue #7)
   - Phase 4 feature

8. **LOW - Shortcut Documentation** (Issue #8)
   - Documentation/config update

---

## Next Steps

1. Fix Issue #1: Connect signal handler
2. Fix Issue #2: Improve menu interaction
3. Fix Issue #3: Settings dialog lifecycle
4. Improve Issues #4-6
5. Re-test all functionality
