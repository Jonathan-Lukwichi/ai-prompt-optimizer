"""
LUKTHAN - AI Prompt Agent
Chat UI Components with NEXAVERSE Theme (Cyan + Purple)
Premium dark mode design with neon accents
"""
import streamlit as st
from typing import Optional, List, Dict, Any
from datetime import datetime
import html


def load_lukthan_theme():
    """Load the comprehensive LUKTHAN + NEXAVERSE theme CSS"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --lukthan-cyan: #00E5FF;
        --lukthan-cyan-dim: #06B6D4;
        --lukthan-purple: #9B5CFF;
        --lukthan-purple-dim: #8B5CF6;
        --lukthan-gradient: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
        --lukthan-bg-deep: #050816;
        --lukthan-bg-card: #0B1020;
        --lukthan-bg-elevated: #111827;
        --lukthan-border: rgba(0, 229, 255, 0.2);
        --lukthan-border-hover: rgba(0, 229, 255, 0.5);
        --lukthan-text-primary: #F0F6FC;
        --lukthan-text-secondary: #8B949E;
        --lukthan-text-muted: #6E7681;
        --lukthan-success: #10B981;
        --lukthan-warning: #F59E0B;
        --lukthan-error: #EF4444;
        --lukthan-glow-cyan: 0 0 20px rgba(0, 229, 255, 0.4);
    }

    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

    .main .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 100%; }

    /* User Message */
    .user-msg {
        background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 4px 20px;
        margin: 1rem 0 1rem 20%;
        box-shadow: 0 4px 20px rgba(0, 229, 255, 0.3);
    }

    .user-msg-content { font-size: 0.95rem; line-height: 1.6; }
    .user-msg-time { font-size: 0.7rem; opacity: 0.7; margin-top: 0.5rem; text-align: right; }

    /* Agent Message */
    .agent-msg {
        background: #0B1020;
        border: 1px solid rgba(0, 229, 255, 0.2);
        color: #F0F6FC;
        padding: 1.5rem;
        border-radius: 20px 20px 20px 4px;
        margin: 1rem 20% 1rem 0;
    }

    .agent-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }

    .agent-avatar {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
    }

    .agent-name {
        font-weight: 600;
        font-size: 0.9rem;
        color: #F0F6FC;
    }

    /* Prompt Output */
    .prompt-box {
        background: #050816;
        border: 1px solid rgba(0, 229, 255, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
        position: relative;
    }

    .prompt-label {
        position: absolute;
        top: -10px;
        left: 16px;
        background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
    }

    .prompt-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        line-height: 1.7;
        color: #F0F6FC;
        white-space: pre-wrap;
        word-wrap: break-word;
    }

    /* Insights Panel */
    .insights-box {
        background: #0B1020;
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
    }

    .insights-title {
        font-size: 1rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }

    .insights-label {
        color: #6E7681;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }

    .insights-section { margin-bottom: 1.25rem; }

    /* Tags */
    .tag-cyan {
        display: inline-block;
        background: rgba(0, 229, 255, 0.15);
        color: #00E5FF;
        border: 1px solid rgba(0, 229, 255, 0.3);
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .tag-purple {
        display: inline-block;
        background: rgba(155, 92, 255, 0.15);
        color: #9B5CFF;
        border: 1px solid rgba(155, 92, 255, 0.3);
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }

    /* Score Circle */
    .score-box {
        text-align: center;
        padding: 1.5rem;
        background: #050816;
        border-radius: 12px;
        border: 1px solid rgba(0, 229, 255, 0.2);
    }

    .score-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
    }

    .score-label {
        color: #8B949E;
        font-size: 0.8rem;
    }

    /* Metric Bar */
    .metric-row {
        display: flex;
        align-items: center;
        margin-bottom: 0.75rem;
    }

    .metric-name {
        color: #8B949E;
        font-size: 0.8rem;
        width: 100px;
    }

    .metric-bar {
        flex: 1;
        height: 6px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 3px;
        margin: 0 0.75rem;
        overflow: hidden;
    }

    .metric-fill {
        height: 100%;
        border-radius: 3px;
    }

    .metric-value {
        color: #F0F6FC;
        font-size: 0.8rem;
        font-weight: 600;
        width: 30px;
        text-align: right;
    }

    /* Tips */
    .tips-box {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.05) 0%, rgba(155, 92, 255, 0.05) 100%);
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 12px;
        padding: 1rem;
    }

    .tips-item {
        color: #8B949E;
        font-size: 0.8rem;
        padding: 0.3rem 0;
        padding-left: 1rem;
        position: relative;
    }

    .tips-item::before {
        content: '>';
        position: absolute;
        left: 0;
        color: #00E5FF;
        font-weight: 700;
    }

    /* Welcome Hero */
    .hero-box {
        text-align: center;
        padding: 2.5rem 1.5rem;
        background: linear-gradient(180deg, rgba(0, 229, 255, 0.05) 0%, transparent 100%);
        border-radius: 20px;
        border: 1px solid rgba(0, 229, 255, 0.2);
        margin-bottom: 1.5rem;
    }

    .hero-icon { font-size: 3.5rem; margin-bottom: 1rem; }

    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        color: #8B949E;
        font-size: 1rem;
        line-height: 1.6;
    }

    /* Quick Start Card */
    .qs-card {
        background: #0B1020;
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }

    .qs-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
    .qs-title { color: #F0F6FC; font-weight: 600; font-size: 0.9rem; }
    .qs-desc { color: #6E7681; font-size: 0.75rem; }

    /* Sidebar Brand */
    .brand-box {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(180deg, rgba(0, 229, 255, 0.08) 0%, rgba(155, 92, 255, 0.08) 100%);
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 16px;
        margin-bottom: 1rem;
    }

    .brand-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }

    .brand-name {
        font-size: 1.75rem;
        font-weight: 900;
        letter-spacing: 0.1em;
        background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .brand-tagline {
        color: #8B949E;
        font-size: 0.8rem;
        margin-top: 0.25rem;
    }

    .brand-badge {
        display: inline-block;
        background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
        color: white;
        font-size: 0.6rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        margin-top: 0.5rem;
        letter-spacing: 0.1em;
    }

    /* Footer */
    .footer-box {
        text-align: center;
        padding: 1.5rem;
        border-top: 1px solid rgba(0, 229, 255, 0.2);
        margin-top: 2rem;
    }

    .footer-brand {
        background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 0.9rem;
        letter-spacing: 0.1em;
    }

    .footer-text {
        color: #6E7681;
        font-size: 0.7rem;
        margin-top: 0.25rem;
    }

    /* File Attachment */
    .file-tag {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(0, 229, 255, 0.1);
        border: 1px solid rgba(0, 229, 255, 0.3);
        border-radius: 8px;
        padding: 0.4rem 0.8rem;
        margin-bottom: 0.5rem;
        font-size: 0.8rem;
        color: #F0F6FC;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Streamlit overrides */
    .stButton > button {
        background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(0, 229, 255, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 229, 255, 0.4) !important;
    }

    .stTextArea > div > div > textarea {
        background: #050816 !important;
        border: 1px solid rgba(0, 229, 255, 0.2) !important;
        border-radius: 10px !important;
        color: #F0F6FC !important;
    }

    .stTextArea > div > div > textarea:focus {
        border-color: #00E5FF !important;
        box-shadow: 0 0 0 2px rgba(0, 229, 255, 0.1) !important;
    }

    .stSelectbox > div > div {
        background: #050816 !important;
        border: 1px solid rgba(0, 229, 255, 0.2) !important;
        border-radius: 10px !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050816 0%, #0B1020 100%) !important;
        border-right: 1px solid rgba(0, 229, 255, 0.2) !important;
    }

    .stExpander {
        background: #0B1020 !important;
        border: 1px solid rgba(0, 229, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the LUKTHAN branded sidebar with settings"""
    with st.sidebar:
        # Logo and Brand
        st.markdown("""
        <div class="brand-box">
            <div class="brand-icon">🧠</div>
            <div class="brand-name">LUKTHAN</div>
            <div class="brand-tagline">AI Prompt Agent</div>
            <div class="brand-badge">RESEARCH & CODE</div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Settings
        st.markdown("**⚙️ Agent Settings**")

        domain_options = ["🔮 Auto Detect", "🔬 Research", "💻 Coding", "📊 Data Science", "🌐 General"]
        st.selectbox("Domain", options=domain_options, index=0, key="domain_setting")

        ai_models = ["ChatGPT (GPT-4)", "Claude 3.5", "Gemini Pro", "Llama 3", "Other"]
        st.selectbox("Target AI Model", options=ai_models, index=0, key="target_ai_setting")

        languages = ["English", "French", "Spanish", "German", "Portuguese", "Chinese"]
        st.selectbox("Output Language", options=languages, index=0, key="language_setting")

        levels = ["Student", "Professional", "Expert", "Academic"]
        st.selectbox("Expertise Level", options=levels, index=1, key="level_setting")

        st.divider()

        with st.expander("💡 Pro Tips"):
            st.markdown("""
            - Be specific about your end goal
            - Include context and constraints
            - Mention desired output format
            - Upload files for better context
            """)

        st.divider()

        if st.button("🗑️ Clear Conversation", use_container_width=True):
            return "clear_chat"

        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; padding: 1rem;">
            <div class="footer-brand">LUKTHAN</div>
            <div class="footer-text">v2.0 Pro</div>
        </div>
        """, unsafe_allow_html=True)

    return None


