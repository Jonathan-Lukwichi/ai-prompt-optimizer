"""
Prompt Lab - Main Feature
Real-time prompt optimization and analysis
"""
import streamlit as st
import json
from core.config import Config
from core.prompt_engine import PromptEngine, PromptAnalysis
from core.database import DatabaseManager
from utils.ui_components import (
    load_custom_css,
    gradient_header,
    score_gauge,
    version_card,
    alert_box,
    voice_or_text_input
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
if 'preferences_loaded' not in st.session_state:
    st.session_state.preferences_loaded = False

# ==================== LOAD SMART DEFAULTS ====================

from core.user_preferences import get_preferences

# Get preferences instance
prefs = get_preferences()

# Load smart defaults (only once per session)
if not st.session_state.preferences_loaded:
    # Try to load from database
    saved_prefs = DatabaseManager.load_preferences(session_key="default")

    if saved_prefs and saved_prefs.get('total_optimizations', 0) > 0:
        # Import saved preferences
        prefs.import_preferences(
            json.dumps({
                'version_usage': saved_prefs['version_usage'],
                'domain_usage': saved_prefs['domain_usage'],
                'role_usage': saved_prefs['role_usage'],
                'task_usage': saved_prefs['task_usage'],
                'combinations': saved_prefs['combinations'],
                'last_updated': saved_prefs['last_updated']
            })
        )

        # Get smart defaults
        defaults = prefs.get_smart_defaults()

        # Apply defaults if available
        if defaults.get('role'):
            st.session_state.user_role = defaults['role']
        if defaults.get('task_type'):
            st.session_state.preferred_task = defaults['task_type']

        st.session_state.using_smart_defaults = True
        st.session_state.smart_defaults = defaults
    else:
        st.session_state.using_smart_defaults = False
        st.session_state.smart_defaults = {}

    st.session_state.preferences_loaded = True

# ==================== HEADER ====================

gradient_header(
    "🎯 Prompt Lab",
    size="h1",
    subtitle="Transform your prompts into powerful, effective requests that get better AI responses"
)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== CONFIGURATION SECTION ====================

# Show smart defaults indicator if using learned preferences
if st.session_state.get('using_smart_defaults'):
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    ">
        <div style="font-size: 1.5rem;">🧠</div>
        <div>
            <div style="color: #10B981; font-weight: 700; font-size: 0.95rem;">
                Smart Defaults Active
            </div>
            <div style="color: #9CA3AF; font-size: 0.85rem;">
                Settings pre-filled based on your usage patterns. Change them anytime!
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
    # Use smart default if available
    default_task = st.session_state.get('preferred_task')
    task_options = list(Config.TASK_TYPES.keys())

    if default_task and default_task in task_options:
        default_index = task_options.index(default_task)
    else:
        default_index = 0

    task_type = st.selectbox(
        "Task Type",
        options=task_options,
        index=default_index,
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
    background: linear-gradient(135deg, #00FF9F 0%, #00D9FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
    margin-bottom: 1rem;
">💬 Your Prompt</h3>
""", unsafe_allow_html=True)

# Voice or Text input - Users can now speak their prompts!
raw_prompt = voice_or_text_input(
    label="What do you want the AI to do?",
    placeholder="""Example: I need to understand the main findings from recent research on transformer models in natural language processing.

Be specific! Include:
- Your goal or question
- Any relevant context
- Desired output format
- Constraints or preferences""",
    height=200,
    key="prompt_lab_input"
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

# ==================== ENHANCEMENT FEATURES ====================

# Add session state for enhancement features
if 'quick_enhanced_prompt' not in st.session_state:
    st.session_state.quick_enhanced_prompt = None
if 'refinement_stage' not in st.session_state:
    st.session_state.refinement_stage = None
if 'refinement_active' not in st.session_state:
    st.session_state.refinement_active = False

# Enhancement buttons row
if raw_prompt and len(raw_prompt.strip()) >= 10:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(249, 115, 22, 0.1) 100%);
        border: 1px solid rgba(251, 191, 36, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    ">
        <div style="color: #F59E0B; font-weight: 700; font-size: 1rem; margin-bottom: 0.5rem;">
            ⚡ Need Help Improving Your Prompt?
        </div>
        <div style="color: #9CA3AF; font-size: 0.85rem;">
            Use Quick Enhance for instant improvement, or Iterative Refinement for step-by-step guidance
        </div>
    </div>
    """, unsafe_allow_html=True)

    enhance_col1, enhance_col2, enhance_col3 = st.columns([2, 2, 1])

    with enhance_col1:
        quick_enhance_btn = st.button(
            "⚡ Quick Enhance",
            help="One-click enhancement using AI best practices",
            use_container_width=True
        )

    with enhance_col2:
        if not st.session_state.refinement_active:
            start_refinement_btn = st.button(
                "🔄 Start Iterative Refinement",
                help="Step-by-step guided improvement process",
                use_container_width=True
            )
        else:
            stop_refinement_btn = st.button(
                "⏹️ Stop Refinement",
                help="Exit refinement mode",
                use_container_width=True
            )

    with enhance_col3:
        show_education = st.checkbox(
            "📚 Learn",
            help="Show explanations for improvements"
        )

    # Handle Quick Enhance
    if quick_enhance_btn:
        with st.spinner("⚡ Enhancing your prompt with AI best practices..."):
            from core.prompt_enhancer import get_enhancer
            enhancer = get_enhancer()

            try:
                enhancement = enhancer.quick_enhance(raw_prompt)
                st.session_state.quick_enhanced_prompt = enhancement

                # Success message
                st.success(f"✅ Enhanced! Score improved from {enhancement.score_before} → {enhancement.score_after} (+{enhancement.score_after - enhancement.score_before} points)")

            except Exception as e:
                st.error(f"Error enhancing prompt: {str(e)}")

    # Handle Start Iterative Refinement
    if 'start_refinement_btn' in locals() and start_refinement_btn:
        with st.spinner("🔄 Starting iterative refinement..."):
            from core.prompt_enhancer import get_enhancer
            enhancer = get_enhancer()

            try:
                stage = enhancer.start_iterative_refinement(raw_prompt)
                st.session_state.refinement_stage = stage
                st.session_state.refinement_active = True
                st.rerun()

            except Exception as e:
                st.error(f"Error starting refinement: {str(e)}")

    # Handle Stop Refinement
    if 'stop_refinement_btn' in locals() and stop_refinement_btn:
        st.session_state.refinement_active = False
        st.session_state.refinement_stage = None
        st.rerun()

    # Display Quick Enhanced Result
    if st.session_state.quick_enhanced_prompt:
        enhancement = st.session_state.quick_enhanced_prompt

        st.markdown("### ⚡ Quick Enhanced Version")

        col_result1, col_result2 = st.columns([3, 1])

        with col_result1:
            st.text_area(
                "Enhanced Prompt",
                value=enhancement.enhanced,
                height=150,
                key="quick_enhanced_display",
                label_visibility="collapsed"
            )

        with col_result2:
            st.metric(
                "Quality Score",
                f"{enhancement.score_after}/100",
                delta=f"+{enhancement.score_after - enhancement.score_before}"
            )

            if st.button("📋 Use This", key="use_enhanced"):
                raw_prompt = enhancement.enhanced
                st.session_state.quick_enhanced_prompt = None
                st.rerun()

        # Show educational explanations if requested
        if show_education and enhancement.changes:
            with st.expander("📚 What Changed & Why", expanded=True):
                st.markdown(f"**Overall Impact**: {enhancement.explanation}")

                st.markdown("**Specific Changes:**")
                for idx, change in enumerate(enhancement.changes, 1):
                    st.markdown(f"""
                    **{idx}. {change['change']}**
                    - 💡 Why: {change['why']}
                    """)

        st.markdown("<br>", unsafe_allow_html=True)

    # Display Iterative Refinement Interface
    if st.session_state.refinement_active and st.session_state.refinement_stage:
        stage = st.session_state.refinement_stage

        st.markdown(f"### 🔄 Iterative Refinement - Stage {stage.stage_number}")

        # Show analysis
        analysis = stage.analysis
        if 'score' in analysis:
            st.metric("Current Prompt Score", f"{analysis['score']}/100")

        if analysis.get('strengths'):
            with st.expander("💪 Strengths", expanded=False):
                for strength in analysis['strengths']:
                    st.markdown(f"- {strength}")

        if analysis.get('weaknesses'):
            with st.expander("⚠️ Areas for Improvement", expanded=True):
                for weakness in analysis['weaknesses']:
                    st.markdown(f"- {weakness}")

        # Show questions if any
        if stage.questions and not analysis.get('complete'):
            st.markdown("**Answer these questions to refine your prompt:**")

            answers = []
            for idx, question in enumerate(stage.questions):
                answer = st.text_input(
                    f"Q{idx+1}: {question}",
                    key=f"refinement_q_{stage.stage_number}_{idx}"
                )
                answers.append(answer)

            if st.button("➡️ Continue Refinement", type="primary"):
                if all(answers):
                    with st.spinner("🔄 Refining..."):
                        from core.prompt_enhancer import get_enhancer
                        enhancer = get_enhancer()

                        try:
                            next_stage = enhancer.refine_with_answers(
                                stage.prompt,
                                stage.questions,
                                answers,
                                stage.stage_number
                            )
                            st.session_state.refinement_stage = next_stage

                            if next_stage.analysis.get('complete'):
                                st.success("✅ Refinement complete! Your prompt is ready.")
                                st.session_state.refinement_active = False

                            st.rerun()

                        except Exception as e:
                            st.error(f"Error refining: {str(e)}")
                else:
                    st.warning("⚠️ Please answer all questions to continue")

        # Show refined prompt
        if stage.prompt != raw_prompt:
            st.markdown("**Refined Prompt:**")
            st.text_area(
                "Refined",
                value=stage.prompt,
                height=150,
                key="refined_display",
                label_visibility="collapsed"
            )

            if st.button("📋 Use Refined Version", key="use_refined"):
                raw_prompt = stage.prompt
                st.session_state.refinement_active = False
                st.session_state.refinement_stage = None
                st.rerun()

        # Show suggestions
        if stage.suggestions:
            with st.expander("💡 Suggestions for Further Improvement"):
                for suggestion in stage.suggestions:
                    st.markdown(f"- {suggestion}")

        st.markdown("<br>", unsafe_allow_html=True)

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

            # Track optimization in preferences
            try:
                # Get domain from optimized result
                domain = optimized.domain if hasattr(optimized, 'domain') else 'academic'

                # Track this optimization
                prefs.track_optimization(
                    domain=domain,
                    role=role,
                    task_type=task_type
                )

                # Save preferences to database
                DatabaseManager.save_preferences(prefs, session_key="default")
            except Exception as e:
                # Don't fail optimization if preference tracking fails
                pass

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

    # ==================== INLINE TEST & COMPARE ====================

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("🔬 Test Your Optimization - See Proof It Works Better!"):
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1.5rem;
        ">
            <div style="color: #10B981; font-weight: 700; margin-bottom: 0.5rem;">
                💡 Quick Test
            </div>
            <div style="color: #9CA3AF; font-size: 0.95rem;">
                Run both your original and optimized prompts through AI and get objective quality scores.
                See exactly how much better the optimized version performs!
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Version selector
        test_col1, test_col2 = st.columns([3, 1])

        with test_col1:
            version_to_test = st.selectbox(
                "Select which optimized version to test:",
                options=["basic", "critical", "tutor", "safe"],
                format_func=lambda x: {
                    "basic": "📝 Basic Version",
                    "critical": "🧠 Critical Thinking",
                    "tutor": "👨‍🏫 Tutor Mode",
                    "safe": "🛡️ Safe Mode"
                }[x],
                key="inline_test_version"
            )

        with test_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            run_test_btn = st.button("🚀 Run Test", use_container_width=True, key="inline_run_test")

        # Run quick test
        if run_test_btn:
            with st.spinner("🧪 Testing both prompts..."):
                try:
                    from core.response_analyzer import ResponseAnalyzer
                    import google.generativeai as genai
                    from core.config import Config

                    # Configure Gemini
                    genai.configure(api_key=Config.GEMINI_API_KEY)
                    model = genai.GenerativeModel(Config.GEMINI_MODEL)

                    # Get responses
                    original_response = model.generate_content(result['raw_prompt']).text
                    optimized_response = model.generate_content(optimized.versions[version_to_test]).text

                    # Analyze quality
                    analyzer = ResponseAnalyzer()
                    original_analysis = analyzer.analyze_response(original_response, result['raw_prompt'])
                    optimized_analysis = analyzer.analyze_response(optimized_response, optimized.versions[version_to_test])

                    # Store results
                    st.session_state.inline_test_result = {
                        'original': original_analysis,
                        'optimized': optimized_analysis,
                        'version': version_to_test
                    }

                except Exception as e:
                    st.error(f"Test failed: {str(e)}")

        # Display results
        if 'inline_test_result' in st.session_state:
            test_result = st.session_state.inline_test_result
            orig = test_result['original']
            opt = test_result['optimized']

            st.markdown("<br>", unsafe_allow_html=True)

            # Quick comparison
            result_col1, result_col2, result_col3 = st.columns([1, 1, 1])

            with result_col1:
                st.markdown(f"""
                <div style="
                    background: rgba(239, 68, 68, 0.1);
                    border: 1px solid rgba(239, 68, 68, 0.3);
                    border-radius: 12px;
                    padding: 1.5rem;
                    text-align: center;
                ">
                    <div style="color: #9CA3AF; font-size: 0.875rem; margin-bottom: 0.5rem;">
                        Original Score
                    </div>
                    <div style="color: #EF4444; font-size: 2.5rem; font-weight: 800;">
                        {orig['overall_score']:.0f}
                    </div>
                    <div style="color: #9CA3AF; font-size: 0.75rem;">
                        out of 100
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with result_col2:
                improvement = opt['overall_score'] - orig['overall_score']
                improvement_color = "#10B981" if improvement > 0 else "#EF4444"
                improvement_sign = "+" if improvement > 0 else ""

                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(6, 182, 212, 0.2) 100%);
                    border: 2px solid {improvement_color};
                    border-radius: 12px;
                    padding: 1.5rem;
                    text-align: center;
                ">
                    <div style="color: #9CA3AF; font-size: 0.875rem; margin-bottom: 0.5rem;">
                        Improvement
                    </div>
                    <div style="color: {improvement_color}; font-size: 2.5rem; font-weight: 800;">
                        {improvement_sign}{improvement:.0f}
                    </div>
                    <div style="color: #9CA3AF; font-size: 0.75rem;">
                        points better
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with result_col3:
                st.markdown(f"""
                <div style="
                    background: rgba(16, 185, 129, 0.1);
                    border: 1px solid rgba(16, 185, 129, 0.3);
                    border-radius: 12px;
                    padding: 1.5rem;
                    text-align: center;
                ">
                    <div style="color: #9CA3AF; font-size: 0.875rem; margin-bottom: 0.5rem;">
                        Optimized Score
                    </div>
                    <div style="color: #10B981; font-size: 2.5rem; font-weight: 800;">
                        {opt['overall_score']:.0f}
                    </div>
                    <div style="color: #9CA3AF; font-size: 0.75rem;">
                        out of 100
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Quick dimension breakdown
            st.markdown("""
            <div style="color: #9CA3AF; font-size: 0.875rem; margin-bottom: 0.5rem;">
                📊 Score Breakdown:
            </div>
            """, unsafe_allow_html=True)

            dimension_col1, dimension_col2 = st.columns(2)

            with dimension_col1:
                for dim in ['completeness', 'clarity']:
                    orig_score = orig['dimensions'][dim]['score']
                    opt_score = opt['dimensions'][dim]['score']
                    diff = opt_score - orig_score
                    diff_color = "#10B981" if diff > 0 else "#9CA3AF"
                    diff_sign = "+" if diff > 0 else ""

                    st.markdown(f"""
                    <div style="
                        background: rgba(26, 27, 61, 0.5);
                        border-radius: 8px;
                        padding: 0.75rem;
                        margin-bottom: 0.5rem;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    ">
                        <span style="color: #E5E7EB; font-weight: 600;">
                            {dim.title()}
                        </span>
                        <span style="color: {diff_color}; font-weight: 700;">
                            {orig_score:.0f} → {opt_score:.0f} ({diff_sign}{diff:.0f})
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

            with dimension_col2:
                for dim in ['specificity', 'actionability']:
                    orig_score = orig['dimensions'][dim]['score']
                    opt_score = opt['dimensions'][dim]['score']
                    diff = opt_score - orig_score
                    diff_color = "#10B981" if diff > 0 else "#9CA3AF"
                    diff_sign = "+" if diff > 0 else ""

                    st.markdown(f"""
                    <div style="
                        background: rgba(26, 27, 61, 0.5);
                        border-radius: 8px;
                        padding: 0.75rem;
                        margin-bottom: 0.5rem;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    ">
                        <span style="color: #E5E7EB; font-weight: 600;">
                            {dim.title()}
                        </span>
                        <span style="color: {diff_color}; font-weight: 700;">
                            {orig_score:.0f} → {opt_score:.0f} ({diff_sign}{diff:.0f})
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Full analysis button
            if st.button("📊 See Full Analysis with Charts & Details", use_container_width=True, key="goto_full_test"):
                # Prepare data for Test & Compare page
                st.session_state.test_compare_data = {
                    'raw_prompt': result['raw_prompt'],
                    'optimized_prompt': optimized.versions[version_to_test],
                    'version_type': version_to_test,
                    'original_analysis': orig,
                    'optimized_analysis': opt
                }
                st.switch_page("pages/5_🔬_Test_Compare.py")

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
