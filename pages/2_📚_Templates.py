"""
Templates Library & Guided Prompt Builder
Browse templates, build prompts with proven frameworks, and upload context
"""
import streamlit as st
from core.config import Config
from core.database import DatabaseManager, PromptTemplate
from core.prompt_builder import PromptBuilder, PromptComponents, get_framework_guide
from core.user_preferences import get_preferences
from utils.ui_components import load_custom_css, gradient_header
import io

# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Templates & Builder | AI Prompt Optimizer",
    page_icon="📚",
    layout="wide"
)

# Load custom CSS
load_custom_css()

# ==================== SESSION STATE ====================

if 'built_prompt' not in st.session_state:
    st.session_state.built_prompt = ""

if 'uploaded_context' not in st.session_state:
    st.session_state.uploaded_context = None

# ==================== HEADER ====================

gradient_header(
    "📚 Templates & Prompt Builder",
    size="h1",
    subtitle="Browse templates or build perfect prompts with proven frameworks"
)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== MAIN TABS ====================

tab1, tab2, tab3 = st.tabs([
    "🏗️ Guided Prompt Builder",
    "📚 Template Library",
    "💡 AI Suggestions"
])

# ==================== TAB 1: GUIDED PROMPT BUILDER ====================

with tab1:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    ">
        <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">🎯 Build Perfect Prompts</div>
        <div style="color: #9CA3AF; font-size: 0.95rem;">
            Use proven frameworks to construct high-quality prompts step by step.
            <br>Choose between the <strong>6-Step Framework</strong> or <strong>CRAFT Formula</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Framework selection
    framework_choice = st.radio(
        "Choose your framework:",
        options=["📋 6-Step Framework (Role → Context → Task → Format → Rules → Examples)",
                 "🎨 CRAFT Formula (Contexte, Rôle, Action, Format, Thinking mode)"],
        horizontal=False
    )

    framework = "6-step" if "6-Step" in framework_choice else "craft"

    # Get framework guide
    guide = get_framework_guide(framework)

    st.markdown(f"### {guide['name']}")
    st.caption(guide['description'])

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================== CONTEXT UPLOAD SECTION ====================

    with st.expander("📎 Upload Image or Document for Context (Optional)", expanded=False):
        st.markdown("""
        Upload an image or document to extract context automatically. This helps the AI understand your situation better.

        **Supported formats:**
        - 🖼️ Images: JPG, PNG, JPEG
        - 📄 Documents: PDF, DOCX, TXT
        """)

        col_upload1, col_upload2 = st.columns([2, 1])

        with col_upload1:
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=['jpg', 'jpeg', 'png', 'pdf', 'docx', 'txt'],
                help="Upload context to help build your prompt"
            )

        with col_upload2:
            user_query = st.text_input(
                "What should I extract?",
                placeholder="e.g., key findings, main topic",
                help="Optional: specify what context to extract"
            )

        if uploaded_file is not None:
            if st.button("🔍 Extract Context from File", type="primary"):
                with st.spinner("🤖 Analyzing file..."):
                    builder = PromptBuilder()

                    try:
                        file_bytes = uploaded_file.read()

                        # Handle different file types
                        if uploaded_file.type.startswith('image/'):
                            # Image file
                            context = builder.extract_context_from_image(file_bytes, user_query)
                            st.session_state.uploaded_context = context

                        elif uploaded_file.type == 'application/pdf':
                            # PDF file - try to import PyPDF2
                            try:
                                import PyPDF2
                                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                                text = ""
                                for page in pdf_reader.pages:
                                    text += page.extract_text()

                                context = builder.extract_context_from_document(text, user_query)
                                st.session_state.uploaded_context = context
                            except ImportError:
                                st.warning("📦 PyPDF2 not installed. Install with: pip install PyPDF2")
                                # Fallback: try to decode as text
                                try:
                                    text = file_bytes.decode('utf-8', errors='ignore')
                                    context = builder.extract_context_from_document(text, user_query)
                                    st.session_state.uploaded_context = context
                                except:
                                    st.error("Could not process PDF file")

                        elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                            # DOCX file - try to import docx
                            try:
                                import docx
                                doc = docx.Document(io.BytesIO(file_bytes))
                                text = "\n".join([para.text for para in doc.paragraphs])

                                context = builder.extract_context_from_document(text, user_query)
                                st.session_state.uploaded_context = context
                            except ImportError:
                                st.warning("📦 python-docx not installed. Install with: pip install python-docx")

                        elif uploaded_file.type == 'text/plain':
                            # TXT file
                            text = file_bytes.decode('utf-8')
                            context = builder.extract_context_from_document(text, user_query)
                            st.session_state.uploaded_context = context

                        st.success("✅ Context extracted successfully!")

                    except Exception as e:
                        st.error(f"❌ Error processing file: {str(e)}")

        # Display extracted context
        if st.session_state.uploaded_context:
            st.markdown("**📝 Extracted Context:**")
            st.info(st.session_state.uploaded_context)

            if st.button("🗑️ Clear Context"):
                st.session_state.uploaded_context = None
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================== BUILD WITH 6-STEP FRAMEWORK ====================

    if framework == "6-step":
        st.markdown("### 📋 Build Your Prompt - 6 Steps")

        components = PromptComponents()

        # Upload context
        if st.session_state.uploaded_context:
            components.uploaded_context = st.session_state.uploaded_context

        # Step 1: Role
        with st.expander("**Step 1: Role** - Define who the AI should be", expanded=True):
            st.caption(guide['steps'][0]['description'])
            st.markdown(f"**Example:** {guide['steps'][0]['example']}")

            components.role = st.text_area(
                "Role",
                placeholder="e.g., You are an expert data scientist with 10 years of experience...",
                height=80,
                key="role_6step",
                label_visibility="collapsed"
            )

            st.markdown("**💡 Tips:**")
            for tip in guide['steps'][0]['tips']:
                st.markdown(f"- {tip}")

        # Step 2: Context
        with st.expander("**Step 2: Context** - Explain the situation", expanded=False):
            st.caption(guide['steps'][1]['description'])
            st.markdown(f"**Example:** {guide['steps'][1]['example']}")

            components.context = st.text_area(
                "Context",
                placeholder="e.g., I'm working on a project to...",
                height=100,
                key="context_6step",
                label_visibility="collapsed"
            )

            st.markdown("**💡 Tips:**")
            for tip in guide['steps'][1]['tips']:
                st.markdown(f"- {tip}")

        # Step 3: Task
        with st.expander("**Step 3: Task** - State what you expect", expanded=False):
            st.caption(guide['steps'][2]['description'])
            st.markdown(f"**Example:** {guide['steps'][2]['example']}")

            components.task = st.text_area(
                "Task",
                placeholder="e.g., Help me analyze..., Create a plan for..., Explain how to...",
                height=100,
                key="task_6step",
                label_visibility="collapsed"
            )

            st.markdown("**💡 Tips:**")
            for tip in guide['steps'][2]['tips']:
                st.markdown(f"- {tip}")

        # Step 4: Format
        with st.expander("**Step 4: Format** - Specify the output type", expanded=False):
            st.caption(guide['steps'][3]['description'])
            st.markdown(f"**Example:** {guide['steps'][3]['example']}")

            components.format = st.text_area(
                "Format",
                placeholder="e.g., Provide a structured table with..., Write 3 paragraphs..., List 5 key points...",
                height=80,
                key="format_6step",
                label_visibility="collapsed"
            )

            st.markdown("**💡 Tips:**")
            for tip in guide['steps'][3]['tips']:
                st.markdown(f"- {tip}")

        # Step 5: Rules
        with st.expander("**Step 5: Rules** - Set constraints", expanded=False):
            st.caption(guide['steps'][4]['description'])
            st.markdown(f"**Example:** {guide['steps'][4]['example']}")

            components.rules = st.text_area(
                "Rules/Constraints",
                placeholder="e.g., Focus only on..., Avoid..., Must include...",
                height=80,
                key="rules_6step",
                label_visibility="collapsed"
            )

            st.markdown("**💡 Tips:**")
            for tip in guide['steps'][4]['tips']:
                st.markdown(f"- {tip}")

        # Step 6: Examples
        with st.expander("**Step 6: Examples** - Provide references", expanded=False):
            st.caption(guide['steps'][5]['description'])
            st.markdown(f"**Example:** {guide['steps'][5]['example']}")

            components.examples = st.text_area(
                "Examples/References",
                placeholder="e.g., Similar to..., Like in the case of..., For example...",
                height=80,
                key="examples_6step",
                label_visibility="collapsed"
            )

            st.markdown("**💡 Tips:**")
            for tip in guide['steps'][5]['tips']:
                st.markdown(f"- {tip}")

        # Build button
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🏗️ Build Prompt from 6-Step Framework", type="primary", use_container_width=True):
            builder = PromptBuilder()
            st.session_state.built_prompt = builder.build_from_6_step(components)
            st.success("✅ Prompt built successfully!")

    # ==================== BUILD WITH CRAFT FORMULA ====================

    else:  # CRAFT
        st.markdown("### 🎨 Build Your Prompt - CRAFT Formula")

        components = PromptComponents()

        # Upload context
        if st.session_state.uploaded_context:
            components.uploaded_context = st.session_state.uploaded_context

        # Contexte
        with st.expander("**C - Contexte** - La situation", expanded=True):
            st.caption(guide['steps'][0]['description'])
            st.markdown(f"**Exemple:** {guide['steps'][0]['example']}")

            components.craft_context = st.text_area(
                "Contexte",
                placeholder="e.g., Je prépare une présentation...",
                height=100,
                key="context_craft",
                label_visibility="collapsed"
            )

            st.markdown("**💡 Conseils:**")
            for tip in guide['steps'][0]['tips']:
                st.markdown(f"- {tip}")

        # Rôle
        with st.expander("**R - Rôle** - Qui doit être l'IA", expanded=False):
            st.caption(guide['steps'][1]['description'])
            st.markdown(f"**Exemple:** {guide['steps'][1]['example']}")

            components.craft_role = st.text_area(
                "Rôle",
                placeholder="e.g., Tu es un consultant en...",
                height=80,
                key="role_craft",
                label_visibility="collapsed"
            )

            st.markdown("**💡 Conseils:**")
            for tip in guide['steps'][1]['tips']:
                st.markdown(f"- {tip}")

        # Action
        with st.expander("**A - Action** - L'action attendue", expanded=False):
            st.caption(guide['steps'][2]['description'])
            st.markdown(f"**Exemple:** {guide['steps'][2]['example']}")

            components.craft_action = st.text_area(
                "Action",
                placeholder="e.g., Crée un plan..., Analyse..., Explique...",
                height=100,
                key="action_craft",
                label_visibility="collapsed"
            )

            st.markdown("**💡 Conseils:**")
            for tip in guide['steps'][2]['tips']:
                st.markdown(f"- {tip}")

        # Format
        with st.expander("**F - Format** - Le type de sortie", expanded=False):
            st.caption(guide['steps'][3]['description'])
            st.markdown(f"**Exemple:** {guide['steps'][3]['example']}")

            components.craft_format = st.text_area(
                "Format",
                placeholder="e.g., Liste numérotée avec..., Tableau comparatif...",
                height=80,
                key="format_craft",
                label_visibility="collapsed"
            )

            st.markdown("**💡 Conseils:**")
            for tip in guide['steps'][3]['tips']:
                st.markdown(f"- {tip}")

        # Thinking mode
        with st.expander("**T - Thinking mode** - Mode de réflexion", expanded=False):
            st.caption(guide['steps'][4]['description'])
            st.markdown(f"**Exemple:** {guide['steps'][4]['example']}")

            components.craft_thinking_mode = st.text_area(
                "Thinking mode",
                placeholder="e.g., Réfléchis de manière stratégique..., Analyse en profondeur...",
                height=80,
                key="thinking_craft",
                label_visibility="collapsed"
            )

            st.markdown("**💡 Conseils:**")
            for tip in guide['steps'][4]['tips']:
                st.markdown(f"- {tip}")

        # Build button
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🎨 Build Prompt from CRAFT Formula", type="primary", use_container_width=True):
            builder = PromptBuilder()
            st.session_state.built_prompt = builder.build_from_craft(components)
            st.success("✅ Prompt construit avec succès!")

    # ==================== DISPLAY BUILT PROMPT ====================

    if st.session_state.built_prompt:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📝 Your Constructed Prompt")

        st.code(st.session_state.built_prompt, language=None)

        # Validate button
        col_v1, col_v2, col_v3, col_v4 = st.columns(4)

        with col_v1:
            if st.button("✅ Validate Quality", use_container_width=True):
                with st.spinner("🤖 Validating prompt quality..."):
                    builder = PromptBuilder()
                    validation = builder.validate_prompt(st.session_state.built_prompt)

                    st.markdown(f"### Quality Score: {validation['score']}/100")

                    if validation['score'] >= 80:
                        st.success("🌟 Excellent prompt!")
                    elif validation['score'] >= 60:
                        st.info("✅ Good prompt, room for improvement")
                    else:
                        st.warning("⚠️ Needs improvement")

                    if validation['strengths']:
                        st.markdown("**💪 Strengths:**")
                        for strength in validation['strengths']:
                            st.markdown(f"- {strength}")

                    if validation['weaknesses']:
                        st.markdown("**⚠️ Weaknesses:**")
                        for weakness in validation['weaknesses']:
                            st.markdown(f"- {weakness}")

                    if validation['recommendations']:
                        st.markdown("**💡 Recommendations:**")
                        for rec in validation['recommendations']:
                            st.markdown(f"- {rec}")

        with col_v2:
            if st.button("🎯 Use in Prompt Lab", use_container_width=True):
                st.session_state.prefill_prompt = st.session_state.built_prompt
                st.success("✅ Prompt loaded! Redirecting...")
                st.switch_page("pages/1_🎯_Prompt_Lab.py")

        with col_v3:
            if st.button("📋 Copy", use_container_width=True):
                st.toast("✅ Copied to clipboard!", icon="✅")

        with col_v4:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.built_prompt = ""
                st.rerun()

