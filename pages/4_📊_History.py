"""
History Page - Enhanced Analytics Dashboard
View past optimization sessions with comprehensive analytics and insights
"""
import streamlit as st
from core.config import Config
from core.database import DatabaseManager, PromptSession, SessionLocal
from core.user_preferences import get_preferences
from utils.ui_components import load_custom_css, gradient_header
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload
from collections import Counter
import json

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

# ==================== LOAD DATA ====================

# Load user preferences for analytics
prefs = get_preferences()
prefs_data = DatabaseManager.load_preferences(session_key="default")
if prefs_data and prefs_data.get('total_optimizations', 0) > 0:
    prefs.import_preferences(json.dumps(prefs_data))

try:
    with SessionLocal() as db:
        # Get all sessions with eagerly loaded versions to avoid DetachedInstanceError
        sessions = db.query(PromptSession).options(joinedload(PromptSession.versions)).order_by(PromptSession.created_at.desc()).limit(100).all()
        total_sessions = db.query(PromptSession).count()

        # Calculate comprehensive stats
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

            # Calculate trends and patterns
            domain_counts = Counter()
            role_counts = Counter()
            version_counts = Counter()
            weekly_activity = {}
            clarity_trend = []

            for session in sessions:
                # Domain tracking (from field or inferred)
                if hasattr(session, 'domain') and session.domain:
                    domain_counts[session.domain] += 1

                # Role tracking
                if session.role:
                    role_counts[session.role] += 1

                # Version tracking
                if hasattr(session, 'versions') and session.versions:
                    for version in session.versions:
                        version_counts[version.label] += 1

                # Weekly activity
                week_key = session.created_at.strftime('%Y-W%U')
                weekly_activity[week_key] = weekly_activity.get(week_key, 0) + 1

                # Clarity trend (chronological)
                if session.clarity_score:
                    clarity_trend.append({
                        'date': session.created_at,
                        'score': session.clarity_score
                    })
        else:
            avg_clarity_score = 0
            avg_safety_score = 0
            most_common_task = "N/A"
            domain_counts = Counter()
            role_counts = Counter()
            version_counts = Counter()
            weekly_activity = {}
            clarity_trend = []

        # Detach sessions from the database session to avoid lazy loading issues
        for session in sessions:
            db.expunge(session)

except Exception as e:
    st.error(f"Error loading history: {str(e)}")
    sessions = []
    total_sessions = 0
    avg_clarity_score = 0
    avg_safety_score = 0
    most_common_task = "N/A"
    domain_counts = Counter()
    role_counts = Counter()
    version_counts = Counter()
    weekly_activity = {}
    clarity_trend = []

# ==================== ENHANCED ANALYTICS DASHBOARD ====================

# Create tabs for different views
analytics_tab, history_tab = st.tabs(["📊 Analytics Dashboard", "📜 Session History"])

