"""
Chat UI Components for AI Prompt Agent
Clean, modern chat interface with NEXAVERSE theme
"""
import streamlit as st
from typing import Optional, List, Dict
from datetime import datetime


def load_chat_css():
    """Load CSS specific to chat interface"""
    st.markdown("""
    <style>
    /* Chat Container */
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 1rem;
    }

    /* Message Bubbles */
    .user-message {
        background: linear-gradient(135deg, #06B6D4 0%, #8B5CF6 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 4px 20px;
        margin: 1rem 0;
        margin-left: 20%;
        box-shadow: 0 4px 20px rgba(6, 182, 212, 0.3);
        animation: slideInRight 0.3s ease;
    }

    .agent-message {
        background: rgba(17, 24, 39, 0.8);
        border: 1px solid rgba(6, 182, 212, 0.3);
        color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 20px 20px 20px 4px;
        margin: 1rem 0;
        margin-right: 10%;
        box-shadow: 0 4px 20px rgba(6, 182, 212, 0.1);
        animation: slideInLeft 0.3s ease;
    }

    /* Prompt Output Box */
    .prompt-output {
        background: rgba(17, 24, 39, 0.9);
        border: 1px solid rgba(6, 182, 212, 0.4);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        line-height: 1.6;
        color: #E5E7EB;
        white-space: pre-wrap;
        position: relative;
    }

    .prompt-output::before {
        content: '✨ Optimized Prompt';
        position: absolute;
        top: -12px;
        left: 16px;
        background: linear-gradient(135deg, #06B6D4 0%, #8B5CF6 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }

    /* Copy Button */
    .copy-btn {
        position: absolute;
        top: 12px;
        right: 12px;
        background: rgba(6, 182, 212, 0.2);
        border: 1px solid rgba(6, 182, 212, 0.4);
        color: #06B6D4;
        padding: 8px 16px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.8rem;
        transition: all 0.3s ease;
    }

    .copy-btn:hover {
        background: rgba(6, 182, 212, 0.3);
        transform: translateY(-2px);
    }

    /* Input Area */
    .chat-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(10, 14, 23, 0.95);
        backdrop-filter: blur(20px);
        border-top: 1px solid rgba(6, 182, 212, 0.2);
        padding: 1rem 2rem;
        z-index: 100;
    }

    .input-wrapper {
        max-width: 900px;
        margin: 0 auto;
        display: flex;
        gap: 1rem;
        align-items: flex-end;
    }

    /* File Upload Area */
    .file-upload-zone {
        background: rgba(17, 24, 39, 0.6);
        border: 2px dashed rgba(6, 182, 212, 0.3);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .file-upload-zone:hover {
        border-color: rgba(6, 182, 212, 0.6);
        background: rgba(6, 182, 212, 0.05);
    }

    /* Details Expander */
    .details-expander {
        background: rgba(17, 24, 39, 0.6);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-top: 0.5rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #9CA3AF;
        font-size: 0.85rem;
        transition: all 0.3s ease;
    }

    .details-expander:hover {
        background: rgba(17, 24, 39, 0.8);
        color: #F8FAFC;
    }

    /* Animations */
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    .typing-indicator {
        display: flex;
        gap: 4px;
        padding: 1rem;
    }

    .typing-dot {
        width: 8px;
        height: 8px;
        background: #06B6D4;
        border-radius: 50%;
        animation: pulse 1.5s ease infinite;
    }

    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }

    /* Welcome Screen */
    .welcome-container {
        text-align: center;
        padding: 4rem 2rem;
        max-width: 700px;
        margin: 0 auto;
    }

    .welcome-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
    }

    .welcome-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #06B6D4 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }

    .welcome-subtitle {
        color: #9CA3AF;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 2rem;
    }

    /* Quick Actions */
    .quick-action {
        background: rgba(17, 24, 39, 0.6);
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
    }

    .quick-action:hover {
        border-color: rgba(6, 182, 212, 0.5);
        background: rgba(6, 182, 212, 0.1);
        transform: translateY(-2px);
    }

    .quick-action-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }

    .quick-action-text {
        color: #F8FAFC;
        font-size: 0.9rem;
        font-weight: 500;
    }

    /* Badge */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .badge-cyan {
        background: rgba(6, 182, 212, 0.2);
        color: #06B6D4;
        border: 1px solid rgba(6, 182, 212, 0.3);
    }

    .badge-purple {
        background: rgba(139, 92, 246, 0.2);
        color: #8B5CF6;
        border: 1px solid rgba(139, 92, 246, 0.3);
    }

    .badge-green {
        background: rgba(16, 185, 129, 0.2);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)


def render_welcome_screen():
    """Render the welcome screen with quick actions"""
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-icon">🤖</div>
        <h1 class="welcome-title">AI Prompt Agent</h1>
        <p class="welcome-subtitle">
            Transform your ideas into powerful, optimized prompts for ChatGPT, Claude, and other AI tools.<br>
            Just describe what you need — I'll handle the rest.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Quick action examples
    st.markdown("<p style='text-align: center; color: #9CA3AF; margin-bottom: 1rem;'>Try an example:</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔬 Research Help", use_container_width=True, key="example_research"):
            return "Help me write a literature review on machine learning in healthcare"

        if st.button("🐍 Python Code", use_container_width=True, key="example_python"):
            return "Create a REST API with FastAPI that handles user authentication"

    with col2:
        if st.button("📊 Data Analysis", use_container_width=True, key="example_data"):
            return "Analyze customer churn data and build a prediction model"

        if st.button("🏗️ Architecture", use_container_width=True, key="example_arch"):
            return "Design a microservices architecture for an e-commerce platform"

    return None


def render_user_message(message: str, timestamp: Optional[str] = None):
    """Render a user message bubble"""
    time_str = timestamp or datetime.now().strftime("%H:%M")
    st.markdown(f"""
    <div class="user-message">
        <div style="font-size: 0.95rem; line-height: 1.5;">{message}</div>
        <div style="font-size: 0.7rem; opacity: 0.7; margin-top: 0.5rem; text-align: right;">{time_str}</div>
    </div>
    """, unsafe_allow_html=True)


def render_agent_message(prompt: str, domain: str, task_type: str, quality_score: int,
                        suggestions: List[str], show_details: bool = False):
    """Render the agent's response with optimized prompt"""

    # Domain badge color
    badge_class = "badge-cyan" if domain in ["coding", "data_science"] else "badge-purple"

    st.markdown(f"""
    <div class="agent-message">
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
            <span style="font-size: 1.5rem;">✨</span>
            <span style="font-weight: 600; color: #F8FAFC;">Here's your optimized prompt</span>
            <span class="badge {badge_class}">{domain.replace('_', ' ').title()}</span>
        </div>

        <div class="prompt-output">
{prompt}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if st.button("📋 Copy", key=f"copy_{hash(prompt)}", use_container_width=True):
            st.toast("✅ Copied to clipboard!", icon="✅")

    with col2:
        if st.button("🔄 Regenerate", key=f"regen_{hash(prompt)}", use_container_width=True):
            return "regenerate"

    # Optional details (collapsed by default)
    with st.expander("📊 View Details", expanded=show_details):
        detail_col1, detail_col2 = st.columns(2)

        with detail_col1:
            st.markdown(f"""
            <div style="padding: 0.5rem;">
                <div style="color: #9CA3AF; font-size: 0.8rem; margin-bottom: 0.25rem;">Quality Score</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: {'#10B981' if quality_score >= 80 else '#F59E0B' if quality_score >= 60 else '#EF4444'};">{quality_score}/100</div>
            </div>
            """, unsafe_allow_html=True)

        with detail_col2:
            st.markdown(f"""
            <div style="padding: 0.5rem;">
                <div style="color: #9CA3AF; font-size: 0.8rem; margin-bottom: 0.25rem;">Task Type</div>
                <div style="font-size: 1rem; font-weight: 600; color: #F8FAFC;">{task_type.replace('_', ' ').title()}</div>
            </div>
            """, unsafe_allow_html=True)

        if suggestions:
            st.markdown("<div style='color: #9CA3AF; font-size: 0.8rem; margin-top: 1rem;'>Suggestions to improve:</div>", unsafe_allow_html=True)
            for suggestion in suggestions:
                st.markdown(f"<div style='color: #F8FAFC; font-size: 0.9rem; padding: 0.25rem 0;'>• {suggestion}</div>", unsafe_allow_html=True)

    return None


def render_typing_indicator():
    """Show typing indicator while processing"""
    st.markdown("""
    <div class="agent-message" style="display: inline-block; padding: 1rem 1.5rem;">
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_file_upload_indicator(filename: str, file_type: str):
    """Show indicator for uploaded file"""
    icons = {
        "documents": "📄",
        "code": "💻",
        "images": "🖼️",
        "audio": "🎵",
        "unknown": "📎"
    }

    st.markdown(f"""
    <div style="
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(6, 182, 212, 0.1);
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin-bottom: 0.5rem;
    ">
        <span>{icons.get(file_type, '📎')}</span>
        <span style="color: #F8FAFC; font-size: 0.9rem;">{filename}</span>
        <span class="badge badge-cyan">{file_type}</span>
    </div>
    """, unsafe_allow_html=True)


def render_chat_input_area():
    """Render the bottom input area with text, voice, and file upload"""
    st.markdown("""
    <div style="
        background: rgba(17, 24, 39, 0.6);
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 16px;
        padding: 1rem;
    ">
    """, unsafe_allow_html=True)

    # Input row
    input_col, btn_col = st.columns([6, 1])

    with input_col:
        user_input = st.text_area(
            "Message",
            placeholder="Describe what you need... (e.g., 'Help me write a Python script for data cleaning')",
            height=80,
            label_visibility="collapsed",
            key="chat_input"
        )

    with btn_col:
        send_clicked = st.button("🚀", use_container_width=True, type="primary", key="send_btn")

    st.markdown("</div>", unsafe_allow_html=True)

    return user_input, send_clicked


def render_sidebar_chat():
    """Render sidebar for chat interface"""
    with st.sidebar:
        st.markdown("""
        <div style="
            text-align: center;
            padding: 1.5rem 0;
            background: rgba(17, 24, 39, 0.6);
            border-radius: 16px;
            border: 1px solid rgba(6, 182, 212, 0.3);
            margin-bottom: 1rem;
        ">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🤖</div>
            <h2 style="
                background: linear-gradient(135deg, #06B6D4 0%, #8B5CF6 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 0;
                font-size: 1.3rem;
                font-weight: 800;
            ">Prompt Agent</h2>
            <p style="color: #9CA3AF; font-size: 0.8rem; margin-top: 0.5rem;">
                Research & Coding Expert
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Capabilities
        st.markdown("""
        <h3 style="
            color: #F8FAFC;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 1rem;
        ">💡 I can help with:</h3>
        """, unsafe_allow_html=True)

        capabilities = [
            ("🔬", "Research & Literature"),
            ("💻", "Code & Development"),
            ("📊", "Data Analysis"),
            ("🏗️", "System Architecture"),
            ("📝", "Documentation"),
            ("🐛", "Debugging")
        ]

        for icon, text in capabilities:
            st.markdown(f"""
            <div style="
                display: flex;
                align-items: center;
                gap: 0.75rem;
                padding: 0.5rem 0;
                color: #9CA3AF;
                font-size: 0.85rem;
            ">
                <span>{icon}</span>
                <span>{text}</span>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Input options
        st.markdown("""
        <h3 style="
            color: #F8FAFC;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 1rem;
        ">📎 Input Options:</h3>
        """, unsafe_allow_html=True)

        input_options = [
            ("💬", "Text message"),
            ("🎤", "Voice input"),
            ("📄", "PDF / Documents"),
            ("💻", "Code files"),
            ("🖼️", "Screenshots"),
        ]

        for icon, text in input_options:
            st.markdown(f"""
            <div style="
                display: flex;
                align-items: center;
                gap: 0.75rem;
                padding: 0.5rem 0;
                color: #9CA3AF;
                font-size: 0.85rem;
            ">
                <span>{icon}</span>
                <span>{text}</span>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            return "clear_chat"

        # Footer
        st.markdown("""
        <div style="
            text-align: center;
            color: #9CA3AF;
            font-size: 0.7rem;
            margin-top: 2rem;
            padding: 1rem;
        ">
            <div>Made for Researchers & Developers</div>
            <div style="
                background: linear-gradient(135deg, #06B6D4 0%, #8B5CF6 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: 700;
                margin-top: 0.5rem;
            ">v2.0 Pro</div>
        </div>
        """, unsafe_allow_html=True)

    return None
