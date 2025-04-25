import smtplib
from email.mime.text import MIMEText

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
        server.login("yourapp@domain.com", "yourpassword")
        server.send_message(msg)
