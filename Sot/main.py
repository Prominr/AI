from flask import Flask, render_template, request, jsonify
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_core import AdvancedAIAssistant

app = Flask(__name__)
ai = AdvancedAIAssistant()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        
        if not user_message.strip():
            return jsonify({'error': 'Empty message'}), 400
            
        response = ai.generate_response(user_message)
        
        return jsonify({
            'response': response,
            'conversation_id': ai.conversation_id
        })
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'AI Assistant'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)