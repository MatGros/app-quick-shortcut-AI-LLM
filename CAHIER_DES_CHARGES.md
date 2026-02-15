# Cahier des Charges - Assistant IA Natif (Remplacement AHK)

## 1. Présentation du Projet

Ce document définit les spécifications pour le développement d'une application de bureau Windows native, destinée à remplacer l'actuel "LLM AutoHotkey Assistant".
L'objectif est de créer une solution **robuste**, **moderne** et **orientée objet**, s'affranchissant totalement de la dépendance à AutoHotKey (AHK), tout en reproduisant et améliorant ses fonctionnalités clés.

## 2. Objectifs Principaux

- **Indépendance AHK** : Plus de scripts AHK. L'application gérera elle-même les interceptions clavier/souris (Hooks bas niveau).
- **Modernité UI/UX** : Interfaces fluides, menus contextuels stylisés (pas de menus système standards), animations soignées, support Dark/Light mode.
- **Robustesse** : Architecture OOP (Orientée Objet), gestion d'erreurs stricte, tests de santé au démarrage (Health Checks).
- **Agnosticisme LLM** : Support universel des fournisseurs (Ollama, OpenAI, Anthropic, OpenRouter) via une couche d'abstraction.

## 3. Spécifications Fonctionnelles

### 3.1. Gestion des Entrées (Input Hooks)

- **Clavier** : Écoute globale des raccourcis (ex: `Ctrl+Clic Droit`, raccourcis personnalisés).
- **Souris** : Détection de la sélection de texte et du contexte.
- **Clipboard** : Lecture et écriture robustes dans le presse-papier pour récupérer le texte sélectionné ou coller les réponses.

### 3.2. Menu Contextuel Intelligent

- **Déclenchement** : Accessible via raccourci (ex: `Ctrl+Clic Droit` ou touche dédiée).
- **Design** : Fenêtre sans bordure (frameless), rendu graphique moderne (XAML/HTML/Qt), supportant :
  - Icônes et Emojis colorés.
  - Sous-menus fluides.
  - Barre de recherche rapide (optionnel).
- **Actions** :
  - **Résumer** : Résume le texte sélectionné.
  - **Traduire** : Traduit le texte.
  - **Prompt Libre** : Ouvre une zone de saisie pour interroger le LLM sur le texte sélectionné.
  - **Capture d'écran** : Envoi automatique du contenu image du clipboard au LLM (Vision).
- **Chat Direct** : Ouvrir l'interface de chat sans contexte sélectionné.

### 3.3. Interface de Chat & Streaming

- **Fenêtre Unique** : Une seule instance de fenêtre de réponse est réutilisée. Si une nouvelle requête est lancée, elle remplace ou s'ajoute à la fenêtre existante sans en ouvrir une nouvelle.
- **Affichage Streaming** : Le texte apparaît mot par mot (effet machine à écrire) pour une perception de rapidité.
- **Composant Textbox** :
  - Design moderne (coins arrondis, padding, typographie soignée).
  - **Auto-extensible** : S'agrandit verticalement selon le contenu (jusqu'à une limite), mais reste redimensionnable manuellement par l'utilisateur.
- **Historique Visuel** : Distinction claire entre User/Assistant.

### 3.4. Fonctionnalité "Auto-Paste"

- Option configurable par prompt ou globalement.
- Si activée : Le texte généré par le LLM remplace automatiquement la sélection de l'utilisateur dans l'application active.
- Doit gérer correctement les délais et le focus fenêtre pour éviter les erreurs de collage.

### 3.5. Configuration & Paramètres

- **Gestion des LLM** : Interface pour ajouter/modifier les endpoints (URL, Clé API, Nom du modèle).
  - Types : OpenI (Standard), Cloud, OLLAMA (Local), OpenRouter.
- **Raccourcis** : Éditeur de raccourcis clavier pour les actions.
- **Thèmes** : Bascule simple entre Light Mode et Dark Mode (affectant menu, chat, paramètres).

### 3.6. Notifications & Feedback

- **Micro Pop-ups** : Notifications "Toast" non-intrusives, ancrées (ex: près du tray ou de la souris).
  - États : "En cours de génération...", "Erreur de connexion", "Copié !".
  - Discrétion : Doit informer sans bloquer l'utilisateur.
- **Tray Icon** : Indicateur d'état (Prêt, Occupé, Erreur).

### 3.7. Historique & Logs

- **Historique des requêtes** : Base de données locale (SQLite ou JSON) stockant les prompts et réponses.
- Interface pour rechercher et relire les anciens échanges.

## 4. Spécifications Techniques

### 4.1. Langage & Framework Recommandé

- **Option A (Privilégiée pour Modernité/Rapidité) : Python + PySide6 (Qt)**
  - **Pourquoi ?** Écosystème IA riche, Qt permet des UIs très stylisées (CSS-like), gestion facile des threads, bibliothèques `pynput` pour les hooks.
- **Option B (Privilégiée pour Intégration Windows) : C# .NET 8 + WPF/WinUI 3**
  - **Pourquoi ?** Performance native, hooks Win32 très stables, déploiement .exe unique facile.

### 4.2. Architecture Logicielle (OOP)

L'application suivra une architecture modulaire stricte (ex: MVVM ou MVC).

- **Core** :
  - `InputManager` : Gestion des hooks clavier/souris (Singleton).
  - `LLMClient` : Classe abstraite avec implémentations (`OllamaClient`, `OpenAIClient`, etc.).
  - `ClipboardManager` : Gestion safe du presse-papier.
- **UI** :
  - Separation de la logique métier et de l'affichage.
  - `FloatingMenu` : Fenêtre contextuelle.
  - `ResponseWindow` : Fenêtre de chat unique.
  - `SettingsDialog`.
- **Services** :
  - `ConfigService` : Persistance des paramètres (JSON/TOML).
  - `HistoryService` : Log des interactions.
  - `NotificationService` : Gestion des pop-ups.

### 4.3. Démarrage & Robustesse (Health Checks)

Au lancement de l'application (avant affichage UI) :

1.  **Check Config** : Vérification de l'intégrité des fichiers de config.
2.  **Check LLM** : Ping des endpoints configurés (ex: `GET /api/tags` pour Ollama).
3.  **Check Permissions** : Vérification des droits pour les Hooks (Admin si nécessaire).
4.  Si échec : Notification claire à l'utilisateur via le système de micro-popup.

## 5. Livrables Attendus

1.  Code source complet (Git).
2.  Exécutable autonome (Portable ou Installateur).
3.  Documentation technique (Architecture, Extension).
