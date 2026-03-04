import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__, static_folder='.')
CORS(app)

# Bare Metal Config
KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")

        # Check if Key exists in environment
        if not KEY:
            return jsonify({"reply": "ERROR: Railway Variable 'GEMINI_API_KEY' is missing."})

        # Bare Metal Call
        response = model.generate_content(f"Context: Mobile City. S25 Ultra is K19,999. User: {user_msg}")
        
        return jsonify({"reply": response.text})

    except Exception as e:
        # This will print the EXACT error message to your chat bubble
        return jsonify({"reply": f"SYSTEM ERROR: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

