import streamlit as st
import pandas as pd

# Sample question data (you can replace this with CSV loading)
questions = [
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "answer": "4"
    },
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Madrid", "Paris"],
        "answer": "Paris"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": "Mars"
    }
]

st.title("📝 Mock Test")

# Store responses in session state
if "responses" not in st.session_state:
    st.session_state.responses = [""] * len(questions)
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Display questions
for i, q in enumerate(questions):
    st.markdown(f"**Q{i+1}: {q['question']}**")
    st.session_state.responses[i] = st.radio(
        f"Choose an answer for Q{i+1}", 
        q["options"], 
        index=q["options"].index(st.session_state.responses[i]) if st.session_state.responses[i] else 0,
        key=f"q{i}"
    )
    st.write("---")

# Submit button
if st.button("Submit"):
    st.session_state.submitted = True

# Score and feedback
if st.session_state.submitted:
    score = 0
    for i, q in enumerate(questions):
        if st.session_state.responses[i] == q["answer"]:
            score += 1
    st.success(f"You scored {score} out of {len(questions)}")

