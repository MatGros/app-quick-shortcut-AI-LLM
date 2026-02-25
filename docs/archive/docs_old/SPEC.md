# Spécifications Techniques — Quick Shortcut AI LLM Assistant

## NOTA BENE (UTILISATION)

> **Règle de maintenance :** Si une fonctionnalité (feature) disparaît ou est retirée, **ne pas supprimer** son texte ou son ID. À la place, **barrer le texte** (ex: `~~[F-00] Fonctionnalité obsolète~~`) pour conserver l'historique des spécifications.

---

## VUE D'ENSEMBLE

| Champ                | Valeur                                                 |
| :------------------- | :----------------------------------------------------- |
| **Nom**              | Quick Shortcut AI LLM Assistant                        |
| **Langage**          | Python 3.10+                                           |
| **Framework**        | PySide6-Essentials (Qt 6.x)                            |
| **Plateforme**       | Windows 10 (1809+), Windows 11 (x64)                   |
| **Licence**          | GPL-3.0-only                                           |
| **Backend LLM**      | Ollama, OpenAI, Anthropic, OpenRouter (multi-provider) |
| **GUI**              | Qt frameless windows avec QSS styling                  |
| **Système d'entrée** | Hooks natifs (pynput) - Pas de dépendance AutoHotkey   |
| **Base de données**  | SQLite 3 (historique, logs)                            |
| **Configuration**    | JSON dans `%APPDATA%\QuickShortcutAI\`                 |
| **Packaging**        | Nuitka (exe standalone < 50MB)                         |

---

## SOMMAIRE DES FONCTIONNALITÉS

> **Légende Statut :** 📋 Planifiée · 🚧 En cours · ✅ Déployée

| ID       | Fonctionnalité                | Description                                                  | Priorité | Statut |
| :------- | :---------------------------- | :----------------------------------------------------------- | :------- | :----: |
| **F-01** | Hooks Globaux (Input Manager) | Détection native Ctrl+Clic Droit sans AHK                    | P0       |   📋   |
| **F-02** | Menu Contextuel Frameless     | Fenêtre flottante moderne avec animations                    | P0       |   📋   |
| **F-03** | Abstraction LLM Providers     | Interface unifiée pour Ollama, OpenAI, Anthropic, OpenRouter | P0       |   📋   |
| **F-04** | Chat & Inline Response        | Fenêtre chat ET popup inline auto-resize près de la souris   | P0       |   📋   |
| **F-05** | Gestion Clipboard             | Lecture/écriture robuste (texte + images)                    | P1       |   📋   |
| **F-06** | Auto-Paste                    | Collage automatique avec gestion focus intelligente          | P1       |   📋   |
| **F-07** | Capture d'Écran + Vision      | Sélection région avec intégration Vision API                 | P1       |   📋   |
| **F-08** | Notifications Toast           | Notifications custom Qt (pas Windows natives)                | P1       |   📋   |
| **F-09** | Historique SQLite             | Recherche, export, statistiques                              | P1       |   📋   |
| **F-10** | Interface Settings            | Configuration multi-tabs (providers, shortcuts, apparence)   | P0       |   📋   |
| **F-11** | Health Checks                 | Vérifications démarrage (config, LLM, permissions)           | P0       |   📋   |
| **F-12** | Système Thèmes                | Dark/Light mode avec QSS dynamique                           | P1       |   📋   |
| **F-13** | Raccourcis Clavier            | Customisables avec détection conflits                        | P0       |   📋   |
| **F-14** | Tray Icon                     | Intégration system tray avec états                           | P1       |   📋   |
| **F-15** | Prompts Personnalisés         | Templates avec variables et substitution                     | P1       |   📋   |
| **F-16** | Rendu Markdown                | Markdown → HTML avec syntax highlighting                     | P1       |   📋   |
| **F-17** | Copy Response                 | Export plain text, markdown, rich HTML                       | P1       |   📋   |
| **F-18** | Retry Mechanism               | Relance requête avec gestion erreurs                         | P1       |   📋   |
| **F-19** | Chat Context Management       | Conversations multi-tours avec gestion contexte              | P1       |   📋   |
| **F-20** | Portable Mode                 | Exe standalone sans installation Python                      | P0       |   📋   |

---

## DESIGN SYSTEM & GUIDE ESTHÉTIQUE

### 🎨 Principes de Design

**Modernité Absolue :**

- ❌ Pas de menus systèmes Windows (ternes, datés)
- ❌ Pas de MsgBox/InputBox standards
- ✅ Tous les composants custom-stylés (QSS)
- ✅ Frameless windows avec ombres portées
- ✅ Animations fluides sur TOUS les éléments

**Fluidité Extrême :**

- Latence perceptible : < 100ms (critère non-négociable)
- Animations 60 FPS minimum
- Scroll parfaitement smooth
- Transitions ease-out (naturel)
- Aucun lag ou micro-stuttering

**Beauté Intemporelle :**

- Palette minimaliste (2-3 couleurs principales)
- Espacement cohérent (8px grid system)
- Typographie claire (Segoe UI ou Inter)
- Aucun skeuomorphisme dépassé
- Design épuré comme macOS/iOS moderne

### 📐 Grid System & Spacing

**Base Unit : 8px**

```
Spacing: 8px, 16px, 24px, 32px, 48px
Padding: 12px, 16px, 20px
Gaps: 8px, 12px, 16px
Radius: 4px (petit), 8px (menu), 12px (cards)
```

### 🎯 Palette Couleurs

**Dark Mode (Par défaut) :**

```css
Primary BG:    #1a1a1a  /* Presque noir, pas pur #000 */
Secondary BG:  #2d2d2d  /* Cards, hover areas */
Tertiary BG:   #3a3a3a  /* Borders, separators */
Text Primary:  #ffffff  /* Blanc pur */
Text Secondary:#b0b0b0  /* Gris clair pour hints *)
Accent:        #0066ff  /* Bleu vibrant pour actions *)
Success:       #10b981  /* Vert pour confirmations *)
Error:         #ef4444  /* Rouge pour erreurs */
Warning:       #f59e0b  /* Ambre pour warnings *)
```

**Light Mode :**

```css
Primary BG:    #ffffff  /* Blanc pur *)
Secondary BG:  #f3f4f6  /* Gris très clair *)
Tertiary BG:   #e5e7eb  /* Gris pour borders *)
Text Primary:  #1f2937  /* Gris très foncé *)
Text Secondary:#6b7280  /* Gris moyen *)
Accent:        #0066ff  /* Bleu (identique *)
```

### ✍️ Typographie

**Font Stack :**

```css
Primary:   'Segoe UI', 'Inter', -apple-system, sans-serif
Monospace: 'Fira Code', 'Courier New', monospace
```

**Sizes & Weights :**

```
Titles:      14-16px, weight 600 (semi-bold)
Body:        13px, weight 400 (regular)
Hints:       12px, weight 400 (regular, lighter color)
Code:        12px, monospace, weight 500
```

### 🎬 Animations Standardisées

**Duration :**

```
Micro:   100ms  (tooltips, state changes)
Quick:   200ms  (menu open, dialog appear)
Normal:  300ms  (transitions, major moves)
Slow:    500ms  (page transitions, only if necessary)
```

**Easing Curves :**

```
Intro:    QEasingCurve.OutCubic    (smooth, natural)
Outro:    QEasingCurve.OutCubic    (consistent)
Bounce:   QEasingCurve.OutBack     (playful, if needed)
Never:    QEasingCurve.Linear      (avoid - feels mechanical)
```

**Examples :**

```python
# Menu fade-in
anim = QPropertyAnimation(self, b"windowOpacity")
anim.setDuration(200)
anim.setStartValue(0.0)
anim.setEndValue(1.0)
anim.setEasingCurve(QEasingCurve.OutCubic)
anim.start()

