import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# File paths
FEEDBACK_FILE = os.path.join(BASE_DIR, 'feedback_data.json')

# Admin credentials (In production, use environment variables)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Feedback categories
FEEDBACK_CATEGORIES = [
    "Product Quality",
    "Customer Service",
    "Store Environment",
    "Pricing & Value",
    "Checkout Experience",
    "Product Availability",
    "Other"
]

# Rating labels
RATING_LABELS = {
    1: "Poor",
    2: "Fair",
    3: "Good",
    4: "Very Good",
    5: "Excellent"
}

# App theme colors
THEME_COLORS = {
    "primary": "#FF4B4B",
    "secondary": "#1E88E5",
    "success": "#4CAF50",
    "warning": "#FF9800",
    "danger": "#F44336"
}
