"""
Academic Workflows
Multi-step guided processes for complex academic tasks
"""
import streamlit as st
from core.config import Config
from core.database import DatabaseManager, Workflow
from utils.ui_components import load_custom_css, gradient_header, progress_steps, alert_box

# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Workflows | AI Prompt Optimizer",
    page_icon="🔬",
    layout="wide"
)

# Load custom CSS
load_custom_css()

# ==================== SESSION STATE ====================

if 'active_workflow' not in st.session_state:
    st.session_state.active_workflow = None
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'workflow_data' not in st.session_state:
    st.session_state.workflow_data = {}

# ==================== HEADER ====================

gradient_header(
    "🔬 Academic Workflows",
    size="h1",
    subtitle="Step-by-step guided processes for complex academic tasks"
)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== LOAD WORKFLOWS ====================

try:
    workflows = DatabaseManager.get_workflows()
except Exception as e:
    st.error(f"Error loading workflows: {str(e)}")
    workflows = []

# ==================== WORKFLOW SELECTION ====================

if not st.session_state.active_workflow:

    st.markdown("""
    <h3 style="color: #8B5CF6; font-weight: 700; margin-bottom: 1.5rem;">
    📋 Available Workflows
    </h3>
    <p style="color: #9CA3AF; font-size: 1.1rem; margin-bottom: 2rem;">
    Choose a workflow to get started with a guided, multi-step process
    </p>
    """, unsafe_allow_html=True)

    # Display available workflows
    if workflows:
        for workflow in workflows:
            st.markdown(f"""
            <div style="
                background: rgba(26, 27, 61, 0.5);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(139, 92, 246, 0.2);
                border-radius: 16px;
                padding: 2rem;
                margin-bottom: 1.5rem;
                transition: all 0.3s ease;
            " onmouseover="this.style.borderColor='rgba(139, 92, 246, 0.5)'"
               onmouseout="this.style.borderColor='rgba(139, 92, 246, 0.2)'">
                <h3 style="
                    color: #E5E7EB;
                    font-size: 1.5rem;
                    font-weight: 700;
                    margin-bottom: 0.5rem;
                ">{workflow.name}</h3>
                <p style="color: #9CA3AF; margin-bottom: 1rem;">
                    {workflow.description}
                </p>
                <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
                    <span style="
                        background: rgba(139, 92, 246, 0.2);
                        color: #8B5CF6;
                        padding: 0.25rem 0.75rem;
                        border-radius: 20px;
                        font-size: 0.875rem;
                        font-weight: 600;
                    ">{len(workflow.steps)} Steps</span>
                    <span style="
                        background: rgba(59, 130, 246, 0.2);
                        color: #3B82F6;
                        padding: 0.25rem 0.75rem;
                        border-radius: 20px;
                        font-size: 0.875rem;
                        font-weight: 600;
                    ">{Config.ACADEMIC_ROLES.get(workflow.role, workflow.role) if workflow.role else 'All Levels'}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"🚀 Start Workflow: {workflow.name}", key=f"start_{workflow.id}", type="primary"):
                st.session_state.active_workflow = workflow
                st.session_state.current_step = 0
                st.session_state.workflow_data = {}
                st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

    else:
        # Sample workflow if none in database
        st.markdown("""
        <div style="
            background: rgba(26, 27, 61, 0.5);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(139, 92, 246, 0.2);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 1.5rem;
        ">
            <h3 style="color: #E5E7EB; font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem;">
            📖 Complete Literature Review
            </h3>
            <p style="color: #9CA3AF; margin-bottom: 1rem;">
                A comprehensive, step-by-step process for conducting a systematic literature review
                from defining research questions to synthesizing findings.
            </p>
            <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
                <span style="
                    background: rgba(139, 92, 246, 0.2);
                    color: #8B5CF6;
                    padding: 0.25rem 0.75rem;
                    border-radius: 20px;
                    font-size: 0.875rem;
                    font-weight: 600;
                ">5 Steps</span>
                <span style="
                    background: rgba(59, 130, 246, 0.2);
                    color: #3B82F6;
                    padding: 0.25rem 0.75rem;
                    border-radius: 20px;
                    font-size: 0.875rem;
                    font-weight: 600;
                ">PhD Level</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Start Literature Review Workflow", type="primary"):
            # Create a demo workflow
            st.session_state.active_workflow = {
                'name': 'Complete Literature Review',
                'description': 'Step-by-step literature review process',
                'steps': [
                    {
                        'step': 1,
                        'name': 'Define Research Questions',
                        'description': 'Clearly articulate what you want to learn from the literature',
                        'prompt_template': 'Help me formulate clear research questions for a literature review on [TOPIC] in the field of [FIELD]. I want to focus on [SPECIFIC ASPECTS].'
                    },
                    {
                        'step': 2,
                        'name': 'Develop Search Strategy',
                        'description': 'Create a comprehensive search plan for academic databases',
                        'prompt_template': 'Create a comprehensive search strategy for my literature review on [RESEARCH QUESTIONS]. Include keywords, Boolean operators, and suggest relevant databases for [FIELD].'
                    },
                    {
                        'step': 3,
                        'name': 'Screen Papers',
                        'description': 'Develop criteria for selecting relevant papers',
                        'prompt_template': 'Help me develop clear inclusion/exclusion criteria for screening papers for my literature review on [TOPIC]. Research questions: [QUESTIONS]'
                    },
                    {
                        'step': 4,
                        'name': 'Extract Information',
                        'description': 'Design a systematic approach to analyzing selected papers',
                        'prompt_template': 'What information should I systematically extract from each paper for my review on [TOPIC]? Suggest a data extraction template.'
                    },
                    {
                        'step': 5,
                        'name': 'Synthesize Findings',
                        'description': 'Integrate and analyze the literature',
                        'prompt_template': 'Help me synthesize findings from [NUMBER] papers on [TOPIC]. Key themes identified: [THEMES]. How should I structure the synthesis?'
                    }
                ]
            }
            st.session_state.current_step = 0
            st.session_state.workflow_data = {}
            st.rerun()

    # ==================== WORKFLOW BENEFITS ====================

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.divider()

    st.markdown("""
    <h2 style="
        background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        margin: 2rem 0 1.5rem;
    ">✨ Why Use Workflows?</h2>
    """, unsafe_allow_html=True)

    benefit_col1, benefit_col2, benefit_col3 = st.columns(3)

    with benefit_col1:
        st.markdown("""
        <div style="
            background: rgba(26, 27, 61, 0.5);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(139, 92, 246, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            height: 100%;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
            <h3 style="color: #8B5CF6; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;">
                Structured Approach
            </h3>
            <p style="color: #9CA3AF; font-size: 0.9rem; margin: 0;">
                Break complex tasks into manageable, sequential steps
            </p>
        </div>
        """, unsafe_allow_html=True)

    with benefit_col2:
        st.markdown("""
        <div style="
            background: rgba(26, 27, 61, 0.5);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(139, 92, 246, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            height: 100%;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🧭</div>
            <h3 style="color: #3B82F6; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;">
                Expert Guidance
            </h3>
            <p style="color: #9CA3AF; font-size: 0.9rem; margin: 0;">
                Follow best practices developed by experienced researchers
            </p>
        </div>
        """, unsafe_allow_html=True)

    with benefit_col3:
        st.markdown("""
        <div style="
            background: rgba(26, 27, 61, 0.5);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(139, 92, 246, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            height: 100%;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">💾</div>
            <h3 style="color: #10B981; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;">
                Save Progress
            </h3>
            <p style="color: #9CA3AF; font-size: 0.9rem; margin: 0;">
                Return anytime and pick up where you left off
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==================== ACTIVE WORKFLOW ====================

else:
    workflow = st.session_state.active_workflow
    current_step = st.session_state.current_step
    steps = workflow['steps'] if isinstance(workflow, dict) else workflow.steps

    # Progress indicator
    st.markdown("<br>", unsafe_allow_html=True)
    progress_steps(
        [step['name'] if isinstance(step, dict) else step.get('name', f'Step {i+1}') for i, step in enumerate(steps)],
        current_step
    )
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Current step
    step = steps[current_step]
    step_name = step['name'] if isinstance(step, dict) else step.get('name', 'Step')
    step_description = step.get('description', '')
    step_template = step.get('prompt_template', '')

    # Step header
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
    ">
        <div style="
            color: #9CA3AF;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        ">Step {current_step + 1} of {len(steps)}</div>
        <h2 style="
            color: #E5E7EB;
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        ">{step_name}</h2>
        <p style="
            color: #9CA3AF;
            font-size: 1.1rem;
            margin: 0;
        ">{step_description}</p>
    </div>
    """, unsafe_allow_html=True)

    # Step content
    st.markdown("""
    <h3 style="color: #8B5CF6; font-weight: 700; margin-bottom: 1rem;">
    📝 Customize Your Prompt
    </h3>
    """, unsafe_allow_html=True)

    # Show template
    st.markdown(f"""
    <div style="
        background: rgba(37, 39, 80, 0.5);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    ">
        <strong style="color: #8B5CF6;">Template:</strong><br>
        <pre style="
            color: #E5E7EB;
            white-space: pre-wrap;
            font-family: 'JetBrains Mono', monospace;
            margin-top: 0.5rem;
            line-height: 1.6;
        ">{step_template}</pre>
    </div>
    """, unsafe_allow_html=True)

    alert_box(
        "Fill in the placeholders (shown in [BRACKETS]) with your specific information",
        "info",
        "💡"
    )

    # Customization area
    customized_prompt = st.text_area(
        "Your Customized Prompt",
        value=st.session_state.workflow_data.get(f'step_{current_step}', step_template),
        height=200,
        help="Edit the template above to fit your specific needs",
        key=f"workflow_prompt_{current_step}"
    )

    # Save to workflow data
    st.session_state.workflow_data[f'step_{current_step}'] = customized_prompt

    st.markdown("<br>", unsafe_allow_html=True)

    # Actions
    action_col1, action_col2, action_col3 = st.columns([1, 1, 1])

    with action_col1:
        if current_step > 0:
            if st.button("⬅️ Previous Step", use_container_width=True):
                st.session_state.current_step -= 1
                st.rerun()

    with action_col2:
        if st.button("🎯 Optimize in Prompt Lab", use_container_width=True, type="primary"):
            # Navigate to Prompt Lab with this prompt
            st.session_state.template_prompt = customized_prompt
            st.switch_page("pages/1_🎯_Prompt_Lab.py")

    with action_col3:
        if current_step < len(steps) - 1:
            if st.button("Next Step ➡️", use_container_width=True):
                st.session_state.current_step += 1
                st.rerun()
        else:
            if st.button("✅ Complete Workflow", use_container_width=True, type="primary"):
                st.balloons()
                st.success(f"🎉 Congratulations! You've completed the {workflow['name'] if isinstance(workflow, dict) else workflow.name} workflow!")

                st.markdown("<br>", unsafe_allow_html=True)

                # Show summary
                with st.expander("📋 View All Your Prompts"):
                    for i, step_data in enumerate(steps):
                        step_name_summary = step_data['name'] if isinstance(step_data, dict) else step_data.get('name', f'Step {i+1}')
                        prompt_text = st.session_state.workflow_data.get(f'step_{i}', '')
                        if prompt_text:
                            st.markdown(f"**Step {i+1}: {step_name_summary}**")
                            st.code(prompt_text, language=None)
                            st.markdown("<br>", unsafe_allow_html=True)

                if st.button("🔄 Start Another Workflow"):
                    st.session_state.active_workflow = None
                    st.session_state.current_step = 0
                    st.session_state.workflow_data = {}
                    st.rerun()

    # Sidebar: Workflow overview
    with st.sidebar:
        st.markdown("""
        <h3 style="color: #8B5CF6; font-weight: 700;">Workflow Overview</h3>
        """, unsafe_allow_html=True)

        for i, step_data in enumerate(steps):
            step_name_sidebar = step_data['name'] if isinstance(step_data, dict) else step_data.get('name', f'Step {i+1}')
            is_current = i == current_step
            is_completed = i < current_step
            is_saved = f'step_{i}' in st.session_state.workflow_data

            icon = "✅" if is_completed else ("🔵" if is_current else "⚪")
            color = "#10B981" if is_completed else ("#8B5CF6" if is_current else "#6B7280")

            st.markdown(f"""
            <div style="
                padding: 0.75rem;
                margin-bottom: 0.5rem;
                border-left: 3px solid {color};
                background: {'rgba(139, 92, 246, 0.1)' if is_current else 'transparent'};
                border-radius: 4px;
            ">
                <div style="color: {color}; font-weight: {'700' if is_current else '500'};">
                    {icon} Step {i+1}: {step_name_sidebar}
                </div>
                {f'<div style="color: #10B981; font-size: 0.75rem; margin-top: 0.25rem;">📝 Saved</div>' if is_saved else ''}
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        if st.button("❌ Exit Workflow", use_container_width=True):
            if st.session_state.workflow_data:
                st.warning("You have unsaved progress. Are you sure?")
            st.session_state.active_workflow = None
            st.session_state.current_step = 0
            st.session_state.workflow_data = {}
            st.rerun()

# ==================== FOOTER ====================

st.markdown("""
<div style="
    text-align: center;
    color: #6B7280;
    font-size: 0.875rem;
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid rgba(139, 92, 246, 0.2);
">
    <p>Need a custom workflow? <a href="mailto:support@example.com" style="color: #8B5CF6;">Contact us</a></p>
</div>
""", unsafe_allow_html=True)
