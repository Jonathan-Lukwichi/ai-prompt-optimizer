"""
Prompt Lab - Main Feature
Real-time prompt optimization and analysis
"""
import streamlit as st
from core.config import Config
from core.prompt_engine import PromptEngine, PromptAnalysis
from core.database import DatabaseManager
from utils.ui_components import (
    load_custom_css,
    gradient_header,
    score_gauge,
    version_card,
    alert_box
)
from datetime import datetime

# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Prompt Lab | AI Prompt Optimizer",
    page_icon="🎯",
    layout="wide"
)

# Load custom CSS
load_custom_css()

# ==================== SESSION STATE ====================

if 'optimization_result' not in st.session_state:
    st.session_state.optimization_result = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = 'phd'
if 'user_field' not in st.session_state:
    st.session_state.user_field = None

# ==================== HEADER ====================

gradient_header(
    "🎯 Prompt Lab",
    size="h1",
    subtitle="Transform your prompts into powerful, effective requests that get better AI responses"
)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== CONFIGURATION SECTION ====================

st.markdown("""
<h3 style="
    color: #8B5CF6;
    font-weight: 700;
    margin-bottom: 1rem;
">⚙️ Configuration</h3>
""", unsafe_allow_html=True)

config_col1, config_col2, config_col3 = st.columns(3)

with config_col1:
    role = st.selectbox(
        "Your Academic Role",
        options=list(Config.ACADEMIC_ROLES.keys()),
        format_func=lambda x: Config.ACADEMIC_ROLES[x],
        index=list(Config.ACADEMIC_ROLES.keys()).index(st.session_state.user_role) if st.session_state.user_role else 2,
        help="Select your current academic position - this helps tailor the optimization"
    )
    st.session_state.user_role = role

with config_col2:
    task_type = st.selectbox(
        "Task Type",
        options=list(Config.TASK_TYPES.keys()),
        format_func=lambda x: Config.TASK_TYPES[x],
        help="What are you trying to accomplish with this prompt?"
    )

with config_col3:
    field = st.text_input(
        "Field of Study",
        value=st.session_state.user_field or "",
        placeholder="e.g., Computer Science, Biology, Economics",
        help="Your academic discipline (optional but recommended)"
    )
    if field:
        st.session_state.user_field = field

st.divider()

# ==================== PROMPT INPUT SECTION ====================

st.markdown("""
<h3 style="
    color: #8B5CF6;
    font-weight: 700;
    margin-bottom: 1rem;
">💬 Your Prompt</h3>
""", unsafe_allow_html=True)

raw_prompt = st.text_area(
    "What do you want the AI to do?",
    placeholder="""Example: I need to understand the main findings from recent research on transformer models in natural language processing.

Be specific! Include:
- Your goal or question
- Any relevant context
- Desired output format
- Constraints or preferences""",
    height=200,
    help="Enter your question or request. Don't worry if it's not perfect - that's what we're here to fix!",
    label_visibility="collapsed"
)

# Tips expander
with st.expander("💡 Tips for Better Prompts"):
    tips_col1, tips_col2 = st.columns(2)

    with tips_col1:
        st.markdown("""
        **Do:**
        - ✅ Be specific about your goal
        - ✅ Mention your knowledge level
        - ✅ Specify output format
        - ✅ Include relevant constraints
        - ✅ Ask for reasoning/sources
        """)

    with tips_col2:
        st.markdown("""
        **Avoid:**
        - ❌ Vague, one-sentence requests
        - ❌ Asking for made-up citations
        - ❌ Requesting ghostwriting
        - ❌ Missing context entirely
        - ❌ Overly complex language
        """)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== OPTIMIZATION BUTTON ====================

optimize_button = st.button(
    "🚀 Optimize My Prompt",
    type="primary",
    use_container_width=True,
    disabled=not raw_prompt or len(raw_prompt.strip()) < 10
)

