# 📅 PLAN D'ACTION: CETTE SEMAINE
## Quick Shortcut AI - Déblocage UAT en 1 Semaine

**Décision Requise**: Maintenant
**Timeline**: Lundi à Vendredi
**Objectif**: App stable prête pour UAT

---

## 🎯 STRATÉGIE CHOISIE: PATH 1 (Fix Python)

### Pourquoi cette approche?
- ✅ Fastest (1 week vs 3-4 weeks)
- ✅ Lowest risk (patterns proven)
- ✅ Keeps Python (your language)
- ✅ 80% code reused
- ✅ Clear fallback options

---

## 📋 CHECKLIST: AVANT DE COMMENCER

- [ ] Lu AUDIT_TECHNOLOGIQUE_COMPLET.md (15 min)
- [ ] Lu RESEARCH_EXECUTIVE_SUMMARY.md (5 min)
- [ ] Lu PRACTICAL_SOLUTIONS_CODE_SNIPPETS.md (20 min)
- [ ] Décidé: Go with Path 1? (Si OUI, continue)
- [ ] Git branch créée: `git checkout -b fix/hotkeys-threading`
- [ ] Python venv activé: `source venv/bin/activate` (ou Windows: `venv\Scripts\activate`)

---

## 📅 JOUR 1-2 (LUNDI-MARDI): FIX HOTKEYS

### Objectif
Remplacer `pynput` → `keyboard` library
Tester que les hotkeys marchent (menu apparaît)

### Tâches

#### 1.1 Remplacer dépendance
```bash
# 1. Uninstall pynput
pip uninstall pynput -y

# 2. Install keyboard
pip install keyboard

# 3. Update requirements.txt
# Remplacer la ligne:
#   pynput>=1.7.6
# par:
#   keyboard>=0.13.5

# 4. Vérifier
pip list | grep keyboard
```

#### 1.2 Refactoriser InputManager

**File: `src/core/input_manager.py`**

Tu as 2 options:

**Option A: Simple (Utilise keyboard library + hotkey texte)**
- Pros: Rapide à implémenter (1-2 heures)
- Cons: Perd détection Ctrl+Right-Click exact (utilise hotkey alternative)
- Code: Dans PRACTICAL_SOLUTIONS_CODE_SNIPPETS.md, section "InputManager"

**Option B: Avancé (Combine keyboard + pynput mouse pour Ctrl+Right-Click)**
- Pros: Garde exact Ctrl+Right-Click detection
- Cons: Légèrement plus complexe, mais même pattern
- Code: Dans PRACTICAL_SOLUTIONS_CODE_SNIPPETS.md, section "InputManagerAdvanced"

**Recommandation**: Essayer Option A d'abord. Si hotkey marche mais menu ne s'affiche pas, passer à Option B.

**Steps:**
1. Ouvre PRACTICAL_SOLUTIONS_CODE_SNIPPETS.md
2. Copie la classe InputManager (Option A ou B)
3. Remplace ENTIÈREMENT le contenu de src/core/input_manager.py
4. Sauvegarde

```bash
# Vérifier la syntaxe
python -m py_compile src/core/input_manager.py
# Si aucune erreur → OK!
```

#### 1.3 Tester les hotkeys

```bash
# 1. Lance l'app
python -m src.main

# 2. Dans une autre fenêtre (ex: Notepad)
# Presse: Ctrl+Shift+Right (selon InputManager code)

# Expected: Menu contextuel apparaît à la position de la souris

# 3. Teste aussi dans terminal
# Presse encore: Ctrl+Shift+Right
# Le app devrait refaire apparaître le menu
```

#### 1.4 Tests automatisés

```bash
# Run tests pour vérifier rien n'est cassé
pytest tests/test_core/test_input_manager.py -v

# Si tests échouent:
# - Vérifier imports (keyboard vs pynput)
# - Vérifier signal names (sig_shortcut_triggered, etc.)
# - Re-read PRACTICAL_SOLUTIONS_CODE_SNIPPETS.md
```

#### 1.5 Valider Jour 2

**Checklist Jour 2 end-of-day:**
- [ ] pynput uninstalled, keyboard installed
- [ ] src/core/input_manager.py refactorisé
- [ ] App lance sans erreur
- [ ] Hotkey testé manuellement → Menu apparaît
- [ ] pytest passe: `pytest tests/test_core/ -v`
- [ ] Commit: `git commit -m "fix: replace pynput with keyboard library"`

---

## 📅 JOUR 2-3 (MARDI-MERCREDI): FIX THREADING

### Objectif
Fixer le chat freeze lors streaming (Ctrl+Enter)
Tokens arrivent progressivement, UI responsive

