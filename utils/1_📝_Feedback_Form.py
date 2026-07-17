import streamlit as st
from components.feedback_form import show_feedback_form
from utils.config import STORE_INFO

st.set_page_config(page_title=f"Feedback - {STORE_INFO['name']}", page_icon="📝", layout="wide")

st.markdown("""
<style>
    .form-header {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF8E53 100%);
        color: white; padding: 1.5rem; border-radius: 12px; text-align: center; margin-bottom: 2rem;
    }
    .form-header h1 { margin: 0; font-size: 2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="form-header"><h1>📝 Customer Feedback Form</h1></div>', unsafe_allow_html=True)
show_feedback_form()

st.markdown("---")
st.page_link("app.py", label="🏠 Back to Home", use_container_width=True)
