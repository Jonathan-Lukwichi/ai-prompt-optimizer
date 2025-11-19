"""
History Page
View and manage past prompt optimization sessions
"""
import streamlit as st
from core.config import Config
from core.database import DatabaseManager, PromptSession, SessionLocal
from utils.ui_components import load_custom_css, gradient_header, metric_card, score_gauge
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
    subtitle="Review your past optimization sessions and track your progress"
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

st.markdown("""
<h3 style="color: #8B5CF6; font-weight: 700; margin-bottom: 1.5rem;">
📈 Overview
</h3>
""", unsafe_allow_html=True)

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    metric_card(
        label="Total Sessions",
        value=str(total_sessions),
        icon="🎯",
        color="#8B5CF6"
    )

with stat_col2:
    metric_card(
        label="Avg Clarity",
        value=f"{int(avg_clarity_score)}/100",
        icon="📊",
        color="#3B82F6"
    )

with stat_col3:
    metric_card(
        label="Avg Safety",
        value=f"{int(avg_safety_score)}/100",
        icon="🛡️",
        color="#10B981"
    )

with stat_col4:
    metric_card(
        label="Most Used Task",
        value=Config.TASK_TYPES.get(most_common_task, most_common_task)[:15] + "...",
        icon="🔥",
        color="#EC4899"
    )

st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()

# ==================== FILTERS ====================

