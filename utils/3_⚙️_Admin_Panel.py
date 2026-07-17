import streamlit as st
from components.admin import show_admin_panel

# Page configuration
st.set_page_config(
    page_title="Admin Panel - Supermarket Feedback System",
    page_icon="⚙️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .admin-header {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Page content
st.markdown('<h1 class="admin-header">⚙️ Admin Control Panel</h1>', unsafe_allow_html=True)
st.markdown("---")

# Display admin panel
show_admin_panel()

# Back to home button
if st.button("🏠 Back to Home"):
    st.switch_page("app.py")
