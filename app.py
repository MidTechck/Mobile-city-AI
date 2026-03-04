import os
import time
import re
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__, static_folder='.')
CORS(app)

# Configuration for stability
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def save_lead(text):
    """Saves Zambian phone numbers to a file for the owner"""
    # Detects numbers starting with +260, 09, or 07
    numbers = re.findall(r'(\+?260|0)[79][567]\d{7}', text)
    if numbers:
        try:
            with open("leads.txt", "a") as f:
                for num in numbers:
                    f.write(f"{time.ctime()}: {num}\n")
        except Exception as e:
            print(f"Lead Save Error: {e}")

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")
        
        # 1. Automate Lead Capture
        save_lead(user_msg)

        # 2. Set the 'Ruthless' AI Context
        context = (
            "You are the Mobile City Enterprise AI. Your word is 'Automation'. "
            "Help the owner grow ROI. Prices: S25 Ultra-K19,999, iPhone 16 Pro Max-K30,999. "
            "Be professional and brief. If the user wants a deal, ask for their phone number "
            "so a manager can call them back."
        )

        # 3. Robust Retry Logic for Demo Stability
        for attempt in range(3):
            try:
                response = model.generate_content(f"{context}\nCustomer: {user_msg}")
                return jsonify({"reply": response.text})
            except Exception as e:
                if attempt < 2:
                    time.sleep(1)
                    continue
                raise e

    except Exception as e:
        print(f"DEBUG LOG: {e}")
        # Professional fallback to hide errors from the client
        return jsonify({
            "reply": "Greetings. Our automated showroom is currently syncing stock levels. "
                     "Please leave your phone number, and we will contact you immediately."
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

