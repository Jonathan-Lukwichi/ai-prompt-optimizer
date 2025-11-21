# 🚀 DEPLOY NOW - Quick Start Guide

Follow these 4 simple steps to deploy your AI Prompt Optimizer in under 10 minutes!

---

## ✅ Step 1: Get Your Gemini API Key (2 minutes)

1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key (starts with `AIza...`)
4. Keep it ready for Step 4

**Cost**: FREE (1,500 requests/day)

---

## ✅ Step 2: Push to GitHub (1 minute)

```bash
# Make sure all changes are committed
git add .
git commit -m "Ready for deployment"
git push origin main
```

**Already done?** Skip to Step 3!

---

## ✅ Step 3: Deploy to Streamlit Cloud (3 minutes)

1. **Go to**: https://streamlit.io/cloud
2. **Sign in** with GitHub
3. **Click "New app"**
4. **Select**:
   - Repository: `Jonathan-Lukwichi/ai-prompt-optimizer`
   - Branch: `main`
   - Main file: `home.py`
5. **Click "Deploy"**

Wait 2-3 minutes for deployment to complete...

---

## ✅ Step 4: Add Your API Key (2 minutes)

1. In Streamlit Cloud, click your app
2. Click "⋮" menu → "Settings"
3. Click "Secrets" tab
4. Paste this (replace with YOUR key):

```toml
GEMINI_API_KEY = "your-actual-gemini-api-key-here"
LLM_PROVIDER = "gemini"
GEMINI_MODEL = "gemini-2.5-flash"
ENVIRONMENT = "production"
```

5. Click "Save"
6. Wait 30 seconds for restart

---

## 🎉 YOU'RE LIVE!

Your app is now accessible at:

**https://your-app-name.streamlit.app**

### Test These Features:

1. ✅ Home → Quick Optimize
2. ✅ Prompt Lab → Optimize a prompt
3. ✅ Batch Optimize → Process 3 prompts
4. ✅ Templates → Try guided builder
5. ✅ History → View analytics

---

## 🐛 Something Not Working?

### **App says "Please configure GEMINI_API_KEY"**
→ Go back to Step 4 and add your API key in Secrets

### **"ModuleNotFoundError"**
→ Check `requirements.txt` is committed and pushed

### **App is slow to load**
→ Normal! First load takes 30-60s, then it's fast

---

## 📱 Share Your App

Your app URL:
```
https://your-app-name.streamlit.app
```

Share it:
- On LinkedIn
- With colleagues
- In your portfolio
- On Twitter/X

---

## 📚 Need More Help?

Read the full guide: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

**Total Time**: ~10 minutes
**Cost**: FREE
**Result**: Production app accessible worldwide! 🌍

🎊 **Congratulations on deploying your app!** 🎊
