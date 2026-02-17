# 🎯 UAT Guide Détaillé - Instructions Complètes

**Pour**: Quelqu'un qui lance l'application pour la première fois
**Durée**: ~45 minutes
**Objectif**: Valider que tout marche correctement

---

## 🚀 AVANT DE COMMENCER - Prérequis

### ✅ Étape 1: Avoir Ollama (ou OpenAI/Anthropic) configuré

**Option A: Ollama (recommandé pour tester localement)**

1. Télécharge Ollama: https://ollama.ai
2. Installe-le
3. Lance-le (il devrait créer une icône systray)
4. Attends que le message dise "Ollama is running"
5. Télécharge un modèle dans le terminal:
   ```
   ollama pull llama2
   ```
   (ou `ollama pull mistral` si tu préfères)
6. Attends que le download finisse (~5 GB)
7. Vérifie que ça marche:
   ```
   curl http://localhost:11434/api/generate -d "{\"model\":\"llama2\",\"prompt\":\"hi\"}"
   ```
   Devrait retourner du texte

**Option B: OpenAI API**
1. Va sur https://platform.openai.com/api-keys
2. Crée une clé API
3. Copie-la (tu la mettras dans Settings plus tard)

### ✅ Étape 2: Télécharge le code
```bash
git clone https://github.com/YOUR_REPO/app-quick-shortcut-AI-LLM
cd app-quick-shortcut-AI-LLM
```

### ✅ Étape 3: Installe Python et dépendances
```bash
# Vérifie que Python 3.10+ est installé
python --version

# Crée un environnement virtuel
python -m venv venv

# Active-le
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Installe les dépendances
pip install -r requirements.txt
```

### ✅ Étape 4: Prépare le test de première utilisation

Supprime la config existante:
```bash
# Windows:
del %APPDATA%\QuickShortcutAI\config.json

# Mac:
rm ~/Library/Application\ Support/QuickShortcutAI/config.json

# Linux:
rm ~/.config/QuickShortcutAI/config.json
```

---

## 📋 PHASE 1: Démarrage et Configuration (5 min)

### TEST 1.1: Première utilisation (aucune config)

#### Étape 1: Lancer l'application
```bash
# Dans le terminal (dans le répertoire du projet avec venv activé):
python -m src.main
```

