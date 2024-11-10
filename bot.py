import os
import asyncio
from flask import Flask, request, jsonify
from rasa.core.agent import Agent
from response_utils import goal_synonym_mapping

app = Flask(__name__)

# Dynamically load the latest model in the 'models' directory
model_directory = "models"
latest_model = max(
    [f for f in os.listdir(model_directory) if f.endswith('.tar.gz')],
    key=lambda x: os.path.getctime(os.path.join(model_directory, x))
)
agent = Agent.load(os.path.join(model_directory, latest_model))

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    # Run the asynchronous handle_text coroutine in a synchronousasynchronous Flask route
    response = asyncio.run(agent.handle_text(user_input))

    # Check if response is None or empty
    if response and len(response) > 0 and response[0].get('text') is not None:
        # return jsonify({"response": response[0].get('text')})
                # Apply synonym mapping on detected goal in response
        modified_text = goal_synonym_mapping(response[0].get('text'))
        return jsonify({"response": modified_text})
    else:
        return jsonify({"response": "I'm not sure how to respond to that."})

if __name__ == '__main__':
    app.run(debug=True)
