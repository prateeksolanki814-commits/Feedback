import streamlit as st
import pandas as pd
import plotly.express as px
from utils.database import load_feedback

def show_analytics():
    feedback_data = load_feedback()
    
    if not feedback_data:
        st.info("ℹ️ No feedback data available yet. Be the first to share your feedback!")
        st.page_link("pages/1_Feedback_Form.py", label="📝 Submit Feedback", use_container_width=True)
        return
    
    df = pd.DataFrame(feedback_data)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Feedback", len(df))
    with col2: st.metric("Average Rating", f"{df['rating'].mean():.1f} ⭐")
    with col3:
        positive = len(df[df['rating'] >= 4])
        st.metric("Positive Feedback", f"{positive} ({positive/len(df)*100:.1f}%)")
    with col4:
        recent = len(df[df['store_visit_date'] >= pd.Timestamp.now().strftime("%Y-%m-%d")])
        st.metric("Recent Feedback", recent)
    
    st.markdown("---")
    
    # Interactive Charts with Plotly
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⭐ Rating Distribution")
        rating_counts = df['rating'].value_counts().sort_index().reset_index()
        rating_counts.columns = ['Rating', 'Count']
        
        fig = px.bar(
            rating_counts, x='Rating', y='Count', 
            color='Rating', 
            color_discrete_map={1:'#F44336', 2:'#FF9800', 3:'#FFC107', 4:'#8BC34A', 5:'#4CAF50'},
            text='Count'
        )
        fig.update_layout(showlegend=False, xaxis=dict(dtick=1))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📝 Feedback by Category")
        category_counts = df['category'].value_counts().reset_index()
        category_counts.columns = ['Category', 'Count']
        
        fig = px.pie(
            category_counts, values='Count', names='Category', 
            hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent Feedback Table
    st.markdown("#### 📅 Recent Feedback")
    recent_df = df.sort_values('submission_time', ascending=False).head(10)
    display_df = recent_df[['customer_name', 'rating', 'category', 'comments', 'store_visit_date']].copy()
    display_df.columns = ['Customer', 'Rating', 'Category', 'Comments', 'Visit Date']
    display_df['Rating'] = display_df['Rating'].apply(lambda x: f"{'⭐'*int(x)}")
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Trends
    st.markdown("#### 📈 Feedback Trends Over Time")
    df['date'] = pd.to_datetime(df['store_visit_date'])
    daily_feedback = df.groupby(df['date'].dt.date).size().reset_index()
    daily_feedback.columns = ['Date', 'Count']
    
    fig = px.line(daily_feedback, x='Date', y='Count', markers=True)
    fig.update_traces(line_color='#FF4B4B', line_width=3)
    fig.update_layout(xaxis_title='Date', yaxis_title='Number of Feedback')
    st.plotly_chart(fig, use_container_width=True)