def render_welcome_hero():
    """Render the premium welcome hero section"""
    st.markdown("""
    <div class="hero-box">
        <div class="hero-icon">🧠</div>
        <div class="hero-title">Welcome to LUKTHAN</div>
        <div class="hero-subtitle">
            Transform rough ideas into powerful, structured prompts for ChatGPT, Claude, Gemini, and more.<br>
            <strong>Specialized for Research & Coding workflows.</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**⚡ Quick Start Examples**")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="qs-card">
            <div class="qs-icon">🔬</div>
            <div class="qs-title">Literature Review</div>
            <div class="qs-desc">Generate prompts for systematic research</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try Research", key="qs_research", use_container_width=True):
            return "Help me write a systematic literature review on machine learning applications in healthcare diagnostics"

        st.markdown("""
        <div class="qs-card">
            <div class="qs-icon">📊</div>
            <div class="qs-title">Data Analysis</div>
            <div class="qs-desc">Analyze datasets and build predictions</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try Analysis", key="qs_data", use_container_width=True):
            return "Create a prompt to analyze customer churn data and build a prediction model"

    with col2:
        st.markdown("""
        <div class="qs-card">
            <div class="qs-icon">💻</div>
            <div class="qs-title">Code Generation</div>
            <div class="qs-desc">Build APIs, scripts, and applications</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try Coding", key="qs_code", use_container_width=True):
            return "Create a REST API with FastAPI that handles user authentication with JWT tokens"

        st.markdown("""
        <div class="qs-card">
            <div class="qs-icon">🏗️</div>
            <div class="qs-title">Architecture Design</div>
            <div class="qs-desc">Design system architectures</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try Architecture", key="qs_arch", use_container_width=True):
            return "Design a microservices architecture for a scalable e-commerce platform"

    return None


def render_user_message(content: str, timestamp: Optional[str] = None, file_info: Optional[Dict] = None):
    """Render a user message bubble"""
    time_str = timestamp or datetime.now().strftime("%H:%M")

    # Escape HTML in content to prevent XSS but keep it safe
    safe_content = html.escape(content)

    file_html = ""
    if file_info:
        icons = {"documents": "📄", "code": "💻", "images": "🖼️", "audio": "🎵"}
        icon = icons.get(file_info.get('type', ''), '📎')
        file_html = f'<div class="file-tag">{icon} {html.escape(file_info.get("name", "File"))}</div>'

    st.markdown(f"""
    <div class="user-msg">
        {file_html}
        <div class="user-msg-content">{safe_content}</div>
        <div class="user-msg-time">{time_str}</div>
    </div>
    """, unsafe_allow_html=True)


def render_agent_response(
    prompt: str,
    domain: str = "general",
    task_type: str = "general",
    quality_score: int = 85,
    metrics: Optional[Dict[str, int]] = None,
    suggestions: Optional[List[str]] = None
):
    """Render the agent's response with optimized prompt"""

    # Escape HTML in prompt
    safe_prompt = html.escape(prompt)

    st.markdown(f"""
    <div class="agent-msg">
        <div class="agent-header">
            <div class="agent-avatar">🧠</div>
            <span class="agent-name">LUKTHAN Agent</span>
        </div>
        <div class="prompt-box">
            <span class="prompt-label">✨ OPTIMIZED PROMPT</span>
            <div class="prompt-text">{safe_prompt}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("📋 Copy", key=f"copy_{hash(prompt)}", use_container_width=True):
            st.toast("Prompt ready to copy!", icon="✅")
    with col2:
        if st.button("🔄 Regenerate", key=f"regen_{hash(prompt)}", use_container_width=True):
            return "regenerate"

    return None


def render_insights_panel(
    domain: str = "general",
    task_type: str = "general",
    quality_score: int = 85,
    metrics: Optional[Dict[str, int]] = None,
    suggestions: Optional[List[str]] = None,
    show_content: bool = True
):
    """Render the insights panel with quality metrics"""

    if not show_content:
        st.markdown("""
        <div class="insights-box" style="text-align: center; padding: 3rem 1.5rem;">
            <div style="font-size: 3rem; opacity: 0.3; margin-bottom: 1rem;">📊</div>
            <div style="color: #6E7681;">Generate a prompt to see insights</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Default metrics
    if metrics is None:
        metrics = {
            "Clarity": min(100, quality_score + 5),
            "Specificity": max(0, quality_score - 3),
            "Structure": min(100, quality_score + 2),
            "Completeness": max(0, quality_score - 5)
        }

    # Score color
    if quality_score >= 80:
        score_color = "#10B981"
    elif quality_score >= 60:
        score_color = "#F59E0B"
    else:
        score_color = "#EF4444"

    # Domain icons
    domain_icons = {"research": "🔬", "coding": "💻", "data_science": "📊", "general": "🌐"}
    task_icons = {"literature_review": "📚", "code_generation": "⚡", "bug_fix": "🐛", "api_design": "🔌", "data_analysis": "📈", "general_query": "💬"}

    d_icon = domain_icons.get(domain.lower(), "🌐")
    t_icon = task_icons.get(task_type.lower(), "💬")

    d_name = domain.replace('_', ' ').title()
    t_name = task_type.replace('_', ' ').title()

    # Build metrics HTML
    metrics_html = ""
    for name, value in metrics.items():
        bar_color = "#10B981" if value >= 80 else "#F59E0B" if value >= 60 else "#EF4444"
        metrics_html += f"""
        <div class="metric-row">
            <span class="metric-name">{name}</span>
            <div class="metric-bar">
                <div class="metric-fill" style="width: {value}%; background: {bar_color};"></div>
            </div>
            <span class="metric-value">{value}</span>
        </div>
        """

    # Build suggestions HTML
    suggestions_html = ""
    if suggestions:
        suggestions_html = '<div class="tips-box">'
        for s in suggestions[:3]:
            suggestions_html += f'<div class="tips-item">{html.escape(s)}</div>'
        suggestions_html += '</div>'

    st.markdown(f"""
    <div class="insights-box">
        <div class="insights-title">📊 Prompt Insights</div>

        <div class="insights-section">
            <div class="insights-label">Detection</div>
            <span class="tag-cyan">{d_icon} {d_name}</span>
            <span class="tag-purple">{t_icon} {t_name}</span>
        </div>

        <div class="insights-section">
            <div class="insights-label">Quality Score</div>
            <div class="score-box">
                <div class="score-value" style="color: {score_color};">{quality_score}</div>
                <div class="score-label">out of 100</div>
            </div>
        </div>

        <div class="insights-section">
            <div class="insights-label">Breakdown</div>
            {metrics_html}
        </div>

        {f'<div class="insights-section"><div class="insights-label">Suggestions</div>{suggestions_html}</div>' if suggestions else ''}

        <div class="insights-section">
            <div class="insights-label">How to Use</div>
            <div class="tips-box">
                <div class="tips-item">Copy the optimized prompt</div>
                <div class="tips-item">Paste into ChatGPT, Claude, or Gemini</div>
                <div class="tips-item">Get more accurate AI responses</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_typing_indicator():
    """Show LUKTHAN thinking animation"""
    st.markdown("""
    <div class="agent-msg" style="display: inline-block; padding: 1rem;">
        <span style="color: #8B949E;">🧠 LUKTHAN is thinking...</span>
    </div>
    """, unsafe_allow_html=True)


def render_file_indicator(filename: str, file_type: str):
    """Show file attachment indicator"""
    icons = {"documents": "📄", "code": "💻", "images": "🖼️", "audio": "🎵", "unknown": "📎"}
    icon = icons.get(file_type, '📎')

    st.markdown(f"""
    <div class="file-tag">
        {icon} {html.escape(filename)} <span style="color: #00E5FF; font-weight: 600;">{file_type.upper()}</span>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    """Render the LUKTHAN footer"""
    st.markdown("""
    <div class="footer-box">
        <div class="footer-brand">LUKTHAN</div>
        <div class="footer-text">Structured prompts for serious research and code.</div>
    </div>
    """, unsafe_allow_html=True)
