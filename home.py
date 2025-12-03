"""
LUKTHAN - AI Prompt Agent
Transform rough ideas into powerful, optimized prompts
Specialized for Research and Coding workflows
"""
import streamlit as st
from datetime import datetime
from typing import Optional
from core.config import Config

# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="LUKTHAN - AI Prompt Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': '# LUKTHAN - AI Prompt Agent\nStructured prompts for serious research and code.'
    }
)

# ==================== LOAD THEME ====================

from utils.chat_components import (
    load_lukthan_theme,
    render_welcome_hero,
    render_user_message,
    render_agent_response,
    render_insights_panel,
    render_file_indicator
)

load_lukthan_theme()

# ==================== API KEY CHECK ====================

if not Config.GEMINI_API_KEY or Config.GEMINI_API_KEY == "":
    st.error("""
    ### ⚠️ Configuration Required

    **Gemini API Key is not configured!**

    To use LUKTHAN:
    1. Get a FREE API key: https://makersuite.google.com/app/apikey
    2. Add to Streamlit Secrets: `GEMINI_API_KEY = "your-key"`
    """)
    st.stop()

# ==================== SESSION STATE ====================

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'uploaded_file_content' not in st.session_state:
    st.session_state.uploaded_file_content = None

if 'uploaded_file_type' not in st.session_state:
    st.session_state.uploaded_file_type = None

if 'uploaded_file_name' not in st.session_state:
    st.session_state.uploaded_file_name = None

if 'last_result' not in st.session_state:
    st.session_state.last_result = None

if 'pending_input' not in st.session_state:
    st.session_state.pending_input = None

# ==================== HEADER ====================

col_brand, col_actions = st.columns([6, 1])

with col_brand:
    st.markdown("### 🧠 LUKTHAN")

with col_actions:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.uploaded_file_content = None
        st.session_state.uploaded_file_type = None
        st.session_state.uploaded_file_name = None
        st.session_state.last_result = None
        st.rerun()

# ==================== TAB NAVIGATION ====================

tab_chat, tab_insights, tab_settings = st.tabs(["💬 Chat", "📊 Insights", "⚙️ Settings"])

# ==================== CHAT TAB ====================