# ==================== TAB 2: TEMPLATE LIBRARY ====================

with tab2:
    st.markdown("### 🔍 Browse Templates")

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

    # Load templates
    try:
        templates = DatabaseManager.get_templates(
            role=None if role_filter == "All" else role_filter,
            task_type=None if task_filter == "All" else task_filter
        )

        if search:
            templates = [t for t in templates if search.lower() in t.name.lower() or search.lower() in t.description.lower()]

    except Exception as e:
        st.error(f"Error loading templates: {str(e)}")
        templates = []

    # Display templates
    if templates:
        st.info(f"📊 Found **{len(templates)}** template(s)")

        for template in templates:
            with st.container():
                st.markdown(f"### {template.name}")
                st.markdown(f"_{template.description}_")

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

                with st.expander("📝 View Template"):
                    st.code(template.base_prompt, language=None)

                    btn_col1, btn_col2 = st.columns(2)

                    with btn_col1:
                        if st.button("🎯 Use in Prompt Lab", key=f"use_{template.id}", type="primary"):
                            st.session_state.template_prompt = template.base_prompt
                            st.session_state.template_role = template.role
                            st.session_state.template_task = template.task_type
                            st.switch_page("pages/1_🎯_Prompt_Lab.py")

                    with btn_col2:
                        if st.button("📋 Copy", key=f"copy_{template.id}"):
                            st.toast("✅ Copied!", icon="✅")

                st.divider()

    else:
        st.warning("📭 No templates found")

