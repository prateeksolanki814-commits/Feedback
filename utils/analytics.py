import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.database import load_feedback
from utils.helpers import format_rating_stars, get_color_for_rating

def show_analytics():
    st.header("📊 Customer Feedback Analytics")
    
    feedback_data = load_feedback()
    
    if not feedback_data:
        st.info("ℹ️ No feedback data available yet. Be the first to share your feedback!")
        if st.button("📝 Submit Feedback"):
            st.switch_page("pages/1_Feedback_Form.py")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(feedback_data)
    
    # Key metrics
    st.subheader("📋 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Feedback", len(df))
    
    with col2:
        avg_rating = df['rating'].mean()
        st.metric("Average Rating", f"{avg_rating:.1f} ⭐")
    
    with col3:
        positive_feedback = len(df[df['rating'] >= 4])
        st.metric("Positive Feedback", f"{positive_feedback} ({positive_feedback/len(df)*100:.1f}%)")
    
    with col4:
        recent_feedback = len(df[df['store_visit_date'] >= pd.Timestamp.now().strftime("%Y-%m-%d")])
        st.metric("Recent Feedback", recent_feedback)
    
    st.markdown("---")
    
    # Rating distribution
    st.subheader("⭐ Rating Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        rating_counts = df['rating'].value_counts().sort_index()
        
        fig, ax = plt.subplots(figsize=(8, 4))
        bars = ax.bar(rating_counts.index, rating_counts.values, color='skyblue')
        ax.set_xlabel('Rating (Stars)')
        ax.set_ylabel('Number of Feedback')
        ax.set_title('Customer Rating Distribution')
        ax.set_xticks(range(1, 6))
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')
        
        st.pyplot(fig)
        plt.close()
    
    with col2:
        # Rating distribution pie chart
        fig, ax = plt.subplots(figsize=(8, 4))
        colors = ['#FF6B6B', '#FFA94D', '#FFD93D', '#6BCB77', '#4D96FF']
        ax.pie(rating_counts.values, labels=rating_counts.index, autopct='%1.1f%%',
               colors=colors, startangle=90)
        ax.set_title('Rating Distribution Percentage')
        st.pyplot(fig)
        plt.close()
    
    # Feedback by category
    st.subheader("📝 Feedback by Category")
    category_counts = df['category'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(category_counts.index, category_counts.values, color='lightgreen')
    ax.set_xlabel('Number of Feedback')
    ax.set_title('Feedback Distribution by Category')
    
    # Add value labels on bars
    for i, (category, count) in enumerate(zip(category_counts.index, category_counts.values)):
        ax.text(count, i, f' {count}', va='center')
    
    st.pyplot(fig)
    plt.close()
    
    # Recent feedback table
    st.subheader("📅 Recent Feedback")
    recent_df = df.sort_values('submission_time', ascending=False).head(10)
    
    # Format display
    display_df = recent_df[['customer_name', 'rating', 'category', 'comments', 'store_visit_date']].copy()
    display_df.columns = ['Customer', 'Rating', 'Category', 'Comments', 'Visit Date']
    display_df['Rating'] = display_df['Rating'].apply(lambda x: f"{x} ⭐")
    
    st.dataframe(display_df, use_container_width=True)
    
    # Feedback trends over time
    st.subheader("📈 Feedback Trends Over Time")
    df['date'] = pd.to_datetime(df['store_visit_date'])
    daily_feedback = df.groupby(df['date'].dt.date).size().reset_index()
    daily_feedback.columns = ['Date', 'Count']
    
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(daily_feedback['Date'], daily_feedback['Count'], 
           marker='o', linewidth=2, markersize=8, color='coral')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Feedback')
    ax.set_title('Daily Feedback Count Trend')
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close()
