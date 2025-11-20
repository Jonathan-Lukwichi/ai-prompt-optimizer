# 🚀 Quick Setup Guide - AI Prompt Optimizer

## ✨ Get Started in 5 Minutes with FREE Google Gemini API!

---

## 📋 **Prerequisites**

- Python 3.8 or higher
- pip (Python package manager)
- Google account (for free Gemini API)

---

## 🎯 **Step 1: Get Your FREE Gemini API Key**

### Option A: Google AI Studio (Recommended - Easiest!)

1. Visit: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Click **"Create API key in new project"** (or select existing project)
5. **Copy your API key** (starts with `AIza...`)

### Option B: Google Cloud Console

1. Visit: https://console.cloud.google.com/
2. Create a new project or select existing
3. Enable the "Generative Language API"
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Copy your API key

**✅ That's it! Gemini has a generous FREE tier:**
- 60 requests per minute
- 1,500 requests per day
- Perfect for personal use and testing!

---

## 🔧 **Step 2: Configure Your API Key**

1. **Open the `.env` file** in the project root directory
2. **Replace** `your_gemini_api_key_here` with your actual API key:

```env
GEMINI_API_KEY=AIzaSyABC123...your-actual-key-here
```

3. **Save the file**

**⚠️ IMPORTANT:** Never share your `.env` file or commit it to GitHub!

---

## 📦 **Step 3: Install Dependencies**

Open your terminal/command prompt in the project directory and run:

```bash
# Install all required packages
pip install -r requirements.txt
```

This will install:
- ✅ streamlit (web framework)
- ✅ google-generativeai (Gemini API)
- ✅ sqlalchemy (database)
- ✅ openai (optional - if you want to use OpenAI later)
- ✅ anthropic (optional - if you want to use Claude later)
- ✅ And other dependencies...

**Expected install time:** 1-2 minutes

---

## 🎨 **Step 4: Run the App**

### Option A: Using Streamlit Command (Recommended)

```bash
streamlit run home.py
```

### Option B: Using Python Module

```bash
python -m streamlit run home.py
```

### Option C: Using VS Code (F5)

1. Open the project in VS Code
2. Press **F5** (or Run → Start Debugging)
3. The app will automatically open in your browser

**🎉 Success!** Your app should open automatically at:
```
http://localhost:8501
```

---

## 🧪 **Step 5: Test the App**

### Quick Test Flow:

1. **Go to "Prompt Lab"** (🎯 in sidebar)
2. **Enter a test prompt**, for example:
   ```
   I need help understanding how neural networks work
   ```
3. **Click "🚀 Optimize My Prompt"**
4. **Wait 5-10 seconds** for Gemini to generate optimized versions
5. **View your results!** You should see:
   - ✅ Clarity and Safety scores
   - ✅ 4 optimized prompt versions
   - ✅ Identified risks and suggestions

**If you see optimized prompts → Everything works! 🎉**

---

## ❓ **Troubleshooting**

### Problem: "No API keys configured"

**Solution:**
- Make sure you saved the `.env` file after adding your key
- Restart the Streamlit app (Ctrl+C, then run again)
- Check that your key starts with `AIza`

### Problem: "API key not valid"

**Solution:**
- Go back to https://makersuite.google.com/app/apikey
- Make sure the API is enabled
- Try generating a new API key
- Copy the ENTIRE key (including `AIza` prefix)

### Problem: "Package not found" errors

**Solution:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Install requirements again
pip install -r requirements.txt
```

### Problem: "Port 8501 already in use"

**Solution:**
```bash
# Use a different port
streamlit run home.py --server.port 8502
```

### Problem: Database errors

**Solution:**
```bash
# Delete and recreate the database
# (Safe - it's empty anyway)
# On Windows:
del data\prompts.db

# On Mac/Linux:
rm data/prompts.db

