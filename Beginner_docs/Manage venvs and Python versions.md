## Python, venv, and Package Management on Mac 
### (PyCharm-friendly, Conda-free)

This workflow lets you **avoid Conda environments** (which don’t play well with PyCharm) and keep Python and venvs simple.
This is preferable even if you used Anaconda to install python.

## Key advantages

1. **Easily update** to the latest version of Python (system-wide). Just swap out your venv in PyCharm’s Interpreter window.
2. **Use different venvs per project** (for older Python or package combos, if needed).
3. **Python version is fixed per venv**, but you can always update packages within the venv.
4. Use **Homebrew to install older Python versions** if needed.
5. This setup works seamlessly with **GitHub and PyPI**.

---

## Steps (macOS)

**Examples:** `python 3.13` (latest), `python 3.11` (old version).

---
### 1. List system-wide installed Python versions

```sh
ls /Library/Frameworks/Python.framework/Versions/   # Official Python.org installs
ls /opt/homebrew/lib/                              # Homebrew Pythons show here
```

---

### 2. Check latest stable Python version

Go to [python.org/downloads](https://www.python.org/downloads/) and note the latest release (e.g., Python 3.13.3).

---

### 3. Install or update Python

**A. To install the latest Python (recommended):**

- Download the `.pkg` installer for Mac from [python.org](https://www.python.org/downloads/mac-osx/).
- Run the installer.
- Confirm install:
    ```sh
    ls /Library/Frameworks/Python.framework/Versions/
    /Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13 --version
    ```

**B. To install *older* versions via Homebrew:**

- Install Homebrew if not present:
    ```sh
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
- Install desired version (example: 3.11):
    ```sh
    brew install python@3.11
    ```
- Confirm:
    ```sh
    /opt/homebrew/bin/python3.11 --version
    ```

---

### 4. Clean up old venvs and PyCharm interpreters

- Deactivate any active venv in your terminal (if any):
    ```sh
    deactivate
    ```
- In PyCharm:  
    - Go to Settings → Project → Python Interpreter  
    - Click the blue up& down arrows → Show All  
    - Select obsolete interpreter and click on -   
    - You’ll add your new venv interpreter below

---

### 5. See all your venvs

```sh
ls ~/PyCharmProjects/venvs
find ~/PyCharmProjects/venvs -type d -name bin
```

---

### 6. Create new venvs

**A. For the newest Python (e.g., 3.13):**
```sh
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13 -m venv ~/PyCharmProjects/venvs/venv_313
ls -l ~/PyCharmProjects/venvs/venv_313/bin/python
```

**B. For an older Python (e.g., 3.11 via Homebrew):**
```sh
/opt/homebrew/bin/python3.11 -m venv ~/PyCharmProjects/venvs/venv_311
ls -l ~/PyCharmProjects/venvs/venv_311/bin/python
```

_Tip: Name venvs for special combos, e.g., `venv_313_numpy_old`._

---


### 7. Configure your venv(s) in PyCharm

- Go to Settings → Project Interpreter → Add Interpreter → Add Local Interpreter
- Select:  
    - Environment: **Existing environment**  
    - Type: **Python** (not Conda)  
    - Python Path: (e.g.) `~/PyCharmProjects/venvs/venv_313/bin/python`
- Click OK, then Apply  
- Your new venv should now show up at the bottom right (e.g., "Python 3.13 virtualenv …")

---

### 8. Select or change venv for any project

1. Open your project in PyCharm.
2. Settings (Cmd+,) → Project: *your_project* → Python Interpreter.
3. Click the blue up& down arrows → Show All → Show All…
4. Select the venv interpreter you want (e.g., `venv_311`).
5. Click OK or Apply.
6. Confirm it shows as selected.

---

## FAQ

**Q: Will this break GitHub or PyPI uploads?**  
A: No — venv folders are not included if you use `.gitignore`.

**Q: Do I need to deactivate before creating a new venv?**  
A: Not required for this workflow, but can help avoid confusion.

**Q: Can I update Python in-place in a venv?**  
A: No — create a new venv with the new Python version and install packages there.

**Q: Can I delete old venvs?**  
A: Yes — delete their folders in `~/PyCharmProjects/venvs/` and remove in PyCharm if shown.

---

## Best Practices

- Store all venvs in `~/PyCharmProjects/venvs/` with clear, versioned names.
- Document any custom/old package versions for reproducibility.
- For publishing: create `requirements.txt` only for repos you share.

---

**Save this file for reference and you’ll rarely need to revisit these steps again!**