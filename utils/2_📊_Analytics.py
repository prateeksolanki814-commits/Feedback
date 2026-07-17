import streamlit as st
from components.analytics import show_analytics
from utils.config import STORE_INFO

st.set_page_config(page_title=f"Analytics - {STORE_INFO['name']}", page_icon="📊", layout="wide")

st.markdown("""
<style>
    .analytics-header {
        background: linear-gradient(135deg, #1E88E5 0%, #42A5F5 100%);
        color: white; padding: 1.5rem; border-radius: 12px; text-align: center; margin-bottom: 2rem;
    }
    .analytics-header h1 { margin: 0; font-size: 2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="analytics-header"><h1>📊 Feedback Analytics Dashboard</h1></div>', unsafe_allow_html=True)
show_analytics()

st.markdown("---")
st.page_link("app.py", label="🏠 Back to Home", use_container_width=True)