**Attends**:
- ~2 secondes
- Tu devrais voir:
  - Une fenêtre console/terminal (peut s'ouvrir en arrière-plan)
  - Une **icône dans la barre systray** (en bas à droite)
  - **L'icône devrait être VERTE** ✅ = Application prête et en attente
    - 🟢 Vert: Prête, configuration valide, LLM accessible
    - 🟡 Jaune: Vérification en cours (santé check)
    - 🔴 Rouge: Erreur, configuration invalide ou LLM indisponible

#### Étape 2: Vérifie l'écran
- **Tray icon en rouge/jaune?** = Normal pour première utilisation, aucune config
- **Pas de fenêtre qui s'ouvre?** = C'est correct, l'app tourne en background

#### Étape 3: Ouvre Settings
- **Right-click** sur l'icône systray (en bas à droite)
- Tu devrais voir un menu avec:
  - "Open Chat"
  - "Settings" ← **Clique ici**
  - "Quit"

#### Étape 4: Fenêtre Settings s'ouvre
Tu devrais voir:
- Une fenêtre avec le titre "Quick Shortcut AI - Settings"
- **4 onglets en haut**: Providers | Shortcuts | Appearance | About

**✅ Résultat attendu**:
- ✅ Settings s'ouvre sans crash
- ✅ Les onglets sont visibles
- ✅ Pas de message d'erreur

---

### TEST 1.2: Configuration de Ollama (ou OpenAI)

#### Étape 1: Tu es déjà dans Settings, clique sur onglet "Providers"

Tu devrais voir:
- Une liste avec "Ollama Local" (ou autres providers)
- Boutons en bas: "Test Connection", "Save Provider", "Delete Provider"

#### Étape 2: Clique sur "Ollama Local" dans la liste

La liste devrait devenir bleue/sélectionnée.

Tu devrais voir les détails:
- **Name**: Ollama Local
- **Type**: ollama (dropdown)
- **Base URL**: http://localhost:11434
- **API Key**: (vide - normal)
- **Default Model**: Sélectionne depuis la liste déroulante (voir étape 3)
- **Enabled**: (checkbox coché)

#### Étape 3: Sélectionner le modèle disponible (NOUVEAU!)

**L'application peut maintenant charger automatiquement les modèles**:

1. Si la liste **"Default Model"** est vide, clique **"Refresh Models"**
2. Cela va scanner Ollama et afficher les modèles disponibles:
   - `llama3.1:latest` (si tu l'as pullé)
   - `llama2:latest`
   - `mistral:latest`
   - `gemma3:4b`
   - etc.
3. **Sélectionne** un modèle de la liste
4. Les modèles se mettent à jour automatiquement si tu changes l'URL ou le type

**ℹ️ IMPORTANT**: Le bouton "Test Connection" ✅ fonctionne maintenant correctement!

#### Étape 4: Teste la connexion
- Clique le bouton **"Test Connection"**
- Une popup devrait apparaître:
  - ✅ **"Connection successful!"** = Ollama/OpenAI fonctionne 🎉
  - ❌ **"Connection failed"** = Vérifie:
    - Ollama tourne bien en local
    - L'URL est correcte
    - Pas de firewall qui bloque

Si tu veux tester avec **OpenAI à la place**:
- **Type**: Change à "openai"
- **Base URL**: https://api.openai.com/v1
- **API Key**: Colle ta clé OpenAI (de https://platform.openai.com/api-keys)
- **Default Model**: Clique "Refresh Models" pour voir (gpt-4o, gpt-3.5-turbo, etc.)
- Clique "Test Connection"

#### Étape 5: Sauvegarde
- Clique **"OK"** (en bas à droite)
- Attends ~1 seconde
- Settings ferme

#### Étape 6: Redémarre l'application
```bash
# Dans le terminal, appuie Ctrl+C (arrête l'app)
# Puis relance:
python -m src.main
```

#### Étape 7: Vérifie que l'icône systray est **VERTE**

- **Icône verte** = App prête ✅
- **Icône rouge/jaune** = Problème de config

**✅ Résultat attendu**:
- ✅ Settings s'ouvre et ferme correctement
- ✅ Config sauvegardée
- ✅ Icône systray devient verte
- ✅ Pas de crash

---

## 🎨 PHASE 2: Interface UX (5 min)

### TEST 2.1: Menu flottant

#### Étape 1: Ouvre un éditeur de texte
- Ouvre **Notepad** (ou VS Code, Word, etc.)
- N'importe quel logiciel

#### Étape 2: Fais l'action "Ctrl + Right-Click"
- **Tiens Ctrl enfoncée**
- Pendant que tu tiens Ctrl:
  - **Right-click** (click droit)
  - **Relâche Ctrl**

#### Étape 3: Regarde
**Tu devrais voir un menu qui apparaît**:
- À la position du curseur (où tu as cliqué)
- Avec 5 boutons:
  1. **Summarize**
  2. **Translate**
  3. **Explain**
  4. **Generate Code**
  5. **Take Screenshot**
- Le menu est semi-transparent (style moderne)

#### Étape 4: Ferme le menu
- **Appuie sur Esc**
- Le menu disparaît

**✅ Résultat attendu**:
- ✅ Menu apparaît en < 1 seconde
- ✅ Les 5 boutons sont lisibles
- ✅ Menu ferme avec Esc

---

### TEST 2.2: Fenêtre de réponse

#### Étape 1: Réouvre le menu
```
Ctrl + Right-Click en n'importe où
```

#### Étape 2: Clique sur "Summarize"

Une **nouvelle fenêtre s'ouvre**:
- Titre: "Quick Shortcut AI - Chat"
- Avec en haut: "Summarize • llama2" (ou ton modèle)

Tu devrais voir:
- **Zone de texte vide** (grandes = pour les réponses)
- **3 boutons en bas**: "Send", "Copy", "Auto-Paste"
- **Bouton rouge**: "Stop" (grisé = pas actif)

#### Étape 3: Teste que la fenêtre est interactive
- **Redimensionne-la** (tire les bords)
- **Ferme-la** (clique X)

**✅ Résultat attendu**:
- ✅ Fenêtre s'ouvre rapidement
- ✅ Les boutons sont visibles
- ✅ Fenêtre peut être redimensionnée et fermée

---

### TEST 2.3: Icône systray et menu

#### Étape 1: Right-click sur l'icône systray
- En bas à droite de l'écran
- **Right-click** (click droit)

Tu devrais voir un menu:
- "Open Chat" ← Ouvre la fenêtre réponse
- "Take Screenshot" ← Pour capturer l'écran
- "Settings" ← Configuration
- "Quit" ← Ferme l'app

#### Étape 2: Teste "Settings"
- Clique "Settings"
- La fenêtre Settings s'ouvre

#### Étape 3: Ferme Settings
- Clique le X

#### Étape 4: Teste "Open Chat"
- Right-click tray → "Open Chat"
- Fenêtre réponse s'ouvre

**✅ Résultat attendu**:
- ✅ Tous les menu items fonctionnent
- ✅ Pas de crash
- ✅ Transitions fluides

---

## 💬 PHASE 3: Tests LLM Réels (10 min)

### TEST 3.1: Test simple de streaming

#### Étape 1: Prépare du texte à traiter
- Ouvre Notepad
- Écris du texte (ou copie ceci):
```
Python is a programming language created by Guido van Rossum.
It is easy to learn and very powerful.
```
- **Sélectionne tout** (Ctrl+A)
- **Copie** (Ctrl+C)

#### Étape 2: Ouvre le menu
```
Ctrl + Right-Click n'importe où
```

#### Étape 3: Clique "Summarize"

#### Étape 4: **OBSERVE LE STREAMING**
Tu devrais voir:
- Texte qui apparaît **progressivement** (mot par mot)
- Pas de freeze/lag
- La fenêtre reste réactive (tu peux la déplacer, redimensionner)
- Le bouton "Stop" devient **rouge** pendant le streaming

#### Étape 5: Attends la fin
- Le texte s'arrête quand c'est fini
- Le bouton "Stop" redevient grisé
- Les boutons "Copy" et "Auto-Paste" deviennent actifs

#### Étape 6: Résultat
Tu devrais voir quelque chose comme:
```
This text discusses Python, a programming language.
Key points: easy to learn, powerful language.
```

**✅ Résultat attendu**:
- ✅ Streaming visible (pas tout d'un coup)
- ✅ UI reste fluide et réactive
- ✅ Pas de crash

---

### TEST 3.2: Test avec texte LONG

#### Étape 1: Copie un long texte
- Va sur Wikipedia ou un article long
- Copie **plusieurs paragraphes** (500+ mots)

#### Étape 2: Demande une traduction
```
Ctrl + Right-Click → Translate
```

#### Étape 3: Observe
- Le texte remplit la fenêtre
- **La textbox grandit automatiquement** (s'agrandit pour faire de la place)
- Le scrolling fonctionne bien
- Pas de crash avec gros volumes

**✅ Résultat attendu**:
- ✅ Long texte géré correctement
- ✅ Pas de freeze
- ✅ Scrolling fluide

---

### TEST 3.3: Test du Markdown avec code

#### Étape 1: Demande du code
- Copie: "Write a Python function to calculate factorial"
- ```
Ctrl + Right-Click → Generate Code
```

#### Étape 2: Regarde la réponse
Tu devrais voir quelque chose comme:
```
Here's a Python function:

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

**Remarque le CODE**: Il devrait avoir des **couleurs** (syntax highlighting):
- `def` en bleu/violet
- Strings en rouge/orange
- Nombres en vert
- Etc.

#### Étape 3: Vérifie l'apparence
- Code lisible et bien formaté
- Pas de texte découpé
- Paragraphes bien séparés

**✅ Résultat attendu**:
- ✅ Code affiché avec couleurs
- ✅ Bien formaté et lisible
- ✅ Markdown rendu correctement

---

## 📋 PHASE 4: Auto-Paste (10 min)

### TEST 4.1: Bouton Copy

#### Étape 1: Tu as une réponse (du TEST 3.1)
Tu devrais voir dans la fenêtre un résumé.

#### Étape 2: Clique le bouton "Copy"
Le texte est copié dans le presse-papiers.

#### Étape 3: Ouvre Notepad
- Clique droit → Paste (ou Ctrl+V)
- Tu devrais voir la réponse complète collée dans Notepad

#### Étape 4: Ferme Notepad
- Pas besoin de sauvegarder

**✅ Résultat attendu**:
- ✅ Copy fonctionne
- ✅ Paste marche dans Notepad
- ✅ Texte correct et complet

---

### TEST 4.2: Auto-Paste dans Notepad

#### Étape 1: Ouvre Notepad
- Vide
- Laisse le curseur dedans (clignotant)

#### Étape 2: Retourne à l'app
- Copie du texte différent
- Ctrl + Right-Click → "Translate"

#### Étape 3: Attends la réponse
- Le streaming finit
- Les boutons "Copy" et "Auto-Paste" deviennent actifs

#### Étape 4: Clique "Auto-Paste"

**MAGIC**: Le texte traduit **s'insère automatiquement dans Notepad**!

#### Étape 5: Vérifie
- Notepad revient en avant
- Le texte est là
- Correct et complet

**✅ Résultat attendu**:
- ✅ Auto-Paste marche
- ✅ Texte inséré correctement
- ✅ Dans la bonne fenêtre

---

### TEST 4.3: Auto-Paste dans un formulaire web

#### Étape 1: Ouvre un navigateur
- Va sur un site qui a un formulaire avec textarea
- (Ex: GitHub issue, Twitter, Gmail compose, etc.)
- Clique dans le textarea

#### Étape 2: Retourne à l'app
- Copie: "Generate a professional email subject"
- Ctrl + Right-Click → "Generate Code"
- Attends la réponse

#### Étape 3: Clique "Auto-Paste"

**Le sujet d'email s'insère dans le textarea du navigateur!**

#### Étape 4: Vérifie
- Le texte est bien là
- Bien formaté

**✅ Résultat attendu**:
- ✅ Auto-Paste marche dans navigateur aussi
- ✅ Fonctionne dans différentes applications

---

## ⚠️ PHASE 5: Gestion des Erreurs (5 min)

### TEST 5.1: Clipboard vide

#### Étape 1: Vide le clipboard
- Clique droit n'importe où → Paste
- (Si rien ne se passe = clipboard vide ✓)

#### Étape 2: Essaie une action
```
Ctrl + Right-Click → Summarize
```

#### Étape 3: Regarde le message
Tu devrais voir:
```
❌ Clipboard is empty. Please copy some text first.
```

**✅ Résultat attendu**:
- ✅ Message d'erreur clair
- ✅ App ne crash pas

---

### TEST 5.2: Arrête Ollama et refais un test

#### Étape 1: Arrête Ollama
- Ferme Ollama (Ctrl+C dans la terminal Ollama)

#### Étape 2: Essaie une action
- Copie du texte
```
Ctrl + Right-Click → Summarize
```

#### Étape 3: Regarde l'erreur
Tu devrais voir quelque chose comme:
```
❌ Error: Connection refused
Please check your configuration in Settings.
```

**✅ Résultat attendu**:
- ✅ Message d'erreur clair
- ✅ App ne crash pas
- ✅ Suggestion pour corriger (Settings)

#### Étape 4: Relance Ollama
- Terminal → `ollama serve`
- Attends "Ollama is running"
- Reteste = devrait marcher

---

### TEST 5.3: Change le thème

#### Étape 1: Right-click tray → Settings

#### Étape 2: Clique onglet "Appearance"

#### Étape 3: Trouve "Theme" dropdown
- Actuellement: "dark"
- Change à: "light"

#### Étape 4: Clique "OK"

#### Étape 5: Observe
**L'interface change de couleur!** ✨
- Dark → Light mode
- Moins de noir, plus de blanc
- Texte devient sombre

**✅ Résultat attendu**:
- ✅ Theme change immédiatement
- ✅ Pas besoin de redémarrer
- ✅ Fluide et professionnel

---

## ✅ CHECKLIST FINALE

Coche quand tu as testé:

```
PHASE 1: Démarrage
[ ] Première utilisation sans config
[ ] Configuration de Ollama/OpenAI
[ ] Icône systray verte après config
[ ] Settings fonctionne

PHASE 2: Interface
[ ] Menu Ctrl+Right-Click apparaît
[ ] 5 boutons visibles: Summarize, Translate, etc.
[ ] Fenêtre réponse s'ouvre
[ ] Tray menu fonctionne

PHASE 3: LLM Real
[ ] Streaming visible (texte progressif)
[ ] Pas de freeze/lag pendant streaming
[ ] Code avec syntax highlighting
[ ] Long texte géré correctement

PHASE 4: Auto-Paste
[ ] Copy dans Notepad fonctionne
[ ] Auto-Paste dans Notepad fonctionne
[ ] Auto-Paste dans navigateur fonctionne
[ ] Texte complètement et correctement collé

PHASE 5: Erreurs
[ ] Clipboard vide → message d'erreur clair
[ ] Ollama arrêté → message d'erreur clair
[ ] Theme change sans problème
[ ] App jamais en crash

GLOBAL
[ ] L'app sent smooth et professionnel
[ ] Aucun crash observé
[ ] Tout fonctionne comme prévu
[ ] Prêt pour release ✅
```

---

## 🎯 Si tu trouves un problème

**Documente-le**:
1. Qu'est-ce que tu faisais?
2. Qu'est-ce que tu attendais?
3. Qu'est-ce qui s'est passé au lieu?
4. Capture d'écran si possible
5. Erreur dans le terminal (copie/colle)

**Puis dis-moi** et on fixe!

---

**Voilà! C'est vraiment simple une fois qu'on détaille chaque action. Bonne chance!** 🚀
