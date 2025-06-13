from flask import Flask, request, jsonify
from flask_cors import CORS
from chat_logic import get_local_response

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    if not user_message.strip():
        return jsonify({"reply": "❌ Please enter a message."})
    
    reply = get_local_response(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
