"""
LUKTHAN - AI Prompt Agent
Chat UI Components with NEXAVERSE Theme (Cyan + Purple)
Using inline styles for reliable rendering
"""
import streamlit as st
from typing import Optional, List, Dict, Any
from datetime import datetime
import html


def load_lukthan_theme():
    """Load basic Streamlit overrides"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    .main .block-container { padding-top: 1rem; max-width: 100%; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stButton > button {
        background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    .stTextArea textarea {
        background: #050816 !important;
        border: 1px solid rgba(0, 229, 255, 0.3) !important;
        border-radius: 10px !important;
        color: #F0F6FC !important;
    }

    .stSelectbox > div > div {
        background: #050816 !important;
        border-radius: 10px !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050816 0%, #0B1020 100%) !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the LUKTHAN branded sidebar"""
    with st.sidebar:
        # Brand box with inline styles
        st.markdown("""
        <div style="
            text-align: center;
            padding: 1.5rem;
            background: linear-gradient(180deg, rgba(0, 229, 255, 0.08) 0%, rgba(155, 92, 255, 0.08) 100%);
            border: 1px solid rgba(0, 229, 255, 0.2);
            border-radius: 16px;
            margin-bottom: 1rem;
        ">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🧠</div>
            <div style="
                font-size: 1.75rem;
                font-weight: 900;
                letter-spacing: 0.1em;
                background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            ">LUKTHAN</div>
            <div style="color: #8B949E; font-size: 0.8rem; margin-top: 0.25rem;">AI Prompt Agent</div>
            <div style="
                display: inline-block;
                background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
                color: white;
                font-size: 0.6rem;
                font-weight: 700;
                padding: 0.2rem 0.6rem;
                border-radius: 20px;
                margin-top: 0.5rem;
            ">RESEARCH & CODE</div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.markdown("**⚙️ Agent Settings**")

        st.selectbox("Domain", ["🔮 Auto Detect", "🔬 Research", "💻 Coding", "📊 Data Science", "🌐 General"], key="domain_setting")
        st.selectbox("Target AI", ["ChatGPT (GPT-4)", "Claude 3.5", "Gemini Pro", "Llama 3"], key="target_ai_setting")
        st.selectbox("Language", ["English", "French", "Spanish", "German", "Portuguese"], key="language_setting")
        st.selectbox("Level", ["Student", "Professional", "Expert", "Academic"], index=1, key="level_setting")

        st.divider()

        with st.expander("💡 Pro Tips"):
            st.markdown("- Be specific about your goal\n- Include context\n- Mention output format")

        st.divider()

        if st.button("🗑️ Clear Conversation", use_container_width=True):
            return "clear_chat"

        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; color: #6E7681; font-size: 0.75rem;">
            <div style="background: linear-gradient(135deg, #00E5FF, #9B5CFF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;">LUKTHAN</div>
            <div>v2.0 Pro</div>
        </div>
        """, unsafe_allow_html=True)

    return None


