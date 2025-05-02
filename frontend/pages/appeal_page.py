import streamlit as st
import requests

st.set_page_config(page_title="Appeal - Bank Verifier", page_icon="🙋", layout="centered")

BACKEND_URL = "http://localhost:5000"

st.title("🙋 Appeal Against Scam Prediction")
st.write("Think the message was wrongly classified? Help us by submitting feedback.")

# ---- USER INPUT ----
message = st.text_area("✉️ Paste the message you analyzed:", height=200)
sender = st.text_input("📨 Sender (Phone Number/Name):")
user_reason = st.text_area("✍️ Why do you think it's wrong?", height=100)

if st.button("Submit Appeal"):
    if not message or not sender or not user_reason:
        st.error("❌ Please fill all fields before submitting.")
    else:
        with st.spinner('Submitting your feedback...'):
            try:
                feedback_response = requests.post(f"{BACKEND_URL}/feedback", json={
                    "message": message,
                    "sender": sender,
                    "user_reason": user_reason
                })
                if feedback_response.status_code == 200:
                    st.success("✅ Thank you for your feedback! We'll review it.")
                else:
                    st.error("❌ Failed to submit feedback. Try again later.")
            except Exception as e:
                st.error(f"Server error during submission: {e}")
