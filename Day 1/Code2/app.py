from flask import Flask, request, jsonify, render_template
from google import genai
import os

app = Flask(__name__)

# --- Gemini API Call Function ---
def make_gemini_api_call(api_key, prompt_content):
    """
    Makes a simple API call to the Gemini model using the Client API.
    """
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_content
        )
        return response.text
    except Exception as e:
        return f"An API error occurred: {e}"

# --- Flask Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    api_key = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
    if not api_key:
        return jsonify({'error': 'GEMINI_API_KEY environment variable not set'}), 500

    bot_response = make_gemini_api_call(api_key, user_message)
    
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True, port = 5001)

