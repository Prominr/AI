import re
import random
import json
import numpy as np
from datetime import datetime
import logging
import os

# Configure logging
logger = logging.getLogger(__name__)

try:
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.naive_bayes import MultinomialNB
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logger.warning("scikit-learn not available, using fallback mode")

try:
    import nltk
    # Download NLTK data
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    logger.warning("NLTK not available, using simple tokenization")

class AdvancedAIAssistant:
    def __init__(self):
        self.name = "CustomAI"
        self.conversation_id = str(random.randint(1000, 9999))
        self.conversation_history = []
        self.knowledge_base = self._initialize_knowledge()
        self.code_templates = self._initialize_code_templates()
        self.ml_model = None
        self.vectorizer = None
        
        # Only train ML model if sklearn is available
        if SKLEARN_AVAILABLE:
            self._train_simple_model()
        else:
            logger.info("Running in fallback mode without ML")
        
    def _initialize_knowledge(self):
        """Load knowledge from JSON file"""
        try:
            with open('knowledge_base.json', 'r', encoding='utf-8') as f:
                knowledge = json.load(f)
                logger.info("Knowledge base loaded successfully")
                return knowledge
        except FileNotFoundError:
            logger.warning("Knowledge base file not found, creating default")
            return self._create_default_knowledge()
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
            return self._create_default_knowledge()
    
    def _create_default_knowledge(self):
        """Create default knowledge base"""
        knowledge = {
            "intents": {
                "greeting": {
                    "patterns": ["hello", "hi", "hey", "good morning", "good afternoon"],
                    "responses": [
                        "Hello! I'm your custom AI assistant deployed on Railway! 🚆 How can I help you today?",
                        "Hi there! I'm running live on the web. What would you like to work on?",
                        "Hey! Your Railway-deployed AI is ready to help! What's on your mind?"
                    ]
                },
                "coding": {
                    "patterns": ["code", "programming", "python", "javascript", "debug", "function"],
                    "responses": [
                        "I can help with coding! What specific language or problem are you working on?",
                        "Sure, I'd be happy to help with programming. What do you need?",
                        "Coding assistance - my specialty! What's the challenge?"
                    ]
                },
                "explanation": {
                    "patterns": ["explain", "what is", "how does", "tell me about", "define"],
                    "responses": [
                        "I can explain that concept. What would you like me to clarify?",
                        "Sure, I'd be happy to explain. What topic are you curious about?",
                        "Explanation mode activated! What concept do you want to understand?"
                    ]
                },
                "help": {
                    "patterns": ["help", "what can you do", "capabilities"],
                    "responses": [
                        "I can help with: coding, explanations, brainstorming, problem-solving, and general conversation!",
                        "My capabilities include: programming assistance, technical explanations, creative projects, and answering questions.",
                        "I'm here to help with coding, learning, creating, and problem-solving. What do you need?"
                    ]
                },
                "railway": {
                    "patterns": ["railway", "deploy", "hosting", "server"],
                    "responses": [
                        "I'm currently deployed on Railway.app - a modern cloud platform that makes deployment easy!",
                        "This AI is running on Railway - no complex setup required!",
                        "Railway makes it simple to deploy apps like me to the cloud instantly!"
                    ]
                }
            },
            "facts": {
                "python": "Python is a high-level programming language known for its simplicity and readability. Perfect for web apps like this one!",
                "javascript": "JavaScript is a programming language primarily used for web development.",
                "ai": "Artificial Intelligence involves creating systems that can perform tasks that typically require human intelligence.",
                "railway": "Railway is a modern app deployment platform that makes it easy to deploy web apps with minimal configuration.",
                "flask": "Flask is a lightweight Python web framework that makes it easy to build web applications and APIs."
            }
        }
        
        # Save to file
        try:
            with open('knowledge_base.json', 'w', encoding='utf-8') as f:
                json.dump(knowledge, f, indent=2)
            logger.info("Default knowledge base created and saved")
        except Exception as e:
            logger.error(f"Error saving knowledge base: {e}")
        
        return knowledge
    
    def _initialize_code_templates(self):
        """Initialize code examples and templates"""
        return {
            "python_hello": {
                "code": '''def hello_world():\n    print("Hello, World!")\n\nhello_world()''',
                "explanation": "Basic Python function that prints 'Hello, World!'"
            },
            "python_calculator": {
                "code": '''def calculator(a, b, operation):\n    if operation == 'add':\n        return a + b\n    elif operation == 'subtract':\n        return a - b\n    elif operation == 'multiply':\n        return a * b\n    elif operation == 'divide':\n        return a / b if b != 0 else "Error: Division by zero"\n    else:\n        return "Invalid operation"\n\n# Example usage:\nresult = calculator(10, 5, 'add')\nprint(result)''',
                "explanation": "Simple calculator function that handles basic arithmetic operations"
            },
            "python_web_app": {
                "code": '''from flask import Flask\n\napp = Flask(__name__)\n\n@app.route('/')\ndef home():\n    return "Hello, Railway!"\n\nif __name__ == '__main__':\n    app.run(host='0.0.0.0', port=5000)''',
                "explanation": "Basic Flask web app - similar to what's running this AI on Railway!"
            }
        }
    
    def _train_simple_model(self):
        """Train a simple ML model for intent classification"""
        if not SKLEARN_AVAILABLE:
            return
            
        try:
            # Training data (patterns and their intents)
            texts = []
            labels = []
            
            for intent_name, intent_data in self.knowledge_base["intents"].items():
                for pattern in intent_data["patterns"]:
                    texts.append(pattern)
                    labels.append(intent_name)
            
            # Add some general patterns
            general_texts = ["okay", "thanks", "thank you", "cool", "nice"]
            texts.extend(general_texts)
            labels.extend(["general"] * len(general_texts))
            
            if texts:
                self.vectorizer = CountVectorizer()
                X = self.vectorizer.fit_transform(texts)
                self.ml_model = MultinomialNB()
                self.ml_model.fit(X, labels)
                logger.info("ML model trained successfully")
        except Exception as e:
            logger.error(f"Error training ML model: {e}")
    
    def analyze_intent(self, user_input):
        """Analyze user intent using ML and pattern matching"""
        user_input = user_input.lower().strip()
        
        # Try ML classification first if available
        if SKLEARN_AVAILABLE and self.ml_model and self.vectorizer:
            try:
                X_test = self.vectorizer.transform([user_input])
                predicted_intent = self.ml_model.predict(X_test)[0]
                confidence = np.max(self.ml_model.predict_proba(X_test))
                
                if confidence > 0.6:  # Confidence threshold
                    intent_data = self.knowledge_base["intents"].get(predicted_intent)
                    if intent_data:
                        logger.info(f"ML classified intent: {predicted_intent} (confidence: {confidence:.2f})")
                        return predicted_intent, intent_data["responses"]
            except Exception as e:
                logger.warning(f"ML classification failed: {e}")
        
        # Fallback to pattern matching
        for intent_name, intent_data in self.knowledge_base["intents"].items():
            for pattern in intent_data["patterns"]:
                if re.search(r'\b' + re.escape(pattern) + r'\b', user_input):
                    logger.info(f"Pattern matched intent: {intent_name}")
                    return intent_name, intent_data["responses"]
        
        # Default response
        logger.info("No intent matched, using general response")
        return "general", [
            "I'm here to help! What would you like to do?",
            "How can I assist you today?",
            "What would you like to work on?"
        ]
    
    def handle_special_requests(self, user_input):
        """Handle specific types of requests"""
        user_input_lower = user_input.lower()
        
        # Code generation requests
        if any(keyword in user_input_lower for keyword in ["code example", "show me code", "python example"]):
            if "hello" in user_input_lower or "basic" in user_input_lower:
                return f"Here's a basic Python example:\n```python\n{self.code_templates['python_hello']['code']}\n```\n{self.code_templates['python_hello']['explanation']}"
            elif "calculator" in user_input_lower:
                return f"Here's a calculator example:\n```python\n{self.code_templates['python_calculator']['code']}\n```\n{self.code_templates['python_calculator']['explanation']}"
            elif "web" in user_input_lower or "flask" in user_input_lower:
                return f"Here's a Flask web app example:\n```python\n{self.code_templates['python_web_app']['code']}\n```\n{self.code_templates['python_web_app']['explanation']}"
        
        # Fact requests
        for topic, fact in self.knowledge_base["facts"].items():
            if topic in user_input_lower:
                return f"**{topic.title()}**: {fact}"
        
        return None
    
    def generate_response(self, user_input):
        """Generate a comprehensive response"""
        logger.info(f"Generating response for: {user_input}")
        
        # Check for special requests first
        special_response = self.handle_special_requests(user_input)
        if special_response:
            response = special_response
            intent = "special"
        else:
            # Analyze intent and get base response
            intent, possible_responses = self.analyze_intent(user_input)
            base_response = random.choice(possible_responses)
            
            # Enhance response based on context
            if intent == "coding":
                response = f"{base_response}\n\nI can provide code examples for: hello world, calculator, web apps, and more. Just ask!"
            elif intent == "explanation":
                response = f"{base_response}\n\nI can explain programming concepts, algorithms, or technical topics."
            elif intent == "railway":
                response = f"{base_response}\n\nThis AI is deployed on Railway - try asking about deployment!"
            else:
                response = base_response
        
        # Store conversation history (limit to last 50 messages)
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "assistant": response,
            "intent": intent,
            "conversation_id": self.conversation_id
        })
        
        # Keep only last 50 messages to prevent memory issues
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]
        
        return response
    
    def get_conversation_history(self):
        """Return conversation history"""
        return self.conversation_history