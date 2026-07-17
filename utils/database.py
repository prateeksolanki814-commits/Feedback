import json
import os
from datetime import datetime
import pandas as pd
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
    except Exception:
        return []

def save_feedback(feedback_data):
    """Save feedback data to the JSON file."""
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback_data, f, indent=2)

def add_feedback(customer_name, rating, category, comments, store_visit_date, contact_info=None):
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
        "sentiment": analyze_sentiment(comments),
        "contact_info": contact_info or {}
    }
    feedback.append(new_entry)
    save_feedback(feedback)
    return new_entry

def delete_feedback(feedback_id):
    """Delete a feedback entry by ID."""
    feedback = load_feedback()
    feedback = [f for f in feedback if f['id'] != feedback_id]
    save_feedback(feedback)

def analyze_sentiment(text):
    """Simple sentiment analysis based on keywords."""
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'best', 'fresh', 'clean', 'helpful', 'friendly']
    negative_words = ['bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'poor', 'disappointing', 'slow', 'rude', 'expired', 'dirty']
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return "Positive"
    elif negative_count > positive_count:
        return "Negative"
    else:
        return "Neutral"
