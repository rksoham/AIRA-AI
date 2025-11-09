from flask import Flask, render_template, request, jsonify
import json
import re
import random
import difflib
from datetime import datetime
import os


app = Flask(__name__)

# File to store learned responses
LEARNED_FILE = 'learned.json'

class HybridChatbot:
    def __init__(self):
        self.intents = self.load_intents()
        self.learned_responses = self.load_learned_responses()
        
    def load_intents(self):
        """Load intents from JSON file"""
        try:
            with open('intents.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            # Default intents if file doesn't exist
            return {
                "intents": [
                    {
                        "tag": "greeting",
                        "patterns": [
                            "hello", "hi", "hey", "good morning", "good afternoon",
                            "good evening", "howdy", "what's up"
                        ],
                        "responses": [
                            "Hello! Welcome to AIRA College Assistant. How can I help you today?",
                            "Hi there! I'm AIRA, your college information assistant.",
                            "Greetings! How may I assist you with college-related queries?"
                        ]
                    },
                    {
                        "tag": "farewell",
                        "patterns": [
                            "bye", "goodbye", "see you", "see ya", "take care",
                            "quit", "exit", "have a good day"
                        ],
                        "responses": [
                            "Goodbye! Feel free to ask if you have more questions.",
                            "See you later! Don't hesitate to return if you need assistance.",
                            "Have a great day! Remember, I'm here to help with college information."
                        ]
                    },
                    {
                        "tag": "name",
                        "patterns": [
                            "what is your name", "who are you", "what should i call you",
                            "are you a bot", "are you human"
                        ],
                        "responses": [
                            "I'm AIRA - Artificial Intelligence Response Assistant, your college chatbot!",
                            "You can call me AIRA. I'm here to help with college information and FAQs.",
                            "I'm AIRA, your virtual college assistant. How can I help you today?"
                        ]
                    },
                    {
                        "tag": "help",
                        "patterns": [
                            "help", "what can you do", "how can you help", "what do you do",
                            "what are your functions", "can you assist me"
                        ],
                        "responses": [
                            "I can help you with college information like admissions, courses, fees, contact details, and general FAQs.",
                            "I'm here to assist with college-related queries including admission procedures, course details, fee structure, and campus information.",
                            "As your college assistant, I can provide information about admissions, courses, fees, campus facilities, and more!"
                        ]
                    },
                    {
                        "tag": "thanks",
                        "patterns": [
                            "thank you", "thanks", "thank you so much", "appreciate it",
                            "thanks a lot", "you're helpful"
                        ],
                        "responses": [
                            "You're welcome! Happy to help.",
                            "Glad I could assist you!",
                            "You're welcome! Let me know if you need anything else."
                        ]
                    },
                    {
                        "tag": "admissions",
            "patterns": [
                "admission", "admission requirements", "how to apply",
                "admission process", "eligibility", "admission criteria",
                "how to get admission", "admission procedure", "apply for college",
                "admission form", "application process"
            ],
            "responses": [
                "Admissions to the Bachelor of Engineering programs at Acharya Institute of Technology are conducted through KCET, COMEDK, or Management Quota. Candidates must have passed 10 & 12 with Physics and Mathematics as compulsory subjects and obtained a minimum of 65 percent aggregate marks."
    
            ]
                    },
                    {
            "tag": "contact",
            "patterns": [
                "contact", "contact number", "phone number", "email",
                "how to contact", "college address", "where are you located",
                "phone", "mobile number", "office number", "location"
            ],
            "responses": [
                "You can reach Acharya Institute of Technology at Phone plus91 74066 44449 or plus91 97317 97677 Email admissions@acharya.ac.in Address Acharya Dr S Radhakrishnan Road Acharya PO Soladevanahalli Bengaluru 560107 Karnataka India.",
                "Contact details are as follows Phone plus91 74066 44449 or plus91 97317 97677 Email admissions@acharya.ac.in Address Acharya Dr S Radhakrishnan Road Soladevanahalli Bengaluru 560107 Karnataka India.",
                "For any enquiries contact Acharya Institute of Technology at plus91 74066 44449 or plus91 97317 97677 or email admissions@acharya.ac.in The campus is located at Acharya Dr S Radhakrishnan Road Soladevanahalli Bengaluru 560107 Karnataka."
            ]
        },
                    {
                        "tag": "courses",
                        "patterns": [
                            "courses", "programs", "what courses do you offer",
                            "available courses", "degree programs", "study programs"
                        ],
                        "responses": [
                            "Our college offers BE (CSE, ISE, ME, EE, CE, BT), BBA with specializations in Marketing, Finance, Human Resource Management, and Business Analytics, BCA with specializations in Cloud Computing, Data Science, Artificial Intelligence, and Web Development, along with MBA and M.Tech programs across various specializations."
                        ]
                    }
                ]
            }
    
    def load_learned_responses(self):
        """Load learned responses from file"""
        try:
            if os.path.exists(LEARNED_FILE):
                with open(LEARNED_FILE, 'r', encoding='utf-8') as file:
                    return json.load(file)
        except Exception as e:
            print(f"Error loading learned responses: {e}")
        return {}
    
    def save_learned_responses(self):
        """Save learned responses to file"""
        try:
            with open(LEARNED_FILE, 'w', encoding='utf-8') as file:
                json.dump(self.learned_responses, file, indent=2)
        except Exception as e:
            print(f"Error saving learned responses: {e}")
    
    def preprocess_text(self, text):
        """Clean and preprocess input text"""
        text = text.lower().strip()
        # Remove punctuation and extra spaces
        text = re.sub(r'[^\w\s]', '', text)
        text = ' '.join(text.split())
        return text
    
    def calculate_similarity(self, text1, text2):
        """Calculate similarity between two texts using sequence matching"""
        return difflib.SequenceMatcher(None, text1, text2).ratio()
    
    def find_best_match(self, user_input):
        """Find the best matching intent using fuzzy matching"""
        user_input = self.preprocess_text(user_input)
        best_match = None
        highest_similarity = 0
        
        for intent in self.intents["intents"]:
            for pattern in intent["patterns"]:
                pattern_clean = self.preprocess_text(pattern)
                similarity = self.calculate_similarity(user_input, pattern_clean)
                
                if similarity > highest_similarity and similarity > 0.5:  # Threshold
                    highest_similarity = similarity
                    best_match = intent
        
        return best_match, highest_similarity
    
    def get_response(self, user_input):
        """Generate response for user input"""
        # Check learned responses first
        user_input_clean = self.preprocess_text(user_input)
        if user_input_clean in self.learned_responses:
            return self.learned_responses[user_input_clean]
        
        # Find best matching intent
        best_match, similarity = self.find_best_match(user_input)
        
        if best_match:
            response = random.choice(best_match["responses"])
            
            # Learn from this interaction if similarity was low but still matched
            if similarity < 0.8:
                self.learned_responses[user_input_clean] = response
                self.save_learned_responses()
            
            return response
        
        # Fallback response
        fallback_responses = [
            "I'm still learning about college information! Could you rephrase your question?",
            "I don't have information about that yet. Try asking about admissions, courses, or fees.",
            "I'm specialized in college FAQs. Could you ask about admissions, courses, or campus facilities?",
            "I'm here to help with college-related queries. Try asking about our programs or admission process."
        ]
        
        # Store the unknown question for learning
        self.learned_responses[user_input_clean] = random.choice(fallback_responses)
        self.save_learned_responses()
        
        return random.choice(fallback_responses)
    
    def learn_new_response(self, question, answer):
        """Manually learn a new response"""
        question_clean = self.preprocess_text(question)
        self.learned_responses[question_clean] = answer
        self.save_learned_responses()
        return True

# Initialize chatbot
chatbot = HybridChatbot()

@app.route('/')
def home():
    """Serve the main chat interface"""
    
    # In real login-based system, replace this with actual user image from session or DB
    user_image_url = "/static/assets/default-user.webp"  
    
    return render_template('index.html', user_image_url=user_image_url)


@app.route('/getResponse', methods=['POST'])
def get_response():
    """API endpoint to get chatbot response"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'reply': 'Please enter a message.'})
        
        # Get response from chatbot
        bot_reply = chatbot.get_response(user_message)
        
        return jsonify({'reply': bot_reply})
        
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'reply': 'I encountered an error. Please try again.'})

@app.route('/learn', methods=['POST'])
def learn_response():
    """Endpoint to manually teach the chatbot"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        answer = data.get('answer', '').strip()
        
        if question and answer:
            success = chatbot.learn_new_response(question, answer)
            if success:
                return jsonify({'status': 'success', 'message': 'Response learned successfully!'})
        
        return jsonify({'status': 'error', 'message': 'Invalid input'})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'AIRA Chatbot'})

if __name__ == '__main__':
    print("Starting AIRA Hybrid Chatbot...")
    print("Access the chatbot at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)