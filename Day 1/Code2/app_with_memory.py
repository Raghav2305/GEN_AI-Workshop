from flask import Flask, request, jsonify, render_template
from google import genai
import os

app = Flask(__name__)

# --- Global Client and Chat Objects ---
# These will persist for the application's lifetime.
client = None
chat = None

def initialize_globals(api_key):
    """Initializes the global client and chat session."""
    global client, chat
    try:
        # Initialize the client if it hasn't been already
        if client is None:
            client = genai.Client(api_key=api_key)
        # Create a new chat session for each user visit to the homepage
        chat = client.chats.create(model='gemini-2.5-flash')
        return True
    except Exception as e:
        print(f"Error initializing globals: {e}")
        return False

# --- Flask Routes ---
@app.route('/')
def index():
    api_key = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
    if not api_key:
        return "Error: GEMINI_API_KEY is not set. Please configure the environment variable.", 500
    
    if not initialize_globals(api_key):
        return "Error: Could not initialize chat with the Gemini API.", 500
        
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def handle_chat():
    global chat
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    if not chat:
        return jsonify({'error': 'Chat session not initialized. Please reload the page.'}), 500

    try:
        response = chat.send_message(user_message)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': f"An API error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
