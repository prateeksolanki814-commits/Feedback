import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.database import load_feedback, delete_feedback
from utils.config import ADMIN_USERNAME, ADMIN_PASSWORD
from utils.helpers import get_table_download_link

def show_admin_panel():
    st.header("⚙️ Admin Panel")
    
    # Authentication
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    
    if not st.session_state.admin_logged_in:
        with st.form("admin_login"):
            st.subheader("🔐 Admin Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")
            
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
        
        # Admin tabs
        admin_tab1, admin_tab2, admin_tab3, admin_tab4 = st.tabs([
            "📊 Dashboard", "📝 All Feedback", "📈 Trends", "📤 Export"
        ])
        
        with admin_tab1:
            st.subheader("📊 Admin Dashboard")
            
            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Feedback", len(df))
            
            with col2:
                avg_rating = df['rating'].mean()
                st.metric("Average Rating", f"{avg_rating:.2f}")
            
            with col3:
                negative_feedback = len(df[df['rating'] <= 2])
                st.metric("Negative Feedback", negative_feedback)
            
            with col4:
                response_rate = (len(df[df['comments'].str.len() > 10]) / len(df)) * 100
                st.metric("Response Rate", f"{response_rate:.1f}%")
            
            # Rating distribution by category
            st.subheader("📊 Rating Distribution by Category")
            
            # Create a pivot table
            pivot_df = df.groupby(['category', 'rating']).size().unstack(fill_value=0)
            
            fig, ax = plt.subplots(figsize=(12, 6))
            pivot_df.plot(kind='bar', stacked=True, ax=ax, 
                         color=['#FF6B6B', '#FFA94D', '#FFD93D', '#6BCB77', '#4D96FF'])
            ax.set_xlabel('Category')
            ax.set_ylabel('Count')
            ax.set_title('Rating Distribution by Category')
            ax.legend(title='Rating', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        
        with admin_tab2:
            st.subheader("📝 All Feedback Records")
            
            # Filter options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                rating_filter = st.multiselect(
                    "Filter by Rating",
                    options=[1, 2, 3, 4, 5],
                    default=[1, 2, 3, 4, 5]
                )
            
            with col2:
                category_filter = st.multiselect(
                    "Filter by Category",
                    options=df['category'].unique(),
                    default=df['category'].unique()
                )
            
            with col3:
                search_term = st.text_input("🔍 Search in Comments")
            
            # Apply filters
            filtered_df = df[
                (df['rating'].isin(rating_filter)) &
                (df['category'].isin(category_filter))
            ]
            
            if search_term:
                filtered_df = filtered_df[
                    filtered_df['comments'].str.contains(search_term, case=False, na=False)
                ]
            
            # Display filtered data
            st.write(f"**Showing {len(filtered_df)} of {len(df)} feedback records**")
            
            # Format display
            display_df = filtered_df[['id', 'customer_name', 'rating', 'category', 
                                     'comments', 'store_visit_date', 'submission_time']].copy()
            display_df.columns = ['ID', 'Customer', 'Rating', 'Category', 'Comments', 
                                  'Visit Date', 'Submission Time']
            display_df['Rating'] = display_df['Rating'].apply(lambda x: f"{x} ⭐")
            
            st.dataframe(display_df, use_container_width=True)
            
            # Feedback details
            if len(filtered_df) > 0:
                selected_id = st.selectbox(
                    "Select Feedback ID for Details",
                    filtered_df['id'].values
                )
                
                selected_feedback = filtered_df[filtered_df['id'] == selected_id].iloc[0]
                
                with st.expander("📋 Feedback Details"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Customer:** {selected_feedback['customer_name']}")
                        st.write(f"**Rating:** {selected_feedback['rating']} ⭐")
                        st.write(f"**Category:** {selected_feedback['category']}")
                        st.write(f"**Visit Date:** {selected_feedback['store_visit_date']}")
                    
                    with col2:
                        st.write(f"**Submission Time:** {selected_feedback['submission_time']}")
                        st.write(f"**Feedback ID:** {selected_feedback['id']}")
                    
                    st.write("**Comments:**")
                    st.write(selected_feedback['comments'])
                    
                    # Delete button
                    if st.button("🗑️ Delete This Feedback"):
                        delete_feedback(selected_id)
                        st.success(f"✅ Feedback ID {selected_id} deleted successfully!")
                        st.rerun()
        
        with admin_tab3:
            st.subheader("📈 Feedback Trends & Analysis")
            
            # Category analysis
            st.write("**Feedback Distribution by Category**")
            category_stats = df.groupby('category').agg({
                'rating': ['count', 'mean', 'std']
            }).round(2)
            category_stats.columns = ['Count', 'Average Rating', 'Std Dev']
            
            st.dataframe(category_stats, use_container_width=True)
            
            # Time series analysis
            st.write("**Feedback Trends Over Time**")
            df['date'] = pd.to_datetime(df['store_visit_date'])
            daily_avg = df.groupby(df['date'].dt.date)['rating'].mean().reset_index()
            daily_avg.columns = ['Date', 'Average Rating']
            
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(daily_avg['Date'], daily_avg['Average Rating'], 
                   marker='o', linewidth=2, markersize=8, color='coral')
            ax.set_xlabel('Date')
            ax.set_ylabel('Average Rating')
            ax.set_title('Daily Average Rating Trend')
            ax.set_ylim(0, 5.5)
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            plt.close()
        
        with admin_tab4:
            st.subheader("📤 Export Feedback Data")
            
            # Export to CSV
            st.markdown(get_table_download_link(df, "supermarket_feedback", "csv"), unsafe_allow_html=True)
            
            # Export to JSON
            st.markdown(get_table_download_link(df, "supermarket_feedback", "json"), unsafe_allow_html=True)
            
            # Display raw data
            with st.expander("View Raw Data"):
                st.json(feedback_data)
            
            # Logout button
            if st.button("🚪 Logout"):
                st.session_state.admin_logged_in = False
                st.rerun()
