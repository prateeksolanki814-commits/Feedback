import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# File paths
FEEDBACK_FILE = os.path.join(BASE_DIR, 'feedback_data.json')

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Store Information
STORE_INFO = {
    "name": "FreshMart Supermarket",
    "tagline": "Fresh Quality, Affordable Prices",
    "address": "123 Market Street, City Center",
    "phone": "+1 (555) 123-4567",
    "email": "hello@freshmart.com",
    "hours": "Mon-Sun: 8:00 AM - 10:00 PM"
}

# Feedback categories
FEEDBACK_CATEGORIES = [
    "Product Quality",
    "Customer Service",
    "Store Environment",
    "Pricing & Value",
    "Checkout Experience",
    "Product Availability",
    "Online Ordering",
    "Delivery Service",
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
