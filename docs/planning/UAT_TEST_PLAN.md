# UAT Test Plan - User Acceptance Testing

**Objectif**: Valider que l'application fonctionne correctement dans des scénarios réels

---

## Phase 1: Tests de Démarrage et Configuration

### Test 1.1: Première utilisation (Pas de configuration)
**Étapes**:
1. Supprimer le fichier config: `%APPDATA%\QuickShortcutAI\config.json`
2. Lancer l'application
3. Vérifier que:
   - Un message d'erreur apparaît (pas de provider configuré)
   - L'interface reste accessible
   - Le menu "Settings" est accessible

**Résultat attendu**:
- ✅ Message d'erreur clair
- ✅ Application ne crashe pas
- ✅ Possible d'ouvrir Settings pour configurer

### Test 1.2: Configuration valide existante
**Étapes**:
1. Configurer Ollama (ou OpenAI/Anthropic) dans Settings
2. Redémarrer l'application
3. Vérifier que:
   - L'application démarre sans erreur
   - Le tray icon s'affiche (vert = Ready)
   - Pas de message d'erreur

**Résultat attendu**:
- ✅ Démarrage silencieux et rapide
- ✅ Tray icon visible et vert
- ✅ Prêt à utiliser

### Test 1.3: Configuration invalide (mauvaise URL)
**Étapes**:
1. Configurer une URL invalide (ex: http://invalid:99999)
2. Redémarrer l'application
3. Vérifier que:
   - Un message d'erreur ou warning s'affiche
   - On peut toujours accéder à Settings
   - On peut corriger la configuration

**Résultat attendu**:
- ✅ Message d'erreur/warning visible
- ✅ Accès à Settings pour correction
- ✅ Après correction, redémarrage = OK

---

## Phase 2: Tests UX et Interface

### Test 2.1: Menu flottant accessible
**Étapes**:
1. Appuyer sur **Ctrl + Right-Click** en n'importe où
2. Vérifier que:
   - Le menu apparaît à la position du curseur
   - Les 5 actions sont visibles: Summarize, Translate, Explain, Generate Code, Take Screenshot
   - Le menu est fermé quand on clique ailleurs

**Résultat attendu**:
- ✅ Menu apparaît < 200ms
- ✅ Tous les boutons lisibles et cliquables
- ✅ Disparaît proprement

### Test 2.2: Fermeture du menu (Esc)
**Étapes**:
1. Ouvrir le menu flottant (Ctrl + Right-Click)
2. Appuyer sur **Esc**
3. Vérifier que le menu ferme

**Résultat attendu**:
- ✅ Menu ferme immédiatement

### Test 2.3: Fenêtre de réponse
**Étapes**:
1. Cliquer sur une action du menu
2. Vérifier que:
   - Une fenêtre s'ouvre avec titre "Summarize • model-name"
   - Les boutons sont en place: Copy, Auto-Paste, Send
   - La fenêtre peut être redimensionnée
   - La fenêtre est fermable (X button)

**Résultat attendu**:
- ✅ Fenêtre s'ouvre en < 100ms
- ✅ Tous les contrôles en place et cliquables
- ✅ Responsive et redimensionnable

### Test 2.4: Tray Icon et menu
**Étapes**:
1. Right-click sur le tray icon
2. Vérifier que:
   - Menu apparaît avec: "Open Chat", "Settings", "Quit"
   - Cliquer sur "Open Chat" → fenêtre de réponse s'ouvre
   - Cliquer sur "Settings" → dialog s'ouvre
   - Cliquer sur "Quit" → application ferme

**Résultat attendu**:
- ✅ Tous les actions du tray fonctionnent
- ✅ Transitions fluides

### Test 2.5: Settings Dialog
**Étapes**:
1. Ouvrir Settings (Tray → Settings)
2. Vérifier que:
   - **Onglet Providers**: Liste des providers, bouton Test Connection, Save, Delete
   - **Onglet Shortcuts**: Affiche tous les raccourcis
   - **Onglet Appearance**: Theme (dark/light), Font settings, Animation speed
   - **Onglet About**: Infos app
3. Changer le theme dark → light
4. Cliquer "OK"
5. Vérifier que le thème change

**Résultat attendu**:
- ✅ Tous les onglets accessibles et corrects
- ✅ Les changements se sauvegardent
- ✅ Thème change immédiatement

---

## Phase 3: Tests Fonctionnels (LLM Real)

### Test 3.1: Workflow complet avec Ollama/OpenAI
**Étapes**:
1. Copier du texte: "Resume this: The quick brown fox jumps over the lazy dog"
2. Appuyer Ctrl + Right-Click
3. Cliquer "Summarize"
4. Attendre la réponse du LLM
5. Vérifier que:
   - Le texte s'affiche progressivement (streaming)
   - Pas de lag/freeze UI
   - Le markdown se rend correctement (si réponse a du formatting)

**Résultat attendu**:
- ✅ Streaming visible et fluide
- ✅ UI reste responsive
- ✅ Réponse complète et lisible

### Test 3.2: Texte long (100+ lignes)
**Étapes**:
1. Copier un texte long (ex: article Wikipedia)
2. Cliquer "Summarize"
3. Vérifier que:
   - La textbox s'auto-expande correctement
   - Le scrolling fonctionne bien
   - Le markdown rend correctement (tables, listes, code, etc.)

**Résultat attendu**:
- ✅ Textbox grandit progressivement
- ✅ Scrolling smooth
- ✅ Tout le contenu visible et formaté

### Test 3.3: Code block rendering
**Étapes**:
1. Copier: "Write Python code to sort a list"
2. Cliquer "Generate Code"
3. Vérifier que:
   - La réponse contient un code block
   - Le code est surlignée syntaxiquement (couleurs)
   - Le code est lisible et non-découpé

**Résultat attendu**:
- ✅ Code block avec couleurs syntaxe
- ✅ Format préservé
- ✅ Lisible et professionnel

### Test 3.4: Tableau markdown
**Étapes**:
1. Copier: "Create a table comparing Python and JavaScript"
2. Cliquer "Explain"
3. Vérifier que:
   - Si la réponse contient un tableau
   - Le tableau est formaté correctement
   - Les colonnes sont alignées

**Résultat attendu**:
- ✅ Tableau bien rendu
- ✅ Lisible et professionnel

### Test 3.5: Erreur LLM (connexion perdue)
**Étapes**:
1. Arrêter le serveur Ollama/OpenAI
2. Copier du texte
3. Cliquer "Summarize"
4. Vérifier que:
   - Un message d'erreur s'affiche
   - L'application ne crashe pas
   - On peut toujours fermer la fenêtre

**Résultat attendu**:
- ✅ Message d'erreur clair
- ✅ Application stable
- ✅ Possible de relancer après correction

---

## Phase 4: Tests d'Auto-Paste

### Test 4.1: Copy button
**Étapes**:
1. Obtenir une réponse (résumé, traduction, etc.)
2. Cliquer "Copy"
3. Aller dans un éditeur (Notepad, VS Code)
4. Cliquer droit → Paste
5. Vérifier que le texte se colle

**Résultat attendu**:
- ✅ Texte copié exactement
- ✅ Paste fonctionne dans n'importe quel app

### Test 4.2: Auto-Paste button
**Étapes**:
1. Ouvrir Notepad et placer le curseur
2. Dans l'app, copier du texte
3. Cliquer "Translate"
4. Attendre la réponse
5. Cliquer "Auto-Paste"
6. Vérifier que:
   - Le texte traduit s'insère dans Notepad
   - Aux coordonnées du curseur
   - L'app revient en focus après

**Résultat attendu**:
- ✅ Auto-paste fonctionne dans Notepad
- ✅ Texte inséré correctement
- ✅ Focus restauré

### Test 4.3: Auto-Paste dans navigateur
**Étapes**:
1. Ouvrir un navigateur avec un formulaire (textarea)
2. Cliquer dans le textarea
3. Lancer LLM et obtenir réponse
4. Cliquer "Auto-Paste"
5. Vérifier que le texte se colle dans le textarea

**Résultat attendu**:
- ✅ Paste fonctionne dans navigateur
- ✅ Texte bien formaté

### Test 4.4: Auto-Paste avec markdown
**Étapes**:
1. Copier: "Format this as markdown: Title\nItem 1\nItem 2"
2. Cliquer "Explain"
3. Si la réponse contient du markdown (# headers, - lists, etc.)
4. Cliquer "Auto-Paste" dans un éditeur markdown
5. Vérifier que le markdown se rend correctement dans l'éditeur

**Résultat attendu**:
- ✅ Markdown se colle correctement
- ✅ Éditeur markdown l'interpréte bien

---

## Phase 5: Tests de Cas Limites

### Test 5.1: Clipboard vide
**Étapes**:
1. Vider le clipboard
2. Cliquer sur une action du menu
3. Vérifier qu'un message d'erreur s'affiche

**Résultat attendu**:
- ✅ Message d'erreur: "Clipboard is empty"
- ✅ Pas de crash

### Test 5.2: Response très longue (10,000+ tokens)
**Étapes**:
1. Copier: "Write a very long article about..."
2. Cliquer "Explain"
3. Attendre la réponse complète
4. Vérifier que:
   - Le scrolling reste fluide
   - Pas de memory leak (RAM reste stable)
   - Pas de freeze UI

**Résultat attendu**:
- ✅ Réponse longue rendues sans problème
- ✅ Performances acceptables
- ✅ Pas de crash

### Test 5.3: Caractères spéciaux (UTF-8, emojis)
**Étapes**:
1. Copier: "Translate to French: Hello 🌍 Café"
2. Cliquer "Translate"
3. Vérifier que:
   - Les emojis s'affichent correctement
   - Les accents sont préservés
   - Pas de caractères cassés

**Résultat attendu**:
- ✅ UTF-8 bien supporté
- ✅ Emojis visibles
- ✅ Accents préservés

### Test 5.4: Changerment de provider pendant streaming
**Étapes**:
1. Lancer une réponse longue
2. Pendant le streaming, aller dans Settings
3. Changer le provider (Ollama → OpenAI par ex)
4. Sauvegarder et revenir
5. Vérifier que:
   - La réponse actuelle continue
   - Les prochaines réponses utilisent le nouveau provider

**Résultat attendu**:
- ✅ Changement de provider fluide
- ✅ Pas d'interruption abrupte

---

## Checklist de Validation Finale

### Démarrage et Configuration
- [ ] Première utilisation → propose configuration
- [ ] Configuration valide → démarrage OK
- [ ] Configuration invalide → erreur + accès config

### Interface
- [ ] Menu flottant accessible (Ctrl+Right-Click)
- [ ] Menu fermable (Esc, clic ailleurs)
- [ ] Fenêtre réponse ouvre et ferme correctement
- [ ] Tray icon fonctionne
- [ ] Settings dialog accède à tous les onglets

### Fonctionnalité LLM
- [ ] Streaming visible et fluide
- [ ] Markdown rendu correctement
- [ ] Code highlighting fonctionne
- [ ] Tableaux formatés
- [ ] Erreurs gérées gracieusement

### Auto-Paste
- [ ] Copy button fonctionne
- [ ] Auto-Paste colle dans Notepad
- [ ] Auto-Paste colle dans navigateur
- [ ] Auto-Paste avec markdown

### Performance et Stabilité
- [ ] Pas de crash ou freeze
- [ ] Memory usage stable
- [ ] Réponses longues gérées
- [ ] UTF-8 et emojis supportés

---

## Notes Importantes

⚠️ **Prérequis**:
- Ollama en local OU OpenAI/Anthropic API key configurée
- Au moins une application tierce pour tester auto-paste (Notepad, VS Code)
- Un navigateur avec formulaire pour tester paste

⚠️ **Durée estimée**: 30-45 minutes pour tous les tests

⚠️ **Critères de réussite**:
- Tous les tests passent ✅
- Aucun crash ou freeze
- UX fluide et professionnel
- Messages d'erreur clairs

---

*Créé le 2026-02-16 pour Phase 3 UAT*
