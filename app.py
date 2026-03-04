import os, time, requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

# Google API Configuration
API_KEY = os.environ.get("GEMINI_API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message", "")
    msg_lower = user_msg.lower()

    # 1. ENTERPRISE KNOWLEDGE BASE (Safety Net)
    # This acts as 'Reflexes' for customer service to ensure accuracy
    if "s25" in msg_lower and ("price" in msg_lower or "how much" in msg_lower):
        return jsonify({"reply": "The Samsung S25 Ultra is K19,999. It includes a 2-year warranty and a free silicon cover. Would you like to reserve one?"})
    
    if "iphone 16" in msg_lower and ("price" in msg_lower or "how much" in msg_lower):
        return jsonify({"reply": "The iPhone 16 Pro Max is K30,999. We currently have Desert Titanium and Black Titanium in stock. Shall I book an appointment for a viewing?"})

    # 2. CUSTOMER SERVICE BRAIN (Google Gemini)
    # The 'Context' tells the AI how to behave like a professional agent
    context = (
        "You are the Lead Customer Service Agent at Mobile City Zambia. "
        "Be polite, professional, and helpful. If a user asks for a discount, "
        "politely ask for their phone number so a manager can contact them. "
        "Your goal is to provide excellent service and close sales."
    )
    
    payload = {
        "contents": [{"parts": [{"text": f"{context}\nCustomer: {user_msg}"}]}]
    }
    
    try:
        response = requests.post(URL, json=payload, timeout=10)
        result = response.json()
        
        # Log response to Railway for debugging
        print(f"DEBUG: {result}")

        # Check for successful AI response
        if 'candidates' in result and result['candidates']:
            answer = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": answer})
        
        # Handle specific Google Errors (like regional blocks or key issues)
        elif 'error' in result:
            error_msg = result['error'].get('message', 'Service Temporarily Unavailable')
            return jsonify({"reply": f"Customer Service Note: {error_msg}. Please leave your number for a callback."})
        
        else:
            return jsonify({"reply": "I am currently checking our live inventory. Please leave your WhatsApp number and I will get back to you in 2 minutes."})
            
    except Exception as e:
        return jsonify({"reply": "System optimization in progress. How else can I assist you today?"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

