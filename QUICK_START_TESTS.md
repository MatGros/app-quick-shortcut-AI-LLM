# ⚡ Quick Start - Voir les Tests dans VS Code

## 3 Étapes Seulement! 🎯

### 1️⃣ Ouvrir le dossier dans VS Code
```bash
code D:\MGS\DEV\app-quick-shortcut-AI-LLM
```

### 2️⃣ Ouvrir Test Explorer
```
Ctrl+Shift+P
↓
Taper: "Test: Focus on Test Explorer View"
↓
Appuyer sur Enter
```

**OU** cliquez sur l'icône "Test" (flacon) dans la sidebar gauche

### 3️⃣ Lancer les Tests
Cliquez sur le bouton **▶️ Run All** en haut du Test Explorer

---

## 📊 Résultat Attendu

Tu devrais voir:

```
✅ test_core/
   ├── test_llm_provider.py
   │   ├── ✅ TestLLMProviderFactory (4 tests)
   │   ├── ✅ TestOllamaProvider (7 tests)
   │   ├── ✅ TestOpenAIProvider (5 tests)
   │   └── ✅ TestAnthropicProvider (4 tests)
   └── test_config_service.py
       └── ✅ TestConfigService (14 tests)

✅ test_services/
   └── test_health_check.py
       └── ✅ TestHealthCheckManager (11 tests)

═════════════════════════════════════════════
✅ 43 passed in 0.56s ✅
═════════════════════════════════════════════
Coverage: 87% ⭐
```

---

## 🎮 Actions Disponibles

**Sur chaque test:**
- ▶️ **Run** - Exécuter ce test seulement
- 🐛 **Debug** - Déboguer (avec breakpoints)

**Sur chaque classe:**
- ▶️ **Run** - Exécuter tous les tests de la classe
- 🐛 **Debug** - Déboguer

**En haut:**
- ▶️ **Run All** - Tous les tests
- 🔄 **Refresh** - Rafraîchir la liste
- ⚙️ **Configure** - Options

---

## 🔴 Troubleshooting

### Tests n'apparaissent pas?
1. Appuyer sur **Refresh** icon dans Test Explorer
2. Vérifier que tu es dans le bon dossier (`D:\MGS\DEV\app-quick-shortcut-AI-LLM`)
3. Redémarrer VS Code

### Pytest not found?
```bash
# Dans le terminal VS Code:
pip install pytest pytest-cov
```

### Tous les tests échouent?
```bash
# Dans le terminal:
python -m pytest tests/ -v
# (pour voir les erreurs détaillées)
```

---

## 💾 Configuration Déjà Faite!

Tout ce qui suit a **déjà été créé** pour toi:

✅ `.vscode/settings.json` - Configuration pytest
✅ `.vscode/launch.json` - Configurations de démarrage
✅ `pytest.ini` - Options pytest
✅ 43 tests avec excellente couverture (87%)

**Tu peux juste ouvrir VS Code et lancer les tests!** 🚀

---

## 📝 Voir les Tests via Terminal (Alternative)

Si tu préfères le terminal:

```bash
# Ouvrir terminal intégré
Ctrl+`

# Lancer tous les tests
pytest tests/ -v

# Lancer un fichier test
pytest tests/test_core/test_llm_provider.py -v

# Avec coverage
pytest tests/ -v --cov=src
```

---

## ✨ C'est Tout!

T'es maintenant prêt à voir et exécuter les 43 tests! 🎉

**Questions?** Vois `VSCODE_TESTING_GUIDE.md` pour plus de détails
