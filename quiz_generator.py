import os
import json
from dotenv import load_dotenv
from langchain_groq.chat_models import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
import random

load_dotenv()

class AIQuizGenerator:
    def __init__(self, model="llama-3.3-70b-versatile", temperature=0.9):
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            raise ValueError("GROQ_API_KEY not found in .env")
        self.ai = ChatGroq(model=model, temperature=temperature)

    def create_quiz(self, topic, difficulty, num_questions):
        system_prompt = """You are a professional quiz creator. Return ONLY valid JSON in this format:

{
  "questions": [
    {
      "question": "string",
      "options": ["A", "B", "C", "D"],
      "correct_answer": 0,
      "explanation": "string"
    }
  ]
}

Rules:
- Exactly 4 options per question
- correct_answer must be index 0..3
- No extra text outside JSON
"""
        user_prompt = f"Create {num_questions} multiple choice questions about {topic} at {difficulty} level. Generate unique questions each time."

        messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]

        try:
            response = self.ai.invoke(messages)
            response_text = getattr(response, "content", str(response)).strip()

            # Remove ```json or ``` if present
            response_text = response_text.replace("```json", "").replace("```", "").strip()

            # Extract first JSON object in response
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            json_text = response_text[start:end]

            quiz_data = json.loads(json_text)
            questions = quiz_data.get("questions", [])

            # Shuffle questions to avoid repetition
            random.shuffle(questions)

            if not questions:
                raise ValueError("Parsed JSON has no questions.")

            return questions

        except Exception as e:
            print(f"❌ AI Error or parse failed: {e}")
            return self._backup_questions(topic, difficulty, num_questions)

    def _backup_questions(self, topic, difficulty, num_questions):
        return [
            {
                "question": f"Sample {difficulty} question about {topic}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": random.randint(0, 3),
                "explanation": "This is a fallback explanation."
            }
            for _ in range(num_questions)
        ]