### Problème Actuel

Dans `src/main.py`, la méthode `_stream_chat_response()` bloque le main thread:

```python
# ❌ WRONG (Actuel)
def _stream_chat_response(self):
    for token in self.provider.stream_chat(...):
        self.response_window.append(token)
        QApplication.processEvents()  # ← Insuffisant!
    # UI gelée jusqu'à fin du streaming
```

### Solution: QThread Worker Pattern

**File: `src/main.py`**

Tu as 2 classes à modifier/ajouter:

#### 2.1 Ajouter classe StreamingWorker

À ajouter dans `src/main.py` AVANT la classe `QuickShortcutApp`:

```python
from PySide6.QtCore import QThread, Signal, QObject

class StreamingWorker(QObject):
    """Worker to run LLM streaming in a separate thread"""

    # Signals (must be defined at class level)
    token_received = Signal(str)      # Emit when token arrives
    streaming_complete = Signal()     # Emit when done
    error_occurred = Signal(str)      # Emit on error

    def __init__(self, provider, messages, model):
        super().__init__()
        self.provider = provider
        self.messages = messages
        self.model = model
        self._is_stopped = False

    def stop(self):
        """Request worker to stop processing"""
        self._is_stopped = True

    def run(self):
        """Run streaming in worker thread"""
        try:
            logger.info("StreamingWorker: Starting...")
            token_count = 0

            for token in self.provider.stream_chat(self.messages, model=self.model):
                if self._is_stopped:
                    logger.info("StreamingWorker: Stopped by user")
                    break

                self.token_received.emit(token)
                token_count += 1

            logger.info(f"StreamingWorker: Complete ({token_count} tokens)")
            self.streaming_complete.emit()

        except Exception as e:
            if not self._is_stopped:
                logger.error(f"StreamingWorker error: {e}", exc_info=True)
                self.error_occurred.emit(str(e))
```

#### 2.2 Remplacer _stream_chat_response()

**Ancienne méthode (à supprimer):**
```python
def _stream_chat_response(self):
    # ❌ OLD CODE - DELETE THIS
```

**Nouvelle méthode (à ajouter):**

```python
def _stream_chat_response(self):
    """Stream response from LLM in a separate thread"""
    logger.info("Starting streaming (threaded)...")

    # Create worker
    worker = StreamingWorker(
        provider=self.provider,
        messages=self.chat_history,
        model=self.current_model
    )

    # Create thread and move worker to it
    thread = QThread()
    worker.moveToThread(thread)

    # Connect signals
    worker.token_received.connect(self._on_token_received)
    worker.streaming_complete.connect(self._on_streaming_complete)
    worker.error_occurred.connect(self._on_streaming_error)

    # Auto-cleanup thread when done
    thread.started.connect(worker.run)
    worker.streaming_complete.connect(thread.quit)
    worker.error_occurred.connect(thread.quit)

    # Store references (prevent garbage collection)
    self._streaming_thread = thread
    self._streaming_worker = worker

    # Start
    thread.start()
```

#### 2.3 Ajouter handlers pour les signals

```python
def _on_token_received(self, token: str):
    """Receive token from streaming worker"""
    try:
        # Update response window
        if self.response_window:
            self.response_window.append_token(token)

        # Force UI update
        QApplication.processEvents()

    except Exception as e:
        logger.error(f"Token handler error: {e}", exc_info=True)

def _on_streaming_complete(self):
    """Called when streaming finishes"""
    logger.info("Streaming complete")
    if self.response_window:
        self.response_window.on_streaming_complete()

    # Clean up
    if self._streaming_thread:
        self._streaming_thread.deleteLater()
        self._streaming_thread = None
    if self._streaming_worker:
        self._streaming_worker = None

def _on_streaming_error(self, error: str):
    """Called when streaming fails"""
    logger.error(f"Streaming error: {error}")
    if self.response_window:
        self.response_window.show_error(error)

    # Clean up
    if self._streaming_thread:
        self._streaming_thread.deleteLater()
        self._streaming_thread = None
```

#### 2.4 Initialiser variables

Dans `__init__` de QuickShortcutApp, ajoute:

```python
def __init__(self):
    # ... existing code ...

    # Streaming thread management
    self._streaming_thread = None
    self._streaming_worker = None
```

#### 2.5 Tester le streaming

```bash
# 1. Lance l'app
python -m src.main

# 2. Dans le chat window:
#    - Type: "Explique le concept de entanglement quantique en 2-3 phrases"
#    - Press: Ctrl+Enter

# Expected:
#    - UI RESTE RESPONSIVE (ne gèle pas)
#    - Tokens apparaissent graduellement (pas toute la réponse à la fin)
#    - Menu/settings clickable pendant qu'on streame

# 3. Si freezing persiste:
#    - Vérifier ResponseWindow.append_token() (ne doit pas bloquer)
#    - Vérifier que _on_token_received() est rapide
```

