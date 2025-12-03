"""
LUKTHAN - AI Prompt Agent
Chat UI Components with NEXAVERSE Theme (Cyan + Purple)
Premium dark mode design with neon accents
"""
import streamlit as st
from typing import Optional, List, Dict, Any
from datetime import datetime


def load_lukthan_theme():
    """Load the comprehensive LUKTHAN + NEXAVERSE theme CSS"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ============================================
       LUKTHAN BRAND COLORS
       ============================================ */
    :root {
        --lukthan-cyan: #00E5FF;
        --lukthan-cyan-dim: #06B6D4;
        --lukthan-purple: #9B5CFF;
        --lukthan-purple-dim: #8B5CF6;
        --lukthan-gradient: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
        --lukthan-gradient-reverse: linear-gradient(135deg, #9B5CFF 0%, #00E5FF 100%);
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
        --lukthan-glow-purple: 0 0 20px rgba(155, 92, 255, 0.4);
    }

    /* ============================================
       GLOBAL RESET
       ============================================ */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }

    /* ============================================
       LUKTHAN LOGO & BRAND
       ============================================ */
    .lukthan-logo-container {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(180deg, rgba(0, 229, 255, 0.08) 0%, rgba(155, 92, 255, 0.08) 100%);
        border: 1px solid var(--lukthan-border);
        border-radius: 20px;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }

    .lukthan-logo-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(0, 229, 255, 0.1), transparent 30%);
        animation: rotate 8s linear infinite;
    }

    @keyframes rotate {
        100% { transform: rotate(360deg); }
    }

    .lukthan-brand-name {
        font-size: 2rem;
        font-weight: 900;
        letter-spacing: 0.1em;
        background: var(--lukthan-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        position: relative;
        text-shadow: 0 0 40px rgba(0, 229, 255, 0.5);
    }

    .lukthan-tagline {
        color: var(--lukthan-text-secondary);
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: 0.5rem;
        letter-spacing: 0.05em;
    }

    .lukthan-badge {
        display: inline-block;
        background: var(--lukthan-gradient);
        color: white;
        font-size: 0.65rem;
        font-weight: 700;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        margin-top: 0.75rem;
        letter-spacing: 0.1em;
    }

    /* ============================================
       HERO SECTION
       ============================================ */
    .lukthan-hero {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(180deg, rgba(0, 229, 255, 0.05) 0%, transparent 100%);
        border-radius: 24px;
        border: 1px solid var(--lukthan-border);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }

    .lukthan-hero::after {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        height: 1px;
        background: var(--lukthan-gradient);
        box-shadow: var(--lukthan-glow-cyan);
    }

    .lukthan-hero-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    .lukthan-hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: var(--lukthan-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.75rem;
        letter-spacing: -0.02em;
    }

    .lukthan-hero-subtitle {
        color: var(--lukthan-text-secondary);
        font-size: 1.1rem;
        line-height: 1.7;
        max-width: 600px;
        margin: 0 auto 2rem;
    }

    /* ============================================
       QUICK START CARDS
       ============================================ */
    .quick-start-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-top: 1.5rem;
    }

    .quick-start-card {
        background: rgba(11, 16, 32, 0.8);
        border: 1px solid var(--lukthan-border);
        border-radius: 16px;
        padding: 1.25rem;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: left;
    }

    .quick-start-card:hover {
        border-color: var(--lukthan-border-hover);
        transform: translateY(-4px);
        box-shadow: var(--lukthan-glow-cyan);
        background: rgba(0, 229, 255, 0.05);
    }

    .quick-start-icon {
        font-size: 1.75rem;
        margin-bottom: 0.75rem;
    }

    .quick-start-title {
        color: var(--lukthan-text-primary);
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.25rem;
    }

    .quick-start-desc {
        color: var(--lukthan-text-muted);
        font-size: 0.8rem;
        line-height: 1.4;
    }

    /* ============================================
       CHAT MESSAGES
       ============================================ */
    .chat-messages-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem 0;
        scroll-behavior: smooth;
    }

    .user-message-bubble {
        background: var(--lukthan-gradient);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 4px 20px;
        margin: 1rem 0 1rem 15%;
        box-shadow: var(--lukthan-glow-cyan);
        animation: slideInRight 0.3s ease-out;
        position: relative;
    }

    .user-message-bubble::after {
        content: '';
        position: absolute;
        bottom: 0;
        right: -8px;
        width: 0;
        height: 0;
        border: 8px solid transparent;
        border-left-color: #9B5CFF;
        border-bottom-color: #9B5CFF;
    }

    .agent-message-bubble {
        background: var(--lukthan-bg-card);
        border: 1px solid var(--lukthan-border);
        color: var(--lukthan-text-primary);
        padding: 1.5rem;
        border-radius: 20px 20px 20px 4px;
        margin: 1rem 15% 1rem 0;
        animation: slideInLeft 0.3s ease-out;
        position: relative;
    }

    .agent-message-bubble::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--lukthan-gradient);
        border-radius: 20px 20px 0 0;
    }

    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    .message-timestamp {
        font-size: 0.7rem;
        opacity: 0.6;
        margin-top: 0.5rem;
        text-align: right;
    }

    .message-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }

    .message-avatar {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        background: var(--lukthan-gradient);
    }

    .message-label {
        font-weight: 600;
        font-size: 0.9rem;
        color: var(--lukthan-text-primary);
    }

    /* ============================================
       OPTIMIZED PROMPT OUTPUT
       ============================================ */
    .prompt-output-container {
        position: relative;
        margin-top: 1rem;
    }

    .prompt-output-label {
        position: absolute;
        top: -12px;
        left: 20px;
        background: var(--lukthan-gradient);
        color: white;
        padding: 4px 16px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        box-shadow: var(--lukthan-glow-cyan);
        z-index: 1;
    }

    .prompt-output-box {
        background: rgba(5, 8, 22, 0.9);
        border: 1px solid var(--lukthan-border);
        border-radius: 16px;
        padding: 2rem 1.5rem 1.5rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        line-height: 1.7;
        color: var(--lukthan-text-primary);
        white-space: pre-wrap;
        word-wrap: break-word;
        max-height: 400px;
        overflow-y: auto;
    }

    .prompt-actions {
        display: flex;
        gap: 0.75rem;
        margin-top: 1rem;
    }

    /* ============================================
       INSIGHTS PANEL
       ============================================ */
    .insights-panel {
        background: var(--lukthan-bg-card);
        border: 1px solid var(--lukthan-border);
        border-radius: 20px;
        padding: 1.5rem;
        height: fit-content;
        position: sticky;
        top: 1rem;
    }

    .insights-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--lukthan-border);
    }

    .insights-title {
        font-size: 1rem;
        font-weight: 700;
        background: var(--lukthan-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .insights-section {
        margin-bottom: 1.5rem;
    }

    .insights-label {
        color: var(--lukthan-text-muted);
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }

    /* ============================================
       DOMAIN & TASK TAGS
       ============================================ */
    .tag-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    .tag-cyan {
        background: rgba(0, 229, 255, 0.15);
        color: var(--lukthan-cyan);
        border: 1px solid rgba(0, 229, 255, 0.3);
    }

    .tag-purple {
        background: rgba(155, 92, 255, 0.15);
        color: var(--lukthan-purple);
        border: 1px solid rgba(155, 92, 255, 0.3);
    }

    .tag-green {
        background: rgba(16, 185, 129, 0.15);
        color: var(--lukthan-success);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    /* ============================================
       QUALITY SCORE
       ============================================ */
    .quality-score-container {
        text-align: center;
        padding: 1.5rem;
        background: rgba(5, 8, 22, 0.6);
        border-radius: 16px;
        border: 1px solid var(--lukthan-border);
    }

    .quality-score-circle {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        position: relative;
        font-size: 2rem;
        font-weight: 800;
    }

    .quality-score-circle::before {
        content: '';
        position: absolute;
        inset: -4px;
        border-radius: 50%;
        padding: 4px;
        background: var(--score-gradient, var(--lukthan-gradient));
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
    }

    .quality-score-label {
        color: var(--lukthan-text-secondary);
        font-size: 0.8rem;
        font-weight: 500;
    }

    /* ============================================
       METRIC BARS
       ============================================ */
    .metric-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.75rem;
    }

    .metric-name {
        color: var(--lukthan-text-secondary);
        font-size: 0.8rem;
        font-weight: 500;
    }

    .metric-bar-container {
        flex: 1;
        height: 6px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 3px;
        margin: 0 1rem;
        overflow: hidden;
    }

    .metric-bar-fill {
        height: 100%;
        border-radius: 3px;
        transition: width 0.5s ease-out;
    }

    .metric-value {
        color: var(--lukthan-text-primary);
        font-size: 0.8rem;
        font-weight: 600;
        min-width: 30px;
        text-align: right;
    }

    /* ============================================
       INPUT AREA
       ============================================ */
    .input-container {
        background: var(--lukthan-bg-card);
        border: 1px solid var(--lukthan-border);
        border-radius: 20px;
        padding: 1.5rem;
        margin-top: 1rem;
    }

    .input-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
    }

    .input-title {
        color: var(--lukthan-text-primary);
        font-size: 0.9rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .input-options {
        display: flex;
        gap: 0.5rem;
    }

    .input-option-btn {
        background: rgba(0, 229, 255, 0.1);
        border: 1px solid var(--lukthan-border);
        border-radius: 10px;
        padding: 0.5rem 0.75rem;
        color: var(--lukthan-text-secondary);
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .input-option-btn:hover {
        background: rgba(0, 229, 255, 0.2);
        border-color: var(--lukthan-border-hover);
        color: var(--lukthan-cyan);
    }

    /* ============================================
       SIDEBAR SETTINGS
       ============================================ */
    .settings-section {
        background: rgba(11, 16, 32, 0.6);
        border: 1px solid var(--lukthan-border);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }

    .settings-title {
        color: var(--lukthan-text-primary);
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ============================================
       TIPS CARD
       ============================================ */
    .tips-card {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.08) 0%, rgba(155, 92, 255, 0.08) 100%);
        border: 1px solid var(--lukthan-border);
        border-radius: 16px;
        padding: 1.25rem;
    }

    .tips-title {
        color: var(--lukthan-cyan);
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .tips-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .tips-list li {
        color: var(--lukthan-text-secondary);
        font-size: 0.8rem;
        padding: 0.4rem 0;
        padding-left: 1.25rem;
        position: relative;
        line-height: 1.5;
    }

    .tips-list li::before {
        content: '>';
        position: absolute;
        left: 0;
        color: var(--lukthan-cyan);
        font-weight: 700;
    }

    /* ============================================
       FILE ATTACHMENT INDICATOR
       ============================================ */
    .file-attachment {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(0, 229, 255, 0.1);
        border: 1px solid var(--lukthan-border);
        border-radius: 10px;
        padding: 0.5rem 1rem;
        margin-bottom: 0.5rem;
    }

    .file-attachment-icon {
        font-size: 1rem;
    }

    .file-attachment-name {
        color: var(--lukthan-text-primary);
        font-size: 0.85rem;
        font-weight: 500;
    }

    .file-attachment-type {
        background: var(--lukthan-gradient);
        color: white;
        font-size: 0.65rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 10px;
    }

    /* ============================================
       TYPING INDICATOR
       ============================================ */
    .typing-indicator {
        display: flex;
        gap: 6px;
        padding: 1rem;
    }

    .typing-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: var(--lukthan-gradient);
        animation: typingBounce 1.4s ease-in-out infinite;
    }

    .typing-dot:nth-child(1) { animation-delay: 0s; }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }

    @keyframes typingBounce {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-10px); }
    }

    /* ============================================
       FOOTER
       ============================================ */
    .lukthan-footer {
        text-align: center;
        padding: 1.5rem;
        border-top: 1px solid var(--lukthan-border);
        margin-top: 2rem;
    }

    .footer-brand {
        background: var(--lukthan-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-size: 0.9rem;
        letter-spacing: 0.1em;
    }

    .footer-text {
        color: var(--lukthan-text-muted);
        font-size: 0.75rem;
        margin-top: 0.25rem;
    }

    /* ============================================
       STREAMLIT OVERRIDES
       ============================================ */
    .stButton > button[data-testid="baseButton-primary"] {
        background: var(--lukthan-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        box-shadow: var(--lukthan-glow-cyan) !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button[data-testid="baseButton-primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 30px rgba(0, 229, 255, 0.6) !important;
    }

    .stButton > button[data-testid="baseButton-secondary"] {
        background: transparent !important;
        color: var(--lukthan-cyan) !important;
        border: 1px solid var(--lukthan-border) !important;
        border-radius: 12px !important;
    }

    .stButton > button[data-testid="baseButton-secondary"]:hover {
        background: rgba(0, 229, 255, 0.1) !important;
        border-color: var(--lukthan-border-hover) !important;
    }

    .stTextArea > div > div > textarea {
        background: var(--lukthan-bg-deep) !important;
        border: 1px solid var(--lukthan-border) !important;
        border-radius: 12px !important;
        color: var(--lukthan-text-primary) !important;
        font-size: 0.95rem !important;
    }

    .stTextArea > div > div > textarea:focus {
        border-color: var(--lukthan-cyan) !important;
        box-shadow: 0 0 0 3px rgba(0, 229, 255, 0.15) !important;
    }

    .stSelectbox > div > div {
        background: var(--lukthan-bg-deep) !important;
        border: 1px solid var(--lukthan-border) !important;
        border-radius: 12px !important;
    }

    .stExpander {
        background: var(--lukthan-bg-card) !important;
        border: 1px solid var(--lukthan-border) !important;
        border-radius: 16px !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050816 0%, #0B1020 50%, #050816 100%) !important;
        border-right: 1px solid var(--lukthan-border) !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the LUKTHAN branded sidebar with settings"""
    with st.sidebar:
        # Logo and Brand
        st.markdown("""
        <div class="lukthan-logo-container">
            <!-- Placeholder for LUKTHAN logo: assets/lukthan_logo.png -->
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🧠</div>
            <h1 class="lukthan-brand-name">LUKTHAN</h1>
            <p class="lukthan-tagline">AI Prompt Agent</p>
            <span class="lukthan-badge">RESEARCH & CODE</span>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Settings Section
        st.markdown("""
        <div class="settings-title">
            <span>⚙️</span> Agent Settings
        </div>
        """, unsafe_allow_html=True)

        # Domain Override
        domain_options = ["🔮 Auto Detect", "🔬 Research", "💻 Coding", "📊 Data Science", "🌐 General"]
        domain = st.selectbox(
            "Domain",
            options=domain_options,
            index=0,
            key="domain_setting",
            help="Let LUKTHAN auto-detect or manually override"
        )

        # Target AI Model
        ai_models = ["ChatGPT (GPT-4)", "Claude 3.5", "Gemini Pro", "Llama 3", "Other"]
        target_ai = st.selectbox(
            "Target AI Model",
            options=ai_models,
            index=0,
            key="target_ai_setting",
            help="Optimize prompt for specific AI model"
        )

        # Output Language
        languages = ["English", "French", "Spanish", "German", "Portuguese", "Chinese", "Japanese"]
        language = st.selectbox(
            "Output Language",
            options=languages,
            index=0,
            key="language_setting"
        )

        # Expertise Level
        levels = ["Student", "Professional", "Expert", "Academic"]
        level = st.selectbox(
            "Expertise Level",
            options=levels,
            index=1,
            key="level_setting",
            help="Adjusts complexity and terminology"
        )

        st.divider()

        # Tips Section
        with st.expander("💡 Pro Tips", expanded=False):
            st.markdown("""
            <div class="tips-card">
                <ul class="tips-list">
                    <li>Be specific about your end goal</li>
                    <li>Include context and constraints</li>
                    <li>Mention desired output format</li>
                    <li>Upload files for better context</li>
                    <li>Use voice for quick ideas</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Clear Chat Button
        if st.button("🗑️ Clear Conversation", use_container_width=True, type="secondary"):
            return "clear_chat"

        # Footer
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; padding: 1rem;">
            <div class="footer-brand">LUKTHAN</div>
            <div class="footer-text">v2.0 Pro • Premium AI Agent</div>
        </div>
        """, unsafe_allow_html=True)

    return None


def render_welcome_hero():
    """Render the premium welcome hero section"""
    st.markdown("""
    <div class="lukthan-hero">
        <div class="lukthan-hero-icon">🧠</div>
        <h1 class="lukthan-hero-title">Welcome to LUKTHAN</h1>
        <p class="lukthan-hero-subtitle">
            Transform rough ideas into powerful, structured prompts for ChatGPT, Claude, Gemini, and more.<br>
            <strong>Specialized for Research & Coding workflows.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='text-align: center; color: #8B949E; margin-bottom: 1rem;'>⚡ Quick Start Examples</p>", unsafe_allow_html=True)

    # Quick start cards
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="quick-start-card" onclick="this.style.borderColor='var(--lukthan-cyan)'">
            <div class="quick-start-icon">🔬</div>
            <div class="quick-start-title">Literature Review</div>
            <div class="quick-start-desc">Generate a prompt for systematic literature review</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try Research", key="qs_research", use_container_width=True):
            return "Help me write a systematic literature review on machine learning applications in healthcare diagnostics"

        st.markdown("""
        <div class="quick-start-card">
            <div class="quick-start-icon">📊</div>
            <div class="quick-start-title">Data Analysis</div>
            <div class="quick-start-desc">Analyze datasets and build predictions</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try Analysis", key="qs_data", use_container_width=True):
            return "Create a prompt to analyze customer churn data and build a prediction model with feature importance"

    with col2:
        st.markdown("""
        <div class="quick-start-card">
            <div class="quick-start-icon">💻</div>
            <div class="quick-start-title">Code Generation</div>
            <div class="quick-start-desc">Build APIs, scripts, and applications</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try Coding", key="qs_code", use_container_width=True):
            return "Create a REST API with FastAPI that handles user authentication with JWT tokens and rate limiting"

        st.markdown("""
        <div class="quick-start-card">
            <div class="quick-start-icon">🏗️</div>
            <div class="quick-start-title">Architecture Design</div>
            <div class="quick-start-desc">Design system architectures</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try Architecture", key="qs_arch", use_container_width=True):
            return "Design a microservices architecture for a scalable e-commerce platform with event-driven communication"

    return None


def render_user_message(content: str, timestamp: Optional[str] = None, file_info: Optional[Dict] = None):
    """Render a user message bubble"""
    time_str = timestamp or datetime.now().strftime("%H:%M")

    file_html = ""
    if file_info:
        icons = {"documents": "📄", "code": "💻", "images": "🖼️", "audio": "🎵"}
        icon = icons.get(file_info.get('type', ''), '📎')
        file_html = f"""
        <div class="file-attachment">
            <span class="file-attachment-icon">{icon}</span>
            <span class="file-attachment-name">{file_info.get('name', 'File')}</span>
            <span class="file-attachment-type">{file_info.get('type', 'file').upper()}</span>
        </div>
        """

    st.markdown(f"""
    <div class="user-message-bubble">
        {file_html}
        <div style="font-size: 0.95rem; line-height: 1.6;">{content}</div>
        <div class="message-timestamp">{time_str}</div>
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

    # Default metrics if not provided
    if metrics is None:
        metrics = {
            "Clarity": quality_score + 5,
            "Specificity": quality_score - 3,
            "Structure": quality_score + 2,
            "Completeness": quality_score - 5
        }
        # Clamp values
        metrics = {k: max(0, min(100, v)) for k, v in metrics.items()}

    st.markdown(f"""
    <div class="agent-message-bubble">
        <div class="message-header">
            <div class="message-avatar">🧠</div>
            <span class="message-label">LUKTHAN Agent</span>
        </div>

        <div class="prompt-output-container">
            <span class="prompt-output-label">✨ OPTIMIZED PROMPT</span>
            <div class="prompt-output-box">{prompt}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("📋 Copy", key=f"copy_{hash(prompt)}", use_container_width=True):
            st.toast("✅ Prompt copied to clipboard!", icon="✅")
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
        <div class="insights-panel" style="text-align: center; padding: 3rem 1.5rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.3;">📊</div>
            <div style="color: var(--lukthan-text-muted); font-size: 0.9rem;">
                Generate a prompt to see insights
            </div>
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
        score_gradient = "linear-gradient(135deg, #10B981 0%, #34D399 100%)"
    elif quality_score >= 60:
        score_color = "#F59E0B"
        score_gradient = "linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%)"
    else:
        score_color = "#EF4444"
        score_gradient = "linear-gradient(135deg, #EF4444 0%, #F87171 100%)"

    # Domain and Task icons
    domain_icons = {
        "research": "🔬", "coding": "💻", "data_science": "📊", "general": "🌐"
    }
    task_icons = {
        "literature_review": "📚", "code_generation": "⚡", "bug_fix": "🐛",
        "api_design": "🔌", "data_analysis": "📈", "general_query": "💬"
    }

    domain_icon = domain_icons.get(domain.lower(), "🌐")
    task_icon = task_icons.get(task_type.lower(), "💬")

    st.markdown(f"""
    <div class="insights-panel">
        <div class="insights-header">
            <span style="font-size: 1.25rem;">📊</span>
            <span class="insights-title">Prompt Insights</span>
        </div>

        <!-- Domain & Task -->
        <div class="insights-section">
            <div class="insights-label">Detection</div>
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                <span class="tag-pill tag-cyan">{domain_icon} {domain.replace('_', ' ').title()}</span>
                <span class="tag-pill tag-purple">{task_icon} {task_type.replace('_', ' ').title()}</span>
            </div>
        </div>

        <!-- Quality Score -->
        <div class="insights-section">
            <div class="insights-label">Quality Score</div>
            <div class="quality-score-container" style="--score-gradient: {score_gradient};">
                <div class="quality-score-circle" style="color: {score_color};">
                    {quality_score}
                </div>
                <div class="quality-score-label">out of 100</div>
            </div>
        </div>

        <!-- Metric Bars -->
        <div class="insights-section">
            <div class="insights-label">Breakdown</div>
    """, unsafe_allow_html=True)

    # Render metric bars
    for metric_name, metric_value in metrics.items():
        bar_color = "#10B981" if metric_value >= 80 else "#F59E0B" if metric_value >= 60 else "#EF4444"
        st.markdown(f"""
        <div class="metric-row">
            <span class="metric-name">{metric_name}</span>
            <div class="metric-bar-container">
                <div class="metric-bar-fill" style="width: {metric_value}%; background: {bar_color};"></div>
            </div>
            <span class="metric-value">{metric_value}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Tips section
    if suggestions and len(suggestions) > 0:
        st.markdown("""
        <div class="insights-section">
            <div class="insights-label">Suggestions</div>
            <div class="tips-card">
                <ul class="tips-list">
        """, unsafe_allow_html=True)

        for suggestion in suggestions[:3]:
            st.markdown(f"<li>{suggestion}</li>", unsafe_allow_html=True)

        st.markdown("""
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # How to use tips
    st.markdown("""
        <div class="insights-section">
            <div class="insights-label">How to Use</div>
            <div class="tips-card">
                <ul class="tips-list">
                    <li>Copy the optimized prompt</li>
                    <li>Paste into ChatGPT, Claude, or Gemini</li>
                    <li>Get more accurate AI responses</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_typing_indicator():
    """Show LUKTHAN thinking animation"""
    st.markdown("""
    <div class="agent-message-bubble" style="display: inline-block; padding: 1rem 1.5rem;">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
            <span style="color: var(--lukthan-text-secondary); font-size: 0.85rem;">LUKTHAN is thinking...</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_file_indicator(filename: str, file_type: str):
    """Show file attachment indicator"""
    icons = {
        "documents": "📄",
        "code": "💻",
        "images": "🖼️",
        "audio": "🎵",
        "unknown": "📎"
    }

    st.markdown(f"""
    <div class="file-attachment">
        <span class="file-attachment-icon">{icons.get(file_type, '📎')}</span>
        <span class="file-attachment-name">{filename}</span>
        <span class="file-attachment-type">{file_type.upper()}</span>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    """Render the LUKTHAN footer"""
    st.markdown("""
    <div class="lukthan-footer">
        <div class="footer-brand">LUKTHAN</div>
        <div class="footer-text">Structured prompts for serious research and code.</div>
        <div style="margin-top: 0.75rem;">
            <span style="color: var(--lukthan-text-muted); font-size: 0.7rem;">
                Powered by Gemini AI • Made for Researchers & Developers
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
