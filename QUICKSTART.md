# 🚀 Quick Start Guide

Get your AI Prompt Optimizer running in 5 minutes!

## Step 1: Install Python Dependencies

Open your terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

## Step 2: Set Up Your API Key

### Option A: OpenAI (Recommended)

1. Get an API key from [platform.openai.com](https://platform.openai.com/api-keys)
2. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env    # Windows
   cp .env.example .env      # macOS/Linux
   ```
3. Open `.env` and add your key:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

### Option B: Anthropic (Claude)

1. Get an API key from [console.anthropic.com](https://console.anthropic.com/)
2. Add to `.env`:
   ```
   ANTHROPIC_API_KEY=your-anthropic-key-here
   ```

## Step 3: Run the App

```bash
streamlit run home.py
```

The app will automatically open in your browser at `http://localhost:8501`

## Step 4: Start Optimizing!

1. Go to **🎯 Prompt Lab** (sidebar or homepage button)
2. Select your academic role and task type
3. Enter your prompt
4. Click **🚀 Optimize My Prompt**
5. Get 4 optimized versions instantly!

---

## Troubleshooting

### "Command 'streamlit' not found"
```bash
pip install streamlit --upgrade
```

### "No module named 'openai'"
```bash
pip install -r requirements.txt
```

### "Invalid API key"
- Check that your `.env` file exists
- Make sure the API key is correct (no extra spaces)
- Restart the app after adding the key

---

## Next Steps

- **Browse Templates**: Check out pre-built templates in the 📚 Templates page
- **Try Workflows**: Use guided workflows for complex tasks in 🔬 Workflows
- **View History**: See all your past sessions in 📊 History

---

**Need help?** Check the [full README](README.md) or open an issue on GitHub.
