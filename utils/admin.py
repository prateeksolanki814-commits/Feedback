import streamlit as st
import pandas as pd
import plotly.express as px
from utils.database import load_feedback, delete_feedback
from utils.config import ADMIN_USERNAME, ADMIN_PASSWORD
from utils.helpers import get_table_download_link

def show_admin_panel():
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    
    if not st.session_state.admin_logged_in:
        with st.form("admin_login"):
            st.markdown("### 🔐 Admin Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login", use_container_width=True)
            
            if login_button:
                if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials!")
    else:
        st.success("✅ Logged in as Admin")
        
        feedback_data = load_feedback()
        if not feedback_data:
            st.info("ℹ️ No feedback data available.")
            return
        
        df = pd.DataFrame(feedback_data)
        tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📝 Manage Feedback", "📤 Export"])
        
        with tab1:
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Total Feedback", len(df))
            with col2: st.metric("Average Rating", f"{df['rating'].mean():.2f}")
            with col3: st.metric("Negative Feedback", len(df[df['rating'] <= 2]))
            
            st.markdown("#### Rating Distribution by Category")
            pivot_df = df.groupby(['category', 'rating']).size().unstack(fill_value=0).reset_index()
            fig = px.bar(pivot_df, x='category', y=[1, 2, 3, 4, 5], 
                         labels={'value':'Count', 'category':'Category', 'variable':'Rating'},
                         color_discrete_map={1:'#F44336', 2:'#FF9800', 3:'#FFC107', 4:'#8BC34A', 5:'#4CAF50'})
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.markdown("#### All Feedback Records")
            
            col1, col2 = st.columns(2)
            with col1:
                rating_filter = st.multiselect("Filter by Rating", options=[1, 2, 3, 4, 5], default=[1, 2, 3, 4, 5])
            with col2:
                search_term = st.text_input("🔍 Search Comments")
            
            filtered_df = df[df['rating'].isin(rating_filter)]
            if search_term:
                filtered_df = filtered_df[filtered_df['comments'].str.contains(search_term, case=False, na=False)]
            
            display_df = filtered_df[['id', 'customer_name', 'rating', 'category', 'comments', 'store_visit_date']].copy()
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            if len(filtered_df) > 0:
                selected_id = st.selectbox("Select Feedback ID to Delete", filtered_df['id'].values)
                if st.button("🗑️ Delete Selected Feedback", type="primary"):
                    delete_feedback(selected_id)
                    st.success(f"✅ Feedback ID {selected_id} deleted successfully!")
                    st.rerun()
        
        with tab3:
            st.markdown("#### Export Feedback Data")
            st.markdown(get_table_download_link(df, "supermarket_feedback", "csv"), unsafe_allow_html=True)
            st.markdown(get_table_download_link(df, "supermarket_feedback", "json"), unsafe_allow_html=True)
            
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.admin_logged_in = False
                st.rerun()