# Button hover
button.setStyleSheet("""
    QPushButton {
        background-color: #0066ff;
        transition: background-color 150ms;
    }
    QPushButton:hover {
        background-color: #0052cc;
    }
""")
```

### 🪟 Composants Custom

**Buttons :**

- Minimum 40px height (touch-friendly)
- Padding: 12px 24px
- Radius: 6px
- Hover: Légère opacité ou changement couleur
- Active: Couleur plus saturée
- Disabled: Gris pâle, curseur désactivé

**Text Fields :**

- Padding: 12px
- Radius: 6px
- Border: 1px, couleur tertiary
- Focus: Border accent (#0066ff)
- Transition: 150ms smooth

**Modals & Dialogs :**

- Shadow: `0 20px 25px -5px rgba(0, 0, 0, 0.3)` (dark) / lighter version (light)
- Backdrop: Semi-transparent (#000 @ 30% ou #000 @ 10% light)
- Animation: Slide-up + fade-in 200ms
- Close: Touche Esc, click backdrop (si permettable)

**Cards & Containers :**

- Padding: 20px
- Radius: 8px
- Border: Subtle line ou ombre douce
- Hover: Ombre légèrement augmentée (micro-interaction)

### 🌓 Dark/Light Transition

**Switching :**

- Instantané (pas de cross-fade pour eviter flashing)
- QApplication.setStyleSheet() appliqué globalement
- Tous les windows reçoivent le nouvel apparence

**System Detection :**

- Windows Registry : `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize`
- Clé : `AppsUseLightTheme` (1=light, 0=dark)
- Detect au démarrage, monitorer pour auto-switch

---

## DÉTAIL DES FEATURES

### [F-01] Hooks Globaux (Input Manager) — P0

**Objectif** : Intercepter `Ctrl+Clic Droit` globalement sans dépendance AutoHotkey.

**Architecture Technique:**

- **Classe** : `InputManager(QObject)` dans `src/core/input_manager.py`
- **Bibliothèque** : `pynput>=1.7.6` pour hooks bas niveau
- **Thread** : QThread dédié pour listener (non-bloquant)
- **Signaux** :
  - `sig_context_menu_requested(int x, int y)` — Menu contextuel
  - `sig_text_selected(str text)` — Texte sélectionné détecté

**Implémentation:**

```python
class InputManager(QObject):
    sig_context_menu_requested = Signal(int, int)
    sig_text_selected = Signal(str)

    def start_listening(self):
        """Démarrer écoute globale en QThread"""
        self._listener_thread = QThread()
        self.moveToThread(self._listener_thread)
        self._listener_thread.start()

    def stop_listening(self):
        """Arrêt propre du listener"""
