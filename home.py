"""
AI Prompt Optimizer for Academia
Main application entry point
"""
import streamlit as st
from core.config import Config
from utils.ui_components import load_custom_css, gradient_header, feature_card, metric_card, glass_card
from core.database import DatabaseManager
from datetime import datetime

# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="AI Prompt Optimizer | Academic Research Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/ai-prompt-optimizer',
        'Report a bug': 'https://github.com/yourusername/ai-prompt-optimizer/issues',
        'About': '# AI Prompt Optimizer\nOptimize your prompts for better AI interactions in academic research.'
    }
)

# Load custom CSS
load_custom_css()

# ==================== SESSION STATE ====================

if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_field' not in st.session_state:
    st.session_state.user_field = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Guest"

# ==================== SIDEBAR ====================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎓</div>
        <h2 style="
            background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0;
            font-size: 1.5rem;
        ">AI Prompt Optimizer</h2>
        <p style="color: #9CA3AF; font-size: 0.875rem; margin-top: 0.25rem;">
            For Academic Excellence
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # User profile section
    st.markdown("### 👤 Your Profile")

    user_name = st.text_input(
        "Name",
        value=st.session_state.user_name,
        placeholder="Enter your name",
        key="sidebar_name"
    )
    if user_name:
        st.session_state.user_name = user_name

    role = st.selectbox(
        "Academic Role",
        options=list(Config.ACADEMIC_ROLES.keys()),
        format_func=lambda x: Config.ACADEMIC_ROLES[x],
        key="sidebar_role",
        index=2 if st.session_state.user_role is None else list(Config.ACADEMIC_ROLES.keys()).index(st.session_state.user_role)
    )
    st.session_state.user_role = role

    field = st.text_input(
        "Field of Study",
        value=st.session_state.user_field or "",
        placeholder="e.g., Computer Science, Biology",
        key="sidebar_field"
    )
    if field:
        st.session_state.user_field = field

    st.divider()

    # Quick stats
    st.markdown("### 📊 Quick Stats")

    # Placeholder stats - in production, fetch from database
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Sessions", "0", delta=None)
    with col2:
        st.metric("Prompts", "0", delta=None)

    st.divider()

    # Quick links
    st.markdown("### 🔗 Quick Links")

    if st.button("🎯 Prompt Lab", use_container_width=True, type="primary"):
        st.switch_page("pages/1_🎯_Prompt_Lab.py")

    if st.button("📚 Templates", use_container_width=True):
        st.switch_page("pages/2_📚_Templates.py")

    if st.button("🔬 Workflows", use_container_width=True):
        st.switch_page("pages/3_🔬_Workflows.py")

    if st.button("📊 History", use_container_width=True):
        st.switch_page("pages/4_📊_History.py")

    st.divider()

    # Footer
    st.markdown("""
    <div style="text-align: center; color: #6B7280; font-size: 0.75rem; margin-top: 2rem;">
        Made with ❤️ for researchers<br>
        v1.0.0 Beta
    </div>
    """, unsafe_allow_html=True)


# ==================== MAIN CONTENT ====================

# Hero Section
st.markdown("""
<div style="text-align: center; padding: 3rem 0 2rem;">
    <h1 style="
        font-size: 3.5rem;
        background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 50%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 1rem;
        line-height: 1.2;
    ">
        Optimize Your AI Prompts<br>for Academic Excellence
    </h1>
    <p style="
        font-size: 1.25rem;
        color: #9CA3AF;
        max-width: 700px;
        margin: 0 auto 2rem;
        line-height: 1.6;
    ">
        Transform vague questions into powerful prompts that get you better results
        from ChatGPT, Claude, and other AI assistants.
    </p>
</div>
""", unsafe_allow_html=True)

# CTA Buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    cta_col1, cta_col2 = st.columns(2)
    with cta_col1:
        if st.button("🚀 Start Optimizing", use_container_width=True, type="primary"):
            st.switch_page("pages/1_🎯_Prompt_Lab.py")
    with cta_col2:
        if st.button("📚 Browse Templates", use_container_width=True):
            st.switch_page("pages/2_📚_Templates.py")

st.markdown("<br><br>", unsafe_allow_html=True)

# ==================== QUICK OPTIMIZE SECTION (NEW!) ====================

