# 🎓 AI Prompt Optimizer for Academia

> Transform your prompts into powerful, effective requests that get better results from ChatGPT, Claude, and other AI assistants.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.30+-red.svg)

A professional, production-ready Streamlit application designed specifically for academic researchers, students, and educators to optimize their AI prompts.

## ✨ Features

### 🎯 Prompt Lab
- **4 Optimized Versions**: Get Basic, Critical-Thinking, Tutor, and Safe versions of every prompt
- **Quality Scoring**: Instant feedback on clarity and safety with actionable suggestions
- **Risk Detection**: Automatically identify potential hallucination risks and academic integrity concerns
- **Real-time Analysis**: Get insights on what's missing in your prompts

### 📚 Templates Library
- Pre-built templates for common academic tasks
- Filter by role, task type, and field
- Create and save your own templates
- Community-contributed templates

### 🔬 Guided Workflows
- Step-by-step processes for complex tasks
- Literature review workflow
- Paper writing workflow
- Reviewer response workflow
- Track progress and save your work

### 📊 History & Analytics
- View all past optimization sessions
- Track your improvement over time
- Filter by task type, role, and date
- Export your optimized prompts

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenAI API key (or Anthropic API key for Claude)

### Installation

1. **Clone or download this repository**

```bash
cd "AI PROMPT OPTIMIZER"
```

2. **Create a virtual environment** (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up your API key**

Create a `.env` file in the project root:

```bash
# Copy the example file
copy .env.example .env   # Windows
cp .env.example .env     # macOS/Linux
```

Edit `.env` and add your API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
# or
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

5. **Run the app**

**Option A: One-Click Run in VS Code (Easiest!)**

If you're using VS Code:
1. Press **F5** (or click the Run button in the sidebar)
2. That's it! App opens automatically

See [HOW_TO_RUN.md](HOW_TO_RUN.md) for visual guide.

**Option B: Command Line**

```bash
streamlit run app.py
```

**Option C: Use Launch Scripts**

```bash
# Windows
run_app.bat

# macOS/Linux
./run_app.sh
```

The app will open in your browser at `http://localhost:8501`

## 🎨 Design

Built with a stunning **neon/fluorescent design** inspired by bolt.ai and lovable.dev:

- 🌈 Vibrant gradient colors
- ✨ Glassmorphism effects
- 🎯 Smooth animations
- 💎 Professional, polished UI
- 🌙 Dark theme optimized for long sessions

## 📁 Project Structure

```
ai-prompt-optimizer/
├── app.py                      # Main entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
│
├── .streamlit/
│   ├── config.toml            # Streamlit configuration
│   └── style.css              # Custom CSS theme
│
├── core/
│   ├── config.py              # App configuration
│   ├── database.py            # Database models & operations
│   └── prompt_engine.py       # Core optimization engine
│
├── utils/
│   └── ui_components.py       # Reusable UI components
│
├── pages/
│   ├── 1_🎯_Prompt_Lab.py    # Main optimization feature
│   ├── 2_📚_Templates.py     # Template library
│   ├── 3_🔬_Workflows.py     # Guided workflows
│   └── 4_📊_History.py       # Session history
│
└── data/
    └── prompts.db             # SQLite database (auto-created)
```

## 🎯 Usage Guide

### Basic Workflow

1. **Select Your Profile**
   - Choose your academic role (Undergrad, PhD, Professor, etc.)
   - Specify your field of study
   - Select the task type

2. **Enter Your Prompt**
   - Type or paste your question/request
   - Don't worry if it's not perfect!

3. **Get Optimized Versions**
   - **Basic**: Clear, structured version for general use
   - **Critical-Thinking**: Forces deeper analysis and questioning
   - **Tutor**: Socratic method for learning
   - **Safe**: Minimizes hallucinations, emphasizes accuracy

4. **Copy & Use**
   - Choose the version that fits your needs
   - Copy it to your AI tool (ChatGPT, Claude, etc.)
   - Get better results!

### When to Use Each Version

| Version | Best For | Example Use Case |
|---------|----------|------------------|
| **📝 Basic** | General questions, exploration | "Explain transformer models in NLP" |
| **🧠 Critical** | Research, methodology | "Evaluate this research design" |
| **👨‍🏫 Tutor** | Learning, understanding | "Help me understand p-values" |
| **🛡️ Safe** | Citations, factual accuracy | "Find papers on topic X" |

## 🔧 Configuration

### API Keys

The app supports multiple LLM providers:

- **OpenAI** (GPT-4, GPT-4o): Recommended for best results
- **Anthropic** (Claude): Alternative option

Set your preferred API key in `.env`.

### Database

By default, uses SQLite (no setup required). The database is created automatically in `data/prompts.db`.

For production use with multiple users, you can configure PostgreSQL or MySQL by modifying `DATABASE_URL` in `core/config.py`.

## 🎓 For Different Academic Roles

### Undergraduates
- Use **Tutor Mode** to learn concepts
- Start with templates for common assignments
- Track your prompt quality improvement

### PhD Students
- Use **Critical-Thinking Mode** for research design
- Literature review workflow
- Methodology development templates

### Professors
- Create custom templates for your field
- Use for teaching material development
- Reviewer response workflow for publications

## 🛡️ Academic Integrity

This tool is designed to **support** academic work, not replace it:

- ✅ Helps you ask better questions
- ✅ Teaches you to think critically
- ✅ Guides you through learning
- ✅ Prevents common AI pitfalls

- ❌ Does NOT write papers for you
- ❌ Does NOT do your homework
- ❌ Does NOT replace your own thinking

**Tutor Mode** explicitly uses the Socratic method to help you learn, not just get answers.

**Safe Mode** instructs AI to acknowledge uncertainty and avoid making up citations.

## 🤝 Contributing

Contributions are welcome! Areas for contribution:

- New templates for specific academic fields
- Additional workflows (grant writing, teaching, etc.)
- UI/UX improvements
- Bug fixes and optimizations
- Documentation improvements

## 📝 License

MIT License - feel free to use this for your research or institution.

## 🐛 Troubleshooting

### "No API key configured"
- Make sure you've created a `.env` file
- Check that your API key is correct
- Restart the Streamlit app after adding the key

### "Database error"
- The `data/` folder should be created automatically
- Check file permissions
- Try deleting `data/prompts.db` and restarting

### Slow optimization
- First run downloads the model, subsequent runs are faster
- Consider using `gpt-4o-mini` for faster responses (edit `core/config.py`)

### CSS not loading
- Clear browser cache
- Check that `.streamlit/style.css` exists
- Try restarting the app

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-prompt-optimizer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-prompt-optimizer/discussions)
- **Email**: support@example.com

## 🙏 Acknowledgments

- Design inspired by [bolt.ai](https://bolt.ai) and [lovable.dev](https://lovable.dev)
- Built with [Streamlit](https://streamlit.io)
- Powered by OpenAI GPT-4 and Anthropic Claude

## 🗺️ Roadmap

- [ ] User authentication and teams
- [ ] Export to PDF/Word
- [ ] Prompt comparison tool
- [ ] Integration with reference managers (Zotero, Mendeley)
- [ ] Mobile app
- [ ] Chrome extension
- [ ] More specialized workflows
- [ ] Multi-language support

---

**Made with ❤️ for the academic community**

⭐ Star this repo if you find it useful!
