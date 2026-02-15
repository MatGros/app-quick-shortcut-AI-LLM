# 🔧 Environment Setup Guide

> **IMPORTANT**: This project uses a **Python Virtual Environment** to avoid polluting your system Python installation.

---

## 📋 What is a Virtual Environment?

A virtual environment is an **isolated Python directory** where:
- Dependencies for this project are installed locally (not system-wide)
- Different projects can use different versions of the same library
- Your system Python stays clean and unaffected

**Think of it like a "sandbox" for this project** 🏜️

---

## 🚀 First Time Setup (5 minutes)

### Windows PowerShell / CMD

```bash
# 1. Navigate to project directory
cd D:\MGS\DEV\app-quick-shortcut-AI-LLM

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
.\venv\Scripts\activate

# Windows PowerShell if above fails:
# .\venv\Scripts\Activate.ps1

# 4. Verify activation (you should see (venv) prefix in terminal)
# (venv) C:\path\to\project>

# 5. Upgrade pip
python -m pip install --upgrade pip

# 6. Install project dependencies
pip install -r requirements.txt

# 7. Verify setup
python -c "import PySide6; import pytest; print('✅ Environment ready!')"
```

### Linux / macOS

```bash
# 1. Navigate to project directory
cd /path/to/app-quick-shortcut-AI-LLM

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Verify activation (you should see (venv) prefix)
# (venv) user@machine:~/project$

# 5. Upgrade pip
python -m pip install --upgrade pip

# 6. Install project dependencies
pip install -r requirements.txt

# 7. Verify setup
python -c "import PySide6; import pytest; print('✅ Environment ready!')"
```

---

## ✅ How to Know It's Working

After activation, you should see:

```
(venv) C:\path\to\project>
```

The `(venv)` prefix confirms your virtual environment is **active**.

---

## 📦 What Gets Installed?

When you run `pip install -r requirements.txt`, **ONLY these packages** are installed:

```
Core:
  - PySide6-Essentials  (Qt GUI framework)
  - pynput              (Global keyboard/mouse hooks)
  - requests            (HTTP client)

Development:
  - pytest              (Testing framework)
  - pytest-qt           (Qt testing)
  - pytest-cov          (Coverage reports)
  - black               (Code formatter)
  - ruff                (Linter)

Build:
  - Nuitka              (Executable builder)
```

**Your system Python is UNTOUCHED** ✨

---

## 🔄 Everyday Usage

### Before Working on Code

```bash
# 1. Open terminal in project directory
cd D:\MGS\DEV\app-quick-shortcut-AI-LLM

# 2. Activate venv (every time you open a new terminal)
.\venv\Scripts\activate

# (venv) should appear in terminal prefix
```

### After Each Git Pull

```bash
# If requirements.txt changed, reinstall dependencies
pip install -r requirements.txt
```

### Running Tests

```bash
# Make sure (venv) is active first!
pytest tests/ -v --cov=src
```

### Installing New Package

```bash
# Install in venv (not system)
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt
```

---

## 🔐 Configuration with .env

### What is .env?

A `.env` file stores **sensitive configuration** that should NOT be in git:

```
API Keys        ← NEVER commit these!
Passwords       ← NEVER commit these!
Local settings  ← Per-user configuration
```

### Files in This Project

```
✅ .env.example       ← Template (SAFE to commit)
✅ .env               ← Actual config (IGNORED by git)
✅ .gitignore         ← Tells git to ignore .env
```

### How to Use .env

**First time setup:**
```bash
# 1. Copy template
copy .env.example .env    # Windows
cp .env.example .env      # Linux/Mac

# 2. Edit .env with your settings
# Edit OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.

# 3. Python automatically loads .env
# (python-dotenv is optional, but config.json preferred)
```

**In code:**
```python
from src.core.config_service import ConfigService

# ConfigService loads from:
# 1. config.json in %APPDATA%
# 2. Environment variables as fallback
# 3. defaults if nothing provided

config = ConfigService()
api_key = config.get("providers")[0]["api_key"]
```

---

## 🛡️ Security Best Practices

### ✅ DO This

```bash
# ✅ Add .env to .gitignore (already done)
# ✅ Keep API keys in .env (not in code)
# ✅ Use .env.example as template
# ✅ Commit .env.example so others know what to set
```

### ❌ DON'T Do This

```bash
# ❌ Never commit .env with real API keys
# ❌ Never hardcode API keys in Python files
# ❌ Never share .env in public repos
# ❌ Never send .env via email/chat
```

**If you accidentally commit .env:**
```bash
# Remove from git history (be careful!)
git rm --cached .env
git commit -m "Remove .env from tracking"
# Then notify team to rotate API keys
```

---

## 🚨 Troubleshooting

### "python is not recognized"

**Windows:**
```bash
# Use full path to Python
C:\Users\YourName\AppData\Local\Programs\Python\Python310\python.exe -m venv venv

# OR check if Python is in PATH
python --version
```

### "no module named PySide6"

```bash
# Verify venv is activated (check for (venv) prefix)
.\venv\Scripts\activate

# Reinstall requirements
pip install -r requirements.txt
```

### "Permission denied on activate.ps1"

```bash
# PowerShell execution policy issue
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activation again
.\venv\Scripts\Activate.ps1
```

### How to Completely Reset venv

```bash
# 1. Deactivate (if active)
deactivate

# 2. Delete venv directory
rmdir /s venv    # Windows
rm -rf venv      # Linux/Mac

# 3. Recreate from scratch
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📊 Verification Checklist

After setup, verify everything:

```bash
# ✅ Virtual environment active?
echo %VIRTUAL_ENV%    # Windows - should show path to venv

# ✅ Python from venv?
which python          # Linux/Mac - should show venv/bin/python
where python          # Windows - should show venv\Scripts\python.exe

# ✅ All packages installed?
pip list | grep -i pyside6

# ✅ Tests discoverable?
pytest --collect-only tests/

# ✅ All tests passing?
pytest tests/ -v --tb=short
```

---

## 🔄 GitHub Workflow with venv

When sharing code on GitHub:

```
✅ COMMIT these:
  - requirements.txt (what to install)
  - .env.example (template)
  - All .py files
  - .gitignore

❌ DON'T COMMIT:
  - venv/ directory (huge!)
  - .env file (secrets!)
  - __pycache__/
  - .pytest_cache/
  - .coverage
```

**Other developers will:**
```bash
git clone <repo>
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

## 💡 Pro Tips

### Activate venv Automatically in VS Code

Create `.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true
}
```

### Save Environment to requirements.txt

```bash
# Whenever you install a new package:
pip freeze > requirements.txt

# Or just the important ones (cleaner):
pip freeze | grep -v "^\-e" > requirements.txt
```

### Create Multiple venvs (Advanced)

```bash
# For different Python versions
python3.10 -m venv venv3.10
python3.11 -m venv venv3.11
```

---

## 📚 Further Reading

- [Python venv documentation](https://docs.python.org/3/tutorial/venv.html)
- [pip requirements.txt format](https://pip.pypa.io/en/latest/reference/requirements-file-format/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

---

## ✅ You're Ready!

Once you've:
1. ✅ Created venv
2. ✅ Activated venv
3. ✅ Installed requirements.txt
4. ✅ Verified with `pytest tests/ -v`

**You have a clean, isolated Python environment for this project!** 🎉

Now you can safely develop without affecting your system Python.

**Questions?** Check `.env.example` or `README.md` for quick start.