st.markdown("""
<div style="text-align: center; margin: 2rem 0 1.5rem;">
    <h2 style="
        font-size: 2.5rem;
        background: linear-gradient(135deg, #10B981 0%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    ">⚡ Quick Optimize</h2>
    <p style="color: #9CA3AF; font-size: 1rem; margin-top: 0.5rem;">
        Paste any prompt, get it optimized in seconds. No dropdowns, no decisions.
    </p>
</div>
""", unsafe_allow_html=True)

# Quick Optimize UI
quick_col1, quick_col2 = st.columns([4, 1])

with quick_col1:
    quick_prompt = st.text_area(
        "Your prompt",
        placeholder="Example: Explain machine learning to me\n\nPaste any prompt here and we'll automatically detect the context and optimize it for you!",
        height=120,
        key="quick_prompt_input",
        label_visibility="collapsed"
    )

with quick_col2:
    st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
    optimize_button = st.button(
        "🚀 Optimize Now",
        use_container_width=True,
        type="primary",
        key="quick_optimize_btn"
    )

    if quick_prompt:
        st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
        if st.button(
            "⚙️ Advanced",
            use_container_width=True,
            key="advanced_mode_btn",
            help="Go to Prompt Lab for full control"
        ):
            st.session_state.prefill_prompt = quick_prompt
            st.switch_page("pages/1_🎯_Prompt_Lab.py")

# Process optimization
if optimize_button and quick_prompt:
    with st.spinner("🤖 Analyzing and optimizing..."):
        try:
            from core.prompt_engine import PromptEngine

            # Initialize engine
            engine = PromptEngine()

            # Smart optimize
            result = engine.smart_optimize(quick_prompt)

            # Store in session state
            st.session_state.quick_result = result

        except Exception as e:
            st.error(f"Oops! Something went wrong: {str(e)}")
            st.session_state.quick_result = None

# Display result
if 'quick_result' in st.session_state and st.session_state.quick_result:
    result = st.session_state.quick_result

    st.markdown("<br>", unsafe_allow_html=True)

    # Success banner
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(6, 182, 212, 0.2) 100%);
        border: 2px solid #10B981;
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    ">
        <div style="
            font-size: 2.5rem;
            flex-shrink: 0;
        ">✅</div>
        <div style="flex: 1;">
            <div style="
                font-size: 1.3rem;
                font-weight: 700;
                background: linear-gradient(135deg, #10B981 0%, #06B6D4 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 0.25rem;
            ">Optimized!</div>
            <div style="color: #9CA3AF; font-size: 0.95rem;">
                +{result['improvement']} quality points improvement •
                Detected: {result['detection']['domain'].replace('-', ' ').replace('_', ' ').title()} •
                Best version: {result['best_version_key'].title()}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Optimized prompt display
    st.markdown("""
    <div style="
        background: rgba(26, 27, 61, 0.6);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    ">
        <div style="
            color: #10B981;
            font-weight: 700;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 1rem;
        ">✨ Your Optimized Prompt</div>
    """, unsafe_allow_html=True)

    st.code(result['best_version'], language=None)

    st.markdown("</div>", unsafe_allow_html=True)

    # Action buttons
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)

    with action_col1:
        st.button("📋 Copy to Clipboard", use_container_width=True, key="copy_result")

    with action_col2:
        if st.button("👀 Show All 4 Versions", use_container_width=True, key="show_all_versions"):
            st.session_state.show_alternatives = True

    with action_col3:
        if st.button("🔬 Test & Compare", use_container_width=True, key="test_quick_result"):
            # Prepare data for Test & Compare page
            st.session_state.optimization_result = {
                'raw_prompt': result['raw_prompt'],
                'optimized': result['optimized'],
                'analysis': result['analysis']
            }
            st.switch_page("pages/5_🔬_Test_Compare.py")

    with action_col4:
        if st.button("🎯 Full Lab", use_container_width=True, key="goto_full_lab"):
            st.session_state.prefill_prompt = quick_prompt
            st.switch_page("pages/1_🎯_Prompt_Lab.py")

    # Show all versions if requested
    if st.session_state.get('show_alternatives', False):
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="
            font-size: 1.1rem;
            font-weight: 700;
            color: #E5E7EB;
            margin-bottom: 1rem;
        ">📚 All 4 Optimized Versions</div>
        """, unsafe_allow_html=True)

        # Get version labels for display
        version_labels = {
            'basic': {'name': 'Basic', 'icon': '📝', 'color': '#3B82F6'},
            'critical': {'name': 'Critical Thinking', 'icon': '🧠', 'color': '#8B5CF6'},
            'tutor': {'name': 'Tutor Mode', 'icon': '👨‍🏫', 'color': '#EC4899'},
            'safe': {'name': 'Safe Mode', 'icon': '🛡️', 'color': '#10B981'}
        }

        for ver_key, ver_text in result['all_versions'].items():
            ver_info = version_labels.get(ver_key, {'name': ver_key.title(), 'icon': '📄', 'color': '#6B7280'})

            with st.expander(f"{ver_info['icon']} {ver_info['name']}", expanded=(ver_key == result['best_version_key'])):
                st.code(ver_text, language=None)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== FEATURES SECTION ====================

st.markdown("""
<div style="text-align: center; margin: 4rem 0 2rem;">
    <h2 style="
        font-size: 2.5rem;
        background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
    ">Why Use Our Optimizer?</h2>
    <p style="color: #9CA3AF; font-size: 1.1rem; margin-top: 0.5rem;">
        Built specifically for academic research and education
    </p>
