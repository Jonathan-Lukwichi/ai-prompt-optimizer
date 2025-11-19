"""
Templates Library
Browse and use pre-built prompt templates
"""
import streamlit as st
from core.config import Config
from core.database import DatabaseManager, PromptTemplate
from utils.ui_components import load_custom_css, gradient_header, feature_card

# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Templates | AI Prompt Optimizer",
    page_icon="📚",
    layout="wide"
)

# Load custom CSS
load_custom_css()

# ==================== HEADER ====================

gradient_header(
    "📚 Prompt Templates",
    size="h1",
    subtitle="Pre-built, field-tested templates for common academic tasks"
)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== FILTERS ====================

st.markdown("""
<h3 style="color: #8B5CF6; font-weight: 700; margin-bottom: 1rem;">
🔍 Filter Templates
</h3>
""", unsafe_allow_html=True)

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    role_filter = st.selectbox(
        "Academic Role",
        options=["All"] + list(Config.ACADEMIC_ROLES.keys()),
        format_func=lambda x: "All Roles" if x == "All" else Config.ACADEMIC_ROLES.get(x, x),
        key="role_filter"
    )

with filter_col2:
    task_filter = st.selectbox(
        "Task Type",
        options=["All"] + list(Config.TASK_TYPES.keys()),
        format_func=lambda x: "All Tasks" if x == "All" else Config.TASK_TYPES.get(x, x),
        key="task_filter"
    )

with filter_col3:
    search = st.text_input(
        "Search",
        placeholder="Search templates...",
        key="search_templates"
    )

st.divider()

# ==================== LOAD TEMPLATES ====================

try:
    # Get templates from database
    templates = DatabaseManager.get_templates(
        role=None if role_filter == "All" else role_filter,
        task_type=None if task_filter == "All" else task_filter
    )

    # Filter by search
    if search:
        templates = [t for t in templates if search.lower() in t.name.lower() or search.lower() in t.description.lower()]

except Exception as e:
    st.error(f"Error loading templates: {str(e)}")
    templates = []

# ==================== DISPLAY TEMPLATES ====================

