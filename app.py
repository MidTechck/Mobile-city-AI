import os, time, re, requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

API_KEY = os.environ.get("GEMINI_API_KEY")
# Direct URL for the stable Gemini 1.5 Flash API
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message", "")
    
    # 1. Hard-coded ROI (The "No-Fail" Zone)
    msg_lower = user_msg.lower()
    if "s25" in msg_lower and "how much" in msg_lower:
        return jsonify({"reply": "The Samsung S25 Ultra is K19,999. Would you like to reserve one?"})
    if "iphone 16" in msg_lower and "how much" in msg_lower:
        return jsonify({"reply": "The iPhone 16 Pro Max is K30,999. We have limited stock in Desert Titanium."})

    # 2. Direct REST API Call (Bypassing the buggy library)
    payload = {
        "contents": [{"parts": [{"text": f"You are Mobile City AI. Help the customer buy. User says: {user_msg}"}]}]
    }
    
    try:
        response = requests.post(URL, json=payload, timeout=10)
        result = response.json()
        
        # Extract the text from the complex Google JSON response
        answer = result['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"reply": answer})
    except Exception as e:
        return jsonify({"reply": f"Automation Syncing... (Error: {str(e)})"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