# Then restart the app
streamlit run home.py
```

---

## 🎛️ **Advanced Configuration**

### Switch to OpenAI (Paid)

1. Get OpenAI API key from: https://platform.openai.com/api-keys
2. Edit `.env`:
   ```env
   OPENAI_API_KEY=sk-your-key-here
   LLM_PROVIDER=openai
   ```
3. Restart the app

### Switch to Anthropic Claude (Paid)

1. Get Anthropic API key from: https://console.anthropic.com/
2. Edit `.env`:
   ```env
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   LLM_PROVIDER=anthropic
   ```
3. Restart the app

### Use Different Gemini Model

In `.env`, you can change:
```env
GEMINI_MODEL=gemini-pro          # Default (recommended)
# GEMINI_MODEL=gemini-pro-vision  # For image support (future)
```

---

## 📁 **Project Structure**

```
AI PROMPT OPTIMIZER/
├── home.py                 # Main landing page
├── .env                    # YOUR API KEYS (keep secret!)
├── .env.example            # Template for .env
├── requirements.txt        # Python dependencies
│
├── pages/                  # Streamlit pages
│   ├── 1_🎯_Prompt_Lab.py
│   ├── 2_📚_Templates.py
│   ├── 3_🔄_Workflows.py
│   └── 4_📊_History.py
│
├── core/                   # Core engine
│   ├── prompt_engine.py    # AI optimization logic
│   ├── config.py           # Configuration
│   └── database.py         # Database models
│
├── utils/                  # Utilities
│   └── ui_components.py    # UI components
│
├── .streamlit/             # Streamlit config
│   ├── config.toml
│   └── style.css           # Custom styling
│
└── data/                   # Database storage
    └── prompts.db          # SQLite database
```

---

## 🎓 **What's Included?**

### 3 Domains:
1. **🎓 Academic & Research**
   - Literature reviews, paper writing, teaching materials

2. **🤖 Machine Learning & Data Science**
   - Model development, data analysis, MLOps

3. **🐍 Python Development**
   - Code optimization, debugging, testing

### Features:
- ✅ Real-time prompt optimization
- ✅ 4 specialized versions per prompt
- ✅ Clarity & safety scoring
- ✅ Risk detection
- ✅ Template library
- ✅ Session history
- ✅ Beautiful UI with neon theme

---

## 🔐 **Security Notes**

### DO:
- ✅ Keep your `.env` file private
- ✅ Add `.env` to `.gitignore` (already done!)
- ✅ Use environment variables for API keys
- ✅ Regenerate keys if accidentally exposed

### DON'T:
- ❌ Commit `.env` to GitHub
- ❌ Share API keys in screenshots
- ❌ Hardcode keys in Python files
- ❌ Share your `.env` file with anyone

---

## 📊 **API Usage Limits**

### Google Gemini (FREE Tier):
- 60 requests per minute
- 1,500 requests per day
- No credit card required!

**Perfect for:**
- Personal use ✅
- Learning & experimentation ✅
- Small projects ✅
- Prototypes ✅

**If you need more:**
- Consider OpenAI GPT-4 (paid, higher limits)
- Or Anthropic Claude (paid, excellent quality)

---

## 🚀 **Next Steps**

1. ✅ **Explore the app** - Try all 4 pages
2. 📚 **Check Templates** - Pre-built prompt templates
3. 🔄 **Try Workflows** - Multi-step optimization flows
4. 📊 **View History** - See your past optimizations
5. 🎨 **Customize** - Edit configs to fit your needs

---

## 💡 **Tips for Best Results**

### For Prompts:
1. Be specific about your goal
2. Include relevant context
3. Mention your knowledge level
4. Specify desired output format
5. Include any constraints

### For the App:
1. Start with templates if unsure
2. Use the appropriate domain
3. Check the risk warnings
4. Try all 4 optimized versions
5. Save good prompts to history

---

## 🆘 **Need Help?**

1. **Check this guide first** - Most issues are covered here
2. **Read error messages carefully** - They usually tell you what's wrong
3. **Check `.env` file** - 90% of issues are API key related
4. **Restart the app** - Fixes many caching issues
5. **Create GitHub Issue** - If nothing else works

---

## 🎉 **You're Ready!**

Your AI Prompt Optimizer is configured and ready to use with **FREE Google Gemini API**!

**Enjoy optimizing your prompts!** 🚀

---

**Built with Claude Code** 🤖