if templates:
    st.markdown(f"""
    <p style="color: #9CA3AF; margin-bottom: 2rem;">
    Found <strong style="color: #8B5CF6;">{len(templates)}</strong> template(s)
    </p>
    """, unsafe_allow_html=True)

    for template in templates:
        # Template card
        st.markdown(f"""
        <div style="
            background: rgba(26, 27, 61, 0.5);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(139, 92, 246, 0.2);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
        " onmouseover="this.style.borderColor='rgba(139, 92, 246, 0.5)'; this.style.transform='translateY(-2px)'"
           onmouseout="this.style.borderColor='rgba(139, 92, 246, 0.2)'; this.style.transform='translateY(0)'">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                <div>
                    <h3 style="
                        color: #E5E7EB;
                        font-size: 1.5rem;
                        font-weight: 700;
                        margin-bottom: 0.5rem;
                    ">{template.name}</h3>
                    <p style="color: #9CA3AF; margin: 0;">
                        {template.description}
                    </p>
                </div>
            </div>

            <div style="display: flex; gap: 1rem; margin-bottom: 1.5rem;">
                <span style="
                    background: rgba(139, 92, 246, 0.2);
                    color: #8B5CF6;
                    padding: 0.25rem 0.75rem;
                    border-radius: 20px;
                    font-size: 0.875rem;
                    font-weight: 600;
                ">{Config.ACADEMIC_ROLES.get(template.role, template.role)}</span>

                <span style="
                    background: rgba(59, 130, 246, 0.2);
                    color: #3B82F6;
                    padding: 0.25rem 0.75rem;
                    border-radius: 20px;
                    font-size: 0.875rem;
                    font-weight: 600;
                ">{Config.TASK_TYPES.get(template.task_type, template.task_type)}</span>

                {f'''<span style="
                    background: rgba(16, 185, 129, 0.2);
                    color: #10B981;
                    padding: 0.25rem 0.75rem;
                    border-radius: 20px;
                    font-size: 0.875rem;
                    font-weight: 600;
                ">{template.field}</span>''' if template.field else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Expandable template content
        with st.expander(f"📝 View Template: {template.name}"):
            st.markdown(f"""
            <div style="
                background: rgba(37, 39, 80, 0.5);
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1rem;
            ">
                <pre style="
                    color: #E5E7EB;
                    white-space: pre-wrap;
                    font-family: 'JetBrains Mono', monospace;
                    margin: 0;
                    line-height: 1.6;
                ">{template.base_prompt}</pre>
            </div>
            """, unsafe_allow_html=True)

            # Actions
            action_col1, action_col2 = st.columns([3, 1])

            with action_col1:
                if st.button(f"🎯 Use in Prompt Lab", key=f"use_{template.id}", use_container_width=True, type="primary"):
                    # Store template in session state and navigate to Prompt Lab
                    st.session_state.template_prompt = template.base_prompt
                    st.session_state.template_role = template.role
                    st.session_state.template_task = template.task_type
                    st.switch_page("pages/1_🎯_Prompt_Lab.py")

            with action_col2:
                if st.button(f"📋 Copy", key=f"copy_{template.id}", use_container_width=True):
                    st.toast(f"✅ Template copied!", icon="✅")

        st.markdown("<br>", unsafe_allow_html=True)

else:
    # No templates found
    st.markdown("""
    <div style="
        text-align: center;
        padding: 4rem 2rem;
        background: rgba(26, 27, 61, 0.3);
        border-radius: 16px;
        border: 2px dashed rgba(139, 92, 246, 0.3);
        margin: 2rem 0;
    ">
        <div style="font-size: 4rem; margin-bottom: 1rem;">📭</div>
        <h3 style="color: #E5E7EB; margin-bottom: 1rem;">No templates found</h3>
        <p style="color: #9CA3AF;">
            Try adjusting your filters or create your own template!
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==================== FEATURED TEMPLATES ====================

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
">✨ Featured Templates</h2>
""", unsafe_allow_html=True)

featured_col1, featured_col2, featured_col3 = st.columns(3)

with featured_col1:
    st.markdown("""
    <div style="
        background: rgba(26, 27, 61, 0.5);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        height: 100%;
    ">
        <div style="font-size: 2.5rem; margin-bottom: 1rem;">📖</div>
        <h3 style="color: #8B5CF6; font-size: 1.25rem; font-weight: 700; margin-bottom: 0.5rem;">
            Literature Review
        </h3>
        <p style="color: #9CA3AF; font-size: 0.95rem; margin-bottom: 1rem;">
            Comprehensive framework for conducting systematic literature reviews
        </p>
        <div style="
            background: rgba(139, 92, 246, 0.1);
            padding: 0.5rem;
            border-radius: 8px;
            font-size: 0.875rem;
            color: #9CA3AF;
        ">
            Most popular for PhD students
        </div>
    </div>
    """, unsafe_allow_html=True)

with featured_col2:
    st.markdown("""
    <div style="
        background: rgba(26, 27, 61, 0.5);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        height: 100%;
    ">
        <div style="font-size: 2.5rem; margin-bottom: 1rem;">📄</div>
        <h3 style="color: #3B82F6; font-size: 1.25rem; font-weight: 700; margin-bottom: 0.5rem;">
            Paper Summary
        </h3>
        <p style="color: #9CA3AF; font-size: 0.95rem; margin-bottom: 1rem;">
            Structured approach to summarizing academic papers effectively
        </p>
        <div style="
            background: rgba(59, 130, 246, 0.1);
            padding: 0.5rem;
            border-radius: 8px;
            font-size: 0.875rem;
            color: #9CA3AF;
        ">
            Great for all levels
        </div>
    </div>
    """, unsafe_allow_html=True)

with featured_col3:
    st.markdown("""
    <div style="
        background: rgba(26, 27, 61, 0.5);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        height: 100%;
    ">
        <div style="font-size: 2.5rem; margin-bottom: 1rem;">💬</div>
        <h3 style="color: #10B981; font-size: 1.25rem; font-weight: 700; margin-bottom: 0.5rem;">
            Reviewer Response
        </h3>
        <p style="color: #9CA3AF; font-size: 0.95rem; margin-bottom: 1rem;">
            Professional framework for responding to peer review comments
        </p>
        <div style="
            background: rgba(16, 185, 129, 0.1);
            padding: 0.5rem;
            border-radius: 8px;
            font-size: 0.875rem;
            color: #9CA3AF;
        ">
            For researchers publishing
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== CREATE YOUR OWN ====================

st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()

st.markdown("""
<h2 style="
    background: linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800;
    margin: 2rem 0 1.5rem;
">➕ Create Your Own Template</h2>
<p style="color: #9CA3AF; font-size: 1.1rem; margin-bottom: 2rem;">
    Have a prompt that works well? Save it as a template for future use!
</p>
""", unsafe_allow_html=True)

with st.expander("✏️ Create New Template"):
    st.markdown("<br>", unsafe_allow_html=True)

    # Template form
    template_col1, template_col2 = st.columns(2)

    with template_col1:
        new_name = st.text_input(
            "Template Name",
            placeholder="e.g., My Methodology Template",
            key="new_template_name"
        )

        new_role = st.selectbox(
            "Target Role",
            options=list(Config.ACADEMIC_ROLES.keys()),
            format_func=lambda x: Config.ACADEMIC_ROLES[x],
            key="new_template_role"
        )

    with template_col2:
        new_task = st.selectbox(
            "Task Type",
            options=list(Config.TASK_TYPES.keys()),
            format_func=lambda x: Config.TASK_TYPES[x],
            key="new_template_task"
        )

        new_field = st.text_input(
            "Field (Optional)",
            placeholder="e.g., Computer Science",
            key="new_template_field"
        )

    new_description = st.text_area(
        "Description",
        placeholder="Describe what this template is for and when to use it...",
        height=80,
        key="new_template_description"
    )

    new_prompt = st.text_area(
        "Template Prompt",
        placeholder="Enter your template prompt here. Use [PLACEHOLDERS] in ALL CAPS for variables...",
        height=200,
        key="new_template_prompt"
    )

    st.markdown("""
    <div style="
        background: rgba(59, 130, 246, 0.1);
        border-left: 3px solid #3B82F6;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    ">
        <strong style="color: #3B82F6;">💡 Tip:</strong><br>
        <span style="color: #9CA3AF;">
        Use placeholders like [TOPIC], [FIELD], [BACKGROUND], etc. in your template.
        This makes it easy to customize for different situations.
        </span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💾 Save Template", type="primary", disabled=not (new_name and new_prompt)):
        try:
            DatabaseManager.create_template(
                name=new_name,
                description=new_description or "",
                role=new_role,
                task_type=new_task,
                base_prompt=new_prompt,
                field=new_field or None,
                is_public=True
            )
            st.success("✅ Template saved successfully!")
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error saving template: {str(e)}")

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
    <p>Templates are community-contributed and continuously improved</p>
    <p style="margin-top: 0.5rem;">
        Have feedback on a template? <a href="mailto:support@example.com" style="color: #8B5CF6;">Let us know</a>
    </p>
</div>
""", unsafe_allow_html=True)
