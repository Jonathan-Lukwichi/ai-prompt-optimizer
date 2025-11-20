"""
Templates Library - Simplified Prototype
Browse and use pre-built prompt templates
"""
import streamlit as st
from core.config import Config
from core.database import DatabaseManager, PromptTemplate
from utils.ui_components import load_custom_css, gradient_header

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
    subtitle="Pre-built templates for common tasks"
)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== FILTERS ====================

st.subheader("🔍 Filter Templates")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    role_filter = st.selectbox(
        "Role",
        options=["All"] + list(Config.ACADEMIC_ROLES.keys()) + list(Config.PROFESSIONAL_ROLES.keys()),
        format_func=lambda x: "All Roles" if x == "All" else Config.ACADEMIC_ROLES.get(x, Config.PROFESSIONAL_ROLES.get(x, x)),
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
    st.info(f"📊 Found **{len(templates)}** template(s)")

    st.markdown("<br>", unsafe_allow_html=True)

    for idx, template in enumerate(templates):
        # Create a container for each template
        with st.container():
            # Template header
            st.markdown(f"### {template.name}")
            st.markdown(f"_{template.description}_")

            # Badges using columns for clean display
            badge_col1, badge_col2, badge_col3, badge_col4 = st.columns([2, 2, 2, 6])

            with badge_col1:
                role_display = Config.ACADEMIC_ROLES.get(template.role, Config.PROFESSIONAL_ROLES.get(template.role, template.role))
                st.markdown(f"**Role:** {role_display}")

            with badge_col2:
                task_display = Config.TASK_TYPES.get(template.task_type, template.task_type)
                st.markdown(f"**Task:** {task_display}")

            with badge_col3:
                if template.field:
                    st.markdown(f"**Field:** {template.field}")

            # Expandable template content
            with st.expander("📝 View Template Content"):
                st.code(template.base_prompt, language=None)

                # Action buttons
                btn_col1, btn_col2, btn_col3 = st.columns([3, 2, 7])

                with btn_col1:
                    if st.button("🎯 Use in Prompt Lab", key=f"use_{template.id}", type="primary"):
                        # Store template in session state and navigate to Prompt Lab
                        st.session_state.template_prompt = template.base_prompt
                        st.session_state.template_role = template.role
                        st.session_state.template_task = template.task_type
                        st.success("✅ Template loaded! Redirecting to Prompt Lab...")
                        st.switch_page("pages/1_🎯_Prompt_Lab.py")

                with btn_col2:
                    if st.button("📋 Copy", key=f"copy_{template.id}"):
                        st.toast("✅ Template copied to clipboard!", icon="✅")

            st.divider()

else:
    # No templates found
    st.warning("📭 No templates found matching your criteria")
    st.info("💡 Try adjusting your filters or search terms")

# ==================== FOOTER ====================

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("💡 **Prototype Version** - Core functionality for demonstrating prompt template management")
