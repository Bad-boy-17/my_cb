from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

# --- Configuration and Initialization ---
app = Flask(__name__)

# Add this line temporarily to check if the key is loaded
print("API Key loaded:", os.getenv("GOOGLE_API_KEY"))

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("API key not found. Please set the GOOGLE_API_KEY environment variable.")
# ... rest of your code ...

# --- Chatbot Logic with Gemini AI ---
def get_ai_response_with_history(conversation_history):
    #try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Gemini expects a specific format for messages
        formatted_messages = []
        for message in conversation_history:
            if message['sender'] == 'user':
                formatted_messages.append({'role': 'user', 'parts': [message['text']]})
            elif message['sender'] == 'bot':
                formatted_messages.append({'role': 'model', 'parts': [message['text']]})
        
        response = model.generate_content(formatted_messages)
        return response.text
    #except Exception as e:
        #print(f"Error calling Gemini API: {e}")
        #return "I'm sorry, I'm having trouble connecting to my brain. Please try again later."

# --- Routes ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=['POST'])
def get_bot_response_api():
    # We now expect a POST request with JSON data
    data = request.get_json()
    conversation_history = data.get('conversation_history', [])
    
    response = get_ai_response_with_history(conversation_history)
    return jsonify({"response": response})

    app.run(debug=True)