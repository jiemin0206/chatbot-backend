import json
import os
from http import HTTPStatus

from google.generativeai import configure as genai_configure, GenerativeModel
from langchain_google_genai import ChatGoogleGenerativeAI

# Configure Generative AI
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai_configure(api_key=GOOGLE_API_KEY)
model = GenerativeModel(model_name="gemini-pro")

def chatbot_response(request):
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return ('', HTTPStatus.NO_CONTENT, headers)  # Respond to preflight request with empty body

    data = request.get_json()
    user_input = data.get('userInput', '')
    response = model.generate_content([user_input])
    return json.dumps({'reply': response.text}), HTTPStatus.OK, {'Content-Type': 'application/json'}

# Entry point for the Vercel serverless function
def handler(request):
    if request.method == 'POST':
        return chatbot_response(request)
    else:
        return '', HTTPStatus.METHOD_NOT_ALLOWED

# For local testing
if __name__ == '__main__':
    from flask import Flask, request
    app = Flask(__name__)

    @app.route('/chatbot', methods=['POST', 'OPTIONS'])
    def local_chatbot():
        return handler(request)

    app.run(debug=True)
