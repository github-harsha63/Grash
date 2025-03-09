from flask import Flask, request, jsonify
import random
import json
from mistral import get_mistral_feedback

app = Flask(__name__)

# Load questions from JSON file
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Endpoint to get 10 random questions
@app.route("/get_questions", methods=["GET"])
def get_questions():
    random_questions = random.sample(questions, 10)
    return jsonify(random_questions)

# Endpoint to submit all responses and get feedback
@app.route("/submit_all_responses", methods=["POST"])
def submit_all_responses():
    user_responses = request.json
    prompt = "What do you suggest for the person who chose the following options?\n"
    for response in user_responses:
        question = response["question"]
        selected_option = response["selected_option"]
        prompt += f"Question: {question['question']}\n"
        prompt += f"Chosen Option: {question[f'description{selected_option}']}\n\n"
    feedback = get_mistral_feedback(prompt)
    return jsonify({"feedback": feedback})

if __name__ == "__main__":
    app.run(debug=True)