import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Admin Dashboard", page_icon="🛡️", layout="wide")

st.title("🛡️ Admin Dashboard - Feedback Monitoring")

# Path to the feedback CSV


feedback_file = os.path.join('bank-message-verifier', 'backend', 'data', 'new_training_data.csv')

# Load feedback data
def load_feedback():
    if os.path.exists(feedback_file):
        return pd.read_csv(feedback_file, usecols=["message", "sender", "user_reason", "label"], on_bad_lines='skip')
    return pd.DataFrame(columns=["message", "sender", "user_reason", "label"])

# Load data
feedback_data = load_feedback()

# Display feedback count
st.subheader("📊 Feedback Summary")
st.metric("Total Feedbacks", len(feedback_data))

# Show feedback table
st.subheader("📝 Feedback Records")
if feedback_data.empty:
    st.warning("⚠️ No feedback data available yet.")
else:
    st.dataframe(feedback_data)

# Footer
st.caption("Made with ❤️ to protect users from scams.")
