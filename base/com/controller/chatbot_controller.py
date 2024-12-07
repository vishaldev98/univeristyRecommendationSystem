import openai
import os
from flask import Blueprint, request, jsonify

# Define a blueprint for the chatbot
chatbot_bp = Blueprint('chatbot', __name__)

# Securely set your OpenAI API key
openai.api_key = os.getenv('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')

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
