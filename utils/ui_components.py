"""
Reusable UI components for Streamlit app
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
        # Inline fallback CSS - Neon Green/Blue Fluorescent Theme
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        * {
            font-family: 'Inter', sans-serif;
        }

        /* Neon/Fluorescent Headers */
        h1, h2, h3 {
            background: linear-gradient(135deg, #00FF9F 0%, #00D9FF 50%, #0099FF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
            text-shadow: 0 0 30px rgba(0, 255, 159, 0.3);
        }

        /* Glowing Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #00FF9F 0%, #00D9FF 100%);
            color: #0A1929;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 700;
            transition: all 0.3s ease;
            box-shadow: 0 4px 25px rgba(0, 255, 159, 0.4), 0 0 15px rgba(0, 217, 255, 0.3);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 35px rgba(0, 255, 159, 0.6), 0 0 25px rgba(0, 217, 255, 0.5);
            filter: brightness(1.1);
        }

        /* Fluorescent Input Fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background-color: rgba(19, 47, 76, 0.5);
            border: 1px solid rgba(0, 255, 159, 0.3);
            border-radius: 8px;
            color: #E7F5FF;
            transition: all 0.3s ease;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #00FF9F;
            box-shadow: 0 0 15px rgba(0, 255, 159, 0.4);
        }

        /* Neon Selectbox */
        .stSelectbox > div > div {
            background-color: rgba(19, 47, 76, 0.5);
            border: 1px solid rgba(0, 255, 159, 0.3);
            border-radius: 8px;
        }

        /* Glowing Divider */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, #00FF9F, #00D9FF, transparent);
            box-shadow: 0 0 10px rgba(0, 255, 159, 0.3);
        }

        /* Fluorescent Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(19, 47, 76, 0.3);
            border-radius: 12px;
            padding: 4px;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border-radius: 8px;
            color: #7DD3C0;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #00FF9F 0%, #00D9FF 100%);
            color: #0A1929;
            box-shadow: 0 0 15px rgba(0, 255, 159, 0.4);
        }

        /* Neon Expander */
        .streamlit-expanderHeader {
            background-color: rgba(19, 47, 76, 0.4);
            border: 1px solid rgba(0, 255, 159, 0.2);
            border-radius: 8px;
            color: #00FF9F;
            font-weight: 600;
        }

        /* Glowing Metric Cards */
        [data-testid="stMetricValue"] {
            background: linear-gradient(135deg, #00FF9F 0%, #00D9FF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
        }

        /* Sidebar Glow */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0A1929 0%, #132F4C 100%);
            border-right: 1px solid rgba(0, 255, 159, 0.2);
        }

        /* Success/Warning/Error Messages with Neon */
        .stSuccess {
            background-color: rgba(0, 255, 159, 0.1);
            border-left: 4px solid #00FF9F;
            box-shadow: 0 0 10px rgba(0, 255, 159, 0.2);
        }

        .stWarning {
            background-color: rgba(255, 215, 0, 0.1);
            border-left: 4px solid #FFD700;
            box-shadow: 0 0 10px rgba(255, 215, 0, 0.2);
        }

        .stError {
            background-color: rgba(255, 69, 58, 0.1);
            border-left: 4px solid #FF453A;
            box-shadow: 0 0 10px rgba(255, 69, 58, 0.2);
        }

        /* Scrollbar Glow */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: #0A1929;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #00FF9F, #00D9FF);
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 255, 159, 0.5);
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #00D9FF, #00FF9F);
        }
        </style>
        """, unsafe_allow_html=True)


def gradient_header(text: str, size: str = "h1", subtitle: Optional[str] = None):
    """
    Create a gradient text header with neon glow

    Args:
        text: Header text
        size: HTML heading size (h1, h2, h3)
        subtitle: Optional subtitle text
    """
    st.markdown(f"""
    <{size} style="
        background: linear-gradient(135deg, #00FF9F 0%, #00D9FF 50%, #0099FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
        filter: drop-shadow(0 0 20px rgba(0, 255, 159, 0.4));
    ">{text}</{size}>
    """, unsafe_allow_html=True)

    if subtitle:
        st.markdown(f"""
        <p style="
            color: #7DD3C0;
            font-size: 1.125rem;
            margin-top: 0;
        ">{subtitle}</p>
        """, unsafe_allow_html=True)


