# Phase 3 - Inventaire des Problèmes et Corrections Nécessaires

**Date**: 2026-02-17
**Statut**: UAT en cours - Blocages identifiés

---

## 🔴 PROBLÈMES CRITIQUES (Bloquent l'usage)

### Problème #1: Settings ferme l'application
**Sévérité**: CRITIQUE
**Description**: En cliquant "OK" dans Settings, toute l'application se ferme
**Attendu**: Settings se ferme, application continue en arrière-plan
**Test effectué**: Ouvrir Settings → Cliquer OK → Application ferme
**Cause probable**: closeEvent mal géré ou parent/child relationship

### Problème #2: Icône reste ROUGE même avec config valide
**Sévérité**: CRITIQUE
**Description**: Même avec fichier config correct et modèle fonctionnel, icône reste rouge
**Attendu**: Icône verte si health check passe
**Test effectué**: Créer config → Configurer Ollama → Icône reste rouge
**Cause probable**: Health check ne se met pas à jour après settings change, ou health check échoue même avec bonne config

### Problème #3: Chat figé quand on envoie
**Sévérité**: CRITIQUE
**Description**: Quand on appuie Ctrl+Enter, l'application se fige en attendant la réponse
**Attendu**: Interface reste réactive, les tokens arrivent progressivement
**Test effectué**: Chat → Ctrl+Enter → Application figée jusqu'à réponse
**Cause probable**: `QApplication.processEvents()` ne suffit pas, besoin vrai threading

### Problème #4: Menu contextuel n'est pas fonctionnel
**Sévérité**: IMPORTANTE
**Description**: Menu apparaît mais ne répond pas aux clics
**Attendu**: Cliquer sur "Summarize" → Obtenir résumé
**Test effectué**: Ctrl+Right-Click → Cliquer sur item → Rien ne se passe
**Cause probable**: Événement click ne se propage, ou signal pas connecté

### Problème #5: Menu Windows s'affiche par-dessus
**Sévérité**: IMPORTANTE (Cosmétique mais problématique)
**Description**: Le menu contextuel Windows s'affiche aussi avec notre menu
**Attendu**: Voir UNIQUEMENT notre menu, pas le menu système
**Test effectué**: Ctrl+Right-Click → Voir 2 menus
**Cause probable**: pynput ne bloque pas le clic souris, besoin Windows API ou autre approche

---

## 📊 Statut des Corrections Tentées

### Corrections Partiellement Réussies (Code implémenté mais bugs subsistent)

| Correction | État | Détails |
|-----------|------|---------|
| Chat Ctrl+Enter | ✅ CODE OK | Signal `sig_input_submitted` connecté, handler `_on_chat_message_submitted()` ajouté, méthode `_stream_chat_response()` implémentée. **MAIS**: Application figée quand on appuie Ctrl+Enter (blocage UI principal) |
| MenuItem click handlers | ✅ CODE OK | Ajouté `mousePressEvent()`, `enterEvent()`, `leaveEvent()` à MenuItem + signal `clicked`. **MAIS**: Menu items toujours non-clickables en pratique |
| Test Connection Button | ✅ CODE OK | Corrigé signature `LLMProviderFactory.create()` pour passer dict config. **MAIS**: Icon reste rouge après config |
| Réponses en français | ✅ OK | Tous les prompts mis à jour pour demander réponses en français |
| Model dropdown | ✅ CODE OK | Changé QLineEdit → QComboBox, ajouté "Refresh Models" button, auto-fetch. **MAIS**: Pas testé en production |
| closeEvent handlers | ✅ CODE OK | Ajouté `closeEvent()` à ResponseWindow, FloatingMenu, SettingsDialog. **MAIS**: Settings ferme encore l'app |
| QApplication.processEvents() | ⚠️ PARTIEL | Ajouté dans boucles streaming pour UI responsiveness. **MAIS**: App figée quand même |

### Résumé
**Statut**: 8 corrections de code implémentées, mais **5 problèmes critiques persistent**. Les bugs sont probablement dus à:
- Architecture UI incorrecte (parent/child relationships)
- Besoin vrai threading pour non-blocking operations
- Event propagation ou signal connections toujours cassées

---

## 📝 Tâches à Ajouter à Phase 3

### Task 3.1: Fixer Settings Dialog closeEvent
- [ ] Tester settings.exec() vs show()
- [ ] Vérifier parent/child relationships
- [ ] Assurer settings fermeture ≠ app shutdown

### Task 3.2: Fixer Health Check Update
- [ ] Health check doit se relancer après settings change
- [ ] Icon doit devenir verte si health check passe
- [ ] Tester avec config valide

### Task 3.3: Fixer Chat Freeze (Threading)
- [ ] Implémenter vrai QThread pour streaming
- [ ] Non-blocking UI pendant réponse LLM
- [ ] Tokens arrivent progressivement sans gèle

### Task 3.4: Fixer Menu Contextuel Click
- [ ] Déboguer pourquoi clics ne fonctionnent pas
- [ ] Tester signal connections
- [ ] Vérifier event propagation

### Task 3.5: Bloquer Menu Windows
- [ ] Trouver solution pour empêcher menu système
- [ ] Options: pynput suppression event, Windows API, ou autre
- [ ] Tester solution

---

## 📋 État de la Documentation

| Document | Statut | Action |
|----------|--------|--------|
| README.md | ? | À vérifier |
| SETUP.md | ? | À vérifier |
| UAT_DETAILED_GUIDE.md | ❌ PÉRIMÉ | À mettre à jour |
| HOTFIX_NOTES.md | ✅ À jour | OK |
| FINAL_UAT_FIXES.md | ❌ PÉRIMÉ | À effacer/mettre à jour |

---

## 🎯 Prochaines Étapes

1. **Audit de Documentation** (THIS SESSION)
   - Vérifier tous les docs
   - Corriger informations périmées
   - Clarifier quoi tester

2. **Mise à Jour des Tâches** (THIS SESSION)
   - Ajouter Tasks 3.1-3.5 comme sous-tâches
   - Clarifier dépendances
   - Créer plan de test

3. **Correction des Bugs** (NEXT SESSION)
   - Corriger une tâche à la fois
   - Tester complètement
   - Documenter résultat
