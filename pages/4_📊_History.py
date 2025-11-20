"""
History Page - Simplified Prototype
View and manage past prompt optimization sessions
"""
import streamlit as st
from core.config import Config
from core.database import DatabaseManager, PromptSession, SessionLocal
from utils.ui_components import load_custom_css, gradient_header
from datetime import datetime, timedelta

# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="History | AI Prompt Optimizer",
    page_icon="📊",
    layout="wide"
)

# Load custom CSS
load_custom_css()

# ==================== HEADER ====================

gradient_header(
    "📊 Your History",
    size="h1",
    subtitle="Review your past optimization sessions"
)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== LOAD SESSIONS ====================

try:
    with SessionLocal() as db:
        # Get all sessions (for demo, we're not filtering by user)
        sessions = db.query(PromptSession).order_by(PromptSession.created_at.desc()).limit(50).all()
        total_sessions = db.query(PromptSession).count()

        # Calculate stats
        if total_sessions > 0:
            avg_clarity = db.query(PromptSession).filter(PromptSession.clarity_score.isnot(None)).all()
            avg_clarity_score = sum(s.clarity_score for s in avg_clarity) / len(avg_clarity) if avg_clarity else 0

            avg_safety = db.query(PromptSession).filter(PromptSession.safety_score.isnot(None)).all()
            avg_safety_score = sum(s.safety_score for s in avg_safety) / len(avg_safety) if avg_safety else 0

            # Sessions by task type
            task_counts = {}
            for session in sessions:
                task_counts[session.task_type] = task_counts.get(session.task_type, 0) + 1
            most_common_task = max(task_counts.items(), key=lambda x: x[1])[0] if task_counts else "N/A"
        else:
            avg_clarity_score = 0
            avg_safety_score = 0
            most_common_task = "N/A"

except Exception as e:
    st.error(f"Error loading history: {str(e)}")
    sessions = []
    total_sessions = 0
    avg_clarity_score = 0
    avg_safety_score = 0
    most_common_task = "N/A"

# ==================== STATS OVERVIEW ====================

st.subheader("📈 Overview")

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.metric("Total Sessions", total_sessions)

with stat_col2:
    st.metric("Avg Clarity", f"{int(avg_clarity_score)}/100")

with stat_col3:
    st.metric("Avg Safety", f"{int(avg_safety_score)}/100")

with stat_col4:
    most_common_display = Config.TASK_TYPES.get(most_common_task, most_common_task)
    st.metric("Most Used", most_common_display[:15] + "..." if len(most_common_display) > 15 else most_common_display)

st.divider()

# ==================== FILTERS ====================

st.subheader("🔍 Filter History")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    task_filter = st.selectbox(
        "Task Type",
        options=["All"] + list(Config.TASK_TYPES.keys()),
        format_func=lambda x: "All Tasks" if x == "All" else Config.TASK_TYPES.get(x, x),
        key="history_task_filter"
    )

with filter_col2:
    role_filter = st.selectbox(
        "Role",
        options=["All"] + list(Config.ACADEMIC_ROLES.keys()) + list(Config.PROFESSIONAL_ROLES.keys()),
        format_func=lambda x: "All Roles" if x == "All" else Config.ACADEMIC_ROLES.get(x, Config.PROFESSIONAL_ROLES.get(x, x)),
        key="history_role_filter"
    )

with filter_col3:
    date_range = st.selectbox(
        "Time Period",
        options=["All Time", "Last 7 Days", "Last 30 Days", "Last 3 Months"],
        key="history_date_filter"
    )

# Apply filters
filtered_sessions = sessions.copy() if sessions else []

if task_filter != "All":
    filtered_sessions = [s for s in filtered_sessions if s.task_type == task_filter]

if role_filter != "All":
    filtered_sessions = [s for s in filtered_sessions if s.role == role_filter]

if date_range != "All Time":
    days_map = {"Last 7 Days": 7, "Last 30 Days": 30, "Last 3 Months": 90}
    cutoff_date = datetime.utcnow() - timedelta(days=days_map[date_range])
    filtered_sessions = [s for s in filtered_sessions if s.created_at >= cutoff_date]

st.divider()

# ==================== SESSIONS LIST ====================

