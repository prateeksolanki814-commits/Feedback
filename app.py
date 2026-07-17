import streamlit as st
import os
from utils.database import init_db, load_feedback
from utils.config import FEEDBACK_FILE, STORE_INFO
import pandas as pd

# Initialize database
init_db()

# Page configuration
st.set_page_config(
    page_title=f"{STORE_INFO['name']} - Feedback System",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF8E53 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.8rem;
        font-weight: 800;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    .info-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-left: 5px solid #FF4B4B;
        margin: 1rem 0;
        transition: transform 0.2s;
    }
    .stat-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stat-card h3 {
        color: #FF4B4B;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 800;
    }
    .stat-card p {
        color: #6c757d;
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }
    .store-info {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1E88E5;
    }
    .footer {
        text-align: center;
        color: #6c757d;
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid #e9ecef;
    }
    /* Style page_link to look like a button */
    div[data-testid="stPageLink-NavLink"] > a > div {
        justify-content: center;
    }
    .stPageLink-NavLink {
        background: white;
        border: 2px solid #FF4B4B;
        color: #FF4B4B;
        padding: 0.8rem 1rem;
        border-radius: 10px;
        font-weight: 600;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
        width: 100%;
        display: block;
    }
    .stPageLink-NavLink:hover {
        background: #FF4B4B;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown(f"""
<div class="main-header">
    <h1>🛒 {STORE_INFO['name']}</h1>
    <p>{STORE_INFO['tagline']}</p>
</div>
""", unsafe_allow_html=True)

# Welcome Section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎯 Welcome to Our Feedback Platform")
    st.markdown("""
    We're committed to providing the best shopping experience. Your feedback helps us understand 
    what we're doing right and where we can improve.
    """)
    
    # Navigation using st.page_link (Crash-proof)
    st.markdown("#### 🚀 Quick Actions")
    nav_col1, nav_col2, nav_col3 = st.columns(3)
    
    with nav_col1:
        st.page_link("pages/1_Feedback_Form.py", label="📝 Submit Feedback", use_container_width=True)
    
    with nav_col2:
        st.page_link("pages/2_Analytics.py", label="📊 View Analytics", use_container_width=True)
    
    with nav_col3:
        st.page_link("pages/3_Admin_Panel.py", label="⚙️ Admin Panel", use_container_width=True)

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

# Stats Section
st.markdown("---")
st.markdown("### 📊 Quick Insights")

if os.path.exists(FEEDBACK_FILE):
    feedback_data = load_feedback()
    if feedback_data:
        df = pd.DataFrame(feedback_data)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <h3>{len(df)}</h3>
                <p>Total Feedback</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_rating = df['rating'].mean()
            st.markdown(f"""
            <div class="stat-card">
                <h3>{avg_rating:.1f}⭐</h3>
                <p>Average Rating</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            positive = len(df[df['rating'] >= 4])
            st.markdown(f"""
            <div class="stat-card">
                <h3>{positive}</h3>
                <p>Positive Reviews</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            recent = len(df[df['store_visit_date'] >= pd.Timestamp.now().strftime("%Y-%m-%d")])
            st.markdown(f"""
            <div class="stat-card">
                <h3>{recent}</h3>
                <p>Recent Feedback</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ No feedback data yet. Be the first to share your experience!")
else:
    st.info("ℹ️ No feedback data yet. Be the first to share your experience!")

# Footer
st.markdown("---")
st.markdown(f"""
<div class="footer">
    <p>© 2024 {STORE_INFO['name']} | Feedback Management System</p>
    <p>Built with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)
