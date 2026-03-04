import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from google import genai

app = Flask(__name__, static_folder='.')
CORS(app)

# Updated Client Initialization
client = genai.Client(api_key=os.environ.get("AIzaSyAS_wZHAiBYT0FJ_zSqCpZcltBNj3HOmj4"))

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")
        
        # Professional Enterprise Prompt
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"You are the Mobile City AI. Brief & Professional. S25 Ultra is K19,999. iPhone 16 Pro Max is K30,999. Customer: {user_msg}"
        )
        
        # Sending 'reply' to match the index.html
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "I'm having trouble connecting to the showroom. Please try again."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

