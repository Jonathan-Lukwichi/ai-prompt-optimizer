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
        # Inline fallback CSS
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        * {
            font-family: 'Inter', sans-serif;
        }

        h1, h2, h3 {
            background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 50%, #06B6D4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
        }

        .stButton > button {
            background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(139, 92, 246, 0.3);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(139, 92, 246, 0.5);
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
        background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 50%, #06B6D4 100%);
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
            color: #9CA3AF;
            font-size: 1.125rem;
            margin-top: 0;
        ">{subtitle}</p>
        """, unsafe_allow_html=True)


def glass_card(content: str, padding: str = "2rem"):
    """
    Create a glassmorphism card

    Args:
        content: HTML content inside card
        padding: CSS padding value
    """
    st.markdown(f"""
    <div style="
        background: rgba(26, 27, 61, 0.5);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: {padding};
        transition: all 0.3s ease;
    ">
        {content}
    </div>
    """, unsafe_allow_html=True)


def metric_card(label: str, value: str, icon: str = "📊", color: str = "#8B5CF6"):
    """
    Create a metric card with icon

    Args:
        label: Metric label
        value: Metric value
        icon: Emoji icon
        color: Accent color
    """
    st.markdown(f"""
    <div style="
        background: rgba(26, 27, 61, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    ">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
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
            color: #9CA3AF;
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

    # Determine color based on score
    if score >= 80:
        color = "#10B981"  # Green
    elif score >= 60:
        color = "#F59E0B"  # Yellow
    else:
        color = "#EF4444"  # Red

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': label, 'font': {'color': '#E5E7EB', 'size': 16}},
        number={'font': {'color': color, 'size': 32, 'family': 'Inter'}},
        gauge={
            'axis': {'range': [None, max_score], 'tickcolor': '#9CA3AF'},
            'bar': {'color': color},
            'bgcolor': 'rgba(26, 27, 61, 0.5)',
            'borderwidth': 2,
            'bordercolor': 'rgba(139, 92, 246, 0.3)',
            'steps': [
                {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.2)'},
                {'range': [40, 70], 'color': 'rgba(245, 158, 11, 0.2)'},
                {'range': [70, 100], 'color': 'rgba(16, 185, 129, 0.2)'}
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
        background: rgba(26, 27, 61, 0.6);
        backdrop-filter: blur(20px);
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
                    font-weight: 700;
                ">{label}</h3>
                <p style="
                    margin: 0;
                    color: #9CA3AF;
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


def feature_card(icon: str, title: str, description: str, color: str = "#8B5CF6"):
    """
    Create a feature highlight card

    Args:
        icon: Emoji icon
        title: Feature title
        description: Feature description
        color: Accent color
    """
    st.markdown(f"""
    <div style="
        background: rgba(26, 27, 61, 0.5);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        height: 100%;
        transition: all 0.3s ease;
    " onmouseover="this.style.borderColor='rgba(139, 92, 246, 0.5)'; this.style.transform='translateY(-4px)'"
       onmouseout="this.style.borderColor='rgba(139, 92, 246, 0.2)'; this.style.transform='translateY(0)'">
        <div style="font-size: 2.5rem; margin-bottom: 1rem;">{icon}</div>
        <h3 style="
            color: {color};
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        ">{title}</h3>
        <p style="
            color: #9CA3AF;
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
        "success": ("#10B981", "✅"),
        "warning": ("#F59E0B", "⚠️"),
        "error": ("#EF4444", "❌")
    }

    color, default_icon = colors.get(alert_type, colors["info"])
    display_icon = icon or default_icon

    st.markdown(f"""
    <div style="
        background: rgba(26, 27, 61, 0.8);
        border-left: 4px solid {color};
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        display: flex;
        align-items: center;
    ">
        <span style="font-size: 1.5rem; margin-right: 1rem;">{display_icon}</span>
        <div style="color: #E5E7EB; flex: 1;">{message}</div>
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
            circle_color = "#10B981"
            text_color = "#10B981"
        elif is_current:
            circle_color = "#8B5CF6"
            text_color = "#E5E7EB"
        else:
            circle_color = "#4B5563"
            text_color = "#6B7280"

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

        # Connector line (positioned between circles)
        if i < total_steps - 1:
            line_color = "#10B981" if is_completed else "#4B5563"
            html += f'<div style="flex: 0 0 60px; height: 3px; background: {line_color}; margin-top: 18px; border-radius: 2px;"></div>'

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
        border-bottom: 1px dotted #8B5CF6;
        color: #E5E7EB;
    ">{text}</span>
    """, unsafe_allow_html=True)
