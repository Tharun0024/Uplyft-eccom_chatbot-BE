from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from chat_logic import get_gpt_response


app = Flask(__name__)
CORS(app)

import os
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({'reply': "❌ Empty message received."})

    # GPT generates SQL or direct reply
    response = get_gpt_response(user_message)
    return jsonify({'reply': response})

if __name__ == '__main__':
    app.run(debug=True)
