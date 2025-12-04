"""
LUKTHAN - AI Prompt Agent
NEXAVERSE Theme - Futuristic Neon UI Components
Cyan (#00E5FF) + Purple (#9B5CFF) + Deep Space (#050816)
"""
import streamlit as st
from typing import Optional, List, Dict, Any
from datetime import datetime
import html


def load_lukthan_theme():
    """Load NEXAVERSE futuristic neon theme"""
    st.markdown("""
    <style>
    /* ===== GOOGLE FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0');

    /* ===== CSS VARIABLES ===== */
    :root {
        --neon-cyan: #00E5FF;
        --neon-purple: #9B5CFF;
        --neon-pink: #FF6B9D;
        --bg-deep: #050816;
        --bg-card: #0A0F1F;
        --bg-elevated: #0D1224;
        --bg-glass: rgba(10, 15, 31, 0.8);
        --border-glow: rgba(0, 229, 255, 0.3);
        --text-primary: #FFFFFF;
        --text-secondary: #8B949E;
        --text-muted: #6E7681;
        --gradient-main: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
        --gradient-reverse: linear-gradient(135deg, #9B5CFF 0%, #00E5FF 100%);
        --glow-cyan: 0 0 20px rgba(0, 229, 255, 0.4), 0 0 40px rgba(0, 229, 255, 0.2);
        --glow-purple: 0 0 20px rgba(155, 92, 255, 0.4), 0 0 40px rgba(155, 92, 255, 0.2);
    }

    /* ===== GLOBAL STYLES ===== */
    .main {
        background: linear-gradient(180deg, #050816 0%, #0A0F1F 50%, #050816 100%) !important;
    }

    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
    }

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050816 0%, #0A0F1F 50%, #050816 100%) !important;
        border-right: 1px solid rgba(0, 229, 255, 0.2) !important;
        width: 300px !important;
        min-width: 300px !important;
    }

    section[data-testid="stSidebar"] > div {
        background: transparent !important;
        padding: 1rem;
    }

    /* Force sidebar to show */
    [data-testid="stSidebarContent"] {
        display: block !important;
        visibility: visible !important;
    }

    [data-testid="stSidebarNav"] {
        background: transparent !important;
    }

    /* Sidebar collapse/expand button - make it visible */
    button[data-testid="baseButton-headerNoPadding"],
    [data-testid="collapsedControl"] {
        color: #00E5FF !important;
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.2) 0%, rgba(155, 92, 255, 0.2) 100%) !important;
        border: 1px solid rgba(0, 229, 255, 0.4) !important;
        border-radius: 12px !important;
        padding: 12px !important;
        margin: 8px !important;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    button[data-testid="baseButton-headerNoPadding"]:hover,
    [data-testid="collapsedControl"]:hover {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.3) 0%, rgba(155, 92, 255, 0.3) 100%) !important;
        box-shadow: 0 0 25px rgba(0, 229, 255, 0.5) !important;
        transform: scale(1.05) !important;
    }

    /* Fix Material Icons display */
    .material-symbols-rounded,
    .material-icons {
        font-family: 'Material Symbols Rounded', 'Material Icons' !important;
        font-size: 24px !important;
    }

    /* Style the sidebar toggle - hide text, show arrow */
    [data-testid="collapsedControl"] span,
    [data-testid="collapsedControl"] svg {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        font-size: 20px !important;
    }

    /* Fallback: Replace text with arrow using CSS */
    button[kind="headerNoPadding"] span,
    [data-testid="stSidebarCollapseButton"] span {
        font-size: 0 !important;
    }

    button[kind="headerNoPadding"] span::after,
    [data-testid="stSidebarCollapseButton"] span::after {
        content: "»" !important;
        font-size: 24px !important;
        font-weight: bold !important;
        color: #00E5FF !important;
    }

    /* When sidebar is collapsed, show expand arrow */
    [data-collapsed="true"] [data-testid="collapsedControl"] {
        font-size: 0 !important;
    }

    [data-collapsed="true"] [data-testid="collapsedControl"]::after {
        content: "»" !important;
        font-size: 24px !important;
        font-weight: bold !important;
        color: #00E5FF !important;
    }

    /* Hide the raw icon text and replace with styled button */
    [data-testid="collapsedControl"] {
        font-size: 0 !important;
        width: 44px !important;
        height: 44px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
    }

    [data-testid="collapsedControl"]::before {
        content: "☰" !important;
        font-size: 22px !important;
        color: #00E5FF !important;
    }

    /* Sidebar selectbox styling */
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(10, 15, 31, 0.9) !important;
        border: 1px solid rgba(0, 229, 255, 0.3) !important;
        border-radius: 8px !important;
    }

    section[data-testid="stSidebar"] .stSelectbox label {
        color: #8B949E !important;
        font-size: 0.85rem !important;
    }

    /* Sidebar divider */
    section[data-testid="stSidebar"] hr {
        border-color: rgba(0, 229, 255, 0.2) !important;
        margin: 1rem 0 !important;
    }

    /* ===== HERO SECTION ===== */
    .hero-container {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.05) 0%, rgba(155, 92, 255, 0.05) 100%);
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 32px;
        padding: 4rem 3rem;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }

    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, rgba(0, 229, 255, 0.15) 0%, transparent 70%);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }

    .hero-container::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(155, 92, 255, 0.15) 0%, transparent 70%);
        border-radius: 50%;
        animation: float 8s ease-in-out infinite reverse;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(5deg); }
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 50%, #FF6B9D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }

    .hero-subtitle {
        font-size: 1.25rem;
        color: #8B949E;
        line-height: 1.6;
        margin-bottom: 2rem;
        max-width: 600px;
        position: relative;
        z-index: 1;
    }

    .hero-glow-orb {
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(0, 229, 255, 0.3) 0%, rgba(155, 92, 255, 0.2) 50%, transparent 70%);
        border-radius: 50%;
        filter: blur(40px);
        animation: pulse 4s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.1); opacity: 1; }
    }

    /* ===== FEATURE CARDS ===== */
    .feature-card {
        background: linear-gradient(135deg, rgba(10, 15, 31, 0.9) 0%, rgba(13, 18, 36, 0.9) 100%);
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 24px;
        padding: 2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(20px);
    }

    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00E5FF, #9B5CFF);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .feature-card:hover {
        transform: translateY(-8px);
        border-color: rgba(0, 229, 255, 0.5);
        box-shadow: 0 20px 40px rgba(0, 229, 255, 0.15), 0 0 60px rgba(155, 92, 255, 0.1);
    }

    .feature-card:hover::before {
        opacity: 1;
    }

    .feature-icon {
        width: 64px;
        height: 64px;
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.2) 0%, rgba(155, 92, 255, 0.2) 100%);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 30px rgba(0, 229, 255, 0.2);
    }

    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 0.75rem;
    }

    .feature-desc {
        font-size: 0.95rem;
        color: #8B949E;
        line-height: 1.6;
    }

    /* ===== TESTIMONIAL CARDS ===== */
    .testimonial-card {
        background: linear-gradient(135deg, rgba(155, 92, 255, 0.1) 0%, rgba(0, 229, 255, 0.1) 100%);
        border: 1px solid rgba(155, 92, 255, 0.3);
        border-radius: 24px;
        padding: 2rem;
        position: relative;
        overflow: hidden;
    }

    .testimonial-card::before {
        content: '"';
        position: absolute;
        top: 20px;
        left: 20px;
        font-size: 4rem;
        color: rgba(0, 229, 255, 0.2);
        font-family: Georgia, serif;
        line-height: 1;
    }

    .testimonial-text {
        font-size: 1rem;
        color: #F0F6FC;
        line-height: 1.7;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 1;
    }

    .testimonial-author {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .testimonial-avatar {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        color: white;
    }

    .testimonial-name {
        font-weight: 600;
        color: #FFFFFF;
    }

    .testimonial-role {
        font-size: 0.85rem;
        color: #6E7681;
    }

    .testimonial-stars {
        color: #FFD700;
        font-size: 0.9rem;
    }

    /* ===== SECTION HEADERS ===== */
    .section-header {
        text-align: center;
        margin-bottom: 3rem;
    }

    .section-tag {
        display: inline-block;
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.2) 0%, rgba(155, 92, 255, 0.2) 100%);
        border: 1px solid rgba(0, 229, 255, 0.3);
        border-radius: 50px;
        padding: 0.5rem 1.5rem;
        font-size: 0.85rem;
        font-weight: 600;
        color: #00E5FF;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FFFFFF 0%, #8B949E 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }

    .section-subtitle {
        font-size: 1.1rem;
        color: #6E7681;
        max-width: 600px;
        margin: 0 auto;
    }

    /* ===== CTA BUTTONS ===== */
    .cta-button-primary {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        text-decoration: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 229, 255, 0.4);
        cursor: pointer;
        border: none;
    }

    .cta-button-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 229, 255, 0.5);
    }

    .cta-button-secondary {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: transparent;
        color: #00E5FF;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        text-decoration: none;
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 229, 255, 0.5);
        cursor: pointer;
    }

    .cta-button-secondary:hover {
        background: rgba(0, 229, 255, 0.1);
        border-color: #00E5FF;
    }

    /* ===== STATS BAR ===== */
    .stats-bar {
        display: flex;
        justify-content: center;
        gap: 4rem;
        padding: 2rem;
        background: rgba(10, 15, 31, 0.6);
        border-radius: 20px;
        border: 1px solid rgba(0, 229, 255, 0.1);
        margin: 3rem 0;
    }

    .stat-item {
        text-align: center;
    }

    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .stat-label {
        font-size: 0.9rem;
        color: #6E7681;
        margin-top: 0.25rem;
    }

    /* ===== FOOTER ===== */
    .footer {
        border-top: 1px solid rgba(0, 229, 255, 0.2);
        padding: 3rem 0 2rem;
        margin-top: 4rem;
        text-align: center;
    }

    .footer-brand {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }

    .footer-tagline {
        color: #6E7681;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }

    .footer-links {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 1.5rem;
    }

    .footer-link {
        color: #8B949E;
        text-decoration: none;
        font-size: 0.9rem;
        transition: color 0.3s ease;
    }

    .footer-link:hover {
        color: #00E5FF;
    }

    .footer-copyright {
        color: #6E7681;
        font-size: 0.8rem;
    }

    /* ===== BUTTONS ===== */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 20px rgba(0, 229, 255, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(0, 229, 255, 0.4) !important;
    }

    .stButton > button:not([kind="primary"]) {
        background: rgba(10, 15, 31, 0.8) !important;
        border: 1px solid rgba(0, 229, 255, 0.3) !important;
        border-radius: 50px !important;
        color: #8B949E !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:not([kind="primary"]):hover {
        background: rgba(0, 229, 255, 0.1) !important;
        border-color: #00E5FF !important;
        color: #00E5FF !important;
    }

    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(10, 15, 31, 0.8);
        border-radius: 16px;
        padding: 6px;
        border: 1px solid rgba(0, 229, 255, 0.2);
        gap: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: #8B949E;
        padding: 12px 24px;
        font-weight: 500;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #F0F6FC;
        background: rgba(255, 255, 255, 0.05);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%) !important;
        color: white !important;
    }

    /* ===== CHAT INPUT AREA - Auto-expanding Textarea ===== */
    [data-testid="stTextArea"] {
        background: transparent !important;
    }

    [data-testid="stTextArea"] > div {
        background: transparent !important;
        border: none !important;
    }

    [data-testid="stTextArea"] textarea {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        color: #F0F6FC !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        min-height: 50px !important;
        max-height: 350px !important;
        height: auto !important;
        resize: none !important;
        overflow-y: auto !important;
        line-height: 1.6 !important;
    }

    [data-testid="stTextArea"] textarea:focus {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }

    [data-testid="stTextArea"] textarea::placeholder {
        color: #6E7681 !important;
    }

    /* Hide textarea label */
    [data-testid="stTextArea"] label {
        display: none !important;
    }

    /* Chat action buttons - circular icons */
    .row-widget.stButton > button {
        min-width: 42px !important;
        max-width: 42px !important;
        min-height: 42px !important;
        max-height: 42px !important;
        padding: 0 !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* Style the send button specifically */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%) !important;
        border: none !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.4) !important;
    }

    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 30px rgba(0, 229, 255, 0.6) !important;
        transform: scale(1.05) !important;
    }

    /* Secondary buttons (attach, mic) */
    .stButton > button:not([kind="primary"]) {
        background: rgba(0, 229, 255, 0.1) !important;
        border: 1px solid rgba(0, 229, 255, 0.3) !important;
    }

    .stButton > button:not([kind="primary"]):hover {
        background: rgba(0, 229, 255, 0.2) !important;
        border-color: #00E5FF !important;
    }

    /* ===== POPOVER ===== */
    .stPopover > div > div > div {
        background: rgba(10, 15, 31, 0.95) !important;
        border: 1px solid rgba(0, 229, 255, 0.3) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(20px) !important;
    }

    .stPopover button {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.1) 0%, rgba(155, 92, 255, 0.1) 100%) !important;
        border: 1px solid rgba(0, 229, 255, 0.3) !important;
        border-radius: 50% !important;
        width: 44px !important;
        height: 44px !important;
        transition: all 0.3s ease !important;
    }

    .stPopover button:hover {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.2) 0%, rgba(155, 92, 255, 0.2) 100%) !important;
        border-color: #00E5FF !important;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.4) !important;
    }

    /* ===== FILE UPLOADER ===== */
    [data-testid="stFileUploader"] {
        background: rgba(10, 15, 31, 0.8) !important;
        border: 2px dashed rgba(0, 229, 255, 0.3) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #00E5FF !important;
        background: rgba(0, 229, 255, 0.05) !important;
    }

    /* ===== SELECTBOX ===== */
    .stSelectbox > div > div {
        background: rgba(10, 15, 31, 0.9) !important;
        border: 1px solid rgba(0, 229, 255, 0.3) !important;
        border-radius: 12px !important;
    }

    /* ===== INFO/SUCCESS/WARNING BOXES ===== */
    .stAlert {
        background: rgba(10, 15, 31, 0.8) !important;
        border-radius: 16px !important;
        border-left: 4px solid #00E5FF !important;
    }

    /* ===== CODE BLOCKS ===== */
    .stCodeBlock {
        background: rgba(5, 8, 22, 0.9) !important;
        border: 1px solid rgba(0, 229, 255, 0.2) !important;
        border-radius: 12px !important;
    }

    /* ===== PROGRESS BARS ===== */
    .stProgress > div > div {
        background: rgba(0, 229, 255, 0.2) !important;
        border-radius: 10px !important;
    }

    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00E5FF 0%, #9B5CFF 100%) !important;
        border-radius: 10px !important;
    }

    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #050816;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00E5FF 0%, #9B5CFF 100%);
        border-radius: 10px;
    }

    /* ===== ANIMATIONS ===== */
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 229, 255, 0.3); }
        50% { box-shadow: 0 0 40px rgba(0, 229, 255, 0.5), 0 0 60px rgba(155, 92, 255, 0.3); }
    }

    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }

    .glow-effect {
        animation: glow 3s ease-in-out infinite;
    }

    .shimmer-effect {
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        background-size: 200% 100%;
        animation: shimmer 2s infinite;
    }
    </style>
    """, unsafe_allow_html=True)


