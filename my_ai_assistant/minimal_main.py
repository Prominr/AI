from flask import Flask, render_template, request, jsonify
import os
import random

app = Flask(__name__)

class SimpleAIAssistant:
    def __init__(self):
        self.responses = {
            "greeting": [
                "Hello! I'm your AI assistant deployed on Railway! 🚆",
                "Hi there! I'm live on the web!",
                "Hey! Your Railway AI is ready to help!"
            ],
            "coding": [
                "I can help with Python, JavaScript, and web development!",
                "Need coding help? I've got you covered!",
                "Let's code something amazing together!"
            ],
            "railway": [
                "This app is deployed on Railway - it's awesome!",
                "Railway makes deployment super easy!",
                "Powered by Railway's cloud platform! 🚆"
            ]
        }
    
    def generate_response(self, user_input):
        user_input = user_input.lower()
        
        if any(word in user_input for word in ['hello', 'hi', 'hey']):
            return random.choice(self.responses["greeting"])
        elif any(word in user_input for word in ['code', 'programming', 'python']):
            return random.choice(self.responses["coding"])
        elif any(word in user_input for word in ['railway', 'deploy', 'hosting']):
            return random.choice(self.responses["railway"])
        else:
            return "I'm here to help! Ask me about coding, Railway, or just say hello!"

ai = SimpleAIAssistant()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    response = ai.generate_response(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)