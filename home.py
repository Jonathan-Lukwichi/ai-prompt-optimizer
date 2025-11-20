"""
AI Prompt Optimizer - Simplified Prototype
Main application entry point
"""
import streamlit as st
from core.config import Config
from utils.ui_components import load_custom_css, gradient_header
from core.database import DatabaseManager

# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="AI Prompt Optimizer | Academic Research Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
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
            Prototype Version
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Quick navigation
    st.markdown("### 🔗 Navigation")

    if st.button("🎯 Prompt Lab", use_container_width=True, type="primary"):
        st.switch_page("pages/1_🎯_Prompt_Lab.py")

    if st.button("📚 Templates", use_container_width=True):
        st.switch_page("pages/2_📚_Templates.py")

    if st.button("🔬 Workflows", use_container_width=True):
        st.switch_page("pages/3_🔬_Workflows.py")

    if st.button("📊 History", use_container_width=True):
        st.switch_page("pages/4_📊_History.py")

    st.divider()

    # User profile section
    st.markdown("### 👤 Your Profile")

    role = st.selectbox(
        "Role",
        options=list(Config.ACADEMIC_ROLES.keys()) + list(Config.PROFESSIONAL_ROLES.keys()),
        format_func=lambda x: Config.ACADEMIC_ROLES.get(x, Config.PROFESSIONAL_ROLES.get(x, x)),
        key="sidebar_role",
        index=2 if st.session_state.user_role is None else 0
    )
    st.session_state.user_role = role

    field = st.text_input(
        "Field",
        value=st.session_state.user_field or "",
        placeholder="e.g., Computer Science",
        key="sidebar_field"
    )
    if field:
        st.session_state.user_field = field


# ==================== MAIN CONTENT ====================

# Hero Section
gradient_header(
    "AI Prompt Optimizer",
    size="h1",
    subtitle="Transform vague questions into powerful prompts for better AI responses"
)

st.markdown("<br>", unsafe_allow_html=True)

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
st.divider()

# ==================== FEATURES SECTION ====================

st.subheader("✨ Core Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🎯 Smart Optimization")
    st.markdown("""
    Get 4 optimized versions of your prompt:
    - **Basic**: Clear and structured
    - **Critical**: Deep analysis
    - **Tutor**: Socratic learning
    - **Safe**: Prevent hallucinations
    """)

with col2:
    st.markdown("### 📊 Quality Scoring")
    st.markdown("""
    Instant feedback on your prompts:
    - Clarity score
    - Safety score
    - Risk detection
    - Improvement suggestions
    """)

with col3:
    st.markdown("### 📚 Ready Templates")
    st.markdown("""
    Pre-built templates for:
    - Literature reviews
    - Research papers
    - Data analysis
    - Code development
    """)

st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()

# ==================== DOMAINS ====================

st.subheader("🎓 Supported Domains")

domain_col1, domain_col2, domain_col3 = st.columns(3)

with domain_col1:
    st.info("""
    **🎓 Academic & Research**

    Literature reviews, research papers, grant proposals, methodology design
    """)

with domain_col2:
    st.info("""
    **🤖 ML & Data Science**

    Model development, data analysis, AI projects, statistical analysis
    """)

with domain_col3:
    st.info("""
    **🐍 Python Development**

    Code writing, debugging, testing, architecture design
    """)

st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()

# ==================== HOW IT WORKS ====================

st.subheader("🚀 How It Works")

step_col1, step_col2, step_col3, step_col4 = st.columns(4)

with step_col1:
    st.markdown("**1️⃣ Configure**")
    st.markdown("Select your role and task type")

with step_col2:
    st.markdown("**2️⃣ Enter Prompt**")
    st.markdown("Type your question or request")

with step_col3:
    st.markdown("**3️⃣ Get Analysis**")
    st.markdown("See quality scores and risks")

with step_col4:
    st.markdown("**4️⃣ Use Optimized**")
    st.markdown("Copy and use the best version")

st.markdown("<br><br>", unsafe_allow_html=True)

# ==================== FINAL CTA ====================

st.markdown("""
<div style="
    text-align: center;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(236, 72, 153, 0.2) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 20px;
    padding: 2rem;
    margin: 2rem 0;
">
    <h3 style="color: #E5E7EB; margin-bottom: 1rem;">Ready to Get Started?</h3>
    <p style="color: #9CA3AF;">
        Start optimizing your prompts and get better results from AI tools
    </p>
</div>
""", unsafe_allow_html=True)

final_col1, final_col2, final_col3 = st.columns([1, 1, 1])
with final_col2:
    if st.button("🚀 Go to Prompt Lab", use_container_width=True, type="primary", key="final_cta"):
        st.switch_page("pages/1_🎯_Prompt_Lab.py")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("💡 **Prototype Version** - Demonstrating AI prompt optimization approach for academic and professional use")