# ==================== TAB 3: AI SUGGESTIONS ====================

with tab3:
    st.markdown("### 💡 AI-Powered Template Suggestions")

    st.markdown("""
    Get personalized template suggestions based on your needs and usage history.
    """)

    # Get user preferences
    prefs = get_preferences()
    stats = prefs.get_usage_stats()

    if stats['total_optimizations'] > 0:
        st.info(f"📊 Based on your **{stats['total_optimizations']} optimizations**, we'll suggest relevant templates")

    # Input for suggestions
    col_s1, col_s2 = st.columns(2)

    with col_s1:
        suggest_role = st.text_input(
            "What role do you need?",
            placeholder="e.g., data scientist, teacher, developer",
            key="suggest_role"
        )

    with col_s2:
        suggest_task = st.text_input(
            "What task?",
            placeholder="e.g., analyze data, explain concept, debug code",
            key="suggest_task"
        )

    if st.button("🤖 Get AI Suggestions", type="primary"):
        if suggest_role or suggest_task:
            with st.spinner("🤖 Generating personalized suggestions..."):
                builder = PromptBuilder()
                components = PromptComponents()
                components.role = suggest_role
                components.task = suggest_task

                user_prefs = {
                    'preferred_domain': prefs.get_preferred_domain(),
                    'preferred_role': prefs.get_preferred_role(),
                    'preferred_task': prefs.get_preferred_task()
                }

                suggestions = builder.get_template_suggestions(components, user_prefs)

                if suggestions:
                    st.markdown("### 🎯 Suggested Templates for You")

                    for idx, template in enumerate(suggestions, 1):
                        with st.expander(f"💡 {template['name']}", expanded=idx==1):
                            st.markdown(f"**When to use:** {template['description']}")
                            st.markdown("**Template:**")
                            st.code(template['content'], language=None)

                            if st.button(f"🎯 Use This Template", key=f"use_suggest_{idx}"):
                                st.session_state.prefill_prompt = template['content']
                                st.switch_page("pages/1_🎯_Prompt_Lab.py")
        else:
            st.warning("⚠️ Please provide at least a role or task")

# ==================== FOOTER ====================

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
### 📖 Framework Resources

**6-Step Framework** benefits:
- Clear structure for any prompt
- Comprehensive coverage of all elements
- Easy to follow and repeat
- Works for simple and complex prompts

**CRAFT Formula** benefits:
- Focus on thinking mode
- French-friendly approach
- Emphasizes reasoning style
- Great for strategic tasks

**Tips for Success:**
- Start with context - it guides everything else
- Be specific in your task description
- Include examples when possible
- Upload relevant files for better context
- Validate your prompt before using it
""")