if optimize_button:
    with st.spinner("🔍 Analyzing your prompt..."):
        try:
            # Initialize engine
            engine = PromptEngine()

            # Analyze prompt
            analysis = engine.analyze_prompt(raw_prompt, role, task_type, field)

            # Show analysis progress
            progress_text = st.empty()
            progress_text.markdown("✨ Generating optimized versions...")

            # Optimize prompt
            optimized = engine.optimize_prompt(raw_prompt, analysis, role, task_type, field)

            # Save to database
            try:
                session = DatabaseManager.create_session(
                    user_id=None,  # For now, no user authentication
                    role=role,
                    task_type=task_type,
                    raw_prompt=raw_prompt,
                    field=field,
                    analysis={
                        'intent': analysis.intent,
                        'clarity_score': analysis.clarity_score,
                        'safety_score': analysis.safety_score,
                        'risks': analysis.risks,
                        'missing_info': analysis.missing_info,
                        'suggestions': analysis.suggestions
                    }
                )

                # Save versions from the versions dictionary
                for label, prompt_text in optimized.versions.items():
                    DatabaseManager.create_version(session.id, label, prompt_text)

            except Exception as e:
                st.warning(f"Note: Could not save to history: {str(e)}")

            # Store result in session state
            st.session_state.optimization_result = {
                'analysis': analysis,
                'optimized': optimized,
                'raw_prompt': raw_prompt,
                'role': role,
                'task_type': task_type,
                'field': field
            }

            progress_text.empty()
            st.success("✅ Optimization complete!")
            st.balloons()

        except Exception as e:
            st.error(f"❌ Error during optimization: {str(e)}")
            st.info("💡 Tip: Make sure you have set your GEMINI_API_KEY in the .env file. Get a free key at: https://makersuite.google.com/app/apikey")

# ==================== RESULTS SECTION ====================

