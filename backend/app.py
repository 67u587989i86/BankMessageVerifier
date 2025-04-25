from flask import Flask, request, jsonify
import pickle
import os
from utils.link_checker import check_links
from email_report import send_cyber_complaint

app = Flask(__name__)

model = pickle.load(open('model/scam_model.pkl', 'rb'))
vectorizer = pickle.load(open('model/vectorizer.pkl', 'rb'))

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

if __name__ == '__main__':
    app.run(debug=True)
