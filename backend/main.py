from flask import Flask, request, jsonify
import random
import json
import requests

app = Flask(__name__)

# Gemini API key and endpoint
API_KEY = "AIzaSyDbT0CEFM5JINvyR4hli6fbWNsrh5Ri_n0"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# Function using Gemini API, named as get_mistral_feedback
def get_mistral_feedback(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(f"{API_URL}?key={API_KEY}", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        print(f"Error: Status Code {response.status_code}")
        print(f"Response: {response.text}")
        return "Failed to get feedback from Gemini."

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
    prompt = "i chose above options , what do i prefer , what to improve on, how many points in morality, and in greater good , moderatly good/good /bad  person i am, answer all these with  the thing: your answer in samll words total response a proper format?\n"
    for response in user_responses:
        question = response["question"]
        selected_option = response["selected_option"]
        prompt += f"Question: {question['question']}\n"
        prompt += f"Chosen Option: {question[f'description{selected_option}']}\n\n"
    feedback = get_mistral_feedback(prompt)
    return jsonify({"feedback": feedback})

if __name__ == "__main__":
    app.run(debug=True)
