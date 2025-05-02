import streamlit as st
import json

st.set_page_config(page_title="Mock Test Software", layout="centered")

if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = []
if "submitted" not in st.session_state:
    st.session_state.submitted = False

def load_questions(file):
    try:
        questions = json.load(file)
        if not isinstance(questions, list):
            st.error("Uploaded JSON must be a list of questions.")
            return []
        for q in questions:
            if not all(k in q for k in ("question", "options", "answer")):
                st.error("Each question must have 'question', 'options', and 'answer' keys.")
                return []
        return questions
    except Exception as e:
        st.error(f"Error loading JSON: {e}")
        return []

def show_admin():
    st.header("Admin - Upload Questions JSON")
    uploaded_file = st.file_uploader("Upload questions JSON file", type=["json"])
    if uploaded_file is not None:
        questions = load_questions(uploaded_file)
        if questions:
            st.session_state.questions = questions
            st.session_state.submitted = False
            st.success(f"Loaded {len(questions)} questions successfully.")

def show_test():
    if not st.session_state.questions:
        st.warning("No questions available. Please ask admin to upload questions.")
        return
    st.header("Take the Mock Test")
    with st.form("test_form"):
        answers = []
        for idx, q in enumerate(st.session_state.questions):
            answer = st.radio(q["question"], q["options"], key=f"q{idx}")
            answers.append(answer)
        submitted = st.form_submit_button("Submit Answers")
        if submitted:
            st.session_state.answers = answers
            st.session_state.submitted = True

def show_results():
    st.header("Test Results")
    score = 0
    for idx, q in enumerate(st.session_state.questions):
        correct = q["answer"] == st.session_state.answers[idx]
        if correct:
            score += 1
        st.markdown(f"**Q{idx+1}: {q['question']}**")
        st.markdown(f"- Your answer: {st.session_state.answers[idx]} {'✅' if correct else '❌'}")
        if not correct:
            st.markdown(f"- Correct answer: {q['answer']}")
        st.write("---")
    st.subheader(f"Your Score: {score} / {len(st.session_state.questions)}")
    if st.button("Retake Test"):
        st.session_state.answers = []
        st.session_state.submitted = False

def main():
    st.title("Mock Test Software")
    menu = ["Admin Upload", "Take Test"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Admin Upload":
        show_admin()
    elif choice == "Take Test":
        if st.session_state.submitted:
            show_results()
        else:
            show_test()

if __name__ == "__main__":
    main()