def render_hero_section():
    """Render the hero section with animated orbs"""
    st.markdown("""
    <div class="hero-container">
        <div style="position: relative; z-index: 1;">
            <div class="hero-title">LUKTHAN</div>
            <div class="hero-title" style="font-size: 2rem; margin-top: -0.5rem;">AI Prompt Intelligence</div>
            <p class="hero-subtitle">
                Transform raw ideas into powerful, structured prompts.
                Optimized for ChatGPT, Claude, and Gemini. Built for researchers and developers.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_stats_bar():
    """Render statistics bar"""
    st.markdown("""
    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-number">10K+</div>
            <div class="stat-label">Prompts Generated</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">95%</div>
            <div class="stat-label">Quality Score</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">50+</div>
            <div class="stat-label">Templates</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Available</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_features_section():
    """Render the features section"""
    st.markdown("""
    <div class="section-header">
        <div class="section-tag">✨ Features</div>
        <div class="section-title">Why Choose LUKTHAN?</div>
        <div class="section-subtitle">Powerful AI-driven prompt optimization built for professionals</div>
    </div>
    """, unsafe_allow_html=True)


def render_feature_card(icon: str, title: str, description: str):
    """Render a single feature card"""
    st.markdown(f"""
    <div class="feature-card">
        <div class="feature-icon">{icon}</div>
        <div class="feature-title">{title}</div>
        <div class="feature-desc">{description}</div>
    </div>
    """, unsafe_allow_html=True)


def render_testimonials_section():
    """Render testimonials header"""
    st.markdown("""
    <div class="section-header">
        <div class="section-tag">💬 Testimonials</div>
        <div class="section-title">Loved by Professionals</div>
        <div class="section-subtitle">See what our users say about LUKTHAN</div>
    </div>
    """, unsafe_allow_html=True)


def render_testimonial_card(text: str, name: str, role: str, initials: str):
    """Render a testimonial card"""
    st.markdown(f"""
    <div class="testimonial-card">
        <div class="testimonial-text">{text}</div>
        <div class="testimonial-author">
            <div class="testimonial-avatar">{initials}</div>
            <div>
                <div class="testimonial-name">{name}</div>
                <div class="testimonial-role">{role}</div>
            </div>
            <div class="testimonial-stars" style="margin-left: auto;">⭐⭐⭐⭐⭐</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    """Render the footer"""
    st.markdown("""
    <div class="footer">
        <div class="footer-brand">🧠 LUKTHAN</div>
        <div class="footer-tagline">AI Prompt Intelligence for Research & Code</div>
        <div class="footer-links">
            <a href="#" class="footer-link">Documentation</a>
            <a href="#" class="footer-link">GitHub</a>
            <a href="#" class="footer-link">Twitter</a>
            <a href="#" class="footer-link">Discord</a>
        </div>
        <div class="footer-copyright">© 2024 LUKTHAN. Built with ❤️ for the AI community.</div>
    </div>
    """, unsafe_allow_html=True)


def render_welcome_hero():
    """Render attractive welcome for chat tab - matching landing page design"""
    st.markdown("""
    <style>
    @keyframes welcomePulse {
        0%, 100% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.1); opacity: 1; }
    }
    .welcome-container {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.08) 0%, rgba(155, 92, 255, 0.08) 100%);
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 24px;
        padding: 3rem 2rem;
        margin: 2rem auto;
        max-width: 700px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .welcome-orb-1 {
        position: absolute;
        top: -50px;
        right: -50px;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(0, 229, 255, 0.2) 0%, transparent 70%);
        border-radius: 50%;
        filter: blur(30px);
        animation: welcomePulse 4s ease-in-out infinite;
    }
    .welcome-orb-2 {
        position: absolute;
        bottom: -30px;
        left: -30px;
        width: 150px;
        height: 150px;
        background: radial-gradient(circle, rgba(155, 92, 255, 0.2) 0%, transparent 70%);
        border-radius: 50%;
        filter: blur(25px);
        animation: welcomePulse 5s ease-in-out infinite reverse;
    }
    .welcome-content {
        position: relative;
        z-index: 1;
    }
    .welcome-icon {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.2) 0%, rgba(155, 92, 255, 0.2) 100%);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem;
        font-size: 2.5rem;
        box-shadow: 0 0 30px rgba(0, 229, 255, 0.3);
    }
    .welcome-title {
        font-size: 2.25rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 50%, #FF6B9D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.75rem;
        line-height: 1.2;
    }
    .welcome-subtitle {
        color: #8B949E;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }
    .welcome-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
    }
    .chip-research {
        background: rgba(0, 229, 255, 0.1);
        border: 1px solid rgba(0, 229, 255, 0.3);
        border-radius: 20px;
        padding: 8px 16px;
        font-size: 0.85rem;
        color: #00E5FF;
    }
    .chip-coding {
        background: rgba(155, 92, 255, 0.1);
        border: 1px solid rgba(155, 92, 255, 0.3);
        border-radius: 20px;
        padding: 8px 16px;
        font-size: 0.85rem;
        color: #9B5CFF;
    }
    .chip-analysis {
        background: rgba(255, 107, 157, 0.1);
        border: 1px solid rgba(255, 107, 157, 0.3);
        border-radius: 20px;
        padding: 8px 16px;
        font-size: 0.85rem;
        color: #FF6B9D;
    }
    .chip-writing {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 20px;
        padding: 8px 16px;
        font-size: 0.85rem;
        color: #10B981;
    }
    </style>
    <div class="welcome-container">
        <div class="welcome-orb-1"></div>
        <div class="welcome-orb-2"></div>
        <div class="welcome-content">
            <div class="welcome-icon">🧠</div>
            <div class="welcome-title">What can I help you with?</div>
            <div class="welcome-subtitle">
                Describe your task and I'll generate an optimized prompt<br>
                for ChatGPT, Claude, or Gemini
            </div>
            <div class="welcome-chips">
                <span class="chip-research">🔬 Research</span>
                <span class="chip-coding">💻 Coding</span>
                <span class="chip-analysis">📊 Analysis</span>
                <span class="chip-writing">✍️ Writing</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    return None


