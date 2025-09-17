# app.py - KnowledgeQuest AI with instant feedback and fun UI

import time
import streamlit as st
from quiz_generator import AIQuizGenerator

# 🎨 Custom CSS for UI
st.markdown(
    """
    <style>
    /* Page background */
    .main {
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        color: white;
    }
    /* Title */
    h1 {
        text-align: center;
        color: #ffeb3b;
        text-shadow: 2px 2px #000;
    }
    /* Tagline */
    .tagline {
        text-align: center;
        font-size: 120%;
        font-weight: bold;
        color: #fff8e1;
        margin-bottom: 20px;
    }
    /* Default purple buttons */
    .stButton>button {
        background: linear-gradient(90deg, #8e2de2, #4a00e0);
        color: white !important;
        border-radius: 12px;
        padding: 12px 24px;
        font-size: 18px;
        font-weight: bold;
        transition: transform 0.2s, background 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #9d50bb, #6e48aa);
    }
    /* Question card */
    .question-box {
        background: rgba(255,255,255,0.15);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    }
    /* Result metrics */
    .stMetric {
        background: rgba(0,0,0,0.3);
        border-radius: 12px;
        padding: 10px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title="KnowledgeQuest AI", layout="wide")
st.markdown("<h1>KnowledgeQuest AI</h1>", unsafe_allow_html=True)
st.markdown("<div class='tagline'>✨ Test your knowledge on any topic with AI-generated questions and get instant feedback! 🚀</div>", unsafe_allow_html=True)

# Initialize AI quiz generator
@st.cache_resource
def load_quiz_generator():
    try:
        return AIQuizGenerator()
    except Exception as e:
        st.error(f"Error loading AI: {e}")
        return None

quiz_gen = load_quiz_generator()
if quiz_gen is None:
    st.error("🔑 Please check your API key in the .env file")
    st.stop()

# Function to reset to home
def go_home():
    for key in ['quiz_started', 'questions', 'current_question', 'user_answers', 'quiz_completed']:
        st.session_state.pop(key, None)
    st.rerun()

# Home / Start Quiz
if 'quiz_started' not in st.session_state or not st.session_state.quiz_started:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📚 Choose Your Topic")
        topic = st.text_input("Enter any topic:", "Python Programming",
                              help="Examples: Python, Geography, History, Math, Science...")
    with col2:
        st.markdown("### ⚙️ Quiz Settings")
        difficulty = st.selectbox("Difficulty:", ["beginner", "intermediate", "advanced"])
        num_questions = st.selectbox("Number of questions:", [5, 10, 15, 20])

    st.markdown("---")
    if st.button("🚀 Generate Quiz", type="primary", use_container_width=True):
        if topic.strip():
            with st.spinner("🤖 AI is creating your personalized quiz..."):
                try:
                    questions = quiz_gen.create_quiz(topic, difficulty, num_questions)
                    st.session_state.questions = questions
                    st.session_state.current_question = 0
                    st.session_state.user_answers = []
                    st.session_state.quiz_started = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating quiz: {e}")
        else:
            st.error("⚠️ Please enter a topic!")

# Quiz interface
if st.session_state.get("quiz_started", False):
    st.markdown("---")
    st.markdown("## 🎯 Your Quiz")

    q_num = st.session_state.current_question
    questions = st.session_state.questions

    # Back to home button
    if st.button("🏠 Back to Home"):
        go_home()

    if q_num < len(questions):
        question = questions[q_num]
        st.markdown(f"<div class='question-box'><h3>❓ {question['question']}</h3></div>", unsafe_allow_html=True)

        # Display answer options
        for i, option in enumerate(question['options']):
            clicked = st.button(f"{chr(65+i)}. {option}", key=f"option_{q_num}_{i}", use_container_width=True)
            if clicked:
                is_correct = option == question.get("options")[question.get("correct_answer", 0)]
                st.session_state.user_answers.append({
                    'question_index': q_num,
                    'selected': i,
                    'correct': question.get("correct_answer", 0),
                    'is_correct': is_correct
                })

                if is_correct:
                    st.success("✅ Correct! 🎉 You're amazing!")
                else:
                    correct_opt = question['options'][question.get("correct_answer", 0)]
                    st.error(f"❌ Wrong! Correct answer: {correct_opt}")

                st.info(f"💡 Explanation: {question.get('explanation','')}")
                st.session_state.current_question += 1
                time.sleep(1)
                st.rerun()

    # Show results if quiz completed
    if st.session_state.get("current_question", 0) >= len(questions):
        st.markdown("---")
        st.markdown("## 🎉 Quiz Results")
        correct_answers = sum(1 for ans in st.session_state.user_answers if ans['is_correct'])
        total_questions = len(st.session_state.user_answers)
        percentage = (correct_answers / total_questions) * 100

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score", f"{correct_answers}/{total_questions}")
        with col2:
            st.metric("Percentage", f"{percentage:.1f}%")
        with col3:
            if percentage >= 80:
                st.metric("Grade", "A - Excellent! 🏆")
            elif percentage >= 60:
                st.metric("Grade", "B - Good job! 👍")
            else:
                st.metric("Grade", "C - Keep practicing! 📚")

        # Reset / Play Again button
        if st.button("🔄 Take Another Quiz"):
            go_home()
