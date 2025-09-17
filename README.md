# KnowledgeQuest AI
✨ Test your knowledge on any topic with AI-generated quizzes and get instant feedback! 🚀

---

## Overview
**KnowledgeQuest AI** is an interactive quiz app powered by **Groq + LangChain**. Users can select any topic, generate a quiz, answer multiple-choice questions, and get instant feedback with explanations. Correct answers turn **green**, wrong answers turn **red**, and results are summarized at the end.

The app is built with **Python** and **Streamlit**, providing a clean, responsive, and fun user interface.

---

## Features
- Generate quizzes on **any topic** dynamically.
- Multiple-choice questions with **4 options** each.
- Instant feedback on answers (**green for correct, red for wrong**).
- Explanations for each question.
- Results summary with **score, percentage, and grade**.
- Elegant UI with **purple default buttons** and smooth animations.
- Fallback questions if AI fails to generate questions.

---

## Demo
Try the live app here: [KnowledgeQuest AI](https://knowledgequest-ai-tsvwydecujwsmynxda8okh.streamlit.app)

---

## Project Structure
```text
knowledgequest-ai/
│
├─ app.py                # Main Streamlit app
├─ quiz_generator.py     # AI Quiz generation logic
├─ requirements.txt      # Python dependencies
├─ style.css             # Optional CSS for styling
├─ .streamlit/
│   └─ secrets.toml      # Groq API key (not tracked in Git)
├─ .gitignore            # Ignore .env, __pycache__, etc.
└─ README.md             # Project documentation
<img width="1808" height="653" alt="image" src="https://github.com/user-attachments/assets/eb5d8bdd-7a13-4a54-8103-bafc73c47366" />