with tab_chat:
    # Chat container
    chat_container = st.container()

    # Display chat history or welcome screen
    with chat_container:
        if not st.session_state.chat_history:
            render_welcome_hero()
        else:
            # Display chat messages
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    file_info = None
                    if message.get('file_name'):
                        file_info = {
                            'name': message['file_name'],
                            'type': message.get('file_type', 'unknown')
                        }
                    render_user_message(
                        message['content'],
                        message.get('timestamp'),
                        file_info
                    )
                else:
                    action = render_agent_response(
                        prompt=message['prompt'],
                        domain=message.get('domain', 'general'),
                        task_type=message.get('task_type', 'general_query'),
                        quality_score=message.get('quality_score', 75),
                        suggestions=message.get('suggestions', [])
                    )
                    if action == "regenerate":
                        st.session_state.regenerate_last = True
                        st.rerun()

    # ==================== INPUT AREA ====================

    # Show attached file chip
    if st.session_state.uploaded_file_name:
        file_col1, file_col2 = st.columns([6, 1])
        with file_col1:
            st.markdown(f"""
            <div style="
                display: inline-flex;
                align-items: center;
                gap: 8px;
                background: rgba(0, 229, 255, 0.1);
                border: 1px solid rgba(0, 229, 255, 0.3);
                border-radius: 20px;
                padding: 6px 12px;
                margin-bottom: 10px;
            ">
                <span>📎</span>
                <span style="color: #F0F6FC; font-size: 0.85rem;">{st.session_state.uploaded_file_name}</span>
            </div>
            """, unsafe_allow_html=True)
        with file_col2:
            if st.button("✕", key="remove_file"):
                st.session_state.uploaded_file_name = None
                st.session_state.uploaded_file_content = None
                st.session_state.uploaded_file_type = None
                st.rerun()

    # Professional input container
    st.markdown("""
    <style>
    .input-container {
        background: #0B1020;
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 28px;
        padding: 8px 8px 8px 16px;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Input row
    col_input, col_attach, col_mic, col_send = st.columns([12, 1, 1, 1])

    # Text input
    with col_input:
        default_value = ""
        if st.session_state.pending_input:
            default_value = st.session_state.pending_input
            st.session_state.pending_input = None

        user_input = st.text_input(
            "Message",
            value=default_value,
            placeholder="Message LUKTHAN...",
            label_visibility="collapsed",
            key="main_input"
        )

    # File upload with popover
    with col_attach:
        with st.popover("📎", use_container_width=True):
            st.markdown("**Upload File**")
            uploaded_file = st.file_uploader(
                "Choose file",
                type=['pdf', 'txt', 'md', 'py', 'js', 'ts', 'java', 'cpp', 'go', 'rs', 'sql', 'json', 'yaml', 'png', 'jpg', 'jpeg', 'gif'],
                label_visibility="collapsed",
                key="file_uploader"
            )
            if uploaded_file:
                st.session_state.uploaded_file_name = uploaded_file.name
                try:
                    from core.file_processor import FileProcessor
                    processor = FileProcessor()
                    content, file_type = processor.process_file(uploaded_file)
                    st.session_state.uploaded_file_content = content
                    st.session_state.uploaded_file_type = file_type
                    st.success(f"✓ {uploaded_file.name}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Voice input
    with col_mic:
        try:
            from audio_recorder_streamlit import audio_recorder
            audio_bytes = audio_recorder(
                text="",
                recording_color="#00E5FF",
                neutral_color="#1a1a2e",
                icon_name="microphone",
                icon_size="lg",
                pause_threshold=2.0,
                key="voice_recorder"
            )
            if audio_bytes:
                try:
                    from core.file_processor import VoiceProcessor
                    transcribed = VoiceProcessor.transcribe_audio_bytes(audio_bytes)
                    if transcribed:
                        st.session_state.pending_input = transcribed
                        st.rerun()
                except Exception:
                    pass
        except ImportError:
            st.button("🎤", key="mic_btn", help="Voice input")

    # Send button
    with col_send:
        send_clicked = st.button("➤", type="primary", key="generate_btn", help="Send message")

# ==================== INSIGHTS TAB ====================

with tab_insights:
    if st.session_state.last_result:
        result = st.session_state.last_result
        render_insights_panel(
            domain=result.get('domain', 'general'),
            task_type=result.get('task_type', 'general'),
            quality_score=result.get('quality_score', 85),
            metrics=result.get('metrics'),
            suggestions=result.get('suggestions', []),
            show_content=True
        )
    else:
        render_insights_panel(show_content=False)

        # Quick tips
        st.markdown("**💡 How it works:**")
        st.markdown("1. Describe your task")
        st.markdown("2. LUKTHAN analyzes context")
        st.markdown("3. Get optimized prompt")
        st.markdown("4. Copy to ChatGPT/Claude")

# ==================== SETTINGS TAB ====================

with tab_settings:
    st.markdown("### ⚙️ Agent Settings")

    col1, col2 = st.columns(2)

    with col1:
        st.selectbox(
            "Domain",
            ["🔮 Auto Detect", "🔬 Research", "💻 Coding", "📊 Data Science", "🌐 General"],
            key="domain_setting"
        )
        st.selectbox(
            "Output Language",
            ["English", "French", "Spanish", "German", "Portuguese"],
            key="language_setting"
        )

    with col2:
        st.selectbox(
            "Target AI",
            ["ChatGPT (GPT-4)", "Claude 3.5", "Gemini Pro", "Llama 3"],
            key="target_ai_setting"
        )
        st.selectbox(
            "Expertise Level",
            ["Student", "Professional", "Expert", "Academic"],
            index=1,
            key="level_setting"
        )

    st.markdown("---")
    st.markdown("**💡 Tips:** Be specific • Include context • Mention output format")

# ==================== PROCESS INPUT ====================

if send_clicked and user_input.strip():
    # Add user message to history
    user_message = {
        'role': 'user',
        'content': user_input,
        'timestamp': datetime.now().strftime("%H:%M"),
        'file_name': st.session_state.uploaded_file_name,
        'file_type': st.session_state.uploaded_file_type
    }
    st.session_state.chat_history.append(user_message)

    # Process with AI Agent
    with st.spinner("🧠 Generating optimized prompt..."):
        try:
            from core.prompt_agent import PromptAgent

            # Get settings
            domain_override = None
            if 'domain_setting' in st.session_state:
                domain_map = {
                    "🔬 Research": "research",
                    "💻 Coding": "coding",
                    "📊 Data Science": "data_science",
                    "🌐 General": "general"
                }
                selected = st.session_state.domain_setting
                if selected != "🔮 Auto Detect":
                    domain_override = domain_map.get(selected)

            agent = PromptAgent()
            result = agent.process_input_sync(
                user_input=user_input,
                file_content=st.session_state.uploaded_file_content,
                file_type=st.session_state.uploaded_file_type
            )

            # Calculate metrics
            base_score = result.quality_score
            metrics = {
                "Clarity": min(100, base_score + 5),
                "Specificity": max(0, base_score - 3),
                "Structure": min(100, base_score + 2),
                "Completeness": max(0, base_score - 5)
            }

            # Add agent response
            agent_message = {
                'role': 'agent',
                'prompt': result.optimized_prompt,
                'domain': result.domain,
                'task_type': result.task_type,
                'quality_score': result.quality_score,
                'suggestions': result.suggestions,
                'timestamp': datetime.now().strftime("%H:%M")
            }
            st.session_state.chat_history.append(agent_message)

            # Store for insights
            st.session_state.last_result = {
                'domain': result.domain,
                'task_type': result.task_type,
                'quality_score': result.quality_score,
                'metrics': metrics,
                'suggestions': result.suggestions
            }

            # Clear file uploads
            st.session_state.uploaded_file_content = None
            st.session_state.uploaded_file_type = None
            st.session_state.uploaded_file_name = None

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.session_state.chat_history.append({
                'role': 'agent',
                'prompt': f"Error: {str(e)}\n\nPlease try again.",
                'domain': 'error',
                'task_type': 'error',
                'quality_score': 0,
                'suggestions': ["Try rephrasing your request"],
                'timestamp': datetime.now().strftime("%H:%M")
            })

    st.rerun()

# Handle regeneration
if hasattr(st.session_state, 'regenerate_last') and st.session_state.regenerate_last:
    st.session_state.regenerate_last = False
    for i in range(len(st.session_state.chat_history) - 1, -1, -1):
        if st.session_state.chat_history[i]['role'] == 'user':
            if i + 1 < len(st.session_state.chat_history):
                st.session_state.chat_history.pop(i + 1)
            st.session_state.pending_input = st.session_state.chat_history[i]['content']
            break
    st.rerun()

# ==================== FOOTER ====================

st.markdown("---")
st.caption("🧠 **LUKTHAN** — Structured prompts for serious research and code.")