if filtered_sessions:
    st.info(f"📊 Showing **{len(filtered_sessions)}** session(s)")

    st.markdown("<br>", unsafe_allow_html=True)

    for idx, session in enumerate(filtered_sessions):
        # Time ago calculation
        time_diff = datetime.utcnow() - session.created_at
        if time_diff.days > 0:
            time_ago = f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
        elif time_diff.seconds // 3600 > 0:
            hours = time_diff.seconds // 3600
            time_ago = f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            minutes = time_diff.seconds // 60
            time_ago = f"{minutes} minute{'s' if minutes > 1 else ''} ago"

        # Session container
        with st.container():
            # Header row with time
            header_col1, header_col2 = st.columns([10, 2])

            with header_col1:
                st.markdown(f"**Session #{idx + 1}**")

            with header_col2:
                st.caption(time_ago)

            # Meta info using columns
            meta_col1, meta_col2, meta_col3, meta_col4 = st.columns([2, 2, 2, 6])

            with meta_col1:
                task_display = Config.TASK_TYPES.get(session.task_type, session.task_type)
                st.markdown(f"**Task:** {task_display}")

            with meta_col2:
                role_display = Config.ACADEMIC_ROLES.get(session.role, Config.PROFESSIONAL_ROLES.get(session.role, session.role))
                st.markdown(f"**Role:** {role_display}")

            with meta_col3:
                if session.field:
                    st.markdown(f"**Field:** {session.field}")

            # Prompt preview
            prompt_preview = session.raw_prompt[:150] + "..." if len(session.raw_prompt) > 150 else session.raw_prompt
            st.markdown(f"_{prompt_preview}_")

            # Scores row
            score_col1, score_col2, score_col3 = st.columns(3)

            with score_col1:
                clarity_color = "🟢" if session.clarity_score and session.clarity_score >= 70 else "🟡" if session.clarity_score and session.clarity_score >= 50 else "🔴"
                st.markdown(f"{clarity_color} **Clarity:** {session.clarity_score if session.clarity_score else 'N/A'}")

            with score_col2:
                safety_color = "🟢" if session.safety_score and session.safety_score >= 70 else "🟡" if session.safety_score and session.safety_score >= 50 else "🔴"
                st.markdown(f"{safety_color} **Safety:** {session.safety_score if session.safety_score else 'N/A'}")

            with score_col3:
                version_count = len(session.versions) if hasattr(session, 'versions') else 0
                st.markdown(f"📄 **Versions:** {version_count}")

            # Expandable details
            with st.expander("📋 View Full Details"):
                detail_col1, detail_col2 = st.columns([2, 1])

                with detail_col1:
                    st.markdown("**Original Prompt:**")
                    st.code(session.raw_prompt, language=None)

                    # Show optimized versions if available
                    if hasattr(session, 'versions') and session.versions:
                        st.markdown("**Optimized Versions:**")
                        for version in session.versions:
                            version_info = Config.VERSION_LABELS.get(version.label, {
                                'name': version.label,
                                'icon': '📝',
                                'color': '#8B5CF6'
                            })

                            with st.expander(f"{version_info.get('icon', '📝')} {version_info.get('name', version.label)}"):
                                st.code(version.optimized_prompt, language=None)

                with detail_col2:
                    st.markdown("**Session Info:**")

                    st.markdown(f"**Created:** {session.created_at.strftime('%Y-%m-%d %H:%M')}")

                    if session.intent:
                        st.markdown(f"**Intent:** {session.intent}")

                    if session.field:
                        st.markdown(f"**Field:** {session.field}")

                    if session.risks:
                        st.markdown("**⚠️ Risks:**")
                        for risk in session.risks:
                            st.markdown(f"- {risk}")

                    if session.suggestions:
                        st.markdown("**💡 Suggestions:**")
                        for suggestion in session.suggestions:
                            st.markdown(f"- {suggestion}")

            st.divider()

else:
    # No sessions found
    st.warning("📭 No sessions found matching your criteria")

    if st.button("🎯 Go to Prompt Lab", type="primary"):
        st.switch_page("pages/1_🎯_Prompt_Lab.py")

# ==================== INSIGHTS ====================

if total_sessions > 5:
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.subheader("💡 Your Insights")

    insight_col1, insight_col2 = st.columns(2)

    with insight_col1:
        st.success("✅ **Your Progress**\n\nYour average clarity score has improved! You're getting better at writing specific, well-structured prompts.")

    with insight_col2:
        st.info(f"🎯 **Most Common Task**\n\nYou use this tool most for **{Config.TASK_TYPES.get(most_common_task, most_common_task)}**. Check out our templates page!")

# ==================== FOOTER ====================

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("💡 **Prototype Version** - Session history and analytics")
