import streamlit as st
from utils.database import add_feedback
from utils.config import FEEDBACK_CATEGORIES

def show_feedback_form():
    st.header("📝 We Value Your Feedback!")
    st.markdown("Please share your experience to help us improve our services.")
    
    # Form layout
    with st.form("feedback_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input(
                "👤 Your Name (Optional)", 
                placeholder="John Doe",
                help="Providing your name is optional but helps us follow up if needed"
            )
            store_visit_date = st.date_input(
                "📅 Visit Date",
                help="Select the date when you visited our supermarket"
            )
        
        with col2:
            st.write("⭐ Overall Rating")
            rating = st.feedback("stars")
            if rating is not None:
                rating += 1  # Convert 0-based to 1-based rating
                st.write(f"You selected: {rating} star(s)")
            
            category = st.selectbox(
                "📝 Feedback Category",
                FEEDBACK_CATEGORIES,
                help="Select the category that best fits your feedback"
            )
        
        # Detailed comments
        comments = st.text_area(
            "💬 Detailed Comments",
            placeholder="Please share specific details about your experience...",
            height=150,
            help="The more details you provide, the better we can understand and address your feedback"
        )
        
        # Optional contact information
        with st.expander("📧 Optional: Contact Information"):
            email = st.text_input("Email Address", placeholder="your.email@example.com")
            phone = st.text_input("Phone Number", placeholder="+1234567890")
        
        # Submit button
        submitted = st.form_submit_button("📤 Submit Feedback", use_container_width=True)
        
        if submitted:
            # Validation
            if rating is None:
                st.error("⚠️ Please provide a star rating!")
            elif not comments.strip():
                st.error("⚠️ Please provide detailed comments!")
            else:
                # Add feedback to database
                new_feedback = add_feedback(
                    customer_name if customer_name else "Anonymous",
                    rating,
                    category,
                    comments,
                    store_visit_date.strftime("%Y-%m-%d")
                )
                
                # Success message
                st.success("✅ Thank you for your feedback! Your input helps us improve.")
                st.balloons()
                
                # Display confirmation
                with st.expander("View Submitted Feedback"):
                    st.json(new_feedback)
                
                # Offer to submit another feedback
                if st.button("📝 Submit Another Feedback"):
                    st.rerun()