def render_user_message(content: str, timestamp: Optional[str] = None, file_info: Optional[Dict] = None):
    """Render user message with neon styling"""
    time_str = timestamp or datetime.now().strftime("%H:%M")

    # Build file indicator if present
    file_html = ""
    if file_info:
        icons = {"documents": "📄", "code": "💻", "images": "🖼️", "audio": "🎵"}
        icon = icons.get(file_info.get('type', ''), '📎')
        file_name = file_info.get("name", "File")
        file_html = f'<p style="font-size: 0.8rem; color: #6E7681; margin: 0 0 0.5rem 0;">{icon} {file_name}</p>'

    # Use st.container with custom styling for better HTML rendering
    st.markdown(f'''<div style="background: linear-gradient(135deg, rgba(0, 229, 255, 0.15) 0%, rgba(155, 92, 255, 0.15) 100%); border: 1px solid rgba(0, 229, 255, 0.3); border-radius: 20px 20px 4px 20px; padding: 1rem 1.5rem; margin: 1rem 0 1rem 15%;">{file_html}<p style="color: #F0F6FC; font-size: 0.95rem; line-height: 1.6; margin: 0;">{content}</p><p style="font-size: 0.75rem; color: #6E7681; margin: 0.5rem 0 0 0; text-align: right;">You • {time_str}</p></div>''', unsafe_allow_html=True)


