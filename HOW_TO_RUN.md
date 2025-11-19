# 🎮 How to Run the App - Visual Guide

## 🚀 **Easiest Way: One-Click Run in VS Code**

### Step 1: Open the Project in VS Code
```bash
cd "AI PROMPT OPTIMIZER"
code .
```

### Step 2: Click the Run Button

Look at the **LEFT SIDEBAR** of VS Code:

```
┌─────────────────────────┐
│  📁 Explorer            │
│  🔍 Search             │
│  ⎇  Source Control     │
│  ▶️ Run and Debug  ← CLICK HERE!
│  📦 Extensions         │
└─────────────────────────┘
```

### Step 3: Select Configuration

At the top of the Debug panel, you'll see a dropdown:

```
┌────────────────────────────────────┐
│ 🚀 Run Streamlit App        ▾     │  ← Click dropdown
└────────────────────────────────────┘

Options:
  • 🚀 Run Streamlit App (Default)
  • 🎯 Run Prompt Lab (Direct)
  • 🐛 Debug Mode (with breakpoints)
  • ✅ Run Setup Check
```

### Step 4: Click the Green Play Button

```
┌────────────────────────────────────┐
│ 🚀 Run Streamlit App        ▾     │
│                                    │
│   ▶️  Start Debugging    ← CLICK!│
└────────────────────────────────────┘
```

**OR just press `F5` on your keyboard!**

### ✨ That's It!

The app will:
- ✅ Start automatically
- ✅ Open in your browser
- ✅ Show you the terminal output
- ✅ Auto-reload when you save files

---

## 🎯 Alternative Methods

### Method A: Using Tasks (Command Palette)

1. Press **`Ctrl+Shift+P`** (Windows/Linux) or **`Cmd+Shift+P`** (Mac)
2. Type: `Tasks: Run Task`
3. Select: **🚀 Run Streamlit App**

```
┌────────────────────────────────────┐
│ > Tasks: Run Task                  │
│                                    │
│   🚀 Run Streamlit App            │  ← Select this
│   📦 Install Dependencies          │
│   ✅ Check Setup                   │
│   🧹 Clean Cache                   │
│   🌐 Open in Browser               │
└────────────────────────────────────┘
```

### Method B: Terminal Commands

**Windows:**
```bash
# Quick run
run_app.bat

# Or manually
streamlit run app.py
```

**Mac/Linux:**
```bash
# Quick run
./run_app.sh

# Or manually
streamlit run app.py
```

### Method C: Python Command

```bash
python -m streamlit run app.py
```

---

## 🐛 Debug Mode (For Developers)

### How to Set Breakpoints:

1. Open any `.py` file
2. Click in the **gutter** (left of line numbers)
3. A **red dot** appears = breakpoint set

```python
def my_function():
    x = 10        ← Click here to add breakpoint
    y = 20
    return x + y
```

### How to Debug:

1. Set your breakpoints
2. Select **🐛 Debug Mode** from dropdown
3. Press **F5** or click Start Debugging
4. When code hits breakpoint:
   - **F10** - Step Over (next line)
   - **F11** - Step Into (go inside function)
   - **Shift+F11** - Step Out (exit function)
   - **F5** - Continue (run until next breakpoint)

### Debug Panel Features:

```
┌─────────────────────────────────┐
│ VARIABLES                        │  ← See all variable values
│   x = 10                         │
│   y = 20                         │
│                                  │
│ WATCH                            │  ← Add expressions to watch
│   x + y = 30                     │
│                                  │
│ CALL STACK                       │  ← See function call chain
│   my_function (line 5)          │
│   main (line 10)                │
└─────────────────────────────────┘
```

---

## 🎮 Keyboard Shortcuts

| Action | Shortcut | Description |
|--------|----------|-------------|
| **Run/Debug** | `F5` | Start the default config |
| **Stop** | `Shift+F5` | Stop debugging |
| **Restart** | `Ctrl+Shift+F5` | Restart debugging |
| **Toggle Breakpoint** | `F9` | Add/remove breakpoint |
| **Step Over** | `F10` | Next line (debug mode) |
| **Step Into** | `F11` | Into function (debug mode) |
| **Step Out** | `Shift+F11` | Out of function (debug mode) |
| **Command Palette** | `Ctrl+Shift+P` | Open command menu |
| **Terminal** | `` Ctrl+` `` | Show/hide terminal |

---

## 📊 What You'll See

### Terminal Output:
```
Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

### Browser:
- App automatically opens at `http://localhost:8501`
- You'll see the beautiful homepage with neon gradients!

---

## 🔧 Configuration Files Reference

All debug configurations are in `.vscode/` folder:

```
.vscode/
├── launch.json         → Debug configurations
├── tasks.json          → Quick tasks
├── settings.json       → Workspace settings
├── extensions.json     → Recommended extensions
└── README_VSCODE.md   → Detailed VS Code guide
```

**See [.vscode/README_VSCODE.md](.vscode/README_VSCODE.md) for advanced usage!**

---

## 💡 Pro Tips

### 1. **Auto-Reload is Enabled**
   - Save any `.py` file → App reloads automatically
   - No need to restart manually!

### 2. **View Multiple Pages**
   - Keep app running
   - Edit different page files
   - Navigate between pages in browser

### 3. **Quick Restart**
   - Press `Ctrl+C` in terminal
   - Press `F5` to restart
   - Or click Stop ▢ then Start ▶️

### 4. **Clean Restart**
   - Run task: **🧹 Clean Cache**
   - Then run: **🚀 Run Streamlit App**

### 5. **Check Configuration**
   - Before first run: **✅ Run Setup Check**
   - Verifies everything is installed correctly

---

## 🚨 Troubleshooting

### ❌ "Cannot find module 'streamlit'"

**Fix:**
1. Press `Ctrl+Shift+P`
2. Type: `Tasks: Run Task`
3. Select: **📦 Install Dependencies**

Or run manually:
```bash
pip install -r requirements.txt
```

### ❌ "Port 8501 is already in use"

**Fix:**
1. Press `Shift+F5` to stop current app
2. Or kill the process:
   ```bash
   # Windows
   taskkill /F /IM streamlit.exe

   # Mac/Linux
   pkill -f streamlit
   ```

### ❌ "No API key configured"

**Fix:**
1. Make sure `.env` file exists
2. Edit `.env` and add your key:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```
3. Restart the app

### ❌ Breakpoints not working

**Fix:**
- Use **🐛 Debug Mode** configuration (not regular Run)
- Make sure file is saved
- Check breakpoint is on an executable line

---

## 🎓 Next Steps

After running the app:

1. **🎯 Visit Prompt Lab** - Optimize your first prompt
2. **📚 Browse Templates** - Check pre-built templates
3. **🔬 Try Workflows** - Use the Literature Review workflow
4. **📊 View History** - See your optimization sessions

---

## 📚 More Help

- **Quick Setup**: [QUICKSTART.md](QUICKSTART.md)
- **Full Documentation**: [README.md](README.md)
- **VS Code Details**: [.vscode/README_VSCODE.md](.vscode/README_VSCODE.md)
- **Project Overview**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

**🎉 Happy Coding!** Press **F5** and let's optimize some prompts! 🚀
