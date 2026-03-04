import os
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from google import genai

app = Flask(__name__, static_folder='.')
CORS(app)

# Initialize the Gemini Client
# Make sure GEMINI_API_KEY is set in Railway Variables
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")
        
        # The 'Automation' Brand Context
        context = (
            "You are the Mobile City AI, powered by MidTechck Automation. "
            "Your goal is ROI: convert interest into sales. "
            "Prices: S25 Ultra-K19,999, iPhone 16 Pro Max-K30,999. "
            "Be professional, fast, and always mention that stock is limited."
        )

        # 3-Attempt Retry Logic to prevent 'Showroom Errors'
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=f"{context}\nCustomer: {user_msg}"
                )
                return jsonify({"reply": response.text})
            except Exception as e:
                if attempt < 2:
                    time.sleep(1)
                    continue
                raise e

    except Exception as e:
        print(f"Ruthless Error Log: {e}")
        # Professional fallback so the user never sees 'undefined'
        return jsonify({"reply": "Our AI is currently processing a high volume of orders. Please leave your number or try again in a moment."}), 500

if __name__ == "__main__":
    # Railway dynamic port binding
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

