import streamlit as st
import requests
import os

# Backend URL
BACKEND_URL = "http://127.0.0.1:5000"

# Initialize session state
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "responses" not in st.session_state:
    st.session_state.responses = []
if "feedback" not in st.session_state:
    st.session_state.feedback = None

# Fetch questions from backend
def fetch_questions():
    response = requests.get(f"{BACKEND_URL}/get_questions")
    if response.status_code == 200:
        st.session_state.questions = response.json()
    else:
        st.error("Failed to fetch questions.")

# Submit response to backend
def submit_response(question_id, selected_option):
    question_data = st.session_state.questions[st.session_state.current_question]
    response_data = {
        "question": question_data,
        "selected_option": selected_option
    }
    st.session_state.responses.append(response_data)
    st.session_state.current_question += 1

# Function to handle different image formats
def get_image_path(image_filename):
    # Check if the image path exists as is
    base_path = "./static/images/"
    
    # If the filename already has an extension, use it directly
    if image_filename.lower().endswith((".png", ".jpg", ".jpeg")):
        full_path = f"{base_path}{image_filename}"
        if os.path.exists(full_path):
            return full_path
        else:
            st.warning(f"File not found: {full_path}")
            return full_path  # Return anyway to let Streamlit handle the error
    
    # Try different extensions
    for ext in [".jpg", ".png", ".jpeg"]:  # Prioritize .jpg first
        full_path = f"{base_path}{image_filename}{ext}"
        if os.path.exists(full_path):
            return full_path
    
    # If no file is found, return a default path and let Streamlit show an error
    st.warning(f"Image not found for {image_filename} in .jpg, .png, or .jpeg")
    return f"{base_path}{image_filename}.jpg"

# Display question and options
def display_question():
    question_data = st.session_state.questions[st.session_state.current_question]
    st.write(f"**Question {st.session_state.current_question + 1}:** {question_data['question']}")

    col1, col2 = st.columns(2)
    with col1:
        image_name = question_data['image1'].split('.')[0]  # Strip any extension
        image_path = get_image_path(image_name)  # Use the helper function
        st.image(image_path, use_container_width=True)
        if st.button(question_data["description1"], key="option1"):
            submit_response(question_data["id"], 1)
            st.rerun()
    with col2:
        image_name = question_data['image2'].split('.')[0]  # Strip any extension
        image_path = get_image_path(image_name)  # Use the helper function
        st.image(image_path, use_container_width=True)
        if st.button(question_data["description2"], key="option2"):
            submit_response(question_data["id"], 2)
            st.rerun()

# Submit all responses to backend for feedback
def submit_all_responses():
    response = requests.post(f"{BACKEND_URL}/submit_all_responses", json=st.session_state.responses)
    if response.status_code == 200:
        st.session_state.feedback = response.json()["feedback"]
    else:
        st.error("Failed to get feedback.")

# Main app logic
def main():
    st.title("AI-Powered Ethical Decision Making Simulations")

    if not st.session_state.questions:
        fetch_questions()

    if st.session_state.current_question < len(st.session_state.questions):
        display_question()
    else:
        if st.button("Submit"):
            submit_all_responses()
            st.rerun()

    if st.session_state.feedback:
        st.write("**Feedback:**")
        st.write(st.session_state.feedback)
        if st.button("Retake Test"):
            st.session_state.current_question = 0
            st.session_state.responses = []
            st.session_state.feedback = None
            st.rerun()
        if st.button("New Test"):
            st.session_state.questions = []
            st.session_state.current_question = 0
            st.session_state.responses = []
            st.session_state.feedback = None
            fetch_questions()
            st.rerun()

if __name__ == "__main__":
    main()