import base64
import pandas as pd
from datetime import datetime

def get_table_download_link(df, filename_prefix, file_type="csv"):
    """Generates a link to download a dataframe as CSV or JSON."""
    if file_type == "csv":
        data = df.to_csv(index=False)
        b64 = base64.b64encode(data.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename_prefix}_{datetime.now().strftime("%Y%m%d")}.csv">📥 Download CSV File</a>'
    else:
        data = df.to_json(orient="records")
        b64 = base64.b64encode(data.encode()).decode()
        href = f'<a href="data:file/json;base64,{b64}" download="{filename_prefix}_{datetime.now().strftime("%Y%m%d")}.json">📥 Download JSON File</a>'
    
    return href

def format_rating_stars(rating):
    """Format rating as stars."""
    full_stars = int(rating)
    half_star = rating - full_stars >= 0.5
    
    stars = "⭐" * full_stars
    if half_star:
        stars += "✨"
    
    return stars

def get_color_for_rating(rating):
    """Get color based on rating."""
    if rating >= 4:
        return "#4CAF50"  # Green
    elif rating >= 3:
        return "#FF9800"  # Orange
    else:
        return "#F44336"  # Red

def get_color_for_sentiment(sentiment):
    """Get color based on sentiment."""
    if sentiment == "Positive":
        return "#4CAF50"
    elif sentiment == "Negative":
        return "#F44336"
    else:
        return "#FF9800"

def create_metrics_card(title, value, color="#1E88E5"):
    """Create a styled metrics card."""
    return f"""
    <div style="
        background-color: {color}15;
        border-left: 5px solid {color};
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    ">
        <h3 style="color: {color}; margin: 0;">{title}</h3>
        <p style="font-size: 1.5rem; margin: 0.5rem 0;">{value}</p>
    </div>
    """
