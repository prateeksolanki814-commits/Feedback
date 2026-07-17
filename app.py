import streamlit as st
import pandas as pd
import os
from utils.database import init_db, load_feedback
from utils.config import FEEDBACK_FILE, STORE_INFO
from components.feedback_form import show_feedback_form
from components.analytics import show_analytics
from components.admin import show_admin_panel

# Initialize database
init_db()

# Page configuration
st.set_page_config(
    page_title=f"{STORE_INFO['name']} - Feedback System",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# PAGE FUNCTIONS
# ==========================================

def home():
    # Custom CSS
    st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(135deg, #FF4B4B 0%, #FF8E53 100%);
            color: white; padding: 2.5rem; border-radius: 15px;
            text-align: center; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .main-header h1 { margin: 0; font-size: 2.8rem; font-weight: 800; }
        .main-header p { margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9; }
        .stat-card {
            background: white; padding: 1.5rem; border-radius: 12px; text-align: center;
            margin: 0.5rem 0; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border-top: 4px solid #FF4B4B;
        }
        .stat-card h3 { color: #FF4B4B; font-size: 2.5rem; margin: 0; font-weight: 800; }
        .stat-card p { color: #6c757d; margin: 0.5rem 0 0 0; font-weight: 500; }
        .store-info {
            background: #f8f9fa; padding: 1.5rem; border-radius: 10px;
            margin: 1rem 0; border-left: 4px solid #1E88E5;
        }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>🛒 {STORE_INFO['name']}</h1>
        <p>{STORE_INFO['tagline']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🎯 Welcome to Our Feedback Platform")
        st.markdown("We're committed to providing the best shopping experience. Your feedback helps us understand what we're doing right and where we can improve.")
        
        st.markdown("#### 🚀 Quick Actions")
        nav_col1, nav_col2, nav_col3 = st.columns(3)
        
        # Safe navigation using page objects
        with nav_col1:
            if st.button("📝 Submit Feedback", use_container_width=True):
                st.switch_page(feedback_pg)
        with nav_col2:
            if st.button("📊 View Analytics", use_container_width=True):
                st.switch_page(analytics_pg)
        with nav_col3:
            if st.button("⚙️ Admin Panel", use_container_width=True):
                st.switch_page(admin_pg)

    with col2:
        st.markdown("#### 🏪 Store Information")
        st.markdown(f"""
        <div class="store-info">
            <p>📍 <strong>Address:</strong><br>{STORE_INFO['address']}</p>
            <p>📞 <strong>Phone:</strong><br>{STORE_INFO['phone']}</p>
            <p>✉️ <strong>Email:</strong><br>{STORE_INFO['email']}</p>
            <p>🕐 <strong>Hours:</strong><br>{STORE_INFO['hours']}</p>
        </div>
        """, unsafe_allow_html=True)

    # Stats
    st.markdown("---")
    st.markdown("### 📊 Quick Insights")

    if os.path.exists(FEEDBACK_FILE) and os.path.getsize(FEEDBACK_FILE) > 2:
        feedback_data = load_feedback()
        if feedback_data:
            df = pd.DataFrame(feedback_data)
            c1, c2, c3, c4 = st.columns(4)
            with c1: st.markdown(f'<div class="stat-card"><h3>{len(df)}</h3><p>Total Feedback</p></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="stat-card"><h3>{df["rating"].mean():.1f}⭐</h3><p>Average Rating</p></div>', unsafe_allow_html=True)
            with c3:
                positive = len(df[df['rating'] >= 4])
                st.markdown(f'<div class="stat-card"><h3>{positive}</h3><p>Positive Reviews</p></div>', unsafe_allow_html=True)
            with c4:
                recent = len(df[df['store_visit_date'] >= pd.Timestamp.now().strftime("%Y-%m-%d")])
                st.markdown(f'<div class="stat-card"><h3>{recent}</h3><p>Recent Feedback</p></div>', unsafe_allow_html=True)
        else:
            st.info("ℹ️ No feedback data yet. Be the first to share your experience!")
    else:
        st.info("ℹ️ No feedback data yet. Be the first to share your experience!")

def feedback_page():
    st.markdown('<h1 style="color:#FF4B4B; text-align:center;">📝 Customer Feedback Form</h1>', unsafe_allow_html=True)
    st.markdown("---")
    show_feedback_form()
    st.markdown("---")
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page(home_pg)

def analytics_page():
    st.markdown('<h1 style="color:#1E88E5; text-align:center;">📊 Feedback Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    show_analytics()
    st.markdown("---")
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page(home_pg)

def admin_page():
    st.markdown('<h1 style="color:#4CAF50; text-align:center;">⚙️ Admin Control Panel</h1>', unsafe_allow_html=True)
    st.markdown("---")
    show_admin_panel()
    st.markdown("---")
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page(home_pg)

# ==========================================
# NAVIGATION SETUP (The Modern Way)
# ==========================================
home_pg = st.Page(home, title="Home", icon="🛒", url_path="home", default=True)
feedback_pg = st.Page(feedback_page, title="Submit Feedback", icon="📝", url_path="submit_feedback")
analytics_pg = st.Page(analytics_page, title="View Analytics", icon="📊", url_path="analytics")
admin_pg = st.Page(admin_page, title="Admin Panel", icon="⚙️", url_path="admin")

# Build the navigation
pg = st.navigation([home_pg, feedback_pg, analytics_pg, admin_pg])

# Run the selected page
pg.run()