def render_welcome_hero():
    """Render welcome section"""
    st.markdown("""
    <div style="
        text-align: center;
        padding: 2.5rem 1.5rem;
        background: linear-gradient(180deg, rgba(0, 229, 255, 0.05) 0%, transparent 100%);
        border-radius: 20px;
        border: 1px solid rgba(0, 229, 255, 0.2);
        margin-bottom: 1.5rem;
    ">
        <div style="font-size: 3.5rem; margin-bottom: 1rem;">🧠</div>
        <div style="
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        ">Welcome to LUKTHAN</div>
        <div style="color: #8B949E; font-size: 1rem; line-height: 1.6;">
            Transform rough ideas into powerful prompts for ChatGPT, Claude, Gemini.<br>
            <strong style="color: #F0F6FC;">Specialized for Research & Coding.</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**⚡ Quick Start Examples**")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background: #0B1020; border: 1px solid rgba(0,229,255,0.2); border-radius: 12px; padding: 1rem; margin-bottom: 0.5rem;">
            <div style="font-size: 1.5rem;">🔬</div>
            <div style="color: #F0F6FC; font-weight: 600;">Literature Review</div>
            <div style="color: #6E7681; font-size: 0.75rem;">Generate research prompts</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try Research", key="qs_research", use_container_width=True):
            return "Help me write a systematic literature review on machine learning in healthcare"

        st.markdown("""
        <div style="background: #0B1020; border: 1px solid rgba(0,229,255,0.2); border-radius: 12px; padding: 1rem; margin-bottom: 0.5rem;">
            <div style="font-size: 1.5rem;">📊</div>
            <div style="color: #F0F6FC; font-weight: 600;">Data Analysis</div>
            <div style="color: #6E7681; font-size: 0.75rem;">Analyze datasets</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try Analysis", key="qs_data", use_container_width=True):
            return "Create a prompt to analyze customer churn data and build a prediction model"

    with col2:
        st.markdown("""
        <div style="background: #0B1020; border: 1px solid rgba(0,229,255,0.2); border-radius: 12px; padding: 1rem; margin-bottom: 0.5rem;">
            <div style="font-size: 1.5rem;">💻</div>
            <div style="color: #F0F6FC; font-weight: 600;">Code Generation</div>
            <div style="color: #6E7681; font-size: 0.75rem;">Build APIs and scripts</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try Coding", key="qs_code", use_container_width=True):
            return "Create a REST API with FastAPI that handles user authentication with JWT"

        st.markdown("""
        <div style="background: #0B1020; border: 1px solid rgba(0,229,255,0.2); border-radius: 12px; padding: 1rem; margin-bottom: 0.5rem;">
            <div style="font-size: 1.5rem;">🏗️</div>
            <div style="color: #F0F6FC; font-weight: 600;">Architecture</div>
            <div style="color: #6E7681; font-size: 0.75rem;">Design systems</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try Architecture", key="qs_arch", use_container_width=True):
            return "Design a microservices architecture for an e-commerce platform"

    return None


def render_user_message(content: str, timestamp: Optional[str] = None, file_info: Optional[Dict] = None):
    """Render user message using native Streamlit components"""
    time_str = timestamp or datetime.now().strftime("%H:%M")

    # Create right-aligned container using columns
    col_spacer, col_msg = st.columns([1, 3])

    with col_msg:
        # File attachment indicator
        if file_info:
            icons = {"documents": "📄", "code": "💻", "images": "🖼️", "audio": "🎵"}
            icon = icons.get(file_info.get('type', ''), '📎')
            st.caption(f"{icon} {file_info.get('name', 'File')}")

        # User message in a styled container
        with st.container():
            st.info(f"**You** ({time_str})\n\n{content}")


def render_agent_response(
    prompt: str,
    domain: str = "general",
    task_type: str = "general",
    quality_score: int = 85,
    metrics: Optional[Dict[str, int]] = None,
    suggestions: Optional[List[str]] = None
):
    """Render agent response using native Streamlit components"""

    # Create left-aligned container using columns
    col_msg, col_spacer = st.columns([3, 1])

    with col_msg:
        # Agent header
        st.markdown("🧠 **LUKTHAN Agent**")

        # Optimized prompt in an expander or container
        with st.container():
            st.success("✨ **OPTIMIZED PROMPT**")
            st.code(prompt, language=None)

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
    """Render insights panel using Streamlit native components"""

    if not show_content:
        st.markdown("""
        <div style="background: #0B1020; border: 1px solid rgba(0, 229, 255, 0.2); border-radius: 16px; padding: 3rem 1.5rem; text-align: center;">
            <div style="font-size: 3rem; opacity: 0.3; margin-bottom: 1rem;">📊</div>
            <div style="color: #6E7681;">Generate a prompt to see insights</div>
        </div>
        """, unsafe_allow_html=True)
        return

    if metrics is None:
        metrics = {
            "Clarity": min(100, quality_score + 5),
            "Specificity": max(0, quality_score - 3),
            "Structure": min(100, quality_score + 2),
            "Completeness": max(0, quality_score - 5)
        }

    score_color = "#10B981" if quality_score >= 80 else "#F59E0B" if quality_score >= 60 else "#EF4444"

    domain_icons = {"research": "🔬", "coding": "💻", "data_science": "📊", "general": "🌐"}
    task_icons = {"literature_review": "📚", "code_generation": "⚡", "bug_fix": "🐛", "api_design": "🔌", "data_analysis": "📈", "general_query": "💬"}

    d_icon = domain_icons.get(domain.lower(), "🌐")
    t_icon = task_icons.get(task_type.lower(), "💬")
    d_name = domain.replace('_', ' ').title()
    t_name = task_type.replace('_', ' ').title()

    # Use a container with custom styling
    with st.container():
        # Header
        st.markdown("### 📊 Prompt Insights")

        # Detection section
        st.markdown("**DETECTION**")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"{d_icon} {d_name}")
        with col2:
            st.info(f"{t_icon} {t_name}")

        st.markdown("")

        # Quality Score
        st.markdown("**QUALITY SCORE**")
        score_col1, score_col2, score_col3 = st.columns([1, 2, 1])
        with score_col2:
            if quality_score >= 80:
                st.success(f"### {quality_score}/100")
            elif quality_score >= 60:
                st.warning(f"### {quality_score}/100")
            else:
                st.error(f"### {quality_score}/100")

        st.markdown("")

        # Breakdown with progress bars
        st.markdown("**BREAKDOWN**")
        for name, value in metrics.items():
            col_label, col_bar = st.columns([1, 3])
            with col_label:
                st.caption(name)
            with col_bar:
                st.progress(value / 100)

        st.markdown("")

        # Suggestions
        if suggestions:
            st.markdown("**SUGGESTIONS**")
            for s in suggestions[:3]:
                st.markdown(f"› {s}")

        st.markdown("")

        # How to Use
        st.markdown("**HOW TO USE**")
        st.markdown("› Copy the optimized prompt")
        st.markdown("› Paste into ChatGPT, Claude, or Gemini")
        st.markdown("› Get more accurate AI responses")


def render_typing_indicator():
    """Show thinking indicator"""
    st.markdown("""
    <div style="
        background: #0B1020;
        border: 1px solid rgba(0, 229, 255, 0.2);
        padding: 1rem;
        border-radius: 12px;
        display: inline-block;
    ">
        <span style="color: #8B949E;">🧠 LUKTHAN is thinking...</span>
    </div>
    """, unsafe_allow_html=True)


def render_file_indicator(filename: str, file_type: str):
    """Show file indicator"""
    icons = {"documents": "📄", "code": "💻", "images": "🖼️", "audio": "🎵", "unknown": "📎"}
    icon = icons.get(file_type, '📎')

    st.markdown(f"""
    <div style="
        display: inline-flex; align-items: center; gap: 0.5rem;
        background: rgba(0, 229, 255, 0.1);
        border: 1px solid rgba(0, 229, 255, 0.3);
        border-radius: 8px;
        padding: 0.4rem 0.8rem;
        font-size: 0.8rem;
        color: #F0F6FC;
    ">
        {icon} {html.escape(filename)}
        <span style="color: #00E5FF; font-weight: 600;">{file_type.upper()}</span>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    """Render footer"""
    st.markdown("""
    <div style="
        text-align: center;
        padding: 1.5rem;
        border-top: 1px solid rgba(0, 229, 255, 0.2);
        margin-top: 2rem;
    ">
        <div style="
            background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 0.9rem;
            letter-spacing: 0.1em;
        ">LUKTHAN</div>
        <div style="color: #6E7681; font-size: 0.7rem; margin-top: 0.25rem;">
            Structured prompts for serious research and code.
        </div>
    </div>
    """, unsafe_allow_html=True)
