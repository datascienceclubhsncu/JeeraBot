from flask import Flask, request, jsonify, render_template
from llamaparse.parse import query_engine
import secrets

app = Flask(__name__, static_folder='templates/assets', static_url_path='/assets')

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
        conversations[user['chat_id']].append({'role': 'assistant', 'content': response})
        return response
    except Exception as e:
        print("Error:", e)
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
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
