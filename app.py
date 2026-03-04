import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__, static_folder='.')
CORS(app)

# Force the API key and configure
KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=KEY)

# CRITICAL FIX: Changed model to 'gemini-1.5-flash-latest'
model = genai.GenerativeModel('gemini-1.5-flash-latest')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")

        if not KEY:
            return jsonify({"reply": "ERROR: API Key missing in Railway."})

        # Test call with the new model name
        response = model.generate_content(f"You are Mobile City AI. S25 Ultra is K19,999. User: {user_msg}")
        
        return jsonify({"reply": response.text})

    except Exception as e:
        # If this still fails, it will tell us why
        return jsonify({"reply": f"CONNECTION ERROR: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