#### 2.6 Valider Jour 3

**Checklist Jour 3 end-of-day:**
- [ ] StreamingWorker classe ajoutée à src/main.py
- [ ] _stream_chat_response() refactorisée (utilise QThread)
- [ ] Handlers connectés (_on_token_received, etc.)
- [ ] App teste manuellement: Ctrl+Enter → UI responsive
- [ ] Tokens arrivent progressivement (pas gelé)
- [ ] pytest passe: `pytest tests/test_ui/ -v` (au minimum)
- [ ] Commit: `git commit -m "fix: implement proper QThread pattern for streaming"`

---

## 📅 JOUR 3-4 (MERCREDI-JEUDI): FIX AUTRES BUGS

### Objectif rapide
Corriger les 3 autres bugs sans rewrite complet:
1. Settings ferme l'app
2. Icône reste rouge
3. Menu non-clickable (peut-être fixé par path 1)

### 3.1 Bug #1: Settings ferme l'app

**File: `src/ui/settings_dialog.py`**

```python
# Problème: probable que closeEvent() ne return pas correctly
# ou parent/child relationship mal géré

# Solution simple:
class SettingsDialog(QDialog):  # ← Doit être QDialog, pas QWidget
    def closeEvent(self, event):
        """Handle close event properly"""
        # Ne pas appeler parent closeEvent qui fermerait l'app
        event.accept()  # Accepte fermeture du dialog UNIQUEMENT
        logger.info("SettingsDialog closed")
        self.reject()  # Ferme le dialog proprement
```

### 3.2 Bug #2: Icône rouge

**File: `src/services/health_check.py`**

```python
# Après qu'on change la config dans Settings,
# Health check doit se relancer

# Dans SettingsDialog.save_settings() ou OK button:
def on_settings_saved(self):
    """Relancer health check quand settings changent"""
    self.health_check_manager.run_check()  # Force re-check
    # Tray icon devrait s'actualiser
```

**File: `src/ui/tray_icon.py`**

```python
# Connecter signal de health_check
class TrayIcon(QSystemTrayIcon):
    def __init__(self, ...):
        # ... existing code ...

        # Connecter health_check results
        self.health_check_manager.check_complete.connect(self._on_health_check)

    def _on_health_check(self, result):
        """Update icon based on health check"""
        if result.is_healthy:
            self.setIcon(QIcon(":/icons/healthy.png"))  # Green
        else:
            self.setIcon(QIcon(":/icons/unhealthy.png"))  # Red
```

### 3.3 Bug #3: Menu non-clickable

Après keyboard library + QThread fix, tester si c'est fixé.
Si pas fixé, c'est probablement event propagation:

**File: `src/ui/floating_menu.py`**

```python
class MenuItem(QLabel):
    def mousePressEvent(self, event):
        """Handle click"""
        if event.button() == Qt.LeftButton:
            # Emit signal
            self.clicked.emit()
            event.accept()  # ← Important: accept() pour arrêter propagation
            # Ne pas appeler super().mousePressEvent()
```

---

## 📅 JOUR 4-5 (JEUDI-VENDREDI): UAT + POLISH

### Objectif
Tester complètement l'app
Petits fixes
Prête pour production

### Testing Checklist

- [ ] **Hotkeys**
  - [ ] Ctrl+Shift+Right → Menu apparaît
  - [ ] Clic sur menu item → Action exécutée
  - [ ] Menu ferme proprement

- [ ] **Streaming**
  - [ ] Chat: Tapez quelque chose
  - [ ] Ctrl+Enter → Réponse progressively
  - [ ] UI responsive pendant streaming
  - [ ] Peut fermer window sans crash

- [ ] **Settings**
  - [ ] Cliquer Settings → Dialog ouvre
  - [ ] Changer quelque chose (ex: Model)
  - [ ] Cliquer OK → Dialog ferme
  - [ ] App continue sans crash
  - [ ] Changement appris (ex: model change persiste)

- [ ] **Health Check**
  - [ ] Demarrage: couleur correcte (green/red)
  - [ ] Après settings change: couleur s'actualise
  - [ ] Click tray icon → Health status visible

- [ ] **Tests**
  - [ ] `pytest tests/ -v` passe
  - [ ] Coverage >= 89%
  - [ ] No warnings

### Commit & Push

