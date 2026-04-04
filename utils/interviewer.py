import google.generativeai as genai
import time
import streamlit as st
import hashlib
import json
from datetime import datetime, timedelta

# Global model instance to avoid recreating
_model = None

# Simple cache for API responses
_cache = {}

def get_model():
    global _model
    if _model is None:
        try:
            _model = genai.GenerativeModel("gemini-2.5-flash")
        except Exception as e:
            st.error(f"Failed to initialize Gemini model: {e}")
            return None
    return _model

def _get_cache_key(text):
    """Generate a cache key from text content"""
    return hashlib.md5(text.encode()).hexdigest()

def _get_cached_response(cache_key):
    """Retrieve cached response if still valid (24 hours)"""
    if cache_key in _cache:
        cached_time, cached_data = _cache[cache_key]
        if datetime.now() - cached_time < timedelta(hours=24):
            return cached_data
        else:
            del _cache[cache_key]  # Expired
    return None

def _set_cached_response(cache_key, data):
    """Store response in cache"""
    _cache[cache_key] = (datetime.now(), data)

def generate_interview_questions(jd, resume_text):
    model = get_model()
    
    # Check cache first
    cache_key = _get_cache_key(f"questions:{jd}:{resume_text}")
    cached = _get_cached_response(cache_key)
    if cached:
        st.info("📦 Using cached interview questions")
        return cached
    
    if model is None:
        return [
            "Tell me about a project relevant to this job.",
            "Describe a technical challenge you solved.",
            "How do you prioritize tasks under tight deadlines?",
            "Explain a piece of technology from your resume.",
            "Why are you interested in this role?",
        ]

    try:
        prompt = f"Based on this JD and the candidate's resume, generate exactly 5 relevant behavioral and technical interview questions tailored to the candidate's experience and skills mentioned in the resume:\nJD: {jd}\nResume: {resume_text}\nReturn only the questions, one per line."
        response = model.generate_content(prompt)
        questions = [q.strip("- ").strip() for q in response.text.split("\n") if q.strip() and not q.startswith("```")]
        questions = questions[:5]
        
        # Cache the result
        _set_cached_response(cache_key, questions)
        return questions
    except Exception as e:
        if "429" in str(e) or "quota" in str(e).lower():
            st.warning("⚠️ Gemini API quota exceeded. Using fallback questions.")
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
    
    # Check cache first
    cache_key = _get_cache_key(f"eval:{question}:{answer}")
    cached = _get_cached_response(cache_key)
    if cached:
        return cached
    
    try:
        prompt = f"Evaluate this answer to the question.\nQuestion: {question}\nAnswer: {answer}\nGive feedback and score out of 10."
        response = model.generate_content(prompt)
        result = response.text
        
        # Cache the result
        _set_cached_response(cache_key, result)
        return result
    except Exception as e:
        if "429" in str(e) or "quota" in str(e).lower():
            return "⚠️ API quota exceeded. Please try again later or upgrade to a paid plan."
        return f"Evaluation failed: {str(e)}"
