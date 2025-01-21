from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Mock OpenAI API"}), 200

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    # Mock response for the ChatCompletion endpoint
    return jsonify({
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1691228532,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "This is a mock response from the ChatCompletion endpoint."
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 5,
            "completion_tokens": 7,
            "total_tokens": 12
        }
    })

if __name__ == '__main__':
    app.run(port=5001)