with analytics_tab:
    if total_sessions == 0:
        st.info("📭 **No data yet!** Start optimizing prompts to see your analytics here.")
        if st.button("🎯 Go to Prompt Lab", type="primary", key="go_to_prompt_lab_analytics"):
            st.switch_page("pages/1_🎯_Prompt_Lab.py")
    else:
        st.markdown("### 📈 Your Optimization Patterns")
        st.markdown("<br>", unsafe_allow_html=True)

        # Top-level metrics
        metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)

        with metric_col1:
            st.metric("Total Optimizations", total_sessions)

        with metric_col2:
            st.metric("Avg Clarity Score", f"{int(avg_clarity_score)}/100")

        with metric_col3:
            st.metric("Avg Safety Score", f"{int(avg_safety_score)}/100")

        with metric_col4:
            # Get preferred version from user preferences
            stats = prefs.get_usage_stats()
            fav_version = stats.get('preferred_version', 'N/A')
            if fav_version != 'N/A':
                fav_display = fav_version.title()
            else:
                fav_display = "N/A"
            st.metric("Favorite Version", fav_display)

        with metric_col5:
            # Calculate average optimizations per week
            if weekly_activity:
                avg_per_week = total_sessions / max(len(weekly_activity), 1)
                st.metric("Avg/Week", f"{avg_per_week:.1f}")
            else:
                st.metric("Avg/Week", "0")

        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()

        # ==================== USAGE PATTERNS ====================

        st.markdown("### 🎯 Usage Patterns")
        st.markdown("<br>", unsafe_allow_html=True)

        pattern_col1, pattern_col2 = st.columns(2)

        with pattern_col1:
            # Domain Distribution
            st.markdown("#### 📊 Domain Distribution")
            if domain_counts or stats.get('domain_usage'):
                # Combine session data with preference data
                combined_domains = domain_counts.copy()
                if stats.get('domain_usage'):
                    for domain, count in stats['domain_usage'].items():
                        combined_domains[domain] = combined_domains.get(domain, 0) + count

                if combined_domains:
                    # Create a simple bar chart using markdown
                    total_domain = sum(combined_domains.values())
                    sorted_domains = combined_domains.most_common(5)

                    for domain, count in sorted_domains:
                        percentage = (count / total_domain) * 100
                        domain_name = Config.DOMAINS.get(domain, {}).get('name', domain.replace('-', ' ').title())
                        bar_length = int(percentage / 2)  # Scale to 50 chars max
                        bar = "█" * bar_length
                        st.markdown(f"**{domain_name}**: {bar} {percentage:.1f}%")
                else:
                    st.info("No domain data available")
            else:
                st.info("No domain data available")

            st.markdown("<br>", unsafe_allow_html=True)

            # Task Type Distribution
            st.markdown("#### 📋 Task Type Distribution")
            if task_counts:
                total_tasks = sum(task_counts.values())
                sorted_tasks = sorted(task_counts.items(), key=lambda x: x[1], reverse=True)[:5]

                for task, count in sorted_tasks:
                    percentage = (count / total_tasks) * 100
                    task_name = Config.TASK_TYPES.get(task, task)
                    bar_length = int(percentage / 2)
                    bar = "█" * bar_length
                    st.markdown(f"**{task_name}**: {bar} {percentage:.1f}%")
            else:
                st.info("No task data available")

        with pattern_col2:
            # Role Distribution
            st.markdown("#### 👤 Role Distribution")
            if role_counts or stats.get('role_usage'):
                # Combine session data with preference data
                combined_roles = role_counts.copy()
                if stats.get('role_usage'):
                    for role, count in stats['role_usage'].items():
                        combined_roles[role] = combined_roles.get(role, 0) + count

                if combined_roles:
                    total_roles = sum(combined_roles.values())
                    sorted_roles = combined_roles.most_common(5)

                    for role, count in sorted_roles:
                        percentage = (count / total_roles) * 100
                        role_name = Config.ACADEMIC_ROLES.get(role, Config.PROFESSIONAL_ROLES.get(role, role.replace('_', ' ').title()))
                        bar_length = int(percentage / 2)
                        bar = "█" * bar_length
                        st.markdown(f"**{role_name}**: {bar} {percentage:.1f}%")
                else:
                    st.info("No role data available")
            else:
                st.info("No role data available")

            st.markdown("<br>", unsafe_allow_html=True)

            # Version Type Preferences
            st.markdown("#### 🎨 Version Type Preferences")
            if version_counts or stats.get('version_usage'):
                # Combine session data with preference data
                combined_versions = version_counts.copy()
                if stats.get('version_usage'):
                    for version, count in stats['version_usage'].items():
                        combined_versions[version] = combined_versions.get(version, 0) + count

                if combined_versions:
                    total_versions = sum(combined_versions.values())
                    sorted_versions = combined_versions.most_common()

                    for version, count in sorted_versions:
                        percentage = (count / total_versions) * 100
                        version_info = Config.VERSION_LABELS.get(version, {'name': version.title()})
                        bar_length = int(percentage / 2)
                        bar = "█" * bar_length
                        st.markdown(f"**{version_info.get('name', version)}**: {bar} {percentage:.1f}%")
                else:
                    st.info("No version data available")
            else:
                st.info("No version data available")

        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()

        # ==================== QUALITY TRENDS ====================

        st.markdown("### 📈 Quality Trends")
        st.markdown("<br>", unsafe_allow_html=True)

        trend_col1, trend_col2 = st.columns(2)

        with trend_col1:
            # Clarity Score Trend
            st.markdown("#### 🎯 Clarity Score Over Time")
            if len(clarity_trend) >= 3:
                # Sort by date
                clarity_trend.sort(key=lambda x: x['date'])

                # Group by week for better visualization
                weekly_clarity = {}
                for entry in clarity_trend:
                    week_key = entry['date'].strftime('%Y-W%U')
                    if week_key not in weekly_clarity:
                        weekly_clarity[week_key] = []
                    weekly_clarity[week_key].append(entry['score'])

                # Calculate average per week
                weeks = sorted(weekly_clarity.keys())[-8:]  # Last 8 weeks
                for week in weeks:
                    avg_score = sum(weekly_clarity[week]) / len(weekly_clarity[week])
                    week_display = datetime.strptime(week + '-1', '%Y-W%U-%w').strftime('%b %d')
                    bar_length = int(avg_score / 2)
                    bar = "█" * bar_length
                    st.markdown(f"**{week_display}**: {bar} {avg_score:.0f}")

                # Calculate improvement
                first_half = [e['score'] for e in clarity_trend[:len(clarity_trend)//2]]
                second_half = [e['score'] for e in clarity_trend[len(clarity_trend)//2:]]
                if first_half and second_half:
                    avg_first = sum(first_half) / len(first_half)
                    avg_second = sum(second_half) / len(second_half)
                    improvement = avg_second - avg_first
                    if improvement > 0:
                        st.success(f"📈 +{improvement:.1f} points improvement!")
                    elif improvement < 0:
                        st.warning(f"📉 {improvement:.1f} points change")
                    else:
                        st.info("➡️ Consistent quality")
            else:
                st.info("Need at least 3 sessions to show trends")

        with trend_col2:
            # Weekly Activity
            st.markdown("#### 📅 Weekly Activity")
            if weekly_activity:
                sorted_weeks = sorted(weekly_activity.keys())[-8:]  # Last 8 weeks
                max_count = max(weekly_activity[w] for w in sorted_weeks) if sorted_weeks else 1

                for week in sorted_weeks:
                    count = weekly_activity[week]
                    week_display = datetime.strptime(week + '-1', '%Y-W%U-%w').strftime('%b %d')
                    bar_length = int((count / max_count) * 50)
                    bar = "█" * bar_length
                    st.markdown(f"**{week_display}**: {bar} {count}")

                # Calculate most productive day
                day_counts = {}
                for session in sessions[:20]:  # Last 20 sessions
                    day_name = session.created_at.strftime('%A')
                    day_counts[day_name] = day_counts.get(day_name, 0) + 1

                if day_counts:
                    most_productive_day = max(day_counts.items(), key=lambda x: x[1])[0]
                    st.info(f"🌟 Most active on **{most_productive_day}s**")
            else:
                st.info("No activity data yet")

        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()

        # ==================== SMART INSIGHTS ====================

        st.markdown("### 💡 Smart Insights")
        st.markdown("<br>", unsafe_allow_html=True)

        insight_col1, insight_col2, insight_col3 = st.columns(3)

        with insight_col1:
            # Activity insight
            if weekly_activity and total_sessions >= 5:
                weeks_active = len(weekly_activity)
                avg_per_week = total_sessions / weeks_active
                if avg_per_week >= 3:
                    st.success(f"🔥 **Power User!**\n\nYou optimize **{avg_per_week:.1f}x per week** on average. You're building great prompt-writing habits!")
                elif avg_per_week >= 1:
                    st.info(f"✅ **Consistent User**\n\nYou optimize **{avg_per_week:.1f}x per week**. Keep up the good work!")
                else:
                    st.info(f"📊 **Getting Started**\n\nYou optimize **{avg_per_week:.1f}x per week**. Use it more to build better habits!")
            else:
                st.info("💡 **Keep Going!**\n\nOptimize more prompts to unlock personalized insights.")

        with insight_col2:
            # Quality insight
            if avg_clarity_score > 0:
                if avg_clarity_score >= 80:
                    st.success(f"⭐ **Excellent Quality!**\n\nYour average clarity score is **{int(avg_clarity_score)}/100**. You write exceptional prompts!")
                elif avg_clarity_score >= 70:
                    st.success(f"✨ **Great Quality!**\n\nYour average clarity score is **{int(avg_clarity_score)}/100**. Your prompts are well-structured!")
                else:
                    st.info(f"📈 **Room to Grow**\n\nYour average clarity is **{int(avg_clarity_score)}/100**. Keep practicing to improve!")

                # Check if improving
                if len(clarity_trend) >= 6:
                    recent = [e['score'] for e in clarity_trend[-3:]]
                    older = [e['score'] for e in clarity_trend[-6:-3]]
                    if recent and older:
                        recent_avg = sum(recent) / len(recent)
                        older_avg = sum(older) / len(older)
                        if recent_avg > older_avg + 5:
                            st.success("📈 Your quality is improving!")
            else:
                st.info("💡 **Start Optimizing!**\n\nOptimize prompts to see quality insights.")

        with insight_col3:
            # Best performing version
            if version_counts or stats.get('version_usage'):
                combined_versions = version_counts.copy()
                if stats.get('version_usage'):
                    for version, count in stats['version_usage'].items():
                        combined_versions[version] = combined_versions.get(version, 0) + count

                if combined_versions:
                    best_version = combined_versions.most_common(1)[0]
                    version_name = Config.VERSION_LABELS.get(best_version[0], {}).get('name', best_version[0].title())
                    total_v = sum(combined_versions.values())
                    percentage = (best_version[1] / total_v) * 100

                    st.info(f"🎨 **Favorite Version**\n\n**{version_name}** is your go-to ({percentage:.0f}% of the time)!")
                else:
                    st.info("💡 **Explore Versions!**\n\nTry different prompt versions to find your favorite.")
            else:
                st.info("💡 **Explore Versions!**\n\nTry different prompt versions to find your favorite.")

        # Additional contextual insights
        if most_common_task != "N/A" and total_sessions >= 5:
            st.markdown("<br>", unsafe_allow_html=True)
            task_display = Config.TASK_TYPES.get(most_common_task, most_common_task)
            st.info(f"🎯 **Most Common Use Case**: You primarily use this tool for **{task_display}**. Check out our [Templates](pages/2_📚_Templates.py) page for specialized templates in this area!")

with history_tab:
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

        if st.button("🎯 Go to Prompt Lab", type="primary", key="go_to_prompt_lab_history"):
            st.switch_page("pages/1_🎯_Prompt_Lab.py")

# ==================== FOOTER ====================

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("💡 **Enhanced Analytics Dashboard** - Track your optimization journey!")
