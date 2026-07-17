import streamlit as st
from utils.database import add_feedback
from utils.config import FEEDBACK_CATEGORIES

def show_feedback_form():
    st.markdown("### We Value Your Feedback!")
    st.markdown("Please share your shopping experience with us. Your feedback helps us improve our services.")
    
    with st.form("feedback_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👤 Your Information")
            customer_name = st.text_input("Name", placeholder="John Doe", help="Optional - helps us follow up if needed")
            store_visit_date = st.date_input("📅 Visit Date", help="When did you visit our store?")
            
            st.markdown("#### ⭐ Overall Rating")
            rating = st.feedback("stars")
            if rating is not None:
                rating += 1
                st.success(f"You selected: {rating} star(s)")
        
        with col2:
            st.markdown("#### 📝 Feedback Details")
            category = st.selectbox("Category", FEEDBACK_CATEGORIES, help="Select the area your feedback relates to")
            
            st.markdown("#### 💬 Your Comments")
            comments = st.text_area("Share your experience", placeholder="Tell us what you liked or what we can improve...", height=120)
            
            with st.expander("📧 Contact Information (Optional)"):
                email = st.text_input("Email", placeholder="your.email@example.com")
                phone = st.text_input("Phone", placeholder="+1234567890")
        
        st.markdown("---")
        submitted = st.form_submit_button("📤 Submit Feedback", use_container_width=True, type="primary")
        
        if submitted:
            if rating is None:
                st.error("⚠️ Please provide a star rating!")
            elif not comments.strip():
                st.error("⚠️ Please provide detailed comments!")
            else:
                contact_info = {}
                if email: contact_info['email'] = email
                if phone: contact_info['phone'] = phone
                
                add_feedback(
                    customer_name if customer_name else "Anonymous",
                    rating,
                    category,
                    comments,
                    store_visit_date.strftime("%Y-%m-%d"),
                    contact_info
                )
                
                st.success("🎉 Thank you for your feedback! We appreciate your time.")
                st.balloons()
