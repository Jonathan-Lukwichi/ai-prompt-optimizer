"""
Test & Compare - Prove Your Optimized Prompts Work Better!
Side-by-side testing of original vs optimized prompts
"""
import streamlit as st
from core.config import Config
from core.prompt_engine import PromptEngine
from core.response_analyzer import ResponseAnalyzer
from utils.ui_components import load_custom_css, gradient_header
import google.generativeai as genai
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Test & Compare | AI Prompt Optimizer",
    page_icon="🔬",
    layout="wide"
)

# Load custom CSS
load_custom_css()

# ==================== HEADER ====================

gradient_header(
    "🔬 Test & Compare",
    size="h1",
    subtitle="Prove your optimized prompts get better results with side-by-side testing"
)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== INTRODUCTION ====================

st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-left: 4px solid #8B5CF6;
    padding: 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(139, 92, 246, 0.1);
">
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
        <div style="
            background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%);
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
        ">🔬</div>
        <h3 style="color: #8B5CF6; margin: 0; font-size: 1.5rem; font-weight: 700;">How It Works</h3>
    </div>
    <p style="color: #E5E7EB; margin-bottom: 1rem; line-height: 1.6;">
        Test your original prompt vs the optimized version with the <strong>same AI model</strong> and see the difference in real-time!
        Our advanced analyzer scores both responses across 4 key dimensions:
    </p>
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem; margin-top: 1rem;">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="color: #10B981;">✓</span>
            <span style="color: #D1D5DB;"><strong>Completeness</strong> - Thoroughness</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="color: #10B981;">✓</span>
            <span style="color: #D1D5DB;"><strong>Clarity</strong> - Readability</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="color: #10B981;">✓</span>
            <span style="color: #D1D5DB;"><strong>Specificity</strong> - Detail Level</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="color: #10B981;">✓</span>
            <span style="color: #D1D5DB;"><strong>Actionability</strong> - Usefulness</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================

if 'comparison_result' not in st.session_state:
    st.session_state.comparison_result = None

# Auto-load prompts from Prompt Lab if available
auto_original = ""
auto_optimized = ""
auto_loaded = False
available_versions = []

# Initialize selected version in session state
if 'selected_test_version' not in st.session_state:
    st.session_state.selected_test_version = 'basic'

if 'optimization_result' in st.session_state and st.session_state.optimization_result:
    result = st.session_state.optimization_result
    auto_original = result.get('raw_prompt', '')
    # Get available versions
    if 'optimized' in result and hasattr(result['optimized'], 'versions'):
        available_versions = list(result['optimized'].versions.keys())
        # Use the selected version from session state
        selected_ver = st.session_state.selected_test_version
        if selected_ver in result['optimized'].versions:
            auto_optimized = result['optimized'].versions[selected_ver]
        elif 'basic' in result['optimized'].versions:
            auto_optimized = result['optimized'].versions['basic']
        elif result['optimized'].versions:
            # Get the first available version
            auto_optimized = list(result['optimized'].versions.values())[0]
    auto_loaded = True

# ==================== AUTO-LOAD NOTIFICATION ====================

