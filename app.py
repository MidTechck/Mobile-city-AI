import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__, static_folder='.')
CORS(app)

# Explicitly configure the API
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Using the most universally compatible model name
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")

        # A "Ruthless" hard-coded check for the demo
        # This ensures that even if the API blinks, you can show the prices.
        if "price" in user_msg.lower() or "how much" in user_msg.lower():
            if "s25" in user_msg.lower():
                return jsonify({"reply": "The Samsung S25 Ultra is K19,999. Would you like to reserve one?"})

        # The Real AI Call
        # We wrap it in a very simple prompt to avoid versioning issues
        response = model.generate_content(user_msg)
        return jsonify({"reply": response.text})

    except Exception as e:
        # If it fails again, we need to see if it's still a 404
        return jsonify({"reply": f"DEBUG: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

