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
    render_hero_section,
    render_stats_bar,
    render_features_section,
    render_feature_card,
    render_testimonials_section,
    render_testimonial_card,
    render_footer,
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

if 'show_chat' not in st.session_state:
    st.session_state.show_chat = False

# ==================== SIDEBAR ====================

with st.sidebar:
    # Brand
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 1.5rem;">
        <span style="font-size: 2.5rem;">🧠</span>
        <div style="
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-top: 0.5rem;
        ">LUKTHAN</div>
        <div style="color: #6E7681; font-size: 0.8rem; margin-top: 0.25rem;">AI Prompt Agent</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Settings Section
    st.markdown("""
    <div style="
        color: #00E5FF;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 1rem;
    ">⚙️ Settings</div>
    """, unsafe_allow_html=True)

    st.selectbox(
        "Domain",
        ["🔮 Auto Detect", "🔬 Research", "💻 Coding", "📊 Data Science", "🌐 General"],
        key="domain_setting"
    )

    st.selectbox(
        "Target AI",
        ["ChatGPT (GPT-4)", "Claude 3.5", "Gemini Pro", "Llama 3", "Mistral"],
        key="target_ai_setting"
    )

    st.selectbox(
        "Expertise Level",
        ["Student", "Professional", "Expert", "Academic"],
        index=1,
        key="level_setting"
    )

    st.selectbox(
        "Output Language",
        ["English", "French", "Spanish", "German", "Portuguese", "Japanese", "Chinese"],
        key="language_setting"
    )

    st.markdown("---")

    # Pro Tips
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.1) 0%, rgba(155, 92, 255, 0.1) 100%);
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 0.5rem;
    ">
        <div style="color: #00E5FF; font-weight: 600; font-size: 0.85rem; margin-bottom: 0.5rem;">💡 Pro Tips</div>
        <div style="color: #8B949E; font-size: 0.8rem; line-height: 1.6;">
            • Be specific about output format<br>
            • Include context & constraints<br>
            • Upload files for more context
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Footer in sidebar
    st.markdown("""
    <div style="text-align: center; color: #6E7681; font-size: 0.75rem; padding-top: 1rem;">
        Built with ❤️ for AI
    </div>
    """, unsafe_allow_html=True)

# ==================== HEADER ====================

col_brand, col_actions = st.columns([6, 1])

