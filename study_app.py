import streamlit as st
import PyPDF2
import random
import time
from collections import defaultdict

# Initialize session state if not already
if 'mistakes' not in st.session_state:
    st.session_state.mistakes = defaultdict(int)
if 'hints' not in st.session_state:
    st.session_state.hints = {}
if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = []

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to generate questions from text (basic placeholder)
def generate_questions(text):
    questions = text.split("?\n")  # Rough split by question mark
    questions = [q.strip() + '?' for q in questions if len(q.strip()) > 10]
    return questions[:20]  # Limit to 20 for now

# Function to provide hints
def get_hint(question):
    return st.session_state.hints.get(question, "Think about similar problems you've solved before.")

# Streamlit UI
st.title("Smart Exam Practice with Flashcards")

uploaded_file = st.file_uploader("Upload your exam PDF", type=["pdf"])

if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file)
    questions = generate_questions(text)
    
    st.write("Select Questions to Study:")
    selected_questions = st.multiselect("Choose questions:", questions)
    st.session_state.selected_questions = selected_questions
    
    st.write("Study Mode")
    for i, question in enumerate(st.session_state.selected_questions):
        with st.expander(f"Question {i+1}"):
            st.write(question)
            
            # Timer setup
            time_limit = st.slider("Set time (seconds)", 10, 300, 60, key=f"timer_{i}")
            start_time = st.button("Start Timer", key=f"start_{i}")
            if start_time:
                with st.empty():
                    for sec in range(time_limit, 0, -1):
                        st.write(f"Time left: {sec}s")
                        time.sleep(1)
                        st.empty()
                st.write("Time's up!")
            
            user_answer = st.text_input("Your Answer", key=f"answer_{i}")
            submit = st.button("Submit", key=f"submit_{i}")
            
            if submit:
                correct = random.choice([True, False])  # Placeholder for actual answer checking
                if correct:
                    st.success("Correct!")
                else:
                    st.error("Incorrect!")
                    st.session_state.mistakes[question] += 1
                    if question not in st.session_state.hints:
                        st.session_state.hints[question] = "Review similar solved examples."
                    st.write("Hint:", get_hint(question))
    
    # Flashcard Mode
    st.write("### Flashcards Mode")
    for i, question in enumerate(st.session_state.selected_questions):
        with st.expander(f"Flashcard {i+1}"):
            st.write(question)
            options = ["Option A", "Option B", "Option C", "Option D"]
            correct_answer = random.choice(options)  # Placeholder for actual correct answer
            user_choice = st.radio("Choose an option:", options, key=f"flashcard_{i}")
            
            if st.button("Check Answer", key=f"check_{i}"):
                if user_choice == correct_answer:
                    st.success("Correct!")
                else:
                    st.error(f"Incorrect! The correct answer was {correct_answer}")

st.write("Mistakes Tracking:")
for q, count in st.session_state.mistakes.items():
    st.write(f"{q} - Mistakes: {count}")


#pip install streamlit

#pip install PyPDF2

