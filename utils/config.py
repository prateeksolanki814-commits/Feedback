import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FEEDBACK_FILE = os.path.join(BASE_DIR, '..', 'feedback_data.json')

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

STORE_INFO = {
    "name": "FreshMart Supermarket",
    "tagline": "Fresh Quality, Affordable Prices",
    "address": "123 Market Street, City Center",
    "phone": "+1 (555) 123-4567",
    "email": "hello@freshmart.com",
    "hours": "Mon-Sun: 8:00 AM - 10:00 PM"
}

FEEDBACK_CATEGORIES = [
    "Product Quality", "Customer Service", "Store Environment",
    "Pricing & Value", "Checkout Experience", "Product Availability",
    "Online Ordering", "Delivery Service", "Other"
]
