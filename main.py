from flask import Flask, request, jsonify, render_template
from llamaparse.parse import query_engine
import secrets
import logging


#initialize flask
app = Flask(__name__, static_folder='static', static_url_path='/')

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

conversations = {}

def chat(message, user):
    bot_name = "Jeera Bot"
    college_data = []

    chats = [{"role": "user", "content": f"Hello my name is {user['name']} and Your name is {bot_name} and you will assist me with this name"}] + college_data

    if user['chat_id'] not in conversations:
        conversations[user['chat_id']] = chats

    try:
        response = query_engine.query(message)
        conversations[user['chat_id']].append({'role': 'user', 'content': message})
        conversations[user['chat_id']].append({'role': 'assistant', 'content': response.response})
        
        # Log user message and bot response
        logging.info(f"User {user['chat_id']} ({user['name']}): {message}")
        logging.info(f"Bot response: {response.response}")

        return response.response
    except Exception as e:
        logging.error(f"Error processing request for user {user['chat_id']}: {e}")
        return "Error in processing request"

@app.route('/')
def chatbot():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    data = request.get_json()
    message = data.get('message')
    user = {
        'name': data.get('user', 'User'),
        'chat_id': secrets.token_hex(16)
    }

    response = chat(message, user)
    logging.info(f"Request from user {user['chat_id']}: {message}")
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')



