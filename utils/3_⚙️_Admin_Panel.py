import streamlit as st
from components.admin import show_admin_panel
from utils.config import STORE_INFO

st.set_page_config(
    page_title=f"Admin - {STORE_INFO['name']}",
    page_icon="⚙️",
    layout="wide"
)

st.markdown("""
<style>
    .admin-header {
        background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .admin-header h1 {
        margin: 0;
        font-size: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="admin-header"><h1>⚙️ Admin Control Panel</h1></div>', unsafe_allow_html=True)

show_admin_panel()

st.markdown("---")
st.page_link("app.py", label="🏠 Back to Home", use_container_width=True)
