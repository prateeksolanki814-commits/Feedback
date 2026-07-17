import streamlit as st
from components.feedback_form import show_feedback_form

# Page configuration
st.set_page_config(
    page_title="Feedback Form - Supermarket Feedback System",
    page_icon="📝",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .feedback-header {
        font-size: 2.5rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Page content
st.markdown('<h1 class="feedback-header">📝 Customer Feedback Form</h1>', unsafe_allow_html=True)
st.markdown("---")

# Display feedback form
show_feedback_form()

# Back to home button
if st.button("🏠 Back to Home"):
    st.switch_page("app.py")
