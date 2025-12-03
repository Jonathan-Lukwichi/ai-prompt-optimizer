"""
Reusable UI components for Streamlit app
Colorful Gradient Theme - Inspired by TECHO Design
Purple, Blue, Orange, Yellow vibrant gradients
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
        # Inline fallback CSS - Colorful Gradient Theme
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        * {
            font-family: 'Inter', sans-serif;
        }

        /* Gradient Headers */
        h1, h2, h3 {
            color: #F8FAFC;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        /* Vibrant Gradient Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 50%, #F97316 100%);
            color: #FFFFFF;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(139, 92, 246, 0.5);
            filter: brightness(1.1);
        }

        /* Gradient Border Input Fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background-color: rgba(26, 16, 37, 0.8);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 12px;
            color: #F8FAFC;
            transition: all 0.3s ease;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #8B5CF6;
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
        }

        /* Gradient Selectbox */
        .stSelectbox > div > div {
            background-color: rgba(26, 16, 37, 0.8);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 12px;
        }

        /* Gradient Divider */
        hr {
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, #8B5CF6, #EC4899, #F97316, transparent);
        }

        /* Colorful Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
            border-radius: 12px;
            padding: 4px;
            border: 1px solid rgba(139, 92, 246, 0.2);
        }

        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border-radius: 8px;
            color: #A78BFA;
            font-weight: 500;
            transition: all 0.3s ease;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
            color: #FFFFFF;
        }

        /* Gradient Expander */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(236, 72, 153, 0.15) 100%);
            border: 1px solid rgba(139, 92, 246, 0.2);
            border-radius: 12px;
            color: #F8FAFC;
            font-weight: 500;
        }

        /* Gradient Metric Cards */
        [data-testid="stMetricValue"] {
            background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 50%, #F97316 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 700;
        }

        /* Gradient Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0F0A1A 0%, #1A1025 50%, #150D20 100%);
            border-right: 1px solid rgba(139, 92, 246, 0.2);
        }

        /* Alert Messages with Gradient */
        .stSuccess {
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(16, 185, 129, 0.15) 100%);
            border-left: 4px solid #22C55E;
        }

        .stWarning {
            background: linear-gradient(135deg, rgba(249, 115, 22, 0.15) 0%, rgba(234, 179, 8, 0.15) 100%);
            border-left: 4px solid #F97316;
        }

        .stError {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(236, 72, 153, 0.15) 100%);
            border-left: 4px solid #EF4444;
        }

        /* Gradient Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: #0F0A1A;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #8B5CF6, #EC4899);
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #A78BFA, #F472B6);
        }
        </style>
        """, unsafe_allow_html=True)


def gradient_header(text: str, size: str = "h1", subtitle: Optional[str] = None):
    """
    Create a gradient text header

    Args:
        text: Header text
        size: HTML heading size (h1, h2, h3)
        subtitle: Optional subtitle text
    """
    st.markdown(f"""
    <{size} style="
        background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 50%, #F97316 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    ">{text}</{size}>
    """, unsafe_allow_html=True)

    if subtitle:
        st.markdown(f"""
        <p style="
            color: #A78BFA;
            font-size: 1.125rem;
            margin-top: 0;
            line-height: 1.6;
        ">{subtitle}</p>
        """, unsafe_allow_html=True)


