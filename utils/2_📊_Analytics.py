import streamlit as st
from components.analytics import show_analytics

# Page configuration
st.set_page_config(
    page_title="Analytics - Supermarket Feedback System",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .analytics-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Page content
st.markdown('<h1 class="analytics-header">📊 Feedback Analytics Dashboard</h1>', unsafe_allow_html=True)
st.markdown("---")

# Display analytics
show_analytics()

# Back to home button
if st.button("🏠 Back to Home"):
    st.switch_page("app.py")