with col_brand:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; padding: 0.5rem 0;">
        <span style="font-size: 1.75rem;">🧠</span>
        <span style="
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        ">LUKTHAN</span>
    </div>
    """, unsafe_allow_html=True)

with col_actions:
    if st.session_state.chat_history:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.uploaded_file_content = None
            st.session_state.uploaded_file_type = None
            st.session_state.uploaded_file_name = None
            st.session_state.last_result = None
            st.session_state.show_chat = False
            st.rerun()

# ==================== TAB NAVIGATION ====================

tab_chat, tab_insights = st.tabs(["💬 Chat", "📊 Insights"])

# Initialize variables that may not be set on landing page
send_clicked = False
user_input = ""

# ==================== CHAT TAB ====================

with tab_chat:
    # Show landing page if no chat history and not explicitly in chat mode
    if not st.session_state.chat_history and not st.session_state.show_chat:
        # ===== HERO SECTION =====
        render_hero_section()

        # ===== CTA BUTTONS =====
        col1, col2, col3 = st.columns([2, 2, 2])
        with col2:
            if st.button("✨ Start Optimizing", type="primary", use_container_width=True):
                st.session_state.show_chat = True
                st.rerun()

        # ===== STATS BAR =====
        render_stats_bar()

        # ===== FEATURES SECTION =====
        st.markdown("<br>", unsafe_allow_html=True)
        render_features_section()

        # Features Grid - 3 columns
        col1, col2, col3 = st.columns(3)

        with col1:
            render_feature_card(
                "🎯",
                "Smart Detection",
                "Automatically identifies your domain - research, coding, data science - and tailors prompts accordingly."
            )

        with col2:
            render_feature_card(
                "⚡",
                "Instant Optimization",
                "Transform rough ideas into structured, high-quality prompts in seconds with AI-powered analysis."
            )

        with col3:
            render_feature_card(
                "📎",
                "Multi-Modal Input",
                "Upload PDFs, code files, or images. Speak your prompts. LUKTHAN handles it all."
            )

        col4, col5, col6 = st.columns(3)

        with col4:
            render_feature_card(
                "🔬",
                "Research Mode",
                "Specialized templates for literature reviews, methodology design, and academic writing."
            )

        with col5:
            render_feature_card(
                "💻",
                "Code Mode",
                "Generate prompts for debugging, API design, code reviews, and documentation."
            )

        with col6:
            render_feature_card(
                "📊",
                "Quality Metrics",
                "Get detailed insights on clarity, specificity, structure, and completeness scores."
            )

        # ===== FOOTER =====
        render_footer()

    else:
        # ===== CHAT INTERFACE =====
        chat_container = st.container()

        # Display chat history or welcome
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

        # Add spacing before input
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

        # Create the unified input card container
        input_container = st.container()

        with input_container:
            # Unified Input Card CSS with auto-expanding textarea
            st.markdown("""
            <style>
            /* ===== UNIFIED INPUT CARD ===== */
            /* Target the input row container */
            [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) {
                background: linear-gradient(135deg, rgba(10, 15, 31, 0.98) 0%, rgba(5, 8, 22, 0.98) 100%) !important;
                border: 1px solid rgba(0, 229, 255, 0.35) !important;
                border-radius: 28px !important;
                padding: 8px 16px !important;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), 0 0 60px rgba(0, 229, 255, 0.12) !important;
                gap: 8px !important;
                align-items: flex-end !important;
            }

            /* Text area - transparent, no border, auto-height */
            [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-testid="stTextArea"] {
                background: transparent !important;
            }

            [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-testid="stTextArea"] > div {
                background: transparent !important;
                border: none !important;
            }

            [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-testid="stTextArea"] textarea {
                background: transparent !important;
                border: none !important;
                color: #F0F6FC !important;
                padding: 12px 8px !important;
                font-size: 1rem !important;
                min-height: 50px !important;
                max-height: 350px !important;
                height: auto !important;
                resize: none !important;
                overflow-y: auto !important;
                line-height: 1.6 !important;
            }

            [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-testid="stTextArea"] textarea:focus {
                border: none !important;
                box-shadow: none !important;
                outline: none !important;
            }

            [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-testid="stTextArea"] textarea::placeholder {
                color: #6E7681 !important;
            }

            /* Hide the textarea label and character counter */
            [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-testid="stTextArea"] label,
            [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-testid="stTextArea"] .stTextArea-instructions {
                display: none !important;
            }

            /* Action buttons - circular icons, aligned to bottom */
            [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) .stButton > button {
                min-width: 44px !important;
                max-width: 44px !important;
                min-height: 44px !important;
                max-height: 44px !important;
                border-radius: 50% !important;
                padding: 0 !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                font-size: 1.2rem !important;
                margin-bottom: 4px !important;
            }

            /* Popover button (Attach) - subtle style */
            [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) .stPopover button {
                background: rgba(0, 229, 255, 0.1) !important;
                border: 1px solid rgba(0, 229, 255, 0.25) !important;
                box-shadow: none !important;
                min-width: 44px !important;
                max-width: 44px !important;
                min-height: 44px !important;
                max-height: 44px !important;
                border-radius: 50% !important;
                margin-bottom: 4px !important;
            }

            [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) .stPopover button:hover {
                background: rgba(0, 229, 255, 0.2) !important;
                border-color: rgba(0, 229, 255, 0.5) !important;
            }

            /* Secondary buttons (Mic fallback) */
            [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-testid="baseButton-secondary"] {
                background: rgba(0, 229, 255, 0.1) !important;
                border: 1px solid rgba(0, 229, 255, 0.25) !important;
                box-shadow: none !important;
            }

            /* Send button - gradient primary */
            [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-testid="baseButton-primary"] {
                background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%) !important;
                border: none !important;
                box-shadow: 0 0 20px rgba(0, 229, 255, 0.4) !important;
            }

            [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-testid="baseButton-primary"]:hover {
                box-shadow: 0 0 30px rgba(0, 229, 255, 0.6) !important;
                transform: scale(1.05) !important;
            }

            /* File chip styling */
            .file-chip {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                background: linear-gradient(135deg, rgba(0, 229, 255, 0.15) 0%, rgba(155, 92, 255, 0.15) 100%);
                border: 1px solid rgba(0, 229, 255, 0.4);
                border-radius: 20px;
                padding: 6px 14px;
                margin: 4px 0 8px 0;
                font-size: 0.85rem;
                color: #F0F6FC;
            }

            .file-chip .remove-btn {
                cursor: pointer;
                opacity: 0.7;
                transition: opacity 0.2s;
            }

            .file-chip .remove-btn:hover {
                opacity: 1;
            }
            </style>
            """, unsafe_allow_html=True)

            # Show attached file chip
            if st.session_state.uploaded_file_name:
                st.markdown(f"""
                <div style="
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    background: linear-gradient(135deg, rgba(0, 229, 255, 0.15) 0%, rgba(155, 92, 255, 0.15) 100%);
                    border: 1px solid rgba(0, 229, 255, 0.4);
                    border-radius: 20px;
                    padding: 6px 14px;
                    margin: 4px 0 8px 8px;
                    font-size: 0.85rem;
                    color: #F0F6FC;
                ">
                    <span>📎</span>
                    <span>{st.session_state.uploaded_file_name}</span>
                    <span style="cursor: pointer; margin-left: 4px; opacity: 0.7;">✕</span>
                </div>
                """, unsafe_allow_html=True)
                # Hidden button for remove functionality
                if st.button("Remove file", key="remove_file", type="secondary"):
                    st.session_state.uploaded_file_name = None
                    st.session_state.uploaded_file_content = None
                    st.session_state.uploaded_file_type = None
                    st.rerun()

            # Input row - all elements in one line
            col_input, col_attach, col_mic, col_send = st.columns([10, 1, 1, 1])

            # Text area (auto-expanding)
            with col_input:
                default_value = ""
                if st.session_state.pending_input:
                    default_value = st.session_state.pending_input
                    st.session_state.pending_input = None

                user_input = st.text_area(
                    "Message",
                    value=default_value,
                    placeholder="Describe what you need a prompt for...",
                    label_visibility="collapsed",
                    key="main_input",
                    height=68
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

            # Voice input with popover
            with col_mic:
                with st.popover("🎤", use_container_width=True):
                    st.markdown("**🎙️ Voice Input**")
                    st.caption("Click the mic and speak your prompt")
                    audio_data = st.audio_input(
                        "Record your voice",
                        label_visibility="collapsed",
                        key="voice_recorder"
                    )
                    if audio_data:
                        with st.spinner("Transcribing..."):
                            try:
                                from core.file_processor import VoiceProcessor
                                audio_bytes = audio_data.read()
                                transcribed = VoiceProcessor.transcribe_audio_bytes(audio_bytes)
                                if transcribed:
                                    st.success(f"✓ Transcribed!")
                                    st.info(f'"{transcribed[:100]}..."' if len(transcribed) > 100 else f'"{transcribed}"')
                                    if st.button("📝 Use this text", key="use_voice_text"):
                                        st.session_state.pending_input = transcribed
                                        st.rerun()
                                else:
                                    st.warning("Could not transcribe audio. Please try again.")
                            except Exception as e:
                                st.error(f"Error: {str(e)}")

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
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="
            background: rgba(10, 15, 31, 0.8);
            border: 1px solid rgba(0, 229, 255, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
        ">
            <div style="color: #F0F6FC; font-weight: 600; margin-bottom: 1rem;">💡 How it works</div>
            <div style="color: #8B949E; line-height: 2;">
                1. Describe your task in the Chat tab<br>
                2. LUKTHAN analyzes context and domain<br>
                3. Get an optimized, structured prompt<br>
                4. Copy to ChatGPT, Claude, or Gemini
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==================== PROCESS INPUT ====================

if send_clicked and user_input.strip():
    # Prevent duplicate consecutive messages
    is_duplicate = False
    if st.session_state.chat_history:
        last_msg = st.session_state.chat_history[-1]
        if last_msg.get('role') == 'user' and last_msg.get('content') == user_input.strip():
            is_duplicate = True

    if not is_duplicate:
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