def glass_card(content: str, padding: str = "2rem"):
    """
    Create a glass card with gradient border

    Args:
        content: HTML content inside card
        padding: CSS padding value
    """
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 16px;
        padding: {padding};
        transition: all 0.3s ease;
    ">
        {content}
    </div>
    """, unsafe_allow_html=True)


def metric_card(label: str, value: str, icon: str = "📊", color: str = "#8B5CF6"):
    """
    Create a metric card with gradient

    Args:
        label: Metric label
        value: Metric value
        icon: Emoji icon
        color: Accent color
    """
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(236, 72, 153, 0.15) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    ">
        <div style="font-size: 2rem; margin-bottom: 0.75rem;">{icon}</div>
        <div style="
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(135deg, {color} 0%, #EC4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.25rem;
        ">{value}</div>
        <div style="
            color: #A78BFA;
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

    # Determine color based on score - Gradient theme
    if score >= 80:
        color = "#22C55E"  # Green
    elif score >= 60:
        color = "#F97316"  # Orange
    else:
        color = "#EF4444"  # Red

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': label, 'font': {'color': '#F8FAFC', 'size': 16}},
        number={'font': {'color': color, 'size': 32, 'family': 'Inter'}},
        gauge={
            'axis': {'range': [None, max_score], 'tickcolor': '#A78BFA'},
            'bar': {'color': color},
            'bgcolor': 'rgba(139, 92, 246, 0.1)',
            'borderwidth': 2,
            'bordercolor': 'rgba(139, 92, 246, 0.3)',
            'steps': [
                {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.2)'},
                {'range': [40, 70], 'color': 'rgba(249, 115, 22, 0.2)'},
                {'range': [70, 100], 'color': 'rgba(34, 197, 94, 0.2)'}
            ],
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#F8FAFC', 'family': 'Inter'},
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
        label: Version label
        prompt: The prompt text
        icon: Emoji icon
        color: Accent color
        description: Description of the version
        key_suffix: Unique suffix for component keys
    """
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-left: 4px solid {color};
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    ">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <span style="font-size: 1.5rem; margin-right: 0.75rem;">{icon}</span>
            <div>
                <h3 style="
                    margin: 0;
                    background: linear-gradient(135deg, {color} 0%, #EC4899 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    font-size: 1.25rem;
                    font-weight: 700;
                ">{label}</h3>
                <p style="
                    margin: 0;
                    color: #A78BFA;
                    font-size: 0.875rem;
                ">{description}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.text_area(
        "",
        value=prompt,
        height=200,
        key=f"prompt_{key_suffix}",
        label_visibility="collapsed"
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button(f"📋 Copy", key=f"copy_{key_suffix}", use_container_width=True):
            st.session_state[f"copied_{key_suffix}"] = True
            st.toast(f"✅ {label} version copied!", icon="✅")


def feature_card(icon: str, title: str, description: str, color: str = "#8B5CF6"):
    """
    Create a feature highlight card with gradient

    Args:
        icon: Emoji icon
        title: Feature title
        description: Feature description
        color: Accent color
    """
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.05) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        height: 100%;
        transition: all 0.3s ease;
    " onmouseover="this.style.borderColor='rgba(236, 72, 153, 0.6)'; this.style.transform='translateY(-4px)'; this.style.boxShadow='0 10px 40px rgba(139, 92, 246, 0.3)'"
       onmouseout="this.style.borderColor='rgba(139, 92, 246, 0.3)'; this.style.transform='translateY(0)'; this.style.boxShadow='none'">
        <div style="font-size: 2.5rem; margin-bottom: 1rem;">{icon}</div>
        <h3 style="
            background: linear-gradient(135deg, {color} 0%, #EC4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        ">{title}</h3>
        <p style="
            color: #C4B5FD;
            font-size: 0.95rem;
            line-height: 1.6;
            margin: 0;
        ">{description}</p>
    </div>
    """, unsafe_allow_html=True)


def alert_box(message: str, alert_type: str = "info", icon: Optional[str] = None):
    """
    Create a custom alert box with gradient

    Args:
        message: Alert message
        alert_type: Type of alert (info, success, warning, error)
        icon: Optional custom icon
    """
    colors = {
        "info": ("#8B5CF6", "ℹ️", "rgba(139, 92, 246, 0.15)"),
        "success": ("#22C55E", "✅", "rgba(34, 197, 94, 0.15)"),
        "warning": ("#F97316", "⚠️", "rgba(249, 115, 22, 0.15)"),
        "error": ("#EF4444", "❌", "rgba(239, 68, 68, 0.15)")
    }

    color, default_icon, bg = colors.get(alert_type, colors["info"])
    display_icon = icon or default_icon

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {bg} 0%, rgba(236, 72, 153, 0.1) 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-left: 4px solid {color};
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        display: flex;
        align-items: center;
    ">
        <span style="font-size: 1.5rem; margin-right: 1rem;">{display_icon}</span>
        <div style="color: #F8FAFC; flex: 1;">{message}</div>
    </div>
    """, unsafe_allow_html=True)


