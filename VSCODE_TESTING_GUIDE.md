# VS Code Testing Guide 🧪

## Setup Rapide

### 1️⃣ Ouvrir le projet dans VS Code

```bash
code D:\MGS\DEV\app-quick-shortcut-AI-LLM
```

### 2️⃣ Extensions Recommandées

Installez ces extensions dans VS Code:
- **Python** (Microsoft) - Essential
- **Pylance** (Microsoft) - IntelliSense
- **Python Test Explorer** (Little Fox Team) - UI pour tests

### 3️⃣ Sélectionner l'Interpréteur Python

```
Ctrl+Shift+P → "Python: Select Interpreter"
→ Choisir l'interpréteur qui a pytest installé
```

---

## 🚀 Lancer les Tests

### Option 1: Test Explorer (Interface Graphique) ⭐ RECOMMANDÉ

1. **Ouvrir le Test Explorer**
   ```
   Ctrl+Shift+P → "Test: Focus on Test Explorer View"
   ```
   Ou cliquez sur l'icône "Test" dans la sidebar gauche (flacon)

2. **Voir tous les tests**
   ```
   test_core/
   ├── test_llm_provider.py
   │   ├── TestLLMProviderFactory
   │   ├── TestOllamaProvider
   │   ├── TestOpenAIProvider
   │   └── TestAnthropicProvider
   └── test_config_service.py
       └── TestConfigService

   test_services/
   └── test_health_check.py
       └── TestHealthCheckManager
   ```

3. **Exécuter les tests**
   - 🟢 Cliquer sur **Run All** (en haut)
   - ▶️ Cliquer sur **Run** à côté d'une classe ou fonction test
   - 🐛 Cliquer sur **Debug** pour déboguer un test

### Option 2: Terminal Intégré

Appuyez sur `Ctrl+`` pour ouvrir le terminal intégré:

```bash
# Lancer tous les tests
python -m pytest tests/ -v

# Lancer un fichier test spécifique
python -m pytest tests/test_core/test_llm_provider.py -v

# Lancer une classe test
python -m pytest tests/test_core/test_config_service.py::TestConfigService -v

# Lancer un test spécifique
python -m pytest tests/test_core/test_config_service.py::TestConfigService::test_config_singleton -v

# Avec coverage
python -m pytest tests/ -v --cov=src --cov-report=html

# Ouvrir le rapport coverage HTML
start htmlcov/index.html
```

### Option 3: VS Code Launch Configurations

Appuyez sur `F5` ou `Ctrl+Shift+D`:

1. **Cliquer sur "Run and Debug"**
2. **Sélectionner une configuration:**
   - `Python: Run Tests` - Exécute tous les tests
   - `Python: Run Tests with Coverage` - Génère rapport HTML

---

## 👀 Voir les Résultats des Tests

### Test Explorer View
- ✅ Green check = Test passed
- ❌ Red X = Test failed
- ⏳ Clock = Test running

### Output Panel
- Affiche les résultats détaillés
- Montre les erreurs & stack traces

### Coverage Report
Après `python -m pytest tests/ --cov=src --cov-report=html`:
```
htmlcov/
└── index.html  ← Ouvrir dans le navigateur
```

---

## 🎯 Scénarios Courants

### Voir tous les tests et leur statut
```
Test Explorer → Run All
```

### Déboguer un test qui échoue
```
Test Explorer → Cliquer sur le test → Debug (icon)
```

### Exécuter un seul test rapidement
```
Test Explorer → Click sur test → Run
```

### Voir la couverture du code
```
Terminal: python -m pytest tests/ --cov=src --cov-report=term-missing
```

### Voir quels tests testent une fonction spécifique
```
Ctrl+Shift+F → Chercher la fonction
→ Voir tous les usages
```

---

## 📊 Interpréter les Résultats

### Format Résultat Standard
```
tests/test_core/test_config_service.py::TestConfigService::test_config_singleton PASSED [  2%]
tests/test_core/test_config_service.py::TestConfigService::test_config_get_default PASSED [  4%]
...
======================== 43 passed, 1 warning in 0.56s ========================
```

### Couverture
```
src\core\config_service.py    : 93% ⭐ (excellent)
src\core\llm_provider.py      : 89% ⭐ (very good)
TOTAL                         : 87% ⭐ (great)
```

### Tout est Green ✅?
**YES!** Tous les 43 tests passent!

---

## 💡 Tips & Tricks

### 🔄 Auto-run tests on save
Dans `.vscode/settings.json` (déjà configuré):
```json
"python.testing.pytestEnabled": true
```

### 🎨 Colorized Output
Tests sont colorisés:
- Green = ✅ Passed
- Red = ❌ Failed
- Yellow = ⚠️ Warning

### 🔍 Filter Tests
Test Explorer → Cliquer sur "Filter" icon

### 🔗 Click to Go To Test
Dans results → Ctrl+Click sur test name → Va au code

### 📝 View Test Code
Test Explorer → Right-click → "Go to Test"

---

## 🐛 Debugging Tests

### Ajouter des Breakpoints
1. Cliquer sur la ligne de code dans le test
2. Appuyer sur `F9` (ou cliquer dans la marge gauche)
3. Cliquer sur "Debug" pour ce test

### Voir les Variables
Lors du debug:
- Variables locales → left panel
- Hover sur variable → voir value
- Console → taper commandes Python

### Exécution Pas-à-Pas
- `F10` = Step over (suivant ligne)
- `F11` = Step into (enter fonction)
- `Shift+F11` = Step out (sortir fonction)
- `F5` = Continue

---

## ✨ Résumé des Commandes Clés

| Action | Shortcut | Menu |
|--------|----------|------|
| Ouvrir Tests | Ctrl+Shift+P + "Test" | View → Test Explorer |
| Run All | Click Play icon | - |
| Run One | Click Play → Test | - |
| Debug Test | Click Debug → Test | - |
| Terminal | Ctrl+` | - |
| Run Tests (Terminal) | `pytest tests/ -v` | - |

---

## 🎬 Quick Start Checklist

- [ ] VS Code ouvert
- [ ] Extensions Python installées
- [ ] Interpréteur Python sélectionné (F1 → "Select Interpreter")
- [ ] Test Explorer visible (Ctrl+Shift+P → "Test: Focus...")
- [ ] Voir 43 tests dans Test Explorer
- [ ] Cliquer "Run All" → Attendre résultats
- [ ] Voir 43 ✅ Green → **SUCCESS!**

---

## 📞 Need Help?

Si tests ne s'affichent pas:
1. Vérifier qu'on est dans le bon dossier projet
2. Vérifier que pytest est installé: `pip list | grep pytest`
3. Redémarrer VS Code
4. Vérifier `.vscode/settings.json` est correct

**Tout est configuré! Tu peux maintenant voir et exécuter les tests! 🚀**
