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


def render_welcome_hero():
    """Render simple welcome message"""
    st.markdown("### 🧠 Welcome to LUKTHAN")
    st.markdown("Transform rough ideas into powerful prompts for **ChatGPT**, **Claude**, **Gemini**.")
    st.caption("Specialized for Research & Coding")
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


def render_file_indicator(filename: str, file_type: str):
    """Show file indicator using native Streamlit"""
    icons = {"documents": "📄", "code": "💻", "images": "🖼️", "audio": "🎵", "unknown": "📎"}
    icon = icons.get(file_type, '📎')
    st.success(f"{icon} **{filename}** ({file_type.upper()})")