def progress_steps(steps: List[str], current_step: int):
    """
    Create a visual progress indicator with gradient

    Args:
        steps: List of step names
        current_step: Current step index (0-based)
    """
    total_steps = len(steps)

    # Define gradient colors for steps
    step_colors = ["#8B5CF6", "#A855F7", "#EC4899", "#F97316"]

    html = '<div style="display: flex; align-items: flex-start; margin: 2rem 0;">'

    for i, step in enumerate(steps):
        is_current = i == current_step
        is_completed = i < current_step
        is_future = i > current_step

        if is_completed:
            circle_color = "#22C55E"
            text_color = "#22C55E"
        elif is_current:
            circle_color = step_colors[i % len(step_colors)]
            text_color = "#F8FAFC"
        else:
            circle_color = "rgba(139, 92, 246, 0.3)"
            text_color = "#A78BFA"

        box_shadow = f"box-shadow: 0 0 20px {circle_color}60;" if is_current else ""

        html += f'''
        <div style="text-align: center; flex: 1; position: relative;">
            <div style="width: 44px; height: 44px; border-radius: 50%; background: {circle_color}; color: white; display: flex; align-items: center; justify-content: center; margin: 0 auto 0.5rem; font-weight: 700; font-size: 1rem; position: relative; z-index: 1; {box_shadow}">
                {i + 1}
            </div>
            <div style="color: {text_color}; font-size: 0.875rem; font-weight: {'600' if is_current else '400'};">
                {step}
            </div>
        </div>
        '''

        if i < total_steps - 1:
            line_color = "#22C55E" if is_completed else "rgba(139, 92, 246, 0.3)"
            html += f'<div style="flex: 0 0 60px; height: 3px; background: {line_color}; margin-top: 20px; border-radius: 2px;"></div>'

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
        border-bottom: 1px dotted #A78BFA;
        color: #F8FAFC;
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

        # Voice input header with gradient
        st.markdown("""
        <div style="
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        ">
            <span style="font-size: 1.25rem;">🎤</span>
            <span style="
                background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: 600;
                font-size: 0.9rem;
            ">Voice Input</span>
            <span style="
                color: #A78BFA;
                font-size: 0.75rem;
            ">(Click to record)</span>
        </div>
        """, unsafe_allow_html=True)

        audio_bytes = audio_recorder(
            text="",
            recording_color="#EC4899",
            neutral_color="#1A1025",
            icon_name="microphone",
            icon_size="2x",
            pause_threshold=2.0,
            sample_rate=16000,
            key=key
        )

        if audio_bytes:
            with st.spinner("🔄 Transcribing your voice..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                        tmp_file.write(audio_bytes)
                        tmp_path = tmp_file.name

                    recognizer = sr.Recognizer()

                    with sr.AudioFile(tmp_path) as source:
                        audio_data = recognizer.record(source)

                    try:
                        text = recognizer.recognize_google(audio_data)

                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(16, 185, 129, 0.15) 100%);
                            border: 1px solid rgba(34, 197, 94, 0.4);
                            border-radius: 12px;
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
                                color: #F8FAFC;
                                font-size: 0.95rem;
                                line-height: 1.5;
                            ">{text}</div>
                        </div>
                        """, unsafe_allow_html=True)

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
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(249, 115, 22, 0.15) 0%, rgba(234, 179, 8, 0.15) 100%);
            border: 1px solid rgba(249, 115, 22, 0.4);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
        ">
            <div style="color: #F97316; font-weight: 600; margin-bottom: 0.5rem;">
                🎤 Voice Input Requires Additional Setup
            </div>
            <div style="color: #C4B5FD; font-size: 0.875rem;">
                Install voice packages: <code style="color: #EC4899;">pip install audio-recorder-streamlit SpeechRecognition pydub</code>
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
    voice_key = f"{key}_voice_text"
    if voice_key not in st.session_state:
        st.session_state[voice_key] = ""

    # Input mode selector with gradient
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(236, 72, 153, 0.1) 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    ">
        <div style="
            background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 600;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        ">
            <span style="-webkit-text-fill-color: initial;">⌨️🎤</span> Choose Input Method
        </div>
    """, unsafe_allow_html=True)

    input_method = st.radio(
        "Input method:",
        options=["⌨️ Type", "🎤 Speak"],
        horizontal=True,
        key=f"{key}_method",
        label_visibility="collapsed"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if input_method == "🎤 Speak":
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(236, 72, 153, 0.1) 0%, rgba(249, 115, 22, 0.1) 100%);
            border: 1px solid rgba(236, 72, 153, 0.3);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            text-align: center;
        ">
            <div style="
                background: linear-gradient(135deg, #EC4899 0%, #F97316 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 1.1rem;
                font-weight: 600;
                margin-bottom: 1rem;
            ">🎙️ Voice Recording Mode</div>
            <div style="
                color: #C4B5FD;
                font-size: 0.85rem;
                margin-bottom: 1rem;
            ">Click the microphone button and speak your prompt clearly</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            voice_text = voice_input_component(key=f"{key}_recorder")

            if voice_text:
                st.session_state[voice_key] = voice_text

        final_text = st.text_area(
            label,
            value=st.session_state[voice_key],
            placeholder="Your voice will appear here... (you can edit it)",
            height=height,
            key=f"{key}_voice_textarea"
        )

        if final_text != st.session_state[voice_key]:
            st.session_state[voice_key] = final_text

        return final_text

    else:
        return st.text_area(
            label,
            placeholder=placeholder,
            height=height,
            key=f"{key}_text"
        )
