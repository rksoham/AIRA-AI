from flask import Flask, request, jsonify, render_template
import requests
import json
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rasa server configuration
RASA_SERVER_URL = os.getenv('RASA_SERVER_URL', 'http://localhost:5005')

# Load intents for fallback
INTENTS_FILE = 'intents.json'
intents_data = {}

try:
    with open(INTENTS_FILE, 'r', encoding='utf-8') as f:
        intents_data = json.load(f)
    logger.info(f"Loaded intents from {INTENTS_FILE}")
except FileNotFoundError:
    logger.warning(f"Intents file {INTENTS_FILE} not found. Fallback responses may be limited.")


@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')


@app.route('/getResponse', methods=['POST'])
def get_response():
    """Main endpoint for chat messages - proxy to Rasa"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        sender_id = data.get('sender_id', 'default_user')
        
        if not user_message:
            return jsonify({'reply': 'Please say something!'})
        
        logger.info(f"User ({sender_id}): {user_message}")
        
        # Send to Rasa
        rasa_response = send_to_rasa(user_message, sender_id)
        
        if rasa_response:
            logger.info(f"Bot: {rasa_response}")
            return jsonify({'reply': rasa_response}), 200
        else:
            # Fallback if Rasa doesn't respond
            fallback = get_fallback_response(user_message)
            logger.info(f"Bot (fallback): {fallback}")
            return jsonify({'reply': fallback}), 200
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'reply': 'Sorry, something went wrong. Please try again.'}), 500


def send_to_rasa(message, sender_id='default_user'):
    """Send message to Rasa server and get response"""
    try:
        rasa_url = f"{RASA_SERVER_URL}/webhooks/rest/webhook"
        payload = {
            "sender": sender_id,
            "message": message
        }
        
        logger.info(f"Sending to Rasa: {payload}")
        response = requests.post(rasa_url, json=payload, timeout=5)
        response.raise_for_status()
        
        rasa_response = response.json()
        logger.info(f"Rasa response: {rasa_response}")
        
        if isinstance(rasa_response, list) and len(rasa_response) > 0:
            # Extract text from Rasa response
            if 'text' in rasa_response[0]:
                return rasa_response[0]['text']
            elif 'custom' in rasa_response[0]:
                return rasa_response[0]['custom'].get('text', 'No response')
        
        return None
        
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to Rasa server. Make sure it's running on " + RASA_SERVER_URL)
        return None
    except Exception as e:
        logger.error(f"Error communicating with Rasa: {str(e)}")
        return None


def get_fallback_response(user_message):
    """Provide fallback response using intents.json if Rasa is unavailable"""
    if not intents_data:
        return "I'm unable to connect to the AI service. Please try again later."
    
    # Simple keyword matching fallback
    message_lower = user_message.lower()
    intents_list = intents_data.get('intents', [])
    
    for intent in intents_list:
        keywords = intent.get('keywords', [])
        if any(keyword in message_lower for keyword in keywords):
            responses = intent.get('responses', ['I am not sure how to respond to that.'])
            return responses[0] if responses else 'I am not sure how to respond to that.'
    
    return "I'm not sure I understand. Could you ask about admissions, courses, fees, contact info, placements, facilities, or campus life?"


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        rasa_health = requests.get(f"{RASA_SERVER_URL}/status", timeout=2)
        rasa_status = rasa_health.status_code == 200
    except:
        rasa_status = False
    
    return jsonify({
        'status': 'healthy',
        'rasa_connected': rasa_status
    }), 200



if _name_ == "_main_":
    import os
    port = int(os.environ.get("PORT", 5000))

    logger.info("Starting AIRA College Chatbot (Rasa-powered)")
    logger.info(f"Rasa server URL: {RASA_SERVER_URL}")

    app.run(host="0.0.0.0", port=port)