# app.py - TalentFlow AI: Resume Screening + Voice Interview Agent
# v1.2.0: Robust secrets handling with fallbacks - forces cache bust
import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import google.generativeai as genai
from utils.resume_parser import extract_text_from_pdf
import utils.interviewer as interviewer
from utils.report_generator import generate_pdf_report
from supabase import create_client
import whisper
import numpy as np
import soundfile as sf
import os
from datetime import datetime

# ===================== UI CONFIG =====================
st.set_page_config(page_title="TalentFlow AI - Rooman Internship", layout="wide")

# ===================== CONFIG & SECRETS HANDLING =====================
# Load Gemini API key safely
gemini_key = st.secrets.get("GEMINI_API_KEY")
if gemini_key:
    try:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        ai_enabled = True
    except Exception:
        model = None
        ai_enabled = False
        st.warning("Failed to configure Gemini model. AI features disabled.")
else:
    model = None
    ai_enabled = False
    st.warning("GEMINI_API_KEY not found in secrets. AI features are disabled. See SECRETS_SETUP.md")

# Create Supabase clients only if keys exist
supabase_public = None
supabase_admin = None
supabase_url = st.secrets.get("SUPABASE_URL")
supabase_key = st.secrets.get("SUPABASE_KEY")
service_role = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY")
if supabase_url and supabase_key:
    try:
        supabase_public = create_client(supabase_url, supabase_key)
    except Exception:
        supabase_public = None
        st.warning("Failed to create Supabase public client. Database features disabled.")
else:
    st.info("Supabase public key or URL missing. Database features will be disabled until configured.")

if supabase_url and service_role:
    try:
        supabase_admin = create_client(supabase_url, service_role)
    except Exception:
        supabase_admin = None
        st.warning("Failed to create Supabase admin client. Admin DB operations disabled.")

# If AI not enabled, provide safe fallbacks in the interviewer module
if not ai_enabled:
    def _fallback_questions(jd, resume_text):
        return [
            "Tell me about a project relevant to this job.",
            "Describe a technical challenge you solved.",
            "How do you prioritize tasks under tight deadlines?",
            "Explain a piece of technology from your resume.",
            "Why are you interested in this role?",
        ]

    def _fallback_evaluate(question, answer, model=None):
        return "AI unavailable — placeholder feedback. Configure GEMINI_API_KEY to enable evaluation."

    interviewer.generate_interview_questions = _fallback_questions
    interviewer.evaluate_answer = _fallback_evaluate

@st.cache_resource
def load_whisper():
    return whisper.load_model("turbo")

whisper_model = load_whisper()

# ===================== AUDIO PROCESSOR =====================
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.frames = []

    def recv(self, frame):
        self.frames.append(frame.to_ndarray())

# ===================== SESSION STATE =====================
if "candidate" not in st.session_state:
    st.session_state.candidate = None
if "interview_stage" not in st.session_state:
    st.session_state.interview_stage = 0
if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = []
if "interview_type" not in st.session_state:
    st.session_state.interview_type = "Text"
if "current_feedback" not in st.session_state:
    st.session_state.current_feedback = ""
if "audio_frames" not in st.session_state:
    st.session_state.audio_frames = []
if "recording" not in st.session_state:
    st.session_state.recording = False
st.title("TalentFlow AI – Resume Screener + Voice Interview Agent")
st.markdown("**Rooman Technologies Internship Challenge 2025 | Combined Agent #2 + #3**")

tab1, tab2, tab3 = st.tabs(["Resume Screening", "Interview", "Final Report"])

with tab1:
    st.header("Step 1: Resume Screening")
    jd = st.text_area("Paste Job Description", height=200)
    resume = st.file_uploader("Upload Resume (PDF)", type="pdf")

    if st.button("Analyze Resume", type="primary") and resume and jd:
        with st.spinner("Extracting resume text..."):
            resume_text = extract_text_from_pdf(resume)

        with st.spinner("AI evaluating candidate..."):
            prompt = f"""
            Job Description: {jd}
            Resume: {resume_text}
            Extract the candidate's full name, academic marks/CGPA for 10th, PU (12th), and Engineering, score this resume out of 100, and return JSON only:
            {{
              "name": "Full name from resume",
              "10th_marks": "CGPA or percentage",
              "pu_marks": "CGPA or percentage",
              "engineering_cgpa": "CGPA",
              "score": 88,
              "match_percentage": "88%",
              "strengths": ["Python", "ML", "3+3 years"],
              "gaps": ["No AWS", "No leadership"],
              "summary": "Strong technical fit"
            }}
            """
            response = model.generate_content(prompt)
            try:
                result = eval(response.text.strip("```json").strip("```"))
            except:
                result = {"name": "Candidate", "score": 85, "match_percentage": "85%", "strengths": [], "gaps": [], "summary": "Good fit"}

            st.session_state.candidate = {
                "name": result["name"],
                "resume_score": result["score"],
                "jd": jd,
                "resume_text": resume_text,
                "details": result
            }
            st.session_state.questions = interviewer.generate_interview_questions(jd, resume_text)

            st.success(f"**{result['name']}** → Resume Score: **{result['score']}/100**")
            st.json(result)

