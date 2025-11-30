from flask import Flask, render_template, request, jsonify
import os
import random

app = Flask(__name__)

class SimpleAI:
    def __init__(self):
        self.responses = [
            "Hello! I'm your AI assistant running on Railway! 🚆",
            "Hi there! I'm successfully deployed!",
            "Hey! Your AI is live and working!",
            "Hello! Railway deployment successful! 🎉",
            "Hi! I'm your custom AI assistant!"
        ]
    
    def get_response(self):
        return random.choice(self.responses)

ai = SimpleAI()

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Assistant - Railway</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
            }
            .container {
                background: white;
                color: black;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }
            .chat-box {
                border: 1px solid #ddd;
                padding: 20px;
                height: 300px;
                overflow-y: auto;
                margin: 20px 0;
                border-radius: 10px;
            }
            input, button {
                padding: 10px;
                margin: 5px;
                border-radius: 5px;
            }
            input {
                width: 70%;
                border: 1px solid #ddd;
            }
            button {
                background: #007bff;
                color: white;
                border: none;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 My AI Assistant</h1>
            <p><strong>Status:</strong> 🟢 Successfully deployed on Railway</p>
            
            <div class="chat-box" id="chat">
                <div><strong>AI:</strong> Hello! I'm your AI assistant running live on Railway! 🚆</div>
            </div>
            
            <div>
                <input type="text" id="message" placeholder="Type your message...">
                <button onclick="sendMessage()">Send</button>
            </div>
            
            <div style="margin-top: 20px;">
                <button onclick="askQuestion('Hello')">Say Hello</button>
                <button onclick="askQuestion('How are you?')">How are you?</button>
                <button onclick="askQuestion('Tell me about Railway')">About Railway</button>
            </div>
        </div>

        <script>
            function askQuestion(question) {
                document.getElementById('message').value = question;
                sendMessage();
            }

            function sendMessage() {
                const message = document.getElementById('message').value;
                if (!message) return;
                
                // Add user message
                const chat = document.getElementById('chat');
                chat.innerHTML += `<div><strong>You:</strong> ${message}</div>`;
                
                // Clear input
                document.getElementById('message').value = '';
                
                // Show loading
                chat.innerHTML += `<div><strong>AI:</strong> Thinking...</div>`;
                chat.scrollTop = chat.scrollHeight;
                
                // Send to backend
                fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({message: message})
                })
                .then(response => response.json())
                .then(data => {
                    // Remove loading message and add AI response
                    chat.innerHTML = chat.innerHTML.replace('Thinking...', '');
                    chat.innerHTML += `<div><strong>AI:</strong> ${data.response}</div>`;
                    chat.scrollTop = chat.scrollHeight;
                })
                .catch(error => {
                    chat.innerHTML = chat.innerHTML.replace('Thinking...', '');
                    chat.innerHTML += `<div><strong>AI:</strong> Sorry, there was an error!</div>`;
                    chat.scrollTop = chat.scrollHeight;
                });
            }
        </script>
    </body>
    </html>
    '''

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    response = ai.get_response()
    return jsonify({'response': response})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'AI Assistant is running!'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)