if st.session_state.optimization_result:
    result = st.session_state.optimization_result
    analysis = result['analysis']
    optimized = result['optimized']

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)

    # ==================== ANALYSIS RESULTS ====================

    st.markdown("""
    <h2 style="
        background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        margin-bottom: 2rem;
    ">📊 Prompt Health Check</h2>
    """, unsafe_allow_html=True)

    # Score gauges
    score_col1, score_col2, score_col3 = st.columns(3)

    with score_col1:
        score_gauge(analysis.clarity_score, 100, "Clarity Score", 180)

    with score_col2:
        score_gauge(analysis.safety_score, 100, "Safety Score", 180)

    with score_col3:
        st.markdown(f"""
        <div style="
            background: rgba(26, 27, 61, 0.6);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(139, 92, 246, 0.2);
            border-radius: 16px;
            padding: 2rem;
            height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="
                color: #9CA3AF;
                font-size: 0.875rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 0.5rem;
            ">Detected Intent</div>
            <div style="
                color: #E5E7EB;
                font-size: 1.5rem;
                font-weight: 700;
                margin-bottom: 1rem;
            ">{analysis.intent}</div>
            <div style="
                color: #9CA3AF;
                font-size: 0.875rem;
            ">for {Config.ACADEMIC_ROLES.get(result['role'], result['role'])}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Risks and Missing Info
    if analysis.risks or analysis.missing_info:
        risk_col1, risk_col2 = st.columns(2)

        with risk_col1:
            if analysis.risks:
                st.markdown("""
                <h4 style="color: #EF4444; font-weight: 700;">⚠️ Identified Risks</h4>
                """, unsafe_allow_html=True)
                for risk in analysis.risks:
                    alert_box(risk, "warning")

        with risk_col2:
            if analysis.missing_info:
                st.markdown("""
                <h4 style="color: #3B82F6; font-weight: 700;">💡 Missing Information</h4>
                """, unsafe_allow_html=True)
                for info in analysis.missing_info:
                    alert_box(f"Consider adding: {info}", "info")

    # Suggestions
    if analysis.suggestions:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <h4 style="color: #10B981; font-weight: 700;">✨ Improvement Suggestions</h4>
        """, unsafe_allow_html=True)
        for suggestion in analysis.suggestions:
            st.markdown(f"- {suggestion}")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)

    # ==================== OPTIMIZED VERSIONS ====================

    st.markdown("""
    <h2 style="
        background: linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        margin-bottom: 1rem;
    ">✨ Optimized Versions</h2>
    <p style="color: #9CA3AF; font-size: 1.1rem; margin-bottom: 2rem;">
        Choose the version that best fits your needs. Each is optimized for a different purpose.
    </p>
    """, unsafe_allow_html=True)

    # Tabs for different versions
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Basic",
        "🧠 Critical Thinking",
        "👨‍🏫 Tutor Mode",
        "🛡️ Safe Mode"
    ])

    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        version_card(
            label="Basic Version",
            prompt=optimized.versions.get("basic", ""),
            icon="📝",
            color="#3B82F6",
            description="Clear, well-structured version for general use. Best for getting comprehensive, straightforward answers.",
            key_suffix="basic"
        )

        st.markdown("""
        <div style="
            background: rgba(59, 130, 246, 0.1);
            border-left: 3px solid #3B82F6;
            padding: 1rem;
            border-radius: 8px;
            margin-top: 1rem;
        ">
            <strong style="color: #3B82F6;">When to use:</strong><br>
            <span style="color: #9CA3AF;">
            Perfect for getting started, exploring a topic, or when you need a clear, comprehensive response
            without additional constraints.
            </span>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        version_card(
            label="Critical Thinking Version",
            prompt=optimized.versions.get("critical", ""),
            icon="🧠",
            color="#8B5CF6",
            description="Forces deeper analysis and questioning of assumptions. Best for research and avoiding bias.",
            key_suffix="critical"
        )

        st.markdown("""
        <div style="
            background: rgba(139, 92, 246, 0.1);
            border-left: 3px solid #8B5CF6;
            padding: 1rem;
            border-radius: 8px;
            margin-top: 1rem;
        ">
            <strong style="color: #8B5CF6;">When to use:</strong><br>
            <span style="color: #9CA3AF;">
            Ideal for research planning, evaluating methodologies, identifying potential issues,
            or when you need to consider multiple perspectives and limitations.
            </span>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        version_card(
            label="Tutor Mode Version",
            prompt=optimized.versions.get("tutor", ""),
            icon="👨‍🏫",
            color="#10B981",
            description="Socratic method - guides you to discover insights yourself. Best for learning and understanding.",
            key_suffix="tutor"
        )

        st.markdown("""
        <div style="
            background: rgba(16, 185, 129, 0.1);
            border-left: 3px solid #10B981;
            padding: 1rem;
            border-radius: 8px;
            margin-top: 1rem;
        ">
            <strong style="color: #10B981;">When to use:</strong><br>
            <span style="color: #9CA3AF;">
            Perfect for learning new concepts, understanding complex topics, or when you want to develop
            your own reasoning skills rather than just getting an answer.
            </span>
        </div>
        """, unsafe_allow_html=True)

    with tab4:
        st.markdown("<br>", unsafe_allow_html=True)
        version_card(
            label="Safe Mode Version",
            prompt=optimized.versions.get("safe", ""),
            icon="🛡️",
            color="#EC4899",
            description="Minimizes hallucinations and emphasizes uncertainty. Best for citations and factual accuracy.",
            key_suffix="safe"
        )

        st.markdown("""
        <div style="
            background: rgba(236, 72, 153, 0.1);
            border-left: 3px solid #EC4899;
            padding: 1rem;
            border-radius: 8px;
            margin-top: 1rem;
        ">
            <strong style="color: #EC4899;">When to use:</strong><br>
            <span style="color: #9CA3AF;">
            Essential when you need factual accuracy, working with citations, or when the cost of
            misinformation is high. Explicitly instructs AI to acknowledge uncertainty.
            </span>
        </div>
        """, unsafe_allow_html=True)

    # ==================== COMPARISON VIEW ====================

    st.markdown("<br><br>", unsafe_allow_html=True)

    with st.expander("🔍 Compare All Versions Side-by-Side"):
        st.markdown("<br>", unsafe_allow_html=True)

        compare_col1, compare_col2 = st.columns(2)

        with compare_col1:
            st.markdown("**📝 Basic**")
            st.text_area("", optimized.versions.get("basic", ""), height=150, key="compare_basic", label_visibility="collapsed")

            st.markdown("**🧠 Critical Thinking**")
            st.text_area("", optimized.versions.get("critical", ""), height=150, key="compare_critical", label_visibility="collapsed")

        with compare_col2:
            st.markdown("**👨‍🏫 Tutor Mode**")
            st.text_area("", optimized.versions.get("tutor", ""), height=150, key="compare_tutor", label_visibility="collapsed")

            st.markdown("**🛡️ Safe Mode**")
            st.text_area("", optimized.versions.get("safe", ""), height=150, key="compare_safe", label_visibility="collapsed")

    # ==================== ORIGINAL PROMPT ====================

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("📋 View Original Prompt"):
        st.markdown(f"""
        <div style="
            background: rgba(26, 27, 61, 0.5);
            border-radius: 12px;
            padding: 1.5rem;
        ">
            <pre style="
                color: #9CA3AF;
                white-space: pre-wrap;
                font-family: 'JetBrains Mono', monospace;
                margin: 0;
            ">{result['raw_prompt']}</pre>
        </div>
        """, unsafe_allow_html=True)

    # ==================== ACTIONS ====================

    st.markdown("<br><br>", unsafe_allow_html=True)

    action_col1, action_col2, action_col3 = st.columns(3)

    with action_col1:
        if st.button("🔄 Optimize Another Prompt", use_container_width=True):
            st.session_state.optimization_result = None
            st.rerun()

    with action_col2:
        if st.button("📚 Browse Templates", use_container_width=True):
            st.switch_page("pages/2_📚_Templates.py")

    with action_col3:
        if st.button("📊 View History", use_container_width=True):
            st.switch_page("pages/4_📊_History.py")


# ==================== EMPTY STATE ====================

else:
    st.markdown("""
    <div style="
        text-align: center;
        padding: 4rem 2rem;
        background: rgba(26, 27, 61, 0.3);
        border-radius: 16px;
        border: 2px dashed rgba(139, 92, 246, 0.3);
        margin: 2rem 0;
    ">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🎯</div>
        <h3 style="color: #E5E7EB; margin-bottom: 1rem;">Ready to optimize your prompt?</h3>
        <p style="color: #9CA3AF; max-width: 600px; margin: 0 auto;">
            Enter your prompt above, configure your role and task type, then click "Optimize My Prompt"
            to get 4 professionally crafted versions tailored to your academic needs.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Quick examples
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <h3 style="color: #8B5CF6; font-weight: 700; margin-bottom: 1rem;">📝 Quick Examples</h3>
    """, unsafe_allow_html=True)

    example_col1, example_col2 = st.columns(2)

    with example_col1:
        with st.expander("Example: Literature Review"):
            if st.button("Use this example", key="example_lit"):
                st.session_state.example_prompt = """I need to review recent research on the applications of machine learning in climate science.

I'm particularly interested in:
- Predictive models for extreme weather events
- Analysis of long-term climate trends
- Integration with physical climate models

I have a basic understanding of ML but limited climate science background."""
                st.rerun()

    with example_col2:
        with st.expander("Example: Concept Understanding"):
            if st.button("Use this example", key="example_concept"):
                st.session_state.example_prompt = """Help me understand the concept of p-values in statistical hypothesis testing.

I know basic statistics but get confused about:
- What a p-value actually means
- How to interpret different p-values
- Common misconceptions

I learn best with examples and analogies."""
                st.rerun()
