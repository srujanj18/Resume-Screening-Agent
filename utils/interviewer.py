import google.generativeai as genai

def generate_interview_questions(jd, resume_text):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"Based on this JD and the candidate's resume, generate exactly 5 relevant behavioral and technical interview questions tailored to the candidate's experience and skills mentioned in the resume:\nJD: {jd}\nResume: {resume_text}\nReturn only the questions, one per line."
        response = model.generate_content(prompt)
        questions = [q.strip("- ").strip() for q in response.text.split("\n") if q.strip() and not q.startswith("```")]
        return questions[:5]
    except Exception as e:
        # Fallback if AI not available
        return [
            "Tell me about a project relevant to this job.",
            "Describe a technical challenge you solved.",
            "How do you prioritize tasks under tight deadlines?",
            "Explain a piece of technology from your resume.",
            "Why are you interested in this role?",
        ]

def evaluate_answer(question, answer, model):
    if model is None:
        return "AI unavailable — placeholder feedback. Configure GEMINI_API_KEY to enable evaluation."
    try:
        prompt = f"Evaluate this answer to the question.\nQuestion: {question}\nAnswer: {answer}\nGive feedback and score out of 10."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Evaluation failed: {str(e)}"