def glass_card(content: str, padding: str = "2rem"):
    """
    Create a glassmorphism card with neon border

    Args:
        content: HTML content inside card
        padding: CSS padding value
    """
    st.markdown(f"""
    <div style="
        background: rgba(19, 47, 76, 0.4);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 255, 159, 0.3);
        border-radius: 16px;
        padding: {padding};
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(0, 255, 159, 0.1);
    ">
        {content}
    </div>
    """, unsafe_allow_html=True)


def metric_card(label: str, value: str, icon: str = "📊", color: str = "#00FF9F"):
    """
    Create a metric card with icon and neon glow

    Args:
        label: Metric label
        value: Metric value
        icon: Emoji icon
        color: Accent color (default: neon green)
    """
    st.markdown(f"""
    <div style="
        background: rgba(19, 47, 76, 0.5);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 255, 159, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(0, 255, 159, 0.15);
    ">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <div style="
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(135deg, {color} 0%, #00D9FF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.25rem;
            filter: drop-shadow(0 0 10px rgba(0, 255, 159, 0.4));
        ">{value}</div>
        <div style="
            color: #7DD3C0;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
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

    # Determine color based on score - Neon theme
    if score >= 80:
        color = "#00FF9F"  # Neon Green
    elif score >= 60:
        color = "#FFD700"  # Gold
    else:
        color = "#FF453A"  # Neon Red

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': label, 'font': {'color': '#E7F5FF', 'size': 16}},
        number={'font': {'color': color, 'size': 32, 'family': 'Inter'}},
        gauge={
            'axis': {'range': [None, max_score], 'tickcolor': '#7DD3C0'},
            'bar': {'color': color},
            'bgcolor': 'rgba(19, 47, 76, 0.5)',
            'borderwidth': 2,
            'bordercolor': 'rgba(0, 255, 159, 0.4)',
            'steps': [
                {'range': [0, 40], 'color': 'rgba(255, 69, 58, 0.2)'},
                {'range': [40, 70], 'color': 'rgba(255, 215, 0, 0.2)'},
                {'range': [70, 100], 'color': 'rgba(0, 255, 159, 0.2)'}
            ],
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#E5E7EB', 'family': 'Inter'},
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
        background: rgba(19, 47, 76, 0.5);
        backdrop-filter: blur(20px);
        border-left: 4px solid {color};
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 0 15px rgba(0, 255, 159, 0.1);
    ">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <span style="font-size: 1.5rem; margin-right: 0.75rem;">{icon}</span>
            <div>
                <h3 style="
                    margin: 0;
                    color: {color};
                    font-size: 1.25rem;
                    font-weight: 700;
                    text-shadow: 0 0 10px {color}40;
                ">{label}</h3>
                <p style="
                    margin: 0;
                    color: #7DD3C0;
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


def feature_card(icon: str, title: str, description: str, color: str = "#00FF9F"):
    """
    Create a feature highlight card with neon glow

    Args:
        icon: Emoji icon
        title: Feature title
        description: Feature description
        color: Accent color (default: neon green)
    """
    st.markdown(f"""
    <div style="
        background: rgba(19, 47, 76, 0.4);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 255, 159, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        height: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(0, 255, 159, 0.1);
    " onmouseover="this.style.borderColor='rgba(0, 255, 159, 0.6)'; this.style.transform='translateY(-4px)'; this.style.boxShadow='0 0 30px rgba(0, 255, 159, 0.3)'"
       onmouseout="this.style.borderColor='rgba(0, 255, 159, 0.3)'; this.style.transform='translateY(0)'; this.style.boxShadow='0 0 15px rgba(0, 255, 159, 0.1)'">
        <div style="font-size: 2.5rem; margin-bottom: 1rem;">{icon}</div>
        <h3 style="
            color: {color};
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 0 0 15px {color}40;
        ">{title}</h3>
        <p style="
            color: #7DD3C0;
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
        "info": ("#00D9FF", "ℹ️"),
        "success": ("#00FF9F", "✅"),
        "warning": ("#FFD700", "⚠️"),
        "error": ("#FF453A", "❌")
    }

    color, default_icon = colors.get(alert_type, colors["info"])
    display_icon = icon or default_icon

    st.markdown(f"""
    <div style="
        background: rgba(19, 47, 76, 0.7);
        border-left: 4px solid {color};
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        display: flex;
        align-items: center;
        box-shadow: 0 0 15px {color}30;
    ">
        <span style="font-size: 1.5rem; margin-right: 1rem;">{display_icon}</span>
        <div style="color: #E7F5FF; flex: 1;">{message}</div>
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

        # Circle color - Neon theme
        if is_completed:
            circle_color = "#00FF9F"
            text_color = "#00FF9F"
        elif is_current:
            circle_color = "#00D9FF"
            text_color = "#E7F5FF"
        else:
            circle_color = "#2D5F7C"
            text_color = "#5A8BA8"

        # Build box-shadow style if current
        box_shadow_style = f"box-shadow: 0 0 20px {circle_color};" if is_current else ""

        # Step container
        html += f'''
        <div style="text-align: center; flex: 1; position: relative;">
            <div style="width: 40px; height: 40px; border-radius: 50%; background: {circle_color}; color: white; display: flex; align-items: center; justify-content: center; margin: 0 auto 0.5rem; font-weight: 700; font-size: 1.1rem; {box_shadow_style} position: relative; z-index: 1;">
                {i + 1}
            </div>
            <div style="color: {text_color}; font-size: 0.875rem; font-weight: {"700" if is_current else "500"};">
                {step}
            </div>
        </div>
        '''

        # Connector line (positioned between circles) - Neon theme
        if i < total_steps - 1:
            line_color = "#00FF9F" if is_completed else "#2D5F7C"
            html += f'<div style="flex: 0 0 60px; height: 3px; background: {line_color}; margin-top: 18px; border-radius: 2px; box-shadow: 0 0 5px {line_color};"></div>'

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
        border-bottom: 1px dotted #00FF9F;
        color: #E7F5FF;
        text-shadow: 0 0 5px rgba(0, 255, 159, 0.2);
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

        # Voice input header with neon styling
        st.markdown("""
        <div style="
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        ">
            <span style="font-size: 1.25rem;">🎤</span>
            <span style="
                color: #00FF9F;
                font-weight: 600;
                font-size: 0.9rem;
            ">Voice Input</span>
            <span style="
                color: #7DD3C0;
                font-size: 0.75rem;
            ">(Click to record)</span>
        </div>
        """, unsafe_allow_html=True)

        # Audio recorder with custom styling
        audio_bytes = audio_recorder(
            text="",
            recording_color="#00FF9F",
            neutral_color="#132F4C",
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
                            background: rgba(0, 255, 159, 0.1);
                            border: 1px solid rgba(0, 255, 159, 0.4);
                            border-radius: 12px;
                            padding: 1rem;
                            margin-top: 0.5rem;
                            box-shadow: 0 0 15px rgba(0, 255, 159, 0.2);
                        ">
                            <div style="
                                color: #00FF9F;
                                font-weight: 600;
                                margin-bottom: 0.5rem;
                                display: flex;
                                align-items: center;
                                gap: 0.5rem;
                            ">
                                <span>✅</span> Voice Captured Successfully!
                            </div>
                            <div style="
                                color: #E7F5FF;
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
            background: rgba(255, 215, 0, 0.1);
            border: 1px solid rgba(255, 215, 0, 0.3);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
        ">
            <div style="color: #FFD700; font-weight: 600; margin-bottom: 0.5rem;">
                🎤 Voice Input Requires Additional Setup
            </div>
            <div style="color: #7DD3C0; font-size: 0.875rem;">
                Install voice packages: <code style="color: #00FF9F;">pip install audio-recorder-streamlit SpeechRecognition pydub</code>
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

    # Input mode selector with neon styling
    st.markdown("""
    <div style="
        background: rgba(19, 47, 76, 0.4);
        border: 1px solid rgba(0, 255, 159, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 0 15px rgba(0, 255, 159, 0.1);
    ">
        <div style="
            color: #00FF9F;
            font-weight: 700;
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
            background: rgba(19, 47, 76, 0.3);
            border: 1px solid rgba(0, 217, 255, 0.3);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            text-align: center;
        ">
            <div style="
                color: #00D9FF;
                font-size: 1.1rem;
                font-weight: 600;
                margin-bottom: 1rem;
            ">🎙️ Voice Recording Mode</div>
            <div style="
                color: #7DD3C0;
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
