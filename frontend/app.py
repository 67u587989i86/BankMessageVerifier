import streamlit as st
import requests
import os
import smtplib
from email.mime.text import MIMEText

st.set_page_config(page_title="Bank Message Verifier", page_icon="🛡️", layout="centered")

# URL of your Flask backend
BACKEND_URL = "http://localhost:5000"

st.title("🔍 Bank Message Verifier")
st.write("Protect yourself from fraud messages. Verify any SMS easily!")

# ---- USER INPUT ----
message = st.text_area("✉️ Paste the message here:", height=200)
sender = st.text_input("📨 Sender (Phone Number/Name):")

# ---- EMAIL REPORT FUNCTION ----
def send_cyber_complaint(sender, message):
    to_email = "helpdesk@cybercrime.gov.in"
    subject = "🚨 Scam Message Report"

    body = f"""
    Sender: {sender}
    Message: {message}
    Please investigate this suspicious message.
    """

    msg = MIMEText(body)
    msg["From"] = "yourapp@domain.com"
    msg["To"] = to_email
    msg["Subject"] = subject

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("dummyajay123@gmail.com", "dlbg dpvw hrfq gelb")  # Replace with real credentials
        server.send_message(msg)

# ---- ANALYZE MESSAGE ----
if st.button("Analyze Message"):
    if not message or not sender:
        st.error("❌ Please provide both message and sender.")
    else:
        with st.spinner('Analyzing...'):
            try:
                response = requests.post(f"{BACKEND_URL}/analyze", json={"message": message, "sender": sender})
                result = response.json()

                is_scam = result['is_scam']
                suspicious_links = result['suspicious_links']

                if is_scam:
                    st.error("🚨 This message is likely a SCAM!")
                else:
                    st.success("✅ This message looks safe!")

                st.markdown("---")
                st.page_link("pages/appeal_page.py", label="🚨 Appeal a Scam Report", icon="🚀")

                if suspicious_links:
                    st.subheader("🔗 Suspicious Links Found:")
                    for link in suspicious_links:
                        st.write(f"- {link}")

            except Exception as e:
                st.error(f"Server error: {e}")

st.divider()

# ---- REPORT to Cyber Cell ----
st.subheader("🚨 Report Message to Cyber Cell")
if st.button("Report Now"):
    if not message or not sender:
        st.error("❌ Please provide both message and sender.")
    else:
        with st.spinner('Reporting...'):
            try:
                send_cyber_complaint(sender, message)
                st.success("✅ Complaint sent to Cybersecurity Department.")
            except Exception as e:
                st.error(f"❌ Failed to send complaint: {e}")

st.divider()

# ---- Admin Section for Retraining ----
st.subheader("🛠️ Admin Tools")
admin_password = st.text_input("🔑 Enter Admin Password:", type="password")
if st.button("Retrain Model"):
    if admin_password == "admin123":
        with st.spinner('Retraining model...'):
            try:
                os.system("python retrain_model.py")
                st.success("✅ Model retrained successfully!")
            except Exception as e:
                st.error(f"Retraining failed: {e}")
    else:
        st.error("❌ Incorrect password.")
