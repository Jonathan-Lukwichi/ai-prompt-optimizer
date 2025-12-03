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
    initial_sidebar_state="expanded",
    menu_items={
        'About': '# LUKTHAN - AI Prompt Agent\nStructured prompts for serious research and code.'
    }
)

# ==================== LOAD THEME ====================

from utils.chat_components import (
    load_lukthan_theme,
    render_sidebar,
    render_welcome_hero,
    render_user_message,
    render_agent_response,
    render_insights_panel,
    render_typing_indicator,
    render_file_indicator,
    render_footer
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

if 'processing' not in st.session_state:
    st.session_state.processing = False

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

# ==================== SIDEBAR ====================

sidebar_action = render_sidebar()

if sidebar_action == "clear_chat":
    st.session_state.chat_history = []
    st.session_state.uploaded_file_content = None
    st.session_state.uploaded_file_type = None
    st.session_state.uploaded_file_name = None
    st.session_state.last_result = None
    st.rerun()

# ==================== MAIN LAYOUT ====================

# Create two columns: Chat (60%) and Insights (40%)
chat_col, insights_col = st.columns([3, 2], gap="large")

# ==================== CHAT COLUMN ====================

with chat_col:
    # Header
    st.markdown("""
    <div style="
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem 0;
        border-bottom: 1px solid rgba(0, 229, 255, 0.2);
        margin-bottom: 1.5rem;
    ">
        <span style="font-size: 2rem;">🧠</span>
        <div>
            <h1 style="
                margin: 0;
                font-size: 1.5rem;
                background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: 800;
            ">LUKTHAN</h1>
            <p style="margin: 0; color: #8B949E; font-size: 0.85rem;">AI Prompt Agent for Research & Code</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat container
    chat_container = st.container()

    # Display chat history or welcome screen
    with chat_container:
        if not st.session_state.chat_history:
            # Show welcome hero with examples
            example_input = render_welcome_hero()
            if example_input:
                st.session_state.pending_input = example_input
                st.rerun()
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

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Input container
    st.markdown("""
    <div style="
        background: rgba(11, 16, 32, 0.8);
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 20px;
        padding: 1.5rem;
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 1rem;
        ">
            <span style="color: #00E5FF;">💬</span>
            <span style="color: #F0F6FC; font-weight: 600; font-size: 0.9rem;">What do you want to create?</span>
        </div>
    """, unsafe_allow_html=True)

    # File upload (collapsible)
    with st.expander("📎 Attach file (optional)", expanded=False):
        uploaded_file = st.file_uploader(
            "Upload a file",
            type=['pdf', 'txt', 'md', 'py', 'js', 'ts', 'java', 'cpp', 'go', 'rs', 'sql',
                  'json', 'yaml', 'png', 'jpg', 'jpeg', 'gif', 'wav', 'mp3'],
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
                render_file_indicator(uploaded_file.name, file_type)
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")

    # Voice and Text input row
    input_row_col1, input_row_col2 = st.columns([1, 8])

    with input_row_col1:
        # Voice input button
        try:
            from audio_recorder_streamlit import audio_recorder
            audio_bytes = audio_recorder(
                text="",
                recording_color="#00E5FF",
                neutral_color="#0B1020",
                icon_name="microphone",
                icon_size="2x",
                pause_threshold=2.0,
                key="voice_recorder"
            )

            if audio_bytes:
                with st.spinner("🎤 Transcribing..."):
                    try:
                        from core.file_processor import VoiceProcessor
                        transcribed = VoiceProcessor.transcribe_audio_bytes(audio_bytes)
                        if transcribed:
                            st.session_state.voice_input = transcribed
                            st.rerun()
                    except Exception as e:
                        st.error(f"Voice error: {str(e)}")
        except ImportError:
            st.markdown("🎤", help="Voice input requires audio-recorder-streamlit package")

    with input_row_col2:
        # Check for voice input or pending input
        default_value = ""
        if hasattr(st.session_state, 'voice_input') and st.session_state.voice_input:
            default_value = st.session_state.voice_input
            st.session_state.voice_input = None
        elif st.session_state.pending_input:
            default_value = st.session_state.pending_input
            st.session_state.pending_input = None

        user_input = st.text_area(
            "Your request",
            value=default_value,
            placeholder="Describe what you need... (e.g., 'Create a Python REST API with authentication')",
            height=100,
            label_visibility="collapsed",
            key="main_input"
        )

    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        send_clicked = st.button(
            "🚀 Generate Optimized Prompt",
            type="primary",
            use_container_width=True,
            key="generate_btn"
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ==================== INSIGHTS COLUMN ====================

with insights_col:
    # Insights header
    st.markdown("""
    <div style="
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem 0;
        border-bottom: 1px solid rgba(0, 229, 255, 0.2);
        margin-bottom: 1.5rem;
    ">
        <span style="font-size: 1.5rem;">📊</span>
        <h2 style="
            margin: 0;
            font-size: 1.25rem;
            background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 700;
        ">Insights & Analysis</h2>
    </div>
    """, unsafe_allow_html=True)

    # Render insights panel based on last result
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

    # Quick tips when no result
    if not st.session_state.last_result:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(0, 229, 255, 0.05) 0%, rgba(155, 92, 255, 0.05) 100%);
            border: 1px solid rgba(0, 229, 255, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
            margin-top: 1rem;
        ">
            <div style="
                color: #00E5FF;
                font-weight: 600;
                font-size: 0.9rem;
                margin-bottom: 1rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            ">
                <span>💡</span> How LUKTHAN Works
            </div>
            <ul style="
                list-style: none;
                padding: 0;
                margin: 0;
            ">
                <li style="
                    color: #8B949E;
                    font-size: 0.85rem;
                    padding: 0.5rem 0;
                    padding-left: 1.5rem;
                    position: relative;
                ">
                    <span style="position: absolute; left: 0; color: #00E5FF;">1.</span>
                    Describe your task in plain language
                </li>
                <li style="
                    color: #8B949E;
                    font-size: 0.85rem;
                    padding: 0.5rem 0;
                    padding-left: 1.5rem;
                    position: relative;
                ">
                    <span style="position: absolute; left: 0; color: #00E5FF;">2.</span>
                    LUKTHAN analyzes and detects context
                </li>
                <li style="
                    color: #8B949E;
                    font-size: 0.85rem;
                    padding: 0.5rem 0;
                    padding-left: 1.5rem;
                    position: relative;
                ">
                    <span style="position: absolute; left: 0; color: #00E5FF;">3.</span>
                    Generates optimized, structured prompt
                </li>
                <li style="
                    color: #8B949E;
                    font-size: 0.85rem;
                    padding: 0.5rem 0;
                    padding-left: 1.5rem;
                    position: relative;
                ">
                    <span style="position: absolute; left: 0; color: #00E5FF;">4.</span>
                    Copy and use in ChatGPT, Claude, etc.
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

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
    with st.spinner("🧠 LUKTHAN is analyzing and generating your optimized prompt..."):
        try:
            from core.prompt_agent import PromptAgent

            # Get settings from sidebar
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

            # Calculate metrics from quality score
            base_score = result.quality_score
            metrics = {
                "Clarity": min(100, base_score + 5),
                "Specificity": max(0, base_score - 3),
                "Structure": min(100, base_score + 2),
                "Completeness": max(0, base_score - 5)
            }

            # Add agent response to history
            agent_message = {
                'role': 'agent',
                'prompt': result.optimized_prompt,
                'domain': result.domain,
                'task_type': result.task_type,
                'quality_score': result.quality_score,
                'suggestions': result.suggestions,
                'template_used': result.template_used,
                'metadata': result.metadata,
                'timestamp': datetime.now().strftime("%H:%M")
            }
            st.session_state.chat_history.append(agent_message)

            # Store last result for insights panel
            st.session_state.last_result = {
                'domain': result.domain,
                'task_type': result.task_type,
                'quality_score': result.quality_score,
                'metrics': metrics,
                'suggestions': result.suggestions
            }

            # Clear file uploads after processing
            st.session_state.uploaded_file_content = None
            st.session_state.uploaded_file_type = None
            st.session_state.uploaded_file_name = None

        except Exception as e:
            st.error(f"Error: {str(e)}")
            # Add error message
            st.session_state.chat_history.append({
                'role': 'agent',
                'prompt': f"I encountered an error: {str(e)}\n\nPlease try again with a different request.",
                'domain': 'error',
                'task_type': 'error',
                'quality_score': 0,
                'suggestions': ["Try rephrasing your request", "Check your API key configuration"],
                'timestamp': datetime.now().strftime("%H:%M")
            })

    st.rerun()

# Handle regeneration
if hasattr(st.session_state, 'regenerate_last') and st.session_state.regenerate_last:
    st.session_state.regenerate_last = False
    # Find last user message
    for i in range(len(st.session_state.chat_history) - 1, -1, -1):
        if st.session_state.chat_history[i]['role'] == 'user':
            # Remove the last agent response
            if i + 1 < len(st.session_state.chat_history):
                st.session_state.chat_history.pop(i + 1)
            # Set input for regeneration
            st.session_state.pending_input = st.session_state.chat_history[i]['content']
            break
    st.rerun()

# ==================== FOOTER ====================

render_footer()
