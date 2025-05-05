from flask import Flask, render_template, request, jsonify, redirect, session
import pickle
import os
import csv
import sqlite3
import smtplib
from email.mime.text import MIMEText
from utils.link_checker import check_links
from email_report import send_cyber_complaint

app = Flask(__name__, template_folder='templates')
app.secret_key = 'securekey123'

# Load model and vectorizer
model = pickle.load(open('model/scam_model.pkl', 'rb'))
vectorizer = pickle.load(open('model/vectorizer.pkl', 'rb'))

def init_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        email TEXT UNIQUE,
                        password TEXT,
                        aadhaar TEXT)''')
    conn.commit()
    conn.close()

# Aadhaar Validation
def is_valid_aadhaar(aadhaar):
    return aadhaar.isdigit() and len(aadhaar) == 12

# Admin Alert Email
def send_admin_alert():
    sender_email = "sg415218@gmail.com"
    receiver_email = "e1062240038@timscdrmumbai.in"
    password = "Ajay@22102002"  # Use App Password

    subject = "🚨 Feedback Threshold Reached!"
    body = "More than 2 feedbacks received. Kindly review and retrain the model."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("✅ Admin Alert Sent")
    except Exception as e:
        print(f"❌ Failed to send alert: {e}")

# --- ROUTES ---

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        aadhaar = request.form['aadhaar']

        if not is_valid_aadhaar(aadhaar):
            return '''<script>alert("❌ Invalid Aadhaar!"); window.history.back();</script>'''

        try:
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, password, aadhaar) VALUES (?, ?, ?, ?)",
                           (name, email, password, aadhaar))
            conn.commit()
            return redirect('/login')
        except sqlite3.IntegrityError:
            return '''<script>alert("⚠️ Email already registered!"); window.history.back();</script>'''
        finally:
            conn.close()
    return render_template('register.html')  # ✅ updated to match new filename

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        aadhaar = request.form['aadhaar']

        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM users WHERE email = ? AND password = ? AND name = ? AND aadhaar = ?",
                       (email, password, name, aadhaar))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = user[0]
            return redirect('/welcome')
        else:
            return '''<script>alert("❌ Invalid credentials!"); window.history.back();</script>'''
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    user_name = session.get('user', 'User')  # fallback to 'User' if not found
    return f'''
        <html>
            <head>
                <title>Welcome</title>
            </head>
            <body style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;">
                <h1>🎉 Login Successful, Welcome {user_name}!😊😊</h1>
                <a href="http://localhost:8502" style="margin-top:20px; padding:15px 30px; background-color:#4CAF50; color:white; text-decoration:none; border-radius:10px; font-size:18px;">🚀 Go to Analyzer</a>
            </body>
        </html>
    '''

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    message = data.get("message")
    sender = data.get("sender")

    vec = vectorizer.transform([message])
    pred = model.predict(vec)[0]

    links = check_links(message)

    return jsonify({
        "is_scam": bool(pred),
        "message": message,
        "suspicious_links": links
    })

@app.route('/report', methods=['POST'])
def report():
    data = request.json
    message = data.get("message")
    sender = data.get("sender")

    send_cyber_complaint(sender, message)

    return jsonify({"status": "reported", "message": "Complaint sent to cybersecurity."})

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    message = data.get("message")
    sender = data.get("sender")
    user_reason = data.get("user_reason")

    feedback_file = 'data/new_training_data.csv'

    # Ensure folder exists
    os.makedirs(os.path.dirname(feedback_file), exist_ok=True)

    # Save feedback
    file_exists = os.path.isfile(feedback_file)
    with open(feedback_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['label', 'message'])  # Header
        writer.writerow(["spam", message])  

    # 🚨 Check if alert needed
    with open(feedback_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        feedback_entries = list(reader)

        if len(feedback_entries) >= 2:
            send_admin_alert()

    return jsonify({"status": "success", "message": "📝 Feedback recorded. Thank you for improving our system!"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
