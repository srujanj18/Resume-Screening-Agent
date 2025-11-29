import google.generativeai as genai

def generate_interview_questions(jd, resume_text):
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"Based on this JD and the candidate's resume, generate exactly 8 relevant behavioral and technical interview questions tailored to the candidate's experience and skills mentioned in the resume:\nJD: {jd}\nResume: {resume_text}\nReturn only the questions, one per line."
    response = model.generate_content(prompt)
    questions = [q.strip("- ").strip() for q in response.text.split("\n") if q.strip() and not q.startswith("```")]
    return questions[:8]

def evaluate_answer(question, answer, model):
    prompt = f"Evaluate this answer to the question.\nQuestion: {question}\nAnswer: {answer}\nGive feedback and score out of 10."
    response = model.generate_content(prompt)
    return response.text