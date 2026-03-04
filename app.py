import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__, static_folder='.')
CORS(app)

# Security: Load key from Railway Environment Variables
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message")
        
        # Professional Prompt Logic
        context = "You are the Mobile City AI. Professional, helpful. S25 Ultra: K19,999. iPhone 16: K30,999. Delivery is free in Lusaka."
        full_prompt = f"{context}\nCustomer: {user_msg}"
        
        response = model.generate_content(full_prompt)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # The 'Railway Bridge' - Dynamic Port Binding
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

