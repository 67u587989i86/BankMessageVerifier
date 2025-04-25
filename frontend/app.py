import streamlit as st
import requests

st.title("🔐 Bank Message Verifier")

message = st.text_area("Paste the message:")
sender = st.text_input("Sender (optional):")

if st.button("Analyze"):
    response = requests.post("http://localhost:5000/analyze", json={"message": message, "sender": sender})
    result = response.json()

    if result['is_scam']:
        st.error("⚠️ This message looks like a scam!")
        st.write("Suspicious links:", result['suspicious_links'])

        if st.button("🚨 Complain & Appeal for Block"):
            report = requests.post("http://localhost:5000/report", json={"message": message, "sender": sender})
            st.success(report.json()['message'])
    else:
        st.success("✅ This message appears safe.")
