import json
import os
from datetime import datetime
from utils.config import FEEDBACK_FILE

def init_db():
    """Initialize the feedback file if it doesn't exist."""
    if not os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'w') as f:
            json.dump([], f)

def load_feedback():
    """Load all feedback data from the JSON file."""
    try:
        with open(FEEDBACK_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading feedback: {e}")
        return []

def save_feedback(feedback_data):
    """Save feedback data to the JSON file."""
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback_data, f, indent=2)

def add_feedback(customer_name, rating, category, comments, store_visit_date):
    """Add a new feedback entry."""
    feedback = load_feedback()
    new_entry = {
        "id": len(feedback) + 1,
        "customer_name": customer_name,
        "rating": rating,
        "category": category,
        "comments": comments,
        "store_visit_date": store_visit_date,
        "submission_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sentiment": analyze_sentiment(comments)
    }
    feedback.append(new_entry)
    save_feedback(feedback)
    return new_entry

def delete_feedback(feedback_id):
    """Delete a feedback entry by ID."""
    feedback = load_feedback()
    feedback = [f for f in feedback if f['id'] != feedback_id]
    save_feedback(feedback)

def get_feedback_by_id(feedback_id):
    """Get a feedback entry by ID."""
    feedback = load_feedback()
    for f in feedback:
        if f['id'] == feedback_id:
            return f
    return None

def get_feedback_stats():
    """Get basic statistics about feedback."""
    feedback = load_feedback()
    if not feedback:
        return {
            "total": 0,
            "average_rating": 0,
            "positive_count": 0,
            "negative_count": 0,
            "category_counts": {}
        }
    
    df = pd.DataFrame(feedback)
    
    return {
        "total": len(df),
        "average_rating": df['rating'].mean(),
        "positive_count": len(df[df['rating'] >= 4]),
        "negative_count": len(df[df['rating'] <= 2]),
        "category_counts": df['category'].value_counts().to_dict()
    }

def analyze_sentiment(text):
    """Simple sentiment analysis based on keywords."""
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'best']
    negative_words = ['bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'poor', 'disappointing']
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return "Positive"
    elif negative_count > positive_count:
        return "Negative"
    else:
        return "Neutral"

# Add pandas import at the top
import pandas as pd
