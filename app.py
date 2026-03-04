import os, requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

API_KEY = os.environ.get("GEMINI_API_KEY")
# Using the stable 'gemini-pro' model name which is highly available
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message", "")
    msg_lower = user_msg.lower()

    # 1. THE REFLEX (Hard-coded safety for the demo)
    if "s25" in msg_lower and "price" in msg_lower:
        return jsonify({"reply": "The Samsung S25 Ultra is K19,999. It's our top-tier flagship. Would you like to reserve one?"})
    
    if "iphone 16" in msg_lower and "price" in msg_lower:
        return jsonify({"reply": "The iPhone 16 Pro Max is K30,999. We have limited stock in Titanium. Shall I book your order?"})

    # 2. THE BRAIN (Customer Service Persona)
    payload = {
        "contents": [{"parts": [{"text": f"You are a professional customer service agent for Mobile City. Be helpful and polite. Customer: {user_msg}"}]}]
    }
    
    try:
        response = requests.post(URL, json=payload, timeout=10)
        result = response.json()
        
        # Check if the model 'gemini-pro' was found and responded
        if 'candidates' in result:
            answer = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": answer})
        else:
            # If gemini-pro isn't found, it will tell us why
            error_info = result.get('error', {}).get('message', 'Model syncing...')
            return jsonify({"reply": f"Service Notice: {error_info}"})
            
    except Exception as e:
        return jsonify({"reply": "Our AI agent is currently busy. Please leave your phone number."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

