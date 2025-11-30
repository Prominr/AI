from flask import Flask, render_template, request, jsonify
from ai_core import AdvancedAIAssistant
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
ai = AdvancedAIAssistant()

# Railway will provide the PORT environment variable
port = int(os.environ.get("PORT", 5000))

@app.route('/')
def home():
    logger.info("Home page accessed")
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        logger.info(f"Received message: {user_message}")
        
        if not user_message.strip():
            return jsonify({'error': 'Empty message'}), 400
            
        response = ai.generate_response(user_message)
        
        return jsonify({
            'response': response,
            'conversation_id': ai.conversation_id
        })
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health():
    """Health check endpoint for Railway"""
    return jsonify({'status': 'healthy', 'service': 'AI Assistant'})

@app.route('/history')
def history():
    return jsonify(ai.get_conversation_history())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)