```bash
# Jour 5 end-of-day:
git add -A
git commit -m "fix: hotkeys, threading, and minor UI bugs - UAT ready"
git push origin fix/hotkeys-threading

# Créer PR pour review
gh pr create --title "Fix critical UAT blockers" --body "..."
```

---

## ⚠️ TROUBLESHOOTING

### Si hotkeys ne marchent pas

**Symptôme**: Ctrl+Shift+Right n'appelle pas hotkey
**Causes possibles**:
1. keyboard library pas installed: `pip list | grep keyboard`
2. App pas en admin mode: Run as Administrator
3. Autre app a réservé le hotkey: Vérifier dans settings

**Fix**:
```bash
# Réinstaller proprement
pip uninstall keyboard -y
pip install keyboard
python -m src.main
```

### Si chat freeze persiste

**Symptôme**: Ctrl+Enter → UI gelée
**Causes possibles**:
1. StreamingWorker pas créé correctement
2. Signal `token_received` pas connecté
3. ResponseWindow.append_token() bloque

**Fix**:
```bash
# Vérifier les signals
python -c "from src.main import StreamingWorker; print(StreamingWorker.token_received)"

# Si erreur: recheck code copy-paste

# Sinon: add debug logs
# Dans _on_token_received():
# print(f"Token: {token[:20]}...")  # Vérifier que ça print rapidement
```

### Si Settings ferme l'app

**Symptôme**: Cliquer OK dans Settings → App entière ferme
**Causes possibles**:
1. SettingsDialog est QWidget au lieu QDialog
2. closeEvent() appelle sys.exit()
3. Parent/child issue

**Fix**:
```python
# Vérifier classe:
class SettingsDialog(QDialog):  # ← DOIT être QDialog

# Vérifier closeEvent:
def closeEvent(self, event):
    event.accept()
    self.reject()  # Ferme dialog uniquement
```

### Si pytest échoue

```bash
# Voir erreur complète
pytest tests/ -v --tb=short

# Si issue dans input_manager tests:
# Probablement keyboard vs pynput imports
# Vérifier que imports sont à jour

# Si issue dans UI tests:
# Vérifier que signals sont bien définies
```

---

## 📞 QUESTIONS?

Avant de demander:
1. Vérifier PRACTICAL_SOLUTIONS_CODE_SNIPPETS.md (code exact)
2. Vérifier RESEARCH_REPORT_ARCHITECTURE_ALTERNATIVES.md (context)
3. Vérifier ce fichier (checklist)

Si toujours bloqué:
- Créer issue dans git avec logs complets
- Pinger pour review

---

## 🚀 FIN DE SEMAINE: SUCCESS CRITERIA

**Vendredi 17h00 - App est PRÊTE si:**

- ✅ Hotkeys marchent (Ctrl+Shift+Right → Menu)
- ✅ Chat responsive (Ctrl+Enter → pas de freeze)
- ✅ Settings stable (OK → app continue)
- ✅ Icône correcte (green si config OK)
- ✅ Menu clickable (clic → action)
- ✅ Tests pass: `pytest tests/ -v`
- ✅ Zero crashes during 5-minute manual test
- ✅ Code committed et pushed

**Si tout green → 🎉 PRÊT POUR UAT LUNDI MATIN**

**Si encore 1-2 bugs → FALLBACK TO REWRITE**
- Dimanche: Start Electron rewrite
- 2-3 semaines: Production ready

---

## 📊 TIMELINE VISUEL

```
LUNDI      MARDI      MERCREDI   JEUDI      VENDREDI
├─ DAY 1-2 ├─ DAY 2-3 ├─ DAY 3-4 ├─ DAY 4-5 ├─ FINAL
│          │          │          │          │
Hotkeys    Threading  Bug fixes  UAT        ✅ Ready
├─ Replace ├─ Add     ├─ Settings├─ Test    │
│ pynput   │ QThread  │ dialog   │ complete │
│          │          │          │          │
│ ✓ Test   │ ✓ Test  │ ✓ Test   │ ✓ pytest │
│ hotkeys  │ streaming│ fixes    │ pass     │
└──────────└──────────└──────────└──────────└─

SUCCESS ENDPOINT: Friday 5 PM - App Production Ready
```

---

## 🎁 BONUS: QUICK START AFTER THIS WEEK

Une fois UAT passée:

```bash
# Build standalone exe
pip install nuitka
python -m nuitka --onefile --windows-icon=icon.ico src/main.py

# Result: quick-shortcut.exe (50 MB, standalone)
# Distributable sans Python installed
```

---

**Ready to start? Open PRACTICAL_SOLUTIONS_CODE_SNIPPETS.md NOW and begin Day 1! 🚀**