with tab2:
    st.header("Step 2: Automated Interview")
    if st.session_state.candidate:
        st.write(f"**Candidate:** {st.session_state.candidate['name']}")
        st.write(f"**Resume Score:** {st.session_state.candidate['resume_score']}/100")

        # Interview type selection
        interview_type = st.radio("Select Interview Type:", ["Text", "Voice"], horizontal=True, key="interview_type_radio")
        st.session_state.interview_type = interview_type

        if st.session_state.interview_stage < len(st.session_state.questions):
            # Display previous answers in chat history
            for i, answer_data in enumerate(st.session_state.answers):
                st.chat_message("user").write(f"Q{i+1}: {answer_data['question']}\n\nA: {answer_data['answer']}")
                st.chat_message("assistant").write(answer_data['feedback'])

            # Display current question
            st.info(f"Question {st.session_state.interview_stage + 1}/{len(st.session_state.questions)}: {st.session_state.questions[st.session_state.interview_stage]}")

            # Check if current question has been answered
            if st.session_state.interview_stage < len(st.session_state.answers):
                # Question already answered, show next question button
                st.success("✓ Answer submitted!")
                if st.button("Next Question", type="secondary", key=f"next_{st.session_state.interview_stage}"):
                    st.session_state.interview_stage += 1
                    st.rerun()
            else:
                # Question not yet answered, show input fields
                answer = None
                submit_button = False

                # Current question input based on type
                if st.session_state.interview_type == "Text":
                    answer = st.text_input("Your answer:", key=f"answer_{st.session_state.interview_stage}", placeholder="Type your answer here...")
                    submit_button = st.button("Submit Answer", type="primary", key=f"submit_{st.session_state.interview_stage}")
                elif st.session_state.interview_type == "Voice":
                    st.write("🎤 Record your voice answer:")
                    audio_processor = AudioProcessor()
                    webrtc_ctx = webrtc_streamer(
                        key=f"audio_{st.session_state.interview_stage}",
                        mode=WebRtcMode.SENDONLY,
                        audio_processor_factory=lambda: audio_processor,
                        media_stream_constraints={"audio": True, "video": False}
                    )

                    if st.button("Process Voice Answer", type="primary", key=f"process_audio_{st.session_state.interview_stage}"):
                        if audio_processor.frames:
                            # Combine audio frames
                            audio_data = np.concatenate(audio_processor.frames, axis=0)
                            # Save to temporary file
                            temp_audio_path = f"temp_audio_{st.session_state.interview_stage}.wav"
                            sf.write(temp_audio_path, audio_data, 16000)

                            # Transcribe with Whisper
                            with st.spinner("Transcribing audio..."):
                                result = whisper_model.transcribe(temp_audio_path)
                                answer = result["text"].strip()

                            # Clean up
                            if os.path.exists(temp_audio_path):
                                os.remove(temp_audio_path)

                            st.success(f"Transcribed: {answer}")
                            submit_button = True
                        else:
                            st.error("No audio recorded. Please record your answer first.")
                            submit_button = False

                if submit_button and answer:
                    # Evaluate answer
                    with st.spinner("Evaluating your answer..."):
                        feedback = interviewer.evaluate_answer(
                            st.session_state.questions[st.session_state.interview_stage],
                            answer,
                            model
                        )
                    
                    st.session_state.answers.append({
                        "question": st.session_state.questions[st.session_state.interview_stage],
                        "answer": answer,
                        "feedback": feedback
                    })
                    
                    st.rerun()
        else:
            st.success("All questions asked! Generating report...")
    else:
        st.warning("Please analyze a resume first")

with tab3:
    st.header("Final Report & Database Save")
    if st.session_state.candidate and len(st.session_state.answers) >= 5:
        interview_score = 80 + len(st.session_state.answers)  # mock scoring
        final_score = (st.session_state.candidate["resume_score"] + interview_score) // 2

        if st.button("Generate Final Report & Save", type="primary"):
            # Save to Supabase using admin client to bypass RLS
            try:
                supabase_admin.table("candidates").insert({
                    "name": st.session_state.candidate["name"],
                    "resume_score": st.session_state.candidate["resume_score"],
                    "interview_score": interview_score,
                    "final_score": final_score,
                    "created_at": datetime.now().isoformat()
                }).execute()
                db_saved = True
                st.success("Report generated and saved to database!")
            except Exception as e:
                st.warning(f"Database save failed: {e}. Proceeding with report generation.")
                db_saved = False
                st.success("Report generated! (Database save skipped)")

            # Generate PDF
            pdf_bytes = generate_pdf_report(st.session_state.candidate, st.session_state.answers, final_score)
            st.download_button(
                "Download Final Report (PDF)",
                pdf_bytes,
                file_name=f"{st.session_state.candidate['name']}_TalentFlow_Report.pdf",
                mime="application/pdf"
            )
    else:
        st.info("Complete interview to generate report")