st.markdown("""
<h3 style="color: #8B5CF6; font-weight: 700; margin: 2rem 0 1rem;">
🔍 Filter History
</h3>
""", unsafe_allow_html=True)

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
        "Academic Role",
        options=["All"] + list(Config.ACADEMIC_ROLES.keys()),
        format_func=lambda x: "All Roles" if x == "All" else Config.ACADEMIC_ROLES.get(x, x),
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
    st.markdown(f"""
    <p style="color: #9CA3AF; margin-bottom: 2rem;">
    Showing <strong style="color: #8B5CF6;">{len(filtered_sessions)}</strong> session(s)
    </p>
    """, unsafe_allow_html=True)

    for session in filtered_sessions:
        # Time ago
        time_diff = datetime.utcnow() - session.created_at
        if time_diff.days > 0:
            time_ago = f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
        elif time_diff.seconds // 3600 > 0:
            hours = time_diff.seconds // 3600
            time_ago = f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            minutes = time_diff.seconds // 60
            time_ago = f"{minutes} minute{'s' if minutes > 1 else ''} ago"

        # Session card
        st.markdown(f"""
        <div style="
            background: rgba(26, 27, 61, 0.5);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(139, 92, 246, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
        " onmouseover="this.style.borderColor='rgba(139, 92, 246, 0.5)'"
           onmouseout="this.style.borderColor='rgba(139, 92, 246, 0.2)'">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                <div style="flex: 1;">
                    <div style="display: flex; gap: 1rem; margin-bottom: 0.5rem;">
                        <span style="
                            background: rgba(139, 92, 246, 0.2);
                            color: #8B5CF6;
                            padding: 0.25rem 0.75rem;
                            border-radius: 20px;
                            font-size: 0.875rem;
                            font-weight: 600;
                        ">{Config.TASK_TYPES.get(session.task_type, session.task_type)}</span>

                        <span style="
                            background: rgba(59, 130, 246, 0.2);
                            color: #3B82F6;
                            padding: 0.25rem 0.75rem;
                            border-radius: 20px;
                            font-size: 0.875rem;
                            font-weight: 600;
                        ">{Config.ACADEMIC_ROLES.get(session.role, session.role)}</span>

                        {f'''<span style="
                            background: rgba(16, 185, 129, 0.2);
                            color: #10B981;
                            padding: 0.25rem 0.75rem;
                            border-radius: 20px;
                            font-size: 0.875rem;
                            font-weight: 600;
                        ">{session.field}</span>''' if session.field else ''}
                    </div>
                    <p style="
                        color: #E5E7EB;
                        font-size: 1rem;
                        margin: 0.5rem 0;
                        line-height: 1.6;
                    ">{session.raw_prompt[:150]}{'...' if len(session.raw_prompt) > 150 else ''}</p>
                </div>
                <div style="
                    color: #9CA3AF;
                    font-size: 0.875rem;
                    margin-left: 1rem;
                    white-space: nowrap;
                ">{time_ago}</div>
            </div>

            <div style="display: flex; gap: 2rem; align-items: center;">
                <div>
                    <span style="color: #9CA3AF; font-size: 0.875rem;">Clarity:</span>
                    <span style="
                        color: {('#10B981' if session.clarity_score and session.clarity_score >= 70 else ('#F59E0B' if session.clarity_score and session.clarity_score >= 50 else '#EF4444'))};
                        font-weight: 700;
                        font-size: 1rem;
                        margin-left: 0.5rem;
                    ">{session.clarity_score if session.clarity_score else 'N/A'}</span>
                </div>
                <div>
                    <span style="color: #9CA3AF; font-size: 0.875rem;">Safety:</span>
                    <span style="
                        color: {('#10B981' if session.safety_score and session.safety_score >= 70 else ('#F59E0B' if session.safety_score and session.safety_score >= 50 else '#EF4444'))};
                        font-weight: 700;
                        font-size: 1rem;
                        margin-left: 0.5rem;
                    ">{session.safety_score if session.safety_score else 'N/A'}</span>
                </div>
                <div>
                    <span style="color: #9CA3AF; font-size: 0.875rem;">Versions:</span>
                    <span style="
                        color: #8B5CF6;
                        font-weight: 700;
                        font-size: 1rem;
                        margin-left: 0.5rem;
                    ">{len(session.versions) if hasattr(session, 'versions') else 0}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Expandable details
        with st.expander(f"📋 View Session Details"):
            detail_col1, detail_col2 = st.columns([2, 1])

            with detail_col1:
                st.markdown("**Original Prompt:**")
                st.markdown(f"""
                <div style="
                    background: rgba(37, 39, 80, 0.5);
                    border-radius: 12px;
                    padding: 1rem;
                    margin-bottom: 1rem;
                ">
                    <pre style="
                        color: #E5E7EB;
                        white-space: pre-wrap;
                        font-family: 'JetBrains Mono', monospace;
                        margin: 0;
                    ">{session.raw_prompt}</pre>
                </div>
                """, unsafe_allow_html=True)

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

                st.markdown(f"""
                <div style="
                    background: rgba(26, 27, 61, 0.5);
                    border-radius: 12px;
                    padding: 1rem;
                    margin-bottom: 1rem;
                ">
                    <div style="margin-bottom: 0.75rem;">
                        <span style="color: #9CA3AF; font-size: 0.875rem;">Created:</span><br>
                        <span style="color: #E5E7EB;">{session.created_at.strftime('%Y-%m-%d %H:%M')}</span>
                    </div>
                    <div style="margin-bottom: 0.75rem;">
                        <span style="color: #9CA3AF; font-size: 0.875rem;">Intent:</span><br>
                        <span style="color: #E5E7EB;">{session.intent if session.intent else 'N/A'}</span>
                    </div>
                    {f'''<div style="margin-bottom: 0.75rem;">
                        <span style="color: #9CA3AF; font-size: 0.875rem;">Field:</span><br>
                        <span style="color: #E5E7EB;">{session.field}</span>
                    </div>''' if session.field else ''}
                </div>
                """, unsafe_allow_html=True)

                if session.risks:
                    st.markdown("**⚠️ Risks:**")
                    for risk in session.risks:
                        st.markdown(f"- {risk}")

                if session.suggestions:
                    st.markdown("**💡 Suggestions:**")
                    for suggestion in session.suggestions:
                        st.markdown(f"- {suggestion}")

        st.markdown("<br>", unsafe_allow_html=True)

else:
    # No sessions found
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
        <h3 style="color: #E5E7EB; margin-bottom: 1rem;">No sessions found</h3>
        <p style="color: #9CA3AF; margin-bottom: 2rem;">
            Start optimizing prompts to build your history!
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🎯 Go to Prompt Lab", type="primary"):
        st.switch_page("pages/1_🎯_Prompt_Lab.py")

# ==================== INSIGHTS ====================

if total_sessions > 5:
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
    ">💡 Your Insights</h2>
    """, unsafe_allow_html=True)

    insight_col1, insight_col2 = st.columns(2)

    with insight_col1:
        st.markdown("""
        <div style="
            background: rgba(26, 27, 61, 0.5);
            backdrop-filter: blur(20px);
            border-left: 4px solid #10B981;
            border-radius: 12px;
            padding: 1.5rem;
        ">
            <h3 style="color: #10B981; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">
            ✅ Your Progress
            </h3>
            <p style="color: #9CA3AF; font-size: 0.95rem; line-height: 1.6; margin: 0;">
            Your average clarity score has improved! You're getting better at writing
            specific, well-structured prompts that get better AI responses.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with insight_col2:
        st.markdown(f"""
        <div style="
            background: rgba(26, 27, 61, 0.5);
            backdrop-filter: blur(20px);
            border-left: 4px solid #8B5CF6;
            border-radius: 12px;
            padding: 1.5rem;
        ">
            <h3 style="color: #8B5CF6; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">
            🎯 Most Common Task
            </h3>
            <p style="color: #9CA3AF; font-size: 0.95rem; line-height: 1.6; margin: 0;">
            You use this tool most for <strong style="color: #E5E7EB;">{Config.TASK_TYPES.get(most_common_task, most_common_task)}</strong>.
            Check out our templates page for pre-built prompts in this category!
            </p>
        </div>
        """, unsafe_allow_html=True)

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
    <p>Your data is stored locally and never shared</p>
</div>
""", unsafe_allow_html=True)
