import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from google import genai  # Updated import

app = Flask(__name__, static_folder='.')
CORS(app)

# Updated Client Initialization
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message")
        
        # Updated Generation Logic
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"You are the Mobile City AI. Prices: S25 Ultra-K19,999. User: {user_msg}"
        )
        
        return jsonify({"reply": response.text}) # Ensure this says 'reply'
    except Exception as e:
        print(f"Error: {e}") # This will show up in Railway logs
        return jsonify({"error": str(e)}), 500

