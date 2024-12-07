import openai
import os
from flask import Blueprint, request, jsonify

# Define a blueprint for the chatbot
chatbot_bp = Blueprint('chatbot', __name__)

# Securely set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """
    Handles chatbot interactions.
    """
    user_message = request.json.get('message', '')  # Extract user message from the POST request

    try:
        # Call OpenAI's API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful chatbot."},
                {"role": "user", "content": user_message}
            ]
        )

        # Extract the reply from OpenAI API
        reply = response['choices'][0]['message']['content']
        return jsonify({'reply': reply})  # Return the response to the user

    except Exception as e:
        # Handle errors and return a default response
        print(f"Error: {e}")
        return jsonify({'reply': "Sorry, there was an error processing your request."})
