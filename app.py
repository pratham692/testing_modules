import streamlit as st
import json
import random
import string
from datetime import datetime
import os

DATA_FILE = "test_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def admin_view(data):
    st.title("Admin Panel - Mock Test")

    menu = ["Create Test Code", "Upload Questions", "View Reports"]
    choice = st.sidebar.selectbox("Select Action", menu)

    if choice == "Create Test Code":
        st.header("Create Test Code")
        if st.button("Generate New Test Code"):
            code = generate_code()
            if code not in data:
                data[code] = {"questions": [], "results": []}
                save_data(data)
                st.success(f"New test code created: {code}")
            else:
                st.error("Code collision, try again.")
        st.write("Existing Test Codes:")
        st.write(list(data.keys()))

    elif choice == "Upload Questions":
        st.header("Upload Questions")
        code = st.text_input("Enter Test Code")
        if code:
            if code not in data:
                st.error("Test code does not exist. Please create it first.")
            else:
                questions_text = st.text_area("Enter Questions JSON", height=200, help='Example: [{"question":"Q1","options":["A","B","C"],"correctAnswer":0}]')
                if st.button("Upload Questions"):
                    try:
                        questions = json.loads(questions_text)
                        if isinstance(questions, list):
                            data[code]["questions"] = questions
                            save_data(data)
                            st.success("Questions uploaded successfully.")
                        else:
                            st.error("Questions JSON must be a list.")
                    except Exception as e:
                        st.error(f"Invalid JSON: {e}")

    elif choice == "View Reports":
        st.header("View Test Reports")
        code = st.text_input("Enter Test Code to View Report")
        if code:
            if code not in data:
                st.error("Test code does not exist.")
            else:
                results = data[code].get("results", [])
                if not results:
                    st.info("No test results found for this code.")
                else:
                    st.write(f"Total Tests Taken: {len(results)}")
                    for i, result in enumerate(results, 1):
                        dt = datetime.fromisoformat(result["date"]).strftime("%Y-%m-%d %H:%M:%S")
                        st.write(f"Test {i}: Score = {result['score']} on {dt}")

def user_view(data):
    st.title("Take Mock Test")

    code = st.text_input("Enter Test Code")
    if code:
        if code not in data:
            st.error("Test code not found.")
            return
        questions = data[code].get("questions", [])
        if not questions:
            st.info("No questions available for this test.")
            return

        answers = []
        with st.form("test_form"):
            for i, q in enumerate(questions):
                st.write(f"**Q{i+1}: {q['question']}**")
                options = q.get("options", [])
                answer = st.radio("", options, key=f"q{i}")
                answers.append(answer)
            submitted = st.form_submit_button("Submit Test")
            if submitted:
                score = 0
                for i, q in enumerate(questions):
                    correct_index = q.get("correctAnswer")
                    if correct_index is not None and options[correct_index] == answers[i]:
                        score += 1
                # Save result
                result = {"score": score, "date": datetime.now().isoformat()}
                data[code].setdefault("results", []).append(result)
                save_data(data)
                st.success(f"Test submitted successfully. Your score: {score} / {len(questions)}")

def main():
    st.sidebar.title("Mock Test System")
    user_type = st.sidebar.radio("Select User Type", ["Admin", "User"])

    data = load_data()

    if user_type == "Admin":
        admin_view(data)
    else:
        user_view(data)

if __name__ == "__main__":
    main()