</div>
""", unsafe_allow_html=True)

# Feature cards
col1, col2, col3 = st.columns(3)

with col1:
    feature_card(
        icon="🎯",
        title="4 Optimized Versions",
        description="Get Basic, Critical-Thinking, Tutor, and Safe versions of every prompt - each tailored for different academic needs.",
        color="#8B5CF6"
    )

with col2:
    feature_card(
        icon="🛡️",
        title="Prevent Hallucinations",
        description="Our Safe Mode explicitly instructs AI to acknowledge uncertainty and avoid making up citations or data.",
        color="#3B82F6"
    )

with col3:
    feature_card(
        icon="📊",
        title="Quality Scoring",
        description="Instant feedback on prompt clarity and safety with actionable suggestions for improvement.",
        color="#10B981"
    )

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    feature_card(
        icon="👨‍🏫",
        title="Tutor Mode",
        description="Transform AI into a Socratic teacher that guides you through reasoning rather than just giving answers.",
        color="#EC4899"
    )

with col2:
    feature_card(
        icon="📚",
        title="Ready-Made Templates",
        description="Pre-built templates for literature reviews, paper summaries, methodology design, and more.",
        color="#06B6D4"
    )

with col3:
    feature_card(
        icon="🔬",
        title="Multi-Step Workflows",
        description="Complete workflows for complex tasks like conducting literature reviews or writing research papers.",
        color="#F59E0B"
    )

# ==================== HOW IT WORKS ====================

st.markdown("""
<div style="text-align: center; margin: 4rem 0 2rem;">
    <h2 style="
        font-size: 2.5rem;
        background: linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
    ">How It Works</h2>
</div>
""", unsafe_allow_html=True)

# Steps
step_col1, step_col2, step_col3, step_col4 = st.columns(4)

with step_col1:
    st.markdown("""
    <div style="
        text-align: center;
        background: rgba(26, 27, 61, 0.5);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 2rem 1rem;
    ">
        <div style="
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem;
            font-weight: 800;
            font-size: 1.5rem;
        ">1</div>
        <h3 style="color: #E5E7EB; font-size: 1.1rem; margin-bottom: 0.5rem;">Select Your Role</h3>
        <p style="color: #9CA3AF; font-size: 0.9rem; margin: 0;">
            Choose your academic level and task type
        </p>
    </div>
    """, unsafe_allow_html=True)

with step_col2:
    st.markdown("""
    <div style="
        text-align: center;
        background: rgba(26, 27, 61, 0.5);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 2rem 1rem;
    ">
        <div style="
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem;
            font-weight: 800;
            font-size: 1.5rem;
        ">2</div>
        <h3 style="color: #E5E7EB; font-size: 1.1rem; margin-bottom: 0.5rem;">Enter Your Prompt</h3>
        <p style="color: #9CA3AF; font-size: 0.9rem; margin: 0;">
            Paste your question or request
        </p>
    </div>
    """, unsafe_allow_html=True)

with step_col3:
    st.markdown("""
    <div style="
        text-align: center;
        background: rgba(26, 27, 61, 0.5);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 2rem 1rem;
    ">
        <div style="
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #10B981 0%, #06B6D4 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem;
            font-weight: 800;
            font-size: 1.5rem;
        ">3</div>
        <h3 style="color: #E5E7EB; font-size: 1.1rem; margin-bottom: 0.5rem;">Get Analysis</h3>
        <p style="color: #9CA3AF; font-size: 0.9rem; margin: 0;">
            See quality scores and improvement tips
        </p>
    </div>
    """, unsafe_allow_html=True)

with step_col4:
    st.markdown("""
    <div style="
        text-align: center;
        background: rgba(26, 27, 61, 0.5);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 2rem 1rem;
    ">
        <div style="
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #EC4899 0%, #F59E0B 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem;
            font-weight: 800;
            font-size: 1.5rem;
        ">4</div>
        <h3 style="color: #E5E7EB; font-size: 1.1rem; margin-bottom: 0.5rem;">Use Optimized Version</h3>
        <p style="color: #9CA3AF; font-size: 0.9rem; margin: 0;">
            Copy and use with any AI tool
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==================== USE CASES ====================

