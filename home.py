"""
AI Prompt Agent - Chat Interface
Transform your ideas into powerful, optimized prompts
Specialized for Research and Coding
"""
import streamlit as st
from datetime import datetime
from typing import Optional
from core.config import Config
from utils.ui_components import load_custom_css
from utils.chat_components import (
    load_chat_css,
    render_welcome_screen,
    render_user_message,
    render_agent_message,
    render_typing_indicator,
    render_file_upload_indicator,
    render_sidebar_chat
)

# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="AI Prompt Agent | Research & Coding",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': '# AI Prompt Agent\nTransform your ideas into powerful prompts for AI tools.'
    }
)

# Load CSS
load_custom_css()
load_chat_css()

# ==================== API KEY CHECK ====================

if not Config.GEMINI_API_KEY or Config.GEMINI_API_KEY == "":
    st.error("""
    ### ⚠️ Configuration Required

    **Gemini API Key is not configured!**

    To use this app:
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

# ==================== SIDEBAR ====================

sidebar_action = render_sidebar_chat()

if sidebar_action == "clear_chat":
    st.session_state.chat_history = []
    st.session_state.uploaded_file_content = None
    st.session_state.uploaded_file_type = None
    st.session_state.uploaded_file_name = None
    st.rerun()

# ==================== MAIN CHAT INTERFACE ====================

# Header
st.markdown("""
<div style="
    text-align: center;
    padding: 1rem 0;
    border-bottom: 1px solid rgba(6, 182, 212, 0.2);
    margin-bottom: 1rem;
">
    <h1 style="
        font-size: 1.5rem;
        background: linear-gradient(135deg, #06B6D4 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        margin: 0;
    ">🤖 AI Prompt Agent</h1>
    <p style="color: #9CA3AF; font-size: 0.85rem; margin-top: 0.25rem;">
        Describe what you need → Get optimized prompts instantly
    </p>
</div>
""", unsafe_allow_html=True)

# Chat container
chat_container = st.container()

# Display chat history or welcome screen
with chat_container:
    if not st.session_state.chat_history:
        # Show welcome screen with examples
        example_input = render_welcome_screen()
        if example_input:
            st.session_state.pending_input = example_input
            st.rerun()
    else:
        # Display chat messages
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                render_user_message(message['content'], message.get('timestamp'))
                if message.get('file_name'):
                    render_file_upload_indicator(message['file_name'], message.get('file_type', 'unknown'))
            else:
                action = render_agent_message(
                    prompt=message['prompt'],
                    domain=message.get('domain', 'general'),
                    task_type=message.get('task_type', 'general_query'),
                    quality_score=message.get('quality_score', 75),
                    suggestions=message.get('suggestions', []),
                    show_details=False
                )
                if action == "regenerate":
                    # Find the original user message and regenerate
                    st.session_state.regenerate_last = True
                    st.rerun()

# ==================== INPUT AREA ====================

st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)  # Spacer

# Input section
st.markdown("""
<div style="
    background: rgba(17, 24, 39, 0.8);
    border: 1px solid rgba(6, 182, 212, 0.3);
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 1rem;
">
""", unsafe_allow_html=True)

# File upload (optional)
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

        # Process file
        try:
            from core.file_processor import FileProcessor
            processor = FileProcessor()
            content, file_type = processor.process_file(uploaded_file)
            st.session_state.uploaded_file_content = content
            st.session_state.uploaded_file_type = file_type
            st.success(f"✅ {uploaded_file.name} ready!")
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

# Voice input option
voice_col, text_col = st.columns([1, 5])

with voice_col:
    try:
        from audio_recorder_streamlit import audio_recorder
        audio_bytes = audio_recorder(
            text="",
            recording_color="#06B6D4",
            neutral_color="#111827",
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

# Text input
with text_col:
    # Check for voice input or pending input
    default_value = ""
    if hasattr(st.session_state, 'voice_input') and st.session_state.voice_input:
        default_value = st.session_state.voice_input
        st.session_state.voice_input = None
    elif hasattr(st.session_state, 'pending_input') and st.session_state.pending_input:
        default_value = st.session_state.pending_input
        st.session_state.pending_input = None

    user_input = st.text_area(
        "Your message",
        value=default_value,
        placeholder="Describe what you need... (e.g., 'Create a Python script for web scraping')",
        height=80,
        label_visibility="collapsed",
        key="main_input"
    )

# Send button
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    send_clicked = st.button("🚀 Generate Prompt", type="primary", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

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
    with st.spinner("🤖 Analyzing and generating optimized prompt..."):
        try:
            from core.prompt_agent import PromptAgent

            agent = PromptAgent()
            result = agent.process_input_sync(
                user_input=user_input,
                file_content=st.session_state.uploaded_file_content,
                file_type=st.session_state.uploaded_file_type
            )

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

st.markdown("""
<div style="
    text-align: center;
    color: #9CA3AF;
    font-size: 0.75rem;
    padding: 2rem 0 1rem;
    border-top: 1px solid rgba(6, 182, 212, 0.1);
    margin-top: 2rem;
">
    <p>AI Prompt Agent • Specialized for Research & Coding</p>
    <p style="margin-top: 0.25rem;">
        <span style="
            background: linear-gradient(135deg, #06B6D4 0%, #8B5CF6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 600;
        ">Powered by Gemini AI</span>
    </p>
</div>
""", unsafe_allow_html=True)