```

**Déclencheur** :

- Trigger : `Ctrl + Clic Droit` (event release, pas press)
- Latence cible : < 50ms signal → UI
- Gestion état clavier/souris pour éviter faux positifs

**Performance Critiques:**

- QThread worker avec pynput.mouse.Listener
- Pas de blocking calls dans main thread
- Debounce 50ms pour éviter doubles-trigger

---

### [F-02] Menu Contextuel Frameless — P0

**Objectif** : Afficher menu d'actions moderne et fluide à la position du curseur.

**Design Visual Exceptionnel:**

- **Fenêtre** : `QWidget` avec flags `Qt.FramelessWindowHint + Qt.WindowStaysOnTopHint + Qt.NoDropShadowWindowHint`
- **Apparence** :
  - Coins arrondis : `border-radius: 8px` (smooth, modern)
  - Ombre portée : `QGraphicsDropShadowEffect(blur=20px, offset=0, color=#000@40%)`
  - Fond :
    - Dark: `#2d2d2d` avec border subtle `#444`
    - Light: `#ffffff` avec border `#e5e7eb`
  - Backdrop blur (si Windows 11) : Acrylic effect
  - Fade-in : `QPropertyAnimation(opacity, 0→1)` 200ms OutCubic

- **Layout** : VBox d'actions
  - Spacing: 4px entre items
  - Padding: 8px (top/bottom), 12px (left/right)
  - Max width: 280px
  - Max height: 600px avec QScrollArea si besoin

**Interactions Fluides:**

- **Hover Effect** :
  - Background change: `#3a3a3a` (dark) ou `#f3f4f6` (light)
  - Transition: 150ms QEasingCurve.OutCubic
  - Légère translation : +2px vers droite
  - Ombre augmente légèrement

- **Animations** :
  - Slide-in depuis position curseur (200ms OutCubic)
  - Hover actions glissent légèrement (50ms OutCubic)
  - Sortie : fade-out + scale down (150ms OutCubic)

- **Visual Polish** :
  - Icons: 24px, sharp & clear (emoji ou SVG coloré)
  - Text: Segoe UI 13px, color #ffffff (dark)
  - Séparateurs: Ligne subtile `#3a3a3a` avec padding 8px
  - État désactivé: Gris pâle #6b7280 avec opacity 0.5

**Fonctionnalités:**

1. **Actions Affichées** :
   - 📝 Summarize — Résumer texte sélectionné
   - 🌐 Translate — Traduire en français/anglais
   - ✍️ Custom Prompt — Question libre sur texte
   - 📸 Screenshot — Capture écran (Vision API)
   - 💬 Chat — Conversation directe sans sélection

2. **Navigation Clavier** :
   - `↑↓` : Navigation actions
   - `Enter` : Sélectionner
   - `Esc` : Fermer
   - Lettres soulignées : Accès direct (ex: `S` pour Summarize)

3. **Positionnement Intelligent** :
   - Affichage à position curseur
   - Détection bords écran (réajustement auto si hors écran)
   - Support multi-monitors
   - Max height 600px avec scrollbar si besoin

4. **Recherche Rapide** (optionnel):
   - Search bar en haut
   - Fuzzy matching sur noms actions
   - Filtrage en temps réel

**Performance:**

- Affichage < 100ms après trigger
- Pas de lag sur navigation clavier
- Smooth animations à 60 FPS

---

### [F-03] Abstraction LLM Providers — P0

**Objectif** : Support unifié de multiples providers LLM.

**Architecture Pattern:**

```python
# Interface abstraite
from abc import ABC, abstractmethod
from typing import List, Dict, Generator

class LLMProvider(ABC):
    @abstractmethod
    def stream_chat(self, messages: List[Dict], model: str,
                   temperature: float = 0.7, **kwargs) -> Generator[str, None, None]:
        """Streaming chat completion"""

    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Lister modèles disponibles"""

    @abstractmethod
    def health_check(self, timeout: int = 5) -> bool:
        """Test connectivité provider"""

    @abstractmethod
    def supports_vision(self) -> bool:
        """Vérifie support images/vision"""
```

**Factory Pattern:**

```python
class LLMProviderFactory:
    @staticmethod
    def create(provider_type: str, config: dict) -> LLMProvider:
        mapping = {
            'ollama': OllamaProvider,
            'openai': OpenAIProvider,
            'anthropic': AnthropicProvider,
            'openrouter': OpenRouterProvider
        }
        return mapping[provider_type](**config)
```

**Implémentations Requises:**

1. **OllamaProvider** (`src/core/ollama_provider.py`)
   - Endpoint : `{base_url}/api/chat`
   - Défaut local : `http://localhost:11434`
   - Auth : Bearer token optionnel
   - Vision : Support llama3.2-vision, llava
   - Format réponse : `{"message": {"content": "..."}}`

2. **OpenAIProvider** (`src/core/openai_provider.py`)
   - Endpoint : `https://api.openai.com/v1/chat/completions`
   - Auth : Header `Authorization: Bearer <api_key>`
   - Vision : gpt-4-vision, gpt-4o
   - Format : Standard OpenAI chat completion

3. **AnthropicProvider** (`src/core/anthropic_provider.py`)
   - Endpoint : `https://api.anthropic.com/v1/messages`
   - Auth : Header `x-api-key`
   - Vision : claude-3-opus, sonnet, haiku
   - Format : Anthropic messages API

4. **OpenRouterProvider** (`src/core/openrouter_provider.py`)
   - Endpoint : `https://openrouter.ai/api/v1/chat/completions`
   - Auth : Bearer token
   - Vision : Provider-dependent
   - Format : OpenAI compatible

**Gestion Erreurs:**

- Timeout : 30s par défaut (configurable)
- Rate limits : Retry exponential backoff
- Auth invalide : Clear error message
- API down : Fallback à provider suivant si multi-provider

---

### [F-04] Fenêtre Chat Streaming — P0

**Objectif** : Single-instance window affichant réponses LLM fluide, moderne, agréable.

**Pattern Singleton:**

```python
class ResponseWindow(QWidget):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

**Design Visuel Moderne:**

- **Window** : Frameless (Qt.FramelessWindowHint) avec drag-to-move sur title bar
- **Size** : 800x600px default, min 400x300px, max-resizable
- **Padding** : 16px tout autour
- **Radius** : 12px corners
- **Shadow** : QGraphicsDropShadowEffect (blur=25px, offset=0, color=#000@35%)
- **Background** :
  - Dark: `#1a1a1a` gradient subtle vers `#242424`
  - Light: `#ffffff` avec subtle border `#e5e7eb`

**Composants UI Sophistiqués:**

1. **Chat Area** : QTextEdit read-only avec bubbles élégantes
   - **User Messages** :
     - Alignement droite, max width 70%
     - Background: `#0066ff` (accent color)
     - Padding: 12px 16px
     - Radius: 12px (rond coin droit, moins arrondi gauche)
     - Text: Blanc #ffffff
     - Animation: Slide-in from right 300ms OutCubic

   - **Assistant Messages** :
     - Alignement gauche, max width 85%
     - Background: `#3a3a3a` (dark) ou `#f3f4f6` (light)
     - Padding: 12px 16px
     - Radius: 12px (moins arrondi côté droit, arrondi côté gauche)
     - Text: `#ffffff` (dark) ou `#1f2937` (light)
     - Animation: Slide-in from left 300ms OutCubic, token-par-token typing effect

   - **Spacing** : 12px gap entre messages
   - **Auto-scroll** : Smooth scroll vers derniers messages
   - **User Scroll Detection** : Arrêt auto-scroll si user scrolle up (UX respectueuse)
   - **Scrollbar** : Custom stylé, mince (6px), hover effect

2. **Input Box** : Auto-expanding avec placeholder stylé
   - **Baseline** : 40px (1 ligne)
   - **Max** : 200px (5 lignes)
   - **Padding** : 12px
   - **Radius** : 8px
   - **Border** : 1px `#444` (dark) / `#e5e7eb` (light)
   - **Focus** : Border change to `#0066ff`, shadow subtil bleu
   - **Placeholder** : `#6b7280` italique, fade on type
   - **Expansion** : Smooth height transition (150ms) quand texte ajouté
   - **Manual Resize** : Drag bottom-right corner (cursor change)

3. **Toolbar** (haut de window) :
   - Height: 44px
   - Layout: Left-align title, Right-align buttons
   - Title: "Chat" ou "[Model Name]" - Segoe UI 13px semi-bold
   - Buttons (right):
     - ⏹️ Stop (rouge si streaming, gris sinon)
     - 📋 Copy (bleu hover)
     - ⚙️ Settings (gris)
     - History toggle
   - Spacing: 8px entre boutons
   - Buttons: 32px square, radius 6px, padding 6px icon
   - Hover: Background change, transition 150ms

4. **Status Bar** (bas) :
   - Height: 28px
   - Background: Subtil séparation `#2d2d2d` (dark)
   - Layout: Left (info), Right (stats)
   - Info: "Ollama • gemma3:4b" - Segoe UI 12px grey
   - Stats: "1,234 tokens • 2.5s"
   - Subtle border top

**Streaming Display Fluide:**

- Token buffering : Accumule tokens 50ms avant update (smooth, pas de flicker)
- Typewriter effect : Apparence progressive sans "jump"
- Markdown rendering : Code blocks avec syntax coloring
- Smooth line wrapping
- Cursor clignotant si génération en cours (subtle animation)

**Performance Targets:**

- Premier token → affichage : < 200ms (CRITIQUE pour perceptio de rapidité)
- Streaming fluide : 60 FPS (no stuttering)
- Scroll performance : Instant même 10k tokens
- Memory: Limit last 100 messages in memory (older = loaded from history)

**Streaming Display:**

- Token buffering : Accumule 50ms de tokens avant update UI
- Smooth append : Utilise QTimer pour batch updates
- Typewriter effect : Apparence progressive sans flashing
- Markdown rendering : Voir F-16

**Performance Targets:**

- Premier token → affichage : < 200ms
- Streaming fluide : 60 FPS
- Scroll performance : Pas de lag même réponses 10k tokens

---

### [F-05] Gestion Clipboard — P1

**Objectif** : Lire/écrire clipboard robustement (texte + images).

**Classe** : `ClipboardManager(QObject)` dans `src/core/clipboard_manager.py`

```python
class ClipboardManager(QObject):
    sig_clipboard_changed = Signal(object)  # ClipboardData

    def get_text(self, retry: int = 3) -> str:
        """Get texte avec retry logic"""
        for attempt in range(retry):
            try:
                return QApplication.clipboard().text()
            except:
                QThread.msleep(50)
        raise ClipboardError("Failed to read clipboard")

    def set_text(self, text: str):
        """Set texte dans clipboard"""

    def get_image(self) -> QImage:
        """Get image du clipboard"""

    def set_image(self, image: QImage):
        """Set image dans clipboard"""

    def monitor_clipboard(self, enabled: bool = True):
        """Monitor changements clipboard avec debounce 100ms"""
```

**Format Support:**

- Plain text : UTF-8
- HTML : Rich formatting
- Images : PNG, JPEG, BMP
- Retry logic : 3 tentatives avec 50ms delay

---

### [F-06] Auto-Paste — P1

**Objectif** : Coller automatiquement réponse dans l'app active.

**Classe** : `AutoPaster` dans `src/core/auto_paster.py`

```python
class AutoPaster(QObject):
    def __init__(self):
        self._original_hwnd = None  # Windows handle
        self._keyboard = Controller()
        self._config = ConfigService()

    def store_active_window(self):
        """Capture fenêtre active (Win32 API via ctypes)"""

    def paste_to_original(self, text: str, delay_ms: int = 100):
        """
        1. Set focus sur fenêtre originale
        2. Attendre delay_ms
        3. Simuler Ctrl+V ou typage direct
        """
```

**Implementation Details:**

- Window handle : `ctypes.windll.user32.GetForegroundWindow()`
- Set focus : `SetForegroundWindow(hwnd)`
- Delay : Configurable (100ms default, évite timing issues)
- Simulation : `pynput.keyboard.Controller` pour Ctrl+V
- Error handling : Fallback si focus fail (notification user)

**Configuration:**

- `auto_paste_enabled` : bool
- `auto_paste_delay_ms` : int (50-500ms)

---

### [F-07] Capture d'Écran + Vision — P1

**Objectif** : Capturer région écran et intégrer Vision API.

**Classe** : `ScreenshotTool` dans `src/ui/screenshot_tool.py`

**Modes de Capture:**

1. **Full Screen** : Entire monitor
2. **Region Selection** : UI interactive overlay
   - Semi-transparent gray overlay
   - Draggable rectangle (highlight)
   - Coordinate display
   - Esc to cancel, Enter to confirm
3. **Active Window** : Capture fenêtre active
4. **Clipboard** : Image existante dans clipboard

**Region Selection UI:**

- QWidget overlay fullscreen semi-transparent
- Mouse drag pour sélectionner région
- Affichage dimensions en temps réel
- Keyboard : Esc cancel, Enter confirm

**Vision API Integration:**

- Format image : PNG pour transmission
- Conversion base64 : `base64.b64encode(png_bytes)`
- Format par provider :
  - **Anthropic** :
    ```json
    {
      "type": "image",
      "source": { "type": "base64", "media_type": "image/png", "data": "..." }
    }
    ```
  - **OpenAI** :
    ```json
    { "type": "image_url", "image_url": { "url": "data:image/png;base64,..." } }
    ```
  - **Ollama** :
    ```json
    { "images": ["base64_string"] }
    ```

---

### [F-08] Notifications Toast — P1

**Objectif** : Notifications custom Qt ultra-fluides et élégantes (PAS Windows natives).

**Classe** : `ToastNotification(QWidget)` dans `src/ui/toast_notification.py`

**Design Premium:**

- **Position** : Bottom-right corner, 24px from edges
- **Size** : 320px width, 68px height (+ icon/close), max 200px text
- **Stacking** : Vertical avec 12px gap (nouvelles au top)
- **Padding** : 16px
- **Radius** : 8px (modern rounded corners)
- **Shadow** : Subtle drop shadow (blur=15px, offset=0, color=#000@30%)
- **Border** : Subtle 1px line matching color (pour definition)

**Types avec Esthétique Moderne:**

| Type           | BG Color  | Icon | Text Color | Animation                     |
| :------------- | :-------- | :--- | :--------- | :---------------------------- |
| ✅ **Success** | `#10b981` | ✓    | `#ffffff`  | Slide-in right + bounce 300ms |
| 🔵 **Info**    | `#3b82f6` | ℹ    | `#ffffff`  | Slide-in right 250ms smooth   |
| ⚠️ **Warning** | `#f59e0b` | !    | `#ffffff`  | Slide-in right 250ms          |
| ❌ **Error**   | `#ef4444` | ✗    | `#ffffff`  | Slide-in right + pulse 300ms  |

**Composants:**

- **Icon** : 24px, left side, padding 8px right
- **Text** : Segoe UI 13px, semi-bold, truncate if long
- **Close Button** : ✕ 16px top-right, hover highlight, fade on hover
- **Dismiss Animation** : Fade-out + slide-out right 200ms OutCubic
- **Auto-dismiss** : 3000ms default (configurable)
- **Progress Bar** (optionnel) : Thin line at bottom showing remaining time

**Interactive:**

- Hover : Slight lift (shadow increase), opacity boost
- Click : Dismiss immediately, emit signal
- Keyboard : Esc key dismisses all toasts

**Example Advanced:**

```python
# Success avec auto-dismiss rapide
NotificationService.show_toast(
    message="✨ Copied to clipboard!",
    type="success",
    duration_ms=2000,
    show_progress=True,
    callback=lambda: print("Dismissed")
)

# Error persistant jusqu'à close
NotificationService.show_toast(
    message="❌ API Connection Failed - Click to retry",
    type="error",
    duration_ms=0,  # Manuel close only
    dismissible=True
)
```

---

### [F-09] Historique SQLite — P1

**Objectif** : Stocker et rechercher conversations.

**Schéma Database:**

```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    context_text TEXT,
    action_type TEXT,  -- 'summarize', 'translate', 'custom'
    tokens_used INTEGER,
    response_time_ms INTEGER
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    role TEXT NOT NULL,  -- 'system', 'user', 'assistant'
    content TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

CREATE INDEX idx_conversations_timestamp ON conversations(timestamp DESC);
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_timestamp ON messages(timestamp DESC);
```

**Classe** : `HistoryService` dans `src/services/history_service.py`

```python
class HistoryService:
    def save_conversation(self, conv: Conversation):
        """Save to SQLite"""

    def search(self, query: str) -> List[Conversation]:
        """Full-text search"""

    def get_statistics(self) -> Dict:
        """Tokens count, avg response time, etc."""

    def export_json(self, conversation_id: int) -> str:
        """Export conversation as JSON"""

    def export_markdown(self, conversation_id: int) -> str:
        """Export as Markdown (user > assistant > user...)"""
```

**Features:**

- Full-text search sur content
- Filtrage par date range
- Statistiques : token count, response times
- Export JSON/Markdown
- Retention configurable (défaut 90 jours)

---

### [F-10] Interface Settings — P0

**Objectif** : Configuration moderne et intuitive dans dialog élégant.

**Classe** : `SettingsDialog(QDialog)` dans `src/ui/settings_dialog.py`

**Design Global:**

- **Window** : Frameless, 900x600px, shadow=20px
- **Title Bar** : 44px avec icon + title "Settings"
- **Layout** : Left sidebar + main content area
- **Sidebar** : 220px width, tabs as list (icon + text)
  - Background: `#2d2d2d` (dark) / `#f9fafb` (light)
  - Selected: Highlight avec background accent + left border bleu
  - Hover: Subtle background change
  - Icons: 20px colorful (differ par tab)
- **Buttons** (bas) : Cancel (gris), Save (bleu accent)
  - Spacing: 8px
  - Size: 36px height

**Tabs Détaillés:**

**1. Providers Tab** 🔗

- List de providers (scrollable)
- Item layout : Icon + Name + Status indicator
  - Connected: 🟢 Green
  - Error: 🔴 Red
  - Hover: Background change, "Edit/Delete" buttons appear
- Action buttons : Add (+ icon), Edit, Delete, Test
- Test Connection UI :
  - Opens mini dialog
  - Progress spinner (animated)
  - Result: ✅ Connected ou ❌ Failed with error message
  - Close auto après success, ou click OK

**2. Shortcuts Tab ⌨️**

- List : Icon | Action Name | Current Binding | Reset button
- Hover sur item : Edit button appears
- Click Edit :
  - Dialog "Record Shortcut"
  - Text: "Press your key combination..."
  - Visual feedback: Keys pressed display in real-time
  - Conflict warning: If conflict detected (bold red)
  - Buttons: OK (save), Cancel, Reset to Default
- Animation: Items fade-in staggered

**3. Appearance Tab 🎨**

- Theme selector : Radio buttons (Dark / Light / System auto)
  - Preview: Show color swatch
  - Immediate apply (no restart)
- Font size : Slider 9-16pt (live preview in list below)
- Animation speed : Slider 100-500ms (label: Slow/Normal/Fast)
- Icon style : Buttons (Emoji / Colorful SVG / Monochrome)
  - Toggle buttons with preview
  - Smooth transition between styles

**4. Behavior Tab ⚙️**

- Checkboxes (with descriptions underneath):
  - Auto-paste enabled
  - Clipboard monitoring
  - Show notifications
  - Run on startup
- Spinners/Selectors:
  - Auto-paste delay: 50-500ms (with labels: Instant/Normal/Slow)
  - Toast duration: 1000-5000ms
  - History retention: 7-365 days
  - Max history items: 100-10000

**5. Advanced Tab 🔧**

- Debug logging toggle
- Network timeout spinner
- Cache size info + "Clear Cache" button
  - Button click: Confirmation dialog
  - Success toast: "Cache cleared"
- Log file location : Text (read-only) + "Open Folder" button
- Reset all to defaults : Big scary button 🚨
  - Confirmation: "This will reset ALL settings. Are you sure?"

**Visual Polish:**

- **Transitions** : Tab change = fade + slight slide (200ms)
- **Spinners/Sliders** : Colored tracks matching theme
- **Checkboxes** : Custom styled (blue check on hover/selected)
- **Section Headers** : Bold, 12px, slight margin top
- **Descriptions** : Small grey text below inputs (helpful hints)
- **Error Messages** : Inline red text if validation fails
- **Success Feedback** : Green checkmark if saved

**Save/Load:**

- Save button : Persist to ConfigService + toast "Settings saved"
- Cancel button : Discard changes (ask if modified)
- Changes apply : Real-time pour appearance, on save pour behavior

---

### [F-11] Health Checks — P0

**Classe** : `HealthCheckManager` dans `src/services/health_check.py`

**Checks Exécutés au Démarrage:**

1. **Config Check** :
   - Fichier config.json existe
   - JSON valide
   - Champs requis présents
   - Types corrects

2. **LLM Connectivity** :
   - Ping chaque provider configuré
   - Timeout 5 secondes
   - Afficher résultat (✅ OK / ❌ FAIL)

3. **Permissions Check** :
   - Admin rights nécessaires ? (pour hooks si requis)
   - Write access à %APPDATA%
   - Test clipboard access

4. **Dependencies Check** :
   - Qt libraries chargées
   - Python version >= 3.10
   - Librairies tierces présentes

**UI Feedback:**

- Splash screen ou dialog
- Progress bar avec étapes
- Messages status pour chaque check
- Option "Skip Checks" ou continue même avec warnings
- Tray icon : Rouge si check fail critique

---

### [F-12] Système Thèmes — P1

**Fichiers QSS:**

- `assets/styles/dark.qss` — Dark theme
- `assets/styles/light.qss` — Light theme

**Classe** : `ThemeManager(QObject)` dans `src/utils/theme_manager.py`

```python
class ThemeManager(QObject):
    sig_theme_changed = Signal(str)  # 'dark' ou 'light'

    def set_theme(self, theme: str):
        """Charger et appliquer QSS à toutes les windows"""
        qss = self._load_qss(theme)
        QApplication.instance().setStyleSheet(qss)
        self.sig_theme_changed.emit(theme)
```

**Variables QSS (CSS-like):**

```css
/* dark.qss */
QWidget {
  background-color: #1e1e1e;
  color: #ffffff;
}

QLineEdit,
QTextEdit {
  background-color: #2d2d2d;
  border: 1px solid #444;
  border-radius: 4px;
}

QPushButton {
  background-color: #0066cc;
  color: white;
  border-radius: 4px;
}
```

**Switching Dynamique:**

- No restart needed
- Apply instantly à toutes windows
- Save preference à config.json
- Auto-detect système Windows (si 'System' selected)

---

### [F-13] Raccourcis Clavier — P0

**Classe** : `ShortcutManager` dans `src/core/shortcut_manager.py`

**Raccourcis Par Défaut:**

| Raccourci          | Action                   | Configurable |
| :----------------- | :----------------------- | :----------- |
| `Ctrl+Right Click` | Afficher menu contextuel | ✅ Oui       |
| `Ctrl+Shift+S`     | Capture d'écran          | ✅ Oui       |
| `Esc`              | Fermer menu / Annuler    | ❌ Non       |
| `Ctrl+W`           | Fermer fenêtre active    | ✅ Oui       |
| `Ctrl+,`           | Ouvrir Settings          | ✅ Oui       |
| `Ctrl+H`           | Afficher Historique      | ✅ Oui       |

**Features:**

- Visual shortcut recorder
- Conflict detection (system + other apps)
- Reset to defaults
- Persist dans config.json

**Conflict Detection:**

```python
def check_conflict(self, shortcut: str) -> bool:
    """Vérifier si raccourci conflicte avec système"""
    # Liste noire : Ctrl+Alt+Delete, Win key combos, etc.
```

---

### [F-14] Tray Icon — P1

**Classe** : `TrayIcon(QSystemTrayIcon)` dans `src/ui/tray_icon.py`

**Icônes d'État:**

- 🟢 **Ready** : Vert, API connectée
- 🟡 **Busy** : Jaune, génération en cours
- 🔴 **Error** : Rouge, API down/erreur
- ⏸️ **Suspended** : Gris/barre, hooks suspendus

**Menu Contextuel:**

```
┌─ Show Window
├─ Quick Actions
│  ├─ Summarize
│  ├─ Translate
│  └─ Screenshot
├─ Settings
├─ Suspend
└─ Exit
```

**Features:**

- Tooltip affichant status + model actuel
- Double-click : Afficher/masquer app
- Right-click : Menu contextuel
- Notifications : Fallback si toasts fail

---

### [F-15] Prompts Personnalisés — P1

**Classe** : `PromptManager` dans `src/core/prompt_manager.py`

**Format Prompt:**

```json
{
  "id": "summarize",
  "name": "Summarize",
  "icon": "📝",
  "system_prompt": "Summarize the following text concisely in 3-5 sentences:",
  "user_prompt_template": "{selected_text}",
  "model": "auto",
  "temperature": 0.7,
  "tags": ["general", "quick"],
  "enabled": true
}
```

**Variables Templates:**

- `{selected_text}` : Texte sélectionné
- `{clipboard}` : Contenu clipboard
- `{date}` : Date actuelle (YYYY-MM-DD)
- `{time}` : Heure actuelle (HH:MM:SS)
- `{file_name}` : Nom fichier actif (si détectable)

**Storage:**

- Defaults : `assets/prompts/default_prompts.json`
- User custom : `%APPDATA%\QuickShortcutAI\custom_prompts.json`
- Merge : Defaults + user customs

---

### [F-16] Rendu Markdown — P1

**Classe** : `MarkdownRenderer` dans `src/utils/markdown_renderer.py`

**Features:**

- Markdown → HTML conversion
- Syntax highlighting : Pygments
- Equations : Support optionnel KaTeX
- Tables : Support Markdown tables
- Code blocks : Colored, language-specific

**Extensions:**

````python
markdown.markdown(text, extensions=[
    'fenced_code',       # ``` code blocks
    'tables',            # | col1 | col2 |
    'toc',               # Auto table of contents
    'extra',             # Extra Markdown features
    'codehilite'         # Syntax coloring via Pygments
])
````

**CSS Styling:**

- Light & dark variants
- Proper padding/margins
- Link colors (blue, underlined)
- Code block background
- Table borders

---

### [F-17] Copy Response — P1

**Formats Supportés:**

- 📄 **Plain Text** : Texte brut sans formatting
- 📝 **Markdown** : Markdown source (si copyAsMarkdown enabled)
- 🎨 **Rich HTML** : HTML avec styles CSS

**Implémentation:**

```python
def copy_response(self, format: str = 'auto'):
    """Copy current response en format spécifié"""
    if format == 'markdown':
        QApplication.clipboard().setText(self._markdown_text)
    elif format == 'html':
        QApplication.clipboard().setHtml(self._html_text)
    else:
        QApplication.clipboard().setText(self._plain_text)

    # Feedback visuel : "Copied!" pendant 2 secondes
```

---

### [F-18] Retry Mechanism — P1

**Behavior:**

- Bouton "Retry" dans response window
- Relance requête avec même contexte/model
- Supprime dernière réponse assistant de l'historique
- Permet correction réponses incomplètes/mauvaises

**Implementation:**

```python
def retry(self):
    """Relancer dernière requête"""
    self._history_service.remove_last_assistant_message()
    self._send_request(self._last_request)
```

---

### [F-19] Chat Context Management — P1

**Gestion Contexte Multi-Turns:**

- System prompt (optionnel, au début)
- User messages + Assistant responses (alternés)
- Context window limit : Couper si > max tokens
- Support conversation history (voir F-09)

**Exemple Payload:**

```json
{
  "messages": [
    { "role": "system", "content": "You are a helpful assistant." },
    { "role": "user", "content": "Hello" },
    { "role": "assistant", "content": "Hi there!" },
    { "role": "user", "content": "Who are you?" }
  ]
}
```

---

### [F-20] Portable Mode — P0

**Objectif** : Exe standalone sans installation Python requise.

**Packaging avec Nuitka:**

```bash
python -m nuitka --standalone --onefile \
  --windows-disable-console \
  --windows-icon-from-ico=assets/icon.ico \
  --enable-plugin=pyside6 \
  --output-dir=dist \
  --company-name="Your Company" \
  --product-name="Quick Shortcut AI" \
  --file-version=1.0.0 \
  --follow-imports \
  src/main.py
```

**Target Metrics:**

- Taille exe : < 50MB (idéal 30-40MB)
- Startup cold : < 2 secondes
- Startup warm : < 1 seconde
- RAM idle : < 150MB
- CPU idle : < 1%

**Optimisations:**

1. PySide6-Essentials au lieu de PySide6 complet
2. UPX compression (réduction ~30% de taille)
3. Lazy imports (charger modules à l'usage)
4. Strip debug symbols en release
5. Exclude unused Qt modules

**Distribution:**

- Single .exe file (pas besoin Python, pas besoin installation)
- Portable : Config dans `./config/` relative ou `%APPDATA%`
- Optional installer (Inno Setup)

---

## ARCHITECTURE

### Arborescence Projet

```
app-quick-shortcut-ai-llm/
├── src/
│   ├── __init__.py
│   ├── main.py                          # Entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── input_manager.py             # F-01: Input hooks
│   │   ├── clipboard_manager.py         # F-05: Clipboard
│   │   ├── config_service.py            # Configuration (Singleton)
│   │   ├── llm_provider.py              # F-03: ABC interface
│   │   ├── provider_factory.py          # F-03: Factory pattern
│   │   ├── ollama_provider.py           # F-03: Ollama impl
│   │   ├── openai_provider.py           # F-03: OpenAI impl
│   │   ├── anthropic_provider.py        # F-03: Anthropic impl
│   │   ├── openrouter_provider.py       # F-03: OpenRouter impl
│   │   ├── auto_paster.py               # F-06: Auto-paste
│   │   ├── shortcut_manager.py          # F-13: Shortcuts
│   │   └── llm_worker.py                # Streaming in QThread
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── floating_menu.py             # F-02: Context menu
│   │   ├── response_window.py           # F-04: Chat window
│   │   ├── settings_dialog.py           # F-10: Settings
│   │   ├── screenshot_tool.py           # F-07: Screenshot UI
│   │   ├── toast_notification.py        # F-08: Toast widget
│   │   ├── tray_icon.py                 # F-14: System tray
│   │   └── widgets/
│   │       ├── auto_expanding_text.py
│   │       ├── syntax_highlighter.py
│   │       └── markdown_text_edit.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── history_service.py           # F-09: SQLite history
│   │   ├── notification_service.py      # Toast orchestration
│   │   ├── health_check.py              # F-11: Startup checks
│   │   └── theme_manager.py             # F-12: Theme switching
│   └── utils/
│       ├── __init__.py
│       ├── win32_helpers.py             # Windows API wrappers
│       ├── markdown_renderer.py         # F-16: Markdown → HTML
│       └── logger.py                    # Logging utility
├── assets/
│   ├── icons/
│   │   ├── tray_ready.png
│   │   ├── tray_busy.png
│   │   ├── tray_error.png
│   │   └── actions/                     # Menu icons (emoji ou SVG)
│   ├── styles/
│   │   ├── dark.qss
│   │   ├── light.qss
│   │   └── variables.qss
│   └── prompts/
│       └── default_prompts.json
├── tests/
│   ├── __init__.py
│   ├── test_core/
│   │   ├── test_input_manager.py
│   │   ├── test_clipboard.py
│   │   ├── test_llm_providers.py
│   │   └── test_config_service.py
│   ├── test_ui/
│   │   ├── test_floating_menu.py
│   │   ├── test_response_window.py
│   │   └── test_settings.py
│   └── test_services/
│       ├── test_history_service.py
│       └── test_health_check.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API.md
│   └── USER_GUIDE.md
├── SPEC.md                              # This file
├── README.md
├── TODO.md                              # Progress tracking
├── IMPLEMENTATION_PLAN.md
├── CAHIER_DES_CHARGES.md
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── .gitignore
├── LICENSE
└── .env.example
```

### Dépendances Principales

| Bibliothèque         | Version   | Raison                          | Taille |
| :------------------- | :-------- | :------------------------------ | :----- |
| `PySide6-Essentials` | >= 6.5.0  | Qt minimal (pas full PySide6)   | ~80MB  |
| `pynput`             | >= 1.7.6  | Hooks clavier/souris globaux    | ~100KB |
| `requests`           | >= 2.31.0 | HTTP client pour LLM APIs       | ~500KB |
| `markdown`           | >= 3.5    | Markdown → HTML                 | ~200KB |
| `Pygments`           | >= 2.16   | Syntax highlighting (optionnel) | ~2MB   |
| `Pillow`             | >= 10.0   | Image handling (optionnel)      | ~2MB   |

**Optional Dependencies (lazy import):**

- `markdown` + `Pygments` : Chargés uniquement si rendering enabled
- `Pillow` : Chargé seulement si screenshot utilisé

**Build Dependencies:**

- `nuitka` >= 1.9 : Compilation Python → C (packaging)
- `black`, `ruff` : Code formatting & linting
- `pytest`, `pytest-qt` : Testing

---

## CONFIGURATION

**Fichier** : `%APPDATA%\QuickShortcutAI\config.json`

**Schéma Complet :**

```json
{
  "version": "1.0.0",
  "app": {
    "first_run": true,
    "last_run_date": "2026-02-15",
    "update_check_enabled": true
  },
  "providers": [
    {
      "id": "ollama-local",
      "type": "ollama",
      "name": "Ollama Local",
      "base_url": "http://localhost:11434",
      "api_key": "",
      "default_model": "llama3.2:latest",
      "enabled": true,
      "timeout_seconds": 30
    },
    {
      "id": "openai",
      "type": "openai",
      "name": "OpenAI",
      "base_url": "https://api.openai.com/v1",
      "api_key": "sk-...",
      "default_model": "gpt-4o",
      "enabled": false,
      "timeout_seconds": 30
    }
  ],
  "default_provider": "ollama-local",
  "shortcuts": {
    "context_menu": "Ctrl+RightClick",
    "screenshot": "Ctrl+Shift+S",
    "settings": "Ctrl+Comma",
    "history": "Ctrl+H"
  },
  "appearance": {
    "theme": "dark",
    "font_family": "Segoe UI",
    "font_size": 11,
    "animation_speed_ms": 200,
    "icon_style": "emoji"
  },
  "behavior": {
    "auto_paste_enabled": false,
    "auto_paste_delay_ms": 100,
    "clipboard_monitoring": true,
    "toast_duration_ms": 3000,
    "history_retention_days": 90,
    "max_history_items": 5000
  },
  "network": {
    "request_timeout_seconds": 30,
    "retry_count": 3,
    "retry_delay_ms": 1000
  },
  "advanced": {
    "debug_logging": false,
    "log_file_path": "%APPDATA%\\QuickShortcutAI\\logs",
    "enable_profiling": false
  }
}
```

---

## PRÉREQUIS SYSTÈME

**Minimum :**

- Windows 10 (version 1809 ou ultérieure)
- Windows 11
- Processeur : x64 (pas 32-bit)
- RAM : 4GB (2GB minimum)
- Disque : 500MB libres
- Connexion internet (pour cloud LLM providers)

**Recommandé :**

- Windows 11
- 8GB RAM
- SSD pour amélioration réactivité
- Provider LLM local (Ollama) pour latence minimale

**Optional :**

- Admin rights (certains Windows versions peuvent exiger pour hooks)
- Ollama installé localement : https://ollama.ai

---

## HISTORIQUE ET VERSIONING

### Version [0.1.0] — Initial Planning — 2026-02-15

#### Added

- Initial project structure
- CAHIER_DES_CHARGES.md specification
- IMPLEMENTATION_PLAN.md roadmap
- SPEC.md technical specification (this document)
- TODO.md progress tracking

#### Planned Phases

- **Phase 0** : Setup initial (structure, dependencies)
- **Phase 1** : Fondation (input hooks, LLM abstraction, config)
- **Phase 2** : UI Core (menu, chat window, shortcuts)
- **Phase 3** : LLM Integration (streaming, providers)
- **Phase 4** : Advanced Features (clipboard, vision, history)
- **Phase 5** : Polish & Packaging (themes, toasts, build)

---

## NOTES DE MAINTENANCE

**Lorsqu'une feature est supprimée :**

```markdown
~~[F-XX] Deprecated Feature — Removed in v1.2~~
_Reason: Feature was replaced by F-YY providing better UX._
```

**Lorsqu'une feature change de statut :**

```
[F-01] ... — Status: 🚧 En cours (Depuis 2026-02-15)
```

---

**Document créé** : 2026-02-15
**Dernière modification** : 2026-02-15
**Auteur** : AI Assistant (Claude)
**Status** : Draft v1.0