st.markdown("""
<div style="text-align: center; margin: 4rem 0 2rem;">
    <h2 style="
        font-size: 2.5rem;
        background: linear-gradient(135deg, #EC4899 0%, #F59E0B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
    ">Perfect For...</h2>
</div>
""", unsafe_allow_html=True)

use_case_col1, use_case_col2 = st.columns(2)

with use_case_col1:
    st.markdown("""
    <div style="
        background: rgba(26, 27, 61, 0.5);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1rem;
    ">
        <h3 style="color: #8B5CF6; margin-bottom: 1rem;">📖 Literature Reviews</h3>
        <p style="color: #9CA3AF; line-height: 1.6; margin: 0;">
            Get help finding papers, identifying themes, and synthesizing findings without
            worrying about hallucinated citations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background: rgba(26, 27, 61, 0.5);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1rem;
    ">
        <h3 style="color: #3B82F6; margin-bottom: 1rem;">✍️ Academic Writing</h3>
        <p style="color: #9CA3AF; line-height: 1.6; margin: 0;">
            Get writing support that helps you learn and improve, not ghostwriting that
            undermines your integrity.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background: rgba(26, 27, 61, 0.5);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 2rem;
    ">
        <h3 style="color: #10B981; margin-bottom: 1rem;">📊 Data Analysis</h3>
        <p style="color: #9CA3AF; line-height: 1.6; margin: 0;">
            Ask better questions about your data and get more insightful analysis
            from AI tools.
        </p>
    </div>
    """, unsafe_allow_html=True)

with use_case_col2:
    st.markdown("""
    <div style="
        background: rgba(26, 27, 61, 0.5);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1rem;
    ">
        <h3 style="color: #EC4899; margin-bottom: 1rem;">🔬 Research Methods</h3>
        <p style="color: #9CA3AF; line-height: 1.6; margin: 0;">
            Get guidance on designing studies, choosing methodologies, and analyzing
            results with critical thinking built in.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background: rgba(26, 27, 61, 0.5);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1rem;
    ">
        <h3 style="color: #06B6D4; margin-bottom: 1rem;">💬 Reviewer Responses</h3>
        <p style="color: #9CA3AF; line-height: 1.6; margin: 0;">
            Craft professional, thorough responses to peer reviewer comments that
            address all concerns.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background: rgba(26, 27, 61, 0.5);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 2rem;
    ">
        <h3 style="color: #F59E0B; margin-bottom: 1rem;">🎓 Learning Concepts</h3>
        <p style="color: #9CA3AF; line-height: 1.6; margin: 0;">
            Use Tutor Mode to truly understand complex topics through guided discovery
            rather than passive reading.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==================== CALL TO ACTION ====================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div style="
    text-align: center;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(236, 72, 153, 0.2) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 20px;
    padding: 3rem 2rem;
    margin: 2rem 0;
">
    <h2 style="
        font-size: 2rem;
        color: #E5E7EB;
        margin-bottom: 1rem;
    ">Ready to Elevate Your Research?</h2>
    <p style="
        color: #9CA3AF;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    ">
        Start optimizing your prompts and get better results from AI tools today.
    </p>
</div>
""", unsafe_allow_html=True)

final_col1, final_col2, final_col3 = st.columns([1, 1, 1])
with final_col2:
    if st.button("🚀 Get Started Now", use_container_width=True, type="primary", key="final_cta"):
        st.switch_page("pages/1_🎯_Prompt_Lab.py")

# Footer
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 0.875rem; margin-top: 4rem; padding: 2rem 0; border-top: 1px solid rgba(139, 92, 246, 0.2);">
    <p>Built with ❤️ for the academic community</p>
    <p style="margin-top: 0.5rem;">
        Questions? Feedback? <a href="mailto:support@example.com" style="color: #8B5CF6;">Get in touch</a>
    </p>
</div>
""", unsafe_allow_html=True)