if auto_loaded and auto_original and auto_optimized:
    notification_col, version_col = st.columns([3, 1])

    with notification_col:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 182, 212, 0.15) 100%);
            border: 1px solid rgba(16, 185, 129, 0.4);
            border-left: 4px solid #10B981;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        ">
            <div style="
                background: linear-gradient(135deg, #10B981 0%, #06B6D4 100%);
                width: 40px;
                height: 40px;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                flex-shrink: 0;
            ">✨</div>
            <div>
                <div style="color: #10B981; font-weight: 700; font-size: 1rem; margin-bottom: 0.25rem;">
                    Prompts Auto-Loaded from Prompt Lab!
                </div>
                <div style="color: #D1D5DB; font-size: 0.875rem;">
                    Your original and optimized prompts have been automatically loaded. You can edit them below or test them as-is.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with version_col:
        # Version selector if multiple versions exist
        if len(available_versions) > 1:
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

            version_labels = {
                'basic': '📝 Basic',
                'critical': '🧠 Critical',
                'tutor': '👨‍🏫 Tutor',
                'safe': '🛡️ Safe'
            }

            # Default to 'basic' if current selection not in available versions
            current_index = 0
            if st.session_state.selected_test_version in available_versions:
                current_index = available_versions.index(st.session_state.selected_test_version)

            selected_version = st.selectbox(
                "Optimized Version",
                options=available_versions,
                index=current_index,
                format_func=lambda x: version_labels.get(x, x.title()),
                help="Choose which optimized version to test",
                key="version_selector"
            )

            # Update session state if selection changed
            if selected_version != st.session_state.selected_test_version:
                st.session_state.selected_test_version = selected_version
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

# ==================== INPUT SECTION ====================

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    ">
        <h3 style="color: #EF4444; margin: 0; font-size: 1.1rem; display: flex; align-items: center; gap: 0.5rem;">
            <span style="
                background: rgba(239, 68, 68, 0.2);
                width: 32px;
                height: 32px;
                border-radius: 8px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
            ">📝</span>
            Original Prompt
        </h3>
    </div>
    """, unsafe_allow_html=True)
    # Use unique key based on whether auto-loaded to reset when changing versions
    original_key = f"original_prompt_input_{st.session_state.selected_test_version if auto_loaded else 'manual'}"
    original_prompt = st.text_area(
        "Enter your original prompt",
        value=auto_original,
        placeholder="Example: Tell me about machine learning",
        height=150,
        key=original_key,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    ">
        <h3 style="color: #10B981; margin: 0; font-size: 1.1rem; display: flex; align-items: center; gap: 0.5rem;">
            <span style="
                background: rgba(16, 185, 129, 0.2);
                width: 32px;
                height: 32px;
                border-radius: 8px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
            ">✨</span>
            Optimized Prompt
        </h3>
    </div>
    """, unsafe_allow_html=True)
    # Use unique key based on selected version to reset when changing versions
    optimized_key = f"optimized_prompt_input_{st.session_state.selected_test_version if auto_loaded else 'manual'}"
    optimized_prompt = st.text_area(
        "Enter your optimized prompt",
        value=auto_optimized,
        placeholder="Example: As a PhD researcher in Computer Science, I need a comprehensive overview of machine learning...",
        height=150,
        key=optimized_key,
        label_visibility="collapsed"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ==================== TEST BUTTON ====================

test_col1, test_col2, test_col3 = st.columns([2, 1, 2])

with test_col2:
    test_button = st.button(
        "🚀 Test Both Prompts",
        type="primary",
        use_container_width=True,
        disabled=not original_prompt or not optimized_prompt or len(original_prompt.strip()) < 10 or len(optimized_prompt.strip()) < 10
    )

# ==================== TESTING LOGIC ====================

if test_button:
    with st.spinner("🔬 Testing both prompts with AI..."):
        try:
            # Configure Gemini
            api_key = Config.GEMINI_API_KEY
            if not api_key:
                st.error("❌ No API key found! Please configure GEMINI_API_KEY in your .env file.")
                st.stop()

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(Config.GEMINI_MODEL)

            # Test original prompt
            with st.spinner("Testing original prompt..."):
                original_response = model.generate_content(original_prompt)
                original_text = original_response.text

            # Test optimized prompt
            with st.spinner("Testing optimized prompt..."):
                optimized_response = model.generate_content(optimized_prompt)
                optimized_text = optimized_response.text

            # Analyze both responses
            with st.spinner("Analyzing response quality..."):
                analyzer = ResponseAnalyzer()
                original_quality = analyzer.analyze_response(original_text, original_prompt)
                optimized_quality = analyzer.analyze_response(optimized_text, optimized_prompt)
                comparison = analyzer.compare_responses(original_quality, optimized_quality)

            # Store results
            st.session_state.comparison_result = {
                'original_prompt': original_prompt,
                'optimized_prompt': optimized_prompt,
                'original_response': original_text,
                'optimized_response': optimized_text,
                'original_quality': original_quality,
                'optimized_quality': optimized_quality,
                'comparison': comparison
            }

            st.success("✅ Testing complete! See results below.")
            st.balloons()

        except Exception as e:
            st.error(f"❌ Error during testing: {str(e)}")
            st.info("💡 Make sure your GEMINI_API_KEY is configured correctly in the .env file")

# ==================== RESULTS SECTION ====================

if st.session_state.comparison_result:
    result = st.session_state.comparison_result

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)

    # ==================== WINNER ANNOUNCEMENT ====================

    if result['comparison']['winner'] == 'optimized':
        improvement = result['comparison']['overall_improvement']
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(6, 182, 212, 0.2) 100%);
            border: 2px solid #10B981;
            border-radius: 20px;
            padding: 3rem 2rem;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 20px 60px rgba(16, 185, 129, 0.3), 0 0 0 1px rgba(16, 185, 129, 0.1);
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(16, 185, 129, 0.1) 0%, transparent 70%);
                animation: pulse 3s ease-in-out infinite;
            "></div>
            <div style="position: relative; z-index: 1;">
                <div style="
                    font-size: 4rem;
                    margin-bottom: 1rem;
                    filter: drop-shadow(0 4px 12px rgba(16, 185, 129, 0.5));
                ">🎉</div>
                <h2 style="
                    background: linear-gradient(135deg, #10B981 0%, #06B6D4 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    margin: 0;
                    font-size: 2.5rem;
                    font-weight: 800;
                ">Optimized Prompt Wins!</h2>
                <div style="
                    background: linear-gradient(135deg, #10B981 0%, #06B6D4 100%);
                    padding: 1rem 2rem;
                    border-radius: 12px;
                    margin: 1.5rem auto 0;
                    max-width: 300px;
                    box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3);
                ">
                    <div style="color: #FFFFFF; font-size: 2rem; font-weight: 800;">
                        +{improvement}
                    </div>
                    <div style="color: rgba(255, 255, 255, 0.9); font-size: 0.875rem; text-transform: uppercase; letter-spacing: 1px;">
                        Points Improvement
                    </div>
                </div>
                <p style="color: #9CA3AF; margin-top: 1.5rem; font-size: 0.95rem;">
                    Your optimized prompt generated a significantly better response!
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(236, 72, 153, 0.15) 0%, rgba(239, 68, 68, 0.15) 100%);
            border: 2px solid #EC4899;
            border-radius: 20px;
            padding: 3rem 2rem;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 20px 60px rgba(236, 72, 153, 0.2);
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🤔</div>
            <h2 style="
                color: #EC4899;
                margin: 0;
                font-size: 2rem;
                font-weight: 700;
            ">Original Prompt Performed Better</h2>
            <p style="color: #D1D5DB; margin: 1rem 0 0 0; line-height: 1.6;">
                The original prompt scored higher. Review the analysis below to understand why,<br>
                and try optimizing with a different approach.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ==================== SCORE COMPARISON ====================

    st.markdown("""
    <h2 style="
        background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        margin-bottom: 1.5rem;
    ">📊 Quality Scores</h2>
    """, unsafe_allow_html=True)

    # Score cards
    score_col1, score_col2, score_col3, score_col4, score_col5 = st.columns(5)

    def create_score_card(title, original_score, optimized_score, improvement):
        """Create a comparison score card"""
        color = "#10B981" if improvement > 0 else "#EF4444" if improvement < 0 else "#6B7280"
        arrow = "↑" if improvement > 0 else "↓" if improvement < 0 else "="

        return f"""
        <div style="
            background: rgba(26, 27, 61, 0.6);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
        ">
            <div style="color: #9CA3AF; font-size: 0.875rem; margin-bottom: 0.5rem;">{title}</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #E5E7EB; margin-bottom: 0.25rem;">
                {original_score} → {optimized_score}
            </div>
            <div style="color: {color}; font-size: 1rem; font-weight: 600;">
                {arrow} {abs(improvement)}
            </div>
        </div>
        """

    with score_col1:
        st.markdown(create_score_card(
            "Overall",
            result['original_quality'].overall_score,
            result['optimized_quality'].overall_score,
            result['comparison']['overall_improvement']
        ), unsafe_allow_html=True)

    with score_col2:
        st.markdown(create_score_card(
            "Completeness",
            result['original_quality'].completeness_score,
            result['optimized_quality'].completeness_score,
            result['comparison']['completeness_improvement']
        ), unsafe_allow_html=True)

    with score_col3:
        st.markdown(create_score_card(
            "Clarity",
            result['original_quality'].clarity_score,
            result['optimized_quality'].clarity_score,
            result['comparison']['clarity_improvement']
        ), unsafe_allow_html=True)

    with score_col4:
        st.markdown(create_score_card(
            "Specificity",
            result['original_quality'].specificity_score,
            result['optimized_quality'].specificity_score,
            result['comparison']['specificity_improvement']
        ), unsafe_allow_html=True)

    with score_col5:
        st.markdown(create_score_card(
            "Actionability",
            result['original_quality'].actionability_score,
            result['optimized_quality'].actionability_score,
            result['comparison']['actionability_improvement']
        ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================== VISUAL COMPARISON CHARTS ====================

    st.markdown("""
    <h2 style="
        background: linear-gradient(135deg, #10B981 0%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        margin-bottom: 1.5rem;
    ">📈 Visual Analysis</h2>
    """, unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # Radar chart comparing all metrics
        categories = ['Completeness', 'Clarity', 'Specificity', 'Actionability', 'Overall']

        fig_radar = go.Figure()

        # Original prompt trace
        fig_radar.add_trace(go.Scatterpolar(
            r=[
                result['original_quality'].completeness_score,
                result['original_quality'].clarity_score,
                result['original_quality'].specificity_score,
                result['original_quality'].actionability_score,
                result['original_quality'].overall_score
            ],
            theta=categories,
            fill='toself',
            name='Original',
            line=dict(color='#EF4444', width=2),
            fillcolor='rgba(239, 68, 68, 0.2)'
        ))

        # Optimized prompt trace
        fig_radar.add_trace(go.Scatterpolar(
            r=[
                result['optimized_quality'].completeness_score,
                result['optimized_quality'].clarity_score,
                result['optimized_quality'].specificity_score,
                result['optimized_quality'].actionability_score,
                result['optimized_quality'].overall_score
            ],
            theta=categories,
            fill='toself',
            name='Optimized',
            line=dict(color='#10B981', width=2),
            fillcolor='rgba(16, 185, 129, 0.2)'
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor='rgba(139, 92, 246, 0.2)',
                    linecolor='rgba(139, 92, 246, 0.3)'
                ),
                angularaxis=dict(
                    gridcolor='rgba(139, 92, 246, 0.2)',
                    linecolor='rgba(139, 92, 246, 0.3)'
                ),
                bgcolor='rgba(0, 0, 0, 0)'
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.1,
                xanchor="center",
                x=0.5,
                font=dict(color='#E5E7EB')
            ),
            paper_bgcolor='rgba(26, 27, 61, 0.4)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            height=400,
            margin=dict(t=80, b=40, l=40, r=40)
        )

        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown("<p style='text-align: center; color: #9CA3AF; font-size: 0.875rem;'>Multi-dimensional Quality Comparison</p>", unsafe_allow_html=True)

    with chart_col2:
        # Bar chart showing improvements
        improvements = [
            result['comparison']['completeness_improvement'],
            result['comparison']['clarity_improvement'],
            result['comparison']['specificity_improvement'],
            result['comparison']['actionability_improvement'],
            result['comparison']['overall_improvement']
        ]

        colors = ['#10B981' if imp > 0 else '#EF4444' if imp < 0 else '#6B7280' for imp in improvements]

        fig_bar = go.Figure()

        fig_bar.add_trace(go.Bar(
            x=categories,
            y=improvements,
            marker=dict(
                color=colors,
                line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
            ),
            text=[f"{'+' if imp > 0 else ''}{imp}" for imp in improvements],
            textposition='outside',
            textfont=dict(color='#E5E7EB', size=12),
            hovertemplate='<b>%{x}</b><br>Improvement: %{y}<extra></extra>'
        ))

        fig_bar.update_layout(
            paper_bgcolor='rgba(26, 27, 61, 0.4)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            xaxis=dict(
                gridcolor='rgba(139, 92, 246, 0.1)',
                linecolor='rgba(139, 92, 246, 0.3)',
                color='#E5E7EB'
            ),
            yaxis=dict(
                gridcolor='rgba(139, 92, 246, 0.2)',
                linecolor='rgba(139, 92, 246, 0.3)',
                color='#E5E7EB',
                title_text='Score Improvement',
                title_font=dict(color='#9CA3AF')
            ),
            height=400,
            margin=dict(t=40, b=40, l=40, r=40),
            showlegend=False
        )

        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("<p style='text-align: center; color: #9CA3AF; font-size: 0.875rem;'>Score Improvements (Points Gained/Lost)</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================== SIDE-BY-SIDE RESPONSES ====================

    st.markdown("""
    <h2 style="
        background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        margin-bottom: 1.5rem;
    ">💬 AI Responses</h2>
    """, unsafe_allow_html=True)

    response_col1, response_col2 = st.columns(2)

    with response_col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
        ">
            <h3 style="color: #EF4444; margin: 0; font-size: 1.1rem; display: flex; align-items: center; gap: 0.5rem;">
                <span>📝</span> From Original Prompt
            </h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="
            background: rgba(26, 27, 61, 0.6);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 12px;
            padding: 1.5rem;
            max-height: 400px;
            overflow-y: auto;
            line-height: 1.6;
            color: #E5E7EB;
            box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.2);
        ">
            {result['original_response']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="
            background: rgba(16, 185, 129, 0.1);
            border-left: 3px solid #10B981;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #10B981;">✓ Strengths</strong>
        </div>
        """, unsafe_allow_html=True)
        for strength in result['original_quality'].strengths:
            st.markdown(f"<div style='color: #D1D5DB; margin-left: 1rem; margin-bottom: 0.5rem;'>• {strength}</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="
            background: rgba(239, 68, 68, 0.1);
            border-left: 3px solid #EF4444;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin: 1rem 0 0.75rem 0;
        ">
            <strong style="color: #EF4444;">⚠ Weaknesses</strong>
        </div>
        """, unsafe_allow_html=True)
        for weakness in result['original_quality'].weaknesses:
            st.markdown(f"<div style='color: #D1D5DB; margin-left: 1rem; margin-bottom: 0.5rem;'>• {weakness}</div>", unsafe_allow_html=True)

    with response_col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
        ">
            <h3 style="color: #10B981; margin: 0; font-size: 1.1rem; display: flex; align-items: center; gap: 0.5rem;">
                <span>✨</span> From Optimized Prompt
            </h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="
            background: rgba(26, 27, 61, 0.6);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 12px;
            padding: 1.5rem;
            max-height: 400px;
            overflow-y: auto;
            line-height: 1.6;
            color: #E5E7EB;
            box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.2);
        ">
            {result['optimized_response']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="
            background: rgba(16, 185, 129, 0.1);
            border-left: 3px solid #10B981;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #10B981;">✓ Strengths</strong>
        </div>
        """, unsafe_allow_html=True)
        for strength in result['optimized_quality'].strengths:
            st.markdown(f"<div style='color: #D1D5DB; margin-left: 1rem; margin-bottom: 0.5rem;'>• {strength}</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="
            background: rgba(239, 68, 68, 0.1);
            border-left: 3px solid #EF4444;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin: 1rem 0 0.75rem 0;
        ">
            <strong style="color: #EF4444;">⚠ Weaknesses</strong>
        </div>
        """, unsafe_allow_html=True)
        for weakness in result['optimized_quality'].weaknesses:
            st.markdown(f"<div style='color: #D1D5DB; margin-left: 1rem; margin-bottom: 0.5rem;'>• {weakness}</div>", unsafe_allow_html=True)

# ==================== FOOTER ====================

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("💡 **Test & Compare** - Powered by AI response analysis")
