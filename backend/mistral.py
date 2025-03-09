import os
import requests

# Gemini API key (set as environment variable or hardcoded)
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "AIzaSyDbT0CEFM5JINvyR4hli6fbWNsrh5Ri_n0")
MISTRAL_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# Function to get feedback from Gemini (named as Mistral)
def get_mistral_feedback(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    # Use query parameter for Gemini API key, not Authorization header
    response = requests.post(f"{MISTRAL_API_URL}?key={MISTRAL_API_KEY}", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        print(f"Error: Status Code {response.status_code}")
        print(f"Response: {response.text}")
        return "Failed to get feedback from Gemini."
