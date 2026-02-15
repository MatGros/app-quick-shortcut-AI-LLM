# Plan d'Implémentation Technique - Assistant IA Natif

Ce document détaille les étapes techniques pour la réalisation de l'application décrite dans le `CAHIER_DES_CHARGES.md`.

## Choix Technologique : Python + PySide6 (Qt)

Pourquoi ce choix ?

- **Python** : Leader incontesté pour l'IA (bibliothèques `openai`, `ollama`, `pillow` pour les images).
- **PySide6 (Qt)** : Framework UI le plus puissant et flexible. Permet des designs "Pixel Perfect" (Stylesheets QSS), des fenêtres transparentes, et une gestion robuste des événements système.
- **Multi-plateforme** : Code portatif (Windows 10/11 principalement ciblé).

---

## Phase 1 : Fondation & Architecture (Semaine 1)

### 1.1. Structure du Projet

Mise en place de l'arborescence :

```text
/src
  /core         # Logique métier (Hooks, Config, LLM)
  /ui           # Composants graphiques (Qt)
  /services     # Services (Historique, Notifications)
  /assets       # Icônes, Styles (QSS)
main.py
requirements.txt
```

### 1.2. Gestion des Entrées (Input Hooks)

- **Objectif** : Intercepter `Ctrl+Clic Droit` sans bloquer le système.
- **Tech** : Bibliothèque `pynput` (ou `keyboard`/`mouse` si besoins plus bas niveau).
- **Implémentation** :
  - Un `BackgroundWorker` (QThread) écoute les inputs.
  - Déclenche un signal Qt `sig_context_menu_requested` vers le thread principal.

### 1.3. Système de Configuration

- **Fichier** : `config.json` dans `%APPDATA%`.
- **Classe** : `ConfigManager` (Singleton) chargeant/sauvegardant les prefs (LLM URL, Raccourcis, Thème).

---

## Phase 2 : Interface Utilisateur Moderne (Semaine 2)

### 2.1. Menu Contextuel (FloatingMenu)

- **Tech** : `QMainWindow` avec flag `Qt.FramelessWindowHint` + `Qt.WindowStaysOnTopHint`.
- **Design** :
  - Fond acrylique/translucide.
  - Liste d'actions avec icônes (Emojis ou SVG).
  - Animation d'apparition (FadeIn / Slide).
- **Positionnement** : À la position de la souris, avec détection des bords d'écran (pour ne pas sortir).

### 2.2. Fenêtre de Chat (ResponseWindow)

- **Tech** : `QWidget` redimensionnable.
- **Composants** :
  - `ChatArea` : `QScrollArea` contenant des bulles de chat (User/Bot).
  - `InputBox` : `QTextEdit` auto-extensible (`textChanged` -> calcul de hauteur).
- **Comportement** : Single Instance. Si déjà ouverte, elle vient au premier plan et ajoute le nouveau prompt.

---

## Phase 3 : Intégration LLM & Streaming (Semaine 3)

### 3.1. Abstraction LLM

- Interface `LLMProvider` :
  - `stream_chat(messages: list) -> Generator`
  - `get_models() -> list`

### 3.2. Implémentation Ollama & OpenAI

- Utilisation de `requests` ou des SDKs officiels.
- Gestion des erreurs (Timeout, API Key invalide).

### 3.3. Streaming UI

- **Tech** : `QThread` pour ne pas geler l'UI pendant la génération.
- **Logique** :
  - Le thread émet un signal `sig_token_received(str)` à chaque "chunk" de texte.
  - L'UI met à jour le texte en temps réel (effet machine à écrire fluide).
  - Support Markdown basique (surtout pour le code).

---

## Phase 4 : Fonctionnalités Avancées (Semaine 4)

### 4.1. Capture d'écran (Vision)

- **Action** : Bouton dans le menu ou auto-détection si image dans clipboard.
- **Tech** : `Pillow` (`ImageGrab.grabclipboard()`).
- **Envoi** : Conversion en Base64 pour l'API LLM (modèles Vision requis, ex: Llama 3.2 Vision, GPT-4o).

### 4.2. Historique (SQLite)

- Stockage local des conversations (JSON ou SQLite).
- Interface pour parcourir l'historique (Sidebar dans `ResponseWindow`).

### 4.3. Auto-Paste

- Simulation clavier (`pynput.keyboard.Controller`) pour coller le texte.
- Gestion du focus : `alt-tab` rapide pour revenir à l'app précédente si nécessaire.

---

## Phase 5 : Polissage & Packaging (Semaine 5)

### 5.1. Thèmes & Styles

- Fichiers `.qss` (CSS pour Qt) séparés pour Light/Dark mode.
- Chargement dynamique sans redémarrage.

### 5.2. Notifications

- Widgets personnalisés (petits Toasts) en bas à droite.
- Pas de notifications système Windows (trop intrusives/lentes), mais des overlays Qt.

### 5.3. Packaging

- Utilisation de `PyInstaller` ou `Nuitka`.
- Création d'un installeur (Inno Setup ou MSI).

## Verification Plan

### Automated Tests

- `pytest` pour la logique métier (Config, Parsing LLM).
- `pytest-qt` pour tester les signaux et les widgets UI sans écran physique.

### Manual Verification

- Lancer l'app.
- Tester `Ctrl+Clic Droit` partout (Bureau, Navigateur).
- Vérifier le streaming (fluidité).
- Vérifier la consommation mémoire (recherche de fuites).
