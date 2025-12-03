"""
Reusable UI components for Streamlit app
Professional Dark Blue Theme - Inspired by Wege Design
"""
import streamlit as st
from pathlib import Path
from typing import Optional, List


def load_custom_css():
    """Load custom CSS styling"""
    css_file = Path(__file__).parent.parent / ".streamlit" / "style.css"

    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        # Inline fallback CSS - Professional Dark Blue Theme
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        * {
            font-family: 'Inter', sans-serif;
        }

        /* Clean Professional Headers */
        h1, h2, h3 {
            color: #F0F6FC;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        /* Professional Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.2s ease;
            box-shadow: 0 4px 14px rgba(59, 130, 246, 0.35);
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.45);
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        }

        /* Clean Input Fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background-color: #161B22;
            border: 1px solid #30363D;
            border-radius: 8px;
            color: #F0F6FC;
            transition: all 0.2s ease;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #3B82F6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
        }

        /* Clean Selectbox */
        .stSelectbox > div > div {
            background-color: #161B22;
            border: 1px solid #30363D;
            border-radius: 8px;
        }

        /* Subtle Divider */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, #30363D, transparent);
        }

        /* Professional Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            background-color: #161B22;
            border-radius: 10px;
            padding: 4px;
            border: 1px solid #30363D;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border-radius: 6px;
            color: #8B949E;
            font-weight: 500;
            transition: all 0.2s ease;
        }

        .stTabs [aria-selected="true"] {
            background: #3B82F6;
            color: #FFFFFF;
        }

        /* Clean Expander */
        .streamlit-expanderHeader {
            background-color: #161B22;
            border: 1px solid #30363D;
            border-radius: 8px;
            color: #F0F6FC;
            font-weight: 500;
        }

        /* Metric Cards */
        [data-testid="stMetricValue"] {
            color: #3B82F6;
            font-weight: 700;
        }

        /* Dark Sidebar */
        [data-testid="stSidebar"] {
            background: #0D1117;
            border-right: 1px solid #21262D;
        }

        /* Alert Messages */
        .stSuccess {
            background-color: rgba(34, 197, 94, 0.1);
            border-left: 4px solid #22C55E;
        }

        .stWarning {
            background-color: rgba(234, 179, 8, 0.1);
            border-left: 4px solid #EAB308;
        }

        .stError {
            background-color: rgba(239, 68, 68, 0.1);
            border-left: 4px solid #EF4444;
        }

        /* Minimal Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #0D1117;
        }

        ::-webkit-scrollbar-thumb {
            background: #30363D;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #484F58;
        }
        </style>
        """, unsafe_allow_html=True)


def gradient_header(text: str, size: str = "h1", subtitle: Optional[str] = None):
    """
    Create a clean header with optional subtitle

    Args:
        text: Header text
        size: HTML heading size (h1, h2, h3)
        subtitle: Optional subtitle text
    """
    st.markdown(f"""
    <{size} style="
        color: #F0F6FC;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    ">{text}</{size}>
    """, unsafe_allow_html=True)

    if subtitle:
        st.markdown(f"""
        <p style="
            color: #8B949E;
            font-size: 1.125rem;
            margin-top: 0;
            line-height: 1.6;
        ">{subtitle}</p>
        """, unsafe_allow_html=True)


def glass_card(content: str, padding: str = "2rem"):
    """
    Create a professional card with subtle border

    Args:
        content: HTML content inside card
        padding: CSS padding value
    """
    st.markdown(f"""
    <div style="
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: {padding};
        transition: all 0.2s ease;
    ">
        {content}
    </div>
    """, unsafe_allow_html=True)


def metric_card(label: str, value: str, icon: str = "📊", color: str = "#3B82F6"):
    """
    Create a metric card with icon

    Args:
        label: Metric label
        value: Metric value
        icon: Emoji icon
        color: Accent color (default: electric blue)
    """
    st.markdown(f"""
    <div style="
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.2s ease;
    ">
        <div style="font-size: 2rem; margin-bottom: 0.75rem; opacity: 0.9;">{icon}</div>
        <div style="
            font-size: 2rem;
            font-weight: 700;
            color: {color};
            margin-bottom: 0.25rem;
        ">{value}</div>
        <div style="
            color: #8B949E;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 500;
        ">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def score_gauge(score: int, max_score: int = 100, label: str = "Score", height: int = 150):
    """
    Create a visual score gauge using Plotly

    Args:
        score: Current score value
        max_score: Maximum possible score
        label: Label for the gauge
        height: Height in pixels
    """
    import plotly.graph_objects as go

    # Determine color based on score
    if score >= 80:
        color = "#22C55E"  # Green
    elif score >= 60:
        color = "#EAB308"  # Yellow
    else:
        color = "#EF4444"  # Red

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': label, 'font': {'color': '#F0F6FC', 'size': 16}},
        number={'font': {'color': color, 'size': 32, 'family': 'Inter'}},
        gauge={
            'axis': {'range': [None, max_score], 'tickcolor': '#8B949E'},
            'bar': {'color': color},
            'bgcolor': '#161B22',
            'borderwidth': 2,
            'bordercolor': '#30363D',
            'steps': [
                {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.15)'},
                {'range': [40, 70], 'color': 'rgba(234, 179, 8, 0.15)'},
                {'range': [70, 100], 'color': 'rgba(34, 197, 94, 0.15)'}
            ],
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#F0F6FC', 'family': 'Inter'},
        height=height,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)


def copy_button(text: str, button_text: str = "📋 Copy", key: Optional[str] = None):
    """
    Create a copy-to-clipboard button

    Args:
        text: Text to copy
        button_text: Button label
        key: Unique key for the button
    """
    if st.button(button_text, key=key, use_container_width=False):
        # Show the text in a code block for easy copying
        st.code(text, language=None)
        st.toast("✅ Select and copy the text above", icon="✅")


def version_card(
    label: str,
    prompt: str,
    icon: str,
    color: str,
    description: str,
    key_suffix: str
):
    """
    Create a styled card for a prompt version

    Args:
        label: Version label (e.g., "Basic", "Critical Thinking")
        prompt: The prompt text
        icon: Emoji icon
        color: Accent color
        description: Description of the version
        key_suffix: Unique suffix for component keys
    """
    st.markdown(f"""
    <div style="
        background: #161B22;
        border: 1px solid #30363D;
        border-left: 4px solid {color};
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    ">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <span style="font-size: 1.5rem; margin-right: 0.75rem;">{icon}</span>
            <div>
                <h3 style="
                    margin: 0;
                    color: {color};
                    font-size: 1.25rem;
                    font-weight: 600;
                ">{label}</h3>
                <p style="
                    margin: 0;
                    color: #8B949E;
                    font-size: 0.875rem;
                ">{description}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Show the prompt in a text area
    st.text_area(
        "",
        value=prompt,
        height=200,
        key=f"prompt_{key_suffix}",
        label_visibility="collapsed"
    )

    # Copy button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button(f"📋 Copy", key=f"copy_{key_suffix}", use_container_width=True):
            st.session_state[f"copied_{key_suffix}"] = True
            st.toast(f"✅ {label} version copied!", icon="✅")


def feature_card(icon: str, title: str, description: str, color: str = "#3B82F6"):
    """
    Create a feature highlight card

    Args:
        icon: Emoji icon
        title: Feature title
        description: Feature description
        color: Accent color (default: electric blue)
    """
    st.markdown(f"""
    <div style="
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 1.5rem;
        height: 100%;
        transition: all 0.2s ease;
    " onmouseover="this.style.borderColor='#3B82F6'; this.style.transform='translateY(-2px)'"
       onmouseout="this.style.borderColor='#30363D'; this.style.transform='translateY(0)'">
        <div style="font-size: 2.5rem; margin-bottom: 1rem;">{icon}</div>
        <h3 style="
            color: #F0F6FC;
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        ">{title}</h3>
        <p style="
            color: #8B949E;
            font-size: 0.95rem;
            line-height: 1.6;
            margin: 0;
        ">{description}</p>
    </div>
    """, unsafe_allow_html=True)


def alert_box(message: str, alert_type: str = "info", icon: Optional[str] = None):
    """
    Create a custom alert box

    Args:
        message: Alert message
        alert_type: Type of alert (info, success, warning, error)
        icon: Optional custom icon
    """
    colors = {
        "info": ("#3B82F6", "ℹ️"),
        "success": ("#22C55E", "✅"),
        "warning": ("#EAB308", "⚠️"),
        "error": ("#EF4444", "❌")
    }

    color, default_icon = colors.get(alert_type, colors["info"])
    display_icon = icon or default_icon

    st.markdown(f"""
    <div style="
        background: #161B22;
        border: 1px solid #30363D;
        border-left: 4px solid {color};
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        display: flex;
        align-items: center;
    ">
        <span style="font-size: 1.5rem; margin-right: 1rem;">{display_icon}</span>
        <div style="color: #F0F6FC; flex: 1;">{message}</div>
    </div>
    """, unsafe_allow_html=True)


def progress_steps(steps: List[str], current_step: int):
    """
    Create a visual progress indicator for multi-step workflows

    Args:
        steps: List of step names
        current_step: Current step index (0-based)
    """
    total_steps = len(steps)

    html = '<div style="display: flex; align-items: flex-start; margin: 2rem 0;">'

    for i, step in enumerate(steps):
        # Determine state
        is_current = i == current_step
        is_completed = i < current_step
        is_future = i > current_step

        # Circle color
        if is_completed:
            circle_color = "#22C55E"
            text_color = "#22C55E"
        elif is_current:
            circle_color = "#3B82F6"
            text_color = "#F0F6FC"
        else:
            circle_color = "#30363D"
            text_color = "#8B949E"

        # Step container
        html += f'''
        <div style="text-align: center; flex: 1; position: relative;">
            <div style="width: 40px; height: 40px; border-radius: 50%; background: {circle_color}; color: white; display: flex; align-items: center; justify-content: center; margin: 0 auto 0.5rem; font-weight: 600; font-size: 1rem; position: relative; z-index: 1;">
                {i + 1}
            </div>
            <div style="color: {text_color}; font-size: 0.875rem; font-weight: {'600' if is_current else '400'};">
                {step}
            </div>
        </div>
        '''

        # Connector line
        if i < total_steps - 1:
            line_color = "#22C55E" if is_completed else "#30363D"
            html += f'<div style="flex: 0 0 60px; height: 2px; background: {line_color}; margin-top: 19px; border-radius: 1px;"></div>'

    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def info_tooltip(text: str, tooltip: str):
    """
    Create text with a tooltip

    Args:
        text: Main text to display
        tooltip: Tooltip text on hover
    """
    st.markdown(f"""
    <span title="{tooltip}" style="
        cursor: help;
        border-bottom: 1px dotted #8B949E;
        color: #F0F6FC;
    ">{text}</span>
    """, unsafe_allow_html=True)


# ==================== VOICE INPUT COMPONENT ====================

def voice_input_component(key: str = "voice_input") -> Optional[str]:
    """
    Create a voice input component with recording and transcription

    Args:
        key: Unique key for the component

    Returns:
        Transcribed text if recording was successful, None otherwise
    """
    try:
        from audio_recorder_streamlit import audio_recorder
        import speech_recognition as sr
        import io
        import tempfile
        import os

        # Voice input header
        st.markdown("""
        <div style="
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        ">
            <span style="font-size: 1.25rem;">🎤</span>
            <span style="
                color: #3B82F6;
                font-weight: 600;
                font-size: 0.9rem;
            ">Voice Input</span>
            <span style="
                color: #8B949E;
                font-size: 0.75rem;
            ">(Click to record)</span>
        </div>
        """, unsafe_allow_html=True)

        # Audio recorder
        audio_bytes = audio_recorder(
            text="",
            recording_color="#3B82F6",
            neutral_color="#161B22",
            icon_name="microphone",
            icon_size="2x",
            pause_threshold=2.0,
            sample_rate=16000,
            key=key
        )

        if audio_bytes:
            # Show processing indicator
            with st.spinner("🔄 Transcribing your voice..."):
                try:
                    # Save audio to temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                        tmp_file.write(audio_bytes)
                        tmp_path = tmp_file.name

                    # Use speech recognition
                    recognizer = sr.Recognizer()

                    with sr.AudioFile(tmp_path) as source:
                        audio_data = recognizer.record(source)

                    # Try Google Speech Recognition (free)
                    try:
                        text = recognizer.recognize_google(audio_data)

                        # Show success message
                        st.markdown(f"""
                        <div style="
                            background: rgba(34, 197, 94, 0.1);
                            border: 1px solid rgba(34, 197, 94, 0.3);
                            border-radius: 8px;
                            padding: 1rem;
                            margin-top: 0.5rem;
                        ">
                            <div style="
                                color: #22C55E;
                                font-weight: 600;
                                margin-bottom: 0.5rem;
                                display: flex;
                                align-items: center;
                                gap: 0.5rem;
                            ">
                                <span>✅</span> Voice Captured Successfully!
                            </div>
                            <div style="
                                color: #F0F6FC;
                                font-size: 0.95rem;
                                line-height: 1.5;
                            ">{text}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Cleanup temp file
                        os.unlink(tmp_path)

                        return text

                    except sr.UnknownValueError:
                        st.warning("🎤 Could not understand audio. Please try again and speak clearly.")
                        os.unlink(tmp_path)
                        return None
                    except sr.RequestError as e:
                        st.error(f"🔌 Speech service error: {e}")
                        os.unlink(tmp_path)
                        return None

                except Exception as e:
                    st.error(f"❌ Error processing audio: {str(e)}")
                    return None

        return None

    except ImportError as e:
        # Fallback if audio packages not installed
        st.markdown("""
        <div style="
            background: rgba(234, 179, 8, 0.1);
            border: 1px solid rgba(234, 179, 8, 0.3);
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
        ">
            <div style="color: #EAB308; font-weight: 600; margin-bottom: 0.5rem;">
                🎤 Voice Input Requires Additional Setup
            </div>
            <div style="color: #8B949E; font-size: 0.875rem;">
                Install voice packages: <code style="color: #3B82F6;">pip install audio-recorder-streamlit SpeechRecognition pydub</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return None


def voice_or_text_input(
    label: str = "Enter your prompt",
    placeholder: str = "Type your prompt here or use voice input...",
    height: int = 150,
    key: str = "prompt_input"
) -> str:
    """
    Combined voice and text input component

    Args:
        label: Label for the text area
        placeholder: Placeholder text
        height: Height of text area
        key: Unique key for the component

    Returns:
        The input text (from voice or typing)
    """
    # Initialize session state for voice text
    voice_key = f"{key}_voice_text"
    if voice_key not in st.session_state:
        st.session_state[voice_key] = ""

    # Input mode selector
    st.markdown("""
    <div style="
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    ">
        <div style="
            color: #F0F6FC;
            font-weight: 600;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        ">
            <span>⌨️🎤</span> Choose Input Method
        </div>
    """, unsafe_allow_html=True)

    # Toggle between typing and voice
    input_method = st.radio(
        "Input method:",
        options=["⌨️ Type", "🎤 Speak"],
        horizontal=True,
        key=f"{key}_method",
        label_visibility="collapsed"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Show the appropriate input based on selection
    if input_method == "🎤 Speak":
        # Voice input section
        st.markdown("""
        <div style="
            background: #161B22;
            border: 1px solid #30363D;
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
            text-align: center;
        ">
            <div style="
                color: #3B82F6;
                font-size: 1.1rem;
                font-weight: 600;
                margin-bottom: 1rem;
            ">🎙️ Voice Recording Mode</div>
            <div style="
                color: #8B949E;
                font-size: 0.85rem;
                margin-bottom: 1rem;
            ">Click the microphone button and speak your prompt clearly</div>
        </div>
        """, unsafe_allow_html=True)

        # Center the recorder
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            voice_text = voice_input_component(key=f"{key}_recorder")

            if voice_text:
                st.session_state[voice_key] = voice_text

        # Show text area with voice transcription (editable)
        final_text = st.text_area(
            label,
            value=st.session_state[voice_key],
            placeholder="Your voice will appear here... (you can edit it)",
            height=height,
            key=f"{key}_voice_textarea"
        )

        # Update session state if user edits
        if final_text != st.session_state[voice_key]:
            st.session_state[voice_key] = final_text

        return final_text

    else:
        # Standard text input
        return st.text_area(
            label,
            placeholder=placeholder,
            height=height,
            key=f"{key}_text"
        )
