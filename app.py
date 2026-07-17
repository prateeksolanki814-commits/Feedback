import streamlit as st
import os
from utils.database import init_db
from utils.config import FEEDBACK_FILE

# Initialize database
init_db()

# Page configuration
st.set_page_config(
    page_title="Supermarket Feedback System",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #1E88E5;
        margin-top: 2rem;
    }
    .info-box {
        background-color: #F0F2F6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown('<h1 class="main-header">🛒 Supermarket Customer Feedback System</h1>', unsafe_allow_html=True)
st.markdown("---")

# Welcome section
st.markdown("""
## 🎯 Welcome to Our Feedback Platform

We value your feedback! This system helps us collect and analyze customer experiences to improve our supermarket services.

### 📋 What You Can Do Here:
- **📝 Submit Feedback**: Share your shopping experience with us
- **📊 View Analytics**: See feedback trends and statistics
- **⚙️ Admin Panel**: Manage feedback (administrators only)

### 👉 How to Use:
1. Use the **sidebar** to navigate between pages
2. On the **Feedback Form** page, share your experience
3. On the **Analytics** page, view feedback insights
4. Admins can log in to the **Admin Panel** to manage all feedback
""")

# Quick stats if data exists
if os.path.exists(FEEDBACK_FILE):
    from utils.database import load_feedback
    import pandas as pd
    
    feedback_data = load_feedback()
    if feedback_data:
        df = pd.DataFrame(feedback_data)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Feedback", len(df))
        
        with col2:
            avg_rating = df['rating'].mean()
            st.metric("Average Rating", f"{avg_rating:.1f} ⭐")
        
        with col3:
            positive = len(df[df['rating'] >= 4])
            st.metric("Positive Feedback", f"{positive} ({positive/len(df)*100:.1f}%)")
        
        st.markdown('<div class="info-box">📊 <strong>Quick Stats:</strong> Our system has collected feedback from many customers. Visit the Analytics page for detailed insights!</div>', unsafe_allow_html=True)

# Call to action
st.markdown("## 🚀 Get Started")
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("📝 Submit Feedback Now", use_container_width=True):
        st.switch_page("pages/1_📝_Feedback_Form.py")

with col2:
    if st.button("📊 View Analytics", use_container_width=True):
        st.switch_page("pages/2_📊_Analytics.py")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Supermarket Feedback System | Created with Streamlit</p>
    <p>Your feedback helps us improve our services</p>
</div>
""", unsafe_allow_html=True)
