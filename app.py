import streamlit as st
from groq import Groq

# Initialize the Groq client
client = Groq(
    api_key="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"
)

def generate_questions(topic, num_questions=5):
    prompt = f"Generate {num_questions} interview questions on the topic: {topic}"
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="mixtral-8x7b-32768",
    )
    return response.choices[0].message.content.split("\n")

def evaluate_answer(question, answer):
    prompt = f"Evaluate the following answer to the question: '{question}'. Answer: '{answer}'. Provide a score out of 10 and suggest improvements."
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="mixtral-8x7b-32768",
    )
    return response.choices[0].message.content

# Streamlit App
st.title("AI-Powered Interview System")

# Input topic for the interview
topic = st.text_input("Enter the interview topic:")

if topic:
    num_questions = st.slider("Number of questions:", 1, 10, 5)
    
    if st.button("Generate Questions"):
        st.session_state.questions = generate_questions(topic, num_questions)
        st.session_state.answers = [""] * num_questions
    
    if "questions" in st.session_state:
        for i, question in enumerate(st.session_state.questions):
            st.subheader(f"Question {i+1}")
            st.write(question)
            st.session_state.answers[i] = st.text_area(f"Your Answer to Question {i+1}", key=f"answer_{i}", value=st.session_state.answers[i])

        if st.button("Evaluate All Answers"):
            st.session_state.evaluations = []
            for question, answer in zip(st.session_state.questions, st.session_state.answers):
                feedback = evaluate_answer(question, answer)
                st.session_state.evaluations.append(feedback)
                
    if "evaluations" in st.session_state:
        st.subheader("Evaluation Results")
        for i, (question, answer, evaluation) in enumerate(zip(st.session_state.questions, st.session_state.answers, st.session_state.evaluations)):
            st.write(f"**Question {i+1}:** {question}")
            st.write(f"**Your Answer:** {answer}")
            st.write(f"**Evaluation:** {evaluation}")

# Streamlit styling for dark mode
st.markdown(
    """
    <style>
    .main {
        background-color: #2E2E2E;
        color: #FFFFFF;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        font-size: 16px;
        border-radius: 12px;
        border: none;
        cursor: pointer;
        margin: 4px 2px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>input {
        background-color: #4F4F4F;
        color: #FFFFFF;
        padding: 12px;
        font-size: 16px;
        border-radius: 12px;
        border: 1px solid #ccc;
    }
    .stTextArea>div>textarea {
        background-color: #4F4F4F;
        color: #FFFFFF;
        padding: 12px;
        font-size: 16px;
        border-radius: 12px;
        border: 1px solid #ccc;
    }
    </style>
    """,
    unsafe_allow_html=True
)
