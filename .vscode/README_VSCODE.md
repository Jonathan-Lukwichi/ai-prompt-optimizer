# VS Code Configuration Guide

This folder contains VS Code configurations to make development easier!

## 🚀 Quick Run Options

### Method 1: Debug Panel (Easiest!)

1. Click the **"Run and Debug"** icon in the left sidebar (▶️ icon)
2. Select one of these options from the dropdown:
   - **🚀 Run Streamlit App** - Start the main app
   - **🎯 Run Prompt Lab (Direct)** - Jump straight to Prompt Lab
   - **🐛 Debug Mode** - Run with debugging & breakpoints
   - **✅ Run Setup Check** - Verify your configuration
3. Click the green **"Start Debugging"** button (▶️)

The app will start and automatically open in your browser!

### Method 2: Keyboard Shortcut

Press **`F5`** to run the default configuration (Run Streamlit App)

### Method 3: Command Palette

1. Press **`Ctrl+Shift+P`** (Windows/Linux) or **`Cmd+Shift+P`** (Mac)
2. Type "Debug: Select and Start Debugging"
3. Choose "🚀 Run Streamlit App"

### Method 4: Tasks Menu

1. Press **`Ctrl+Shift+P`** (Windows/Linux) or **`Cmd+Shift+P`** (Mac)
2. Type "Tasks: Run Task"
3. Choose from:
   - **🚀 Run Streamlit App**
   - **📦 Install Dependencies**
   - **✅ Check Setup**
   - **🧹 Clean Cache**
   - **🌐 Open in Browser**

## 📁 Configuration Files

### `launch.json` - Debug Configurations

**Available Configurations:**

1. **🚀 Run Streamlit App**
   - Default configuration
   - Runs `home.py` on port 8502
   - Opens automatically in browser

2. **🎯 Run Prompt Lab (Direct)**
   - Skips homepage, goes straight to Prompt Lab
   - Useful for testing the main feature

3. **🐛 Debug Mode (with breakpoints)**
   - Full debugging support
   - Set breakpoints by clicking left of line numbers
   - Step through code, inspect variables
   - Includes debug logging

4. **✅ Run Setup Check**
   - Verifies your environment is configured
   - Checks dependencies, API keys, files

### `tasks.json` - Quick Commands

**Available Tasks:**

- **🚀 Run Streamlit App** - Start the application
- **📦 Install Dependencies** - Run `pip install -r requirements.txt`
- **✅ Check Setup** - Verify configuration
- **🧹 Clean Cache** - Remove `__pycache__` and compiled files
- **🌐 Open in Browser** - Open http://localhost:8502

### `settings.json` - Workspace Settings

Configures:
- Python interpreter (uses `venv/` if it exists)
- Auto-save enabled
- Format on save (using Black formatter)
- File exclusions for cleaner workspace
- Python linting (Flake8)

### `extensions.json` - Recommended Extensions

VS Code will prompt you to install these helpful extensions:
- **Python** - Python language support
- **Debugpy** - Python debugging
- **Pylance** - Fast Python IntelliSense
- **Jupyter** - Notebook support
- **Ruff** - Fast Python linter
- **IntelliCode** - AI-assisted code completion
- **Code Spell Checker** - Catch typos
- **GitLens** - Enhanced Git features

## 🎯 How to Use Each Configuration

### For Regular Development:

1. **First Time:**
   - Run task: **📦 Install Dependencies**
   - Run task: **✅ Check Setup**
   - Edit `.env` file with your API key

2. **Daily Work:**
   - Press **F5** to start the app
   - Edit code and save (auto-reload enabled)
   - View changes in browser

### For Debugging:

1. Set breakpoints:
   - Click left of line number (red dot appears)
   - Or press **F9** on any line

2. Run **🐛 Debug Mode**

3. When code hits breakpoint:
   - **F10** - Step over
   - **F11** - Step into
   - **Shift+F11** - Step out
   - **F5** - Continue
   - Hover over variables to see values

### For Testing Specific Features:

- Use **🎯 Run Prompt Lab (Direct)** to test the main optimization feature
- Edit the configuration in `launch.json` to test other pages

## 🔧 Customization

### Change Port Number:

Edit `launch.json` and change:
```json
"--server.port",
"8502"
```
to your preferred port.

### Add Your Own Configuration:

Copy an existing configuration in `launch.json` and modify:
```json
{
    "name": "My Custom Config",
    "type": "debugpy",
    "request": "launch",
    "module": "streamlit",
    "args": [
        "run",
        "${workspaceFolder}/pages/my_page.py"
    ],
    "console": "integratedTerminal"
}
```

### Add Custom Tasks:

Edit `tasks.json` and add:
```json
{
    "label": "My Task",
    "type": "shell",
    "command": "your-command-here"
}
```

## 💡 Pro Tips

1. **Quick Restart:**
   - Press **Ctrl+C** in terminal
   - Press **F5** to restart

2. **Multiple Terminals:**
   - Each debug session uses a new terminal
   - Close old terminals to keep workspace clean

3. **Auto-Reload:**
   - Streamlit auto-reloads when you save Python files
   - No need to restart manually!

4. **View Logs:**
   - Check the terminal output for errors
   - Streamlit shows helpful error messages

5. **Stop Debugging:**
   - Press **Shift+F5**
   - Or click the stop button in debug toolbar

## 🐛 Troubleshooting

### "Module 'streamlit' not found"
- Run task: **📦 Install Dependencies**
- Or manually: `pip install -r requirements.txt`

### "Python interpreter not found"
- Open Command Palette (**Ctrl+Shift+P**)
- Type "Python: Select Interpreter"
- Choose your Python installation or venv

### "Port already in use"
- Stop the running app (**Shift+F5**)
- Or change port in `launch.json`

### Breakpoints not working
- Make sure you're using **🐛 Debug Mode**
- Check that `"justMyCode": true` in `launch.json`
- Ensure the file is part of your workspace

## 🎓 Learning Resources

- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [VS Code Debugging](https://code.visualstudio.com/docs/editor/debugging)
- [Streamlit Documentation](https://docs.streamlit.io)

---

**Need help?** Check the main [README.md](../README.md) or open an issue!