def render_agent_response(
    prompt: str,
    domain: str = "general",
    task_type: str = "general",
    quality_score: int = 85,
    metrics: Optional[Dict[str, int]] = None,
    suggestions: Optional[List[str]] = None
):
    """Render agent response with premium neon styling using inline styles"""

    # Domain icons and colors
    domain_config = {
        "research": {"icon": "🔬", "color": "#00E5FF", "label": "Research"},
        "coding": {"icon": "💻", "color": "#9B5CFF", "label": "Coding"},
        "data_science": {"icon": "📊", "color": "#FF6B9D", "label": "Data Science"},
        "general": {"icon": "🌐", "color": "#10B981", "label": "General"},
    }
    config = domain_config.get(domain, domain_config["general"])

    # Quality color based on score
    if quality_score >= 85:
        quality_color = "#10B981"
        quality_label = "Excellent"
    elif quality_score >= 70:
        quality_color = "#00E5FF"
        quality_label = "Good"
    elif quality_score >= 50:
        quality_color = "#F59E0B"
        quality_label = "Fair"
    else:
        quality_color = "#EF4444"
        quality_label = "Needs Work"

    # Escape prompt content for HTML (preserve line breaks)
    prompt_escaped = prompt.replace('\n', '<br>')

    # Build HTML with all inline styles on single line for Streamlit compatibility
    st.markdown(f'<div style="background: linear-gradient(135deg, rgba(10, 15, 31, 0.95) 0%, rgba(15, 20, 40, 0.95) 100%); border: 1px solid rgba(155, 92, 255, 0.4); border-radius: 24px; padding: 1.5rem; margin: 1rem 0; position: relative; overflow: hidden; box-shadow: 0 0 25px rgba(155, 92, 255, 0.3), 0 0 50px rgba(0, 229, 255, 0.1);"><div style="display: flex; align-items: center; gap: 12px; margin-bottom: 1rem;"><div style="width: 48px; height: 48px; background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; box-shadow: 0 0 20px rgba(0, 229, 255, 0.4);">🧠</div><div style="flex: 1;"><div style="color: #F0F6FC; font-weight: 700; font-size: 1.1rem;">LUKTHAN Agent</div><div style="color: #8B949E; font-size: 0.8rem;">AI-Optimized Prompt</div></div><span style="background: linear-gradient(135deg, #00E5FF 0%, #9B5CFF 100%); color: white; font-size: 0.7rem; padding: 5px 12px; border-radius: 20px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">✨ Optimized</span></div><div style="display: flex; gap: 8px; margin-bottom: 1rem; flex-wrap: wrap;"><span style="background: rgba(0, 229, 255, 0.1); border: 1px solid {config["color"]}; color: {config["color"]}; font-size: 0.75rem; padding: 4px 10px; border-radius: 12px;">{config["icon"]} {config["label"]}</span><span style="background: rgba(16, 185, 129, 0.15); border: 1px solid {quality_color}; color: {quality_color}; font-size: 0.75rem; padding: 4px 10px; border-radius: 12px; font-weight: 600;">⚡ {quality_score}% {quality_label}</span></div><div style="color: #8B949E; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;">📝 Your Optimized Prompt</div><div style="background: linear-gradient(135deg, rgba(5, 8, 22, 0.8) 0%, rgba(10, 15, 31, 0.8) 100%); border: 1px solid rgba(0, 229, 255, 0.2); border-radius: 16px; padding: 1.25rem; color: #F0F6FC; font-size: 0.95rem; line-height: 1.7;">{prompt_escaped}</div></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("📋 Copy", key=f"copy_{hash(prompt)}", use_container_width=True):
            st.toast("Prompt copied to clipboard!", icon="✅")
    with col2:
        if st.button("🔄 Regenerate", key=f"regen_{hash(prompt)}", use_container_width=True):
            return "regenerate"

    return None


def render_insights_panel(
    domain: str = "general",
    task_type: str = "general",
    quality_score: int = 85,
    metrics: Optional[Dict[str, int]] = None,
    suggestions: Optional[List[str]] = None,
    show_content: bool = True
):
    """Render insights panel with neon styling"""
    if not show_content:
        st.markdown("""
        <div style="
            background: rgba(10, 15, 31, 0.8);
            border: 1px solid rgba(0, 229, 255, 0.2);
            border-radius: 20px;
            padding: 3rem;
            text-align: center;
        ">
            <div style="font-size: 3rem; opacity: 0.3; margin-bottom: 1rem;">📊</div>
            <div style="color: #6E7681;">Generate a prompt to see insights</div>
        </div>
        """, unsafe_allow_html=True)
        return

    if metrics is None:
        metrics = {
            "Clarity": min(100, quality_score + 5),
            "Specificity": max(0, quality_score - 3),
            "Structure": min(100, quality_score + 2),
            "Completeness": max(0, quality_score - 5)
        }

    domain_icons = {"research": "🔬", "coding": "💻", "data_science": "📊", "general": "🌐"}
    task_icons = {"literature_review": "📚", "code_generation": "⚡", "bug_fix": "🐛", "api_design": "🔌", "data_analysis": "📈", "general_query": "💬"}

    d_icon = domain_icons.get(domain.lower(), "🌐")
    t_icon = task_icons.get(task_type.lower(), "💬")

    st.markdown("### 📊 Prompt Insights")

    col1, col2 = st.columns(2)
    with col1:
        st.info(f"{d_icon} {domain.replace('_', ' ').title()}")
    with col2:
        st.info(f"{t_icon} {task_type.replace('_', ' ').title()}")

    st.markdown("**Quality Score**")
    if quality_score >= 80:
        st.success(f"### {quality_score}/100")
    elif quality_score >= 60:
        st.warning(f"### {quality_score}/100")
    else:
        st.error(f"### {quality_score}/100")

    st.markdown("**Breakdown**")
    for name, value in metrics.items():
        st.caption(name)
        st.progress(value / 100)

    if suggestions:
        st.markdown("**Suggestions**")
        for s in suggestions[:3]:
            st.markdown(f"› {s}")


def render_file_indicator(filename: str, file_type: str):
    """Show file indicator"""
    icons = {"documents": "📄", "code": "💻", "images": "🖼️", "audio": "🎵", "unknown": "📎"}
    icon = icons.get(file_type, '📎')
    st.success(f"{icon} **{filename}**")
