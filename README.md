# TalentFlow AI - Resume Screening + Voice Interview Agent

## Overview of the Agent
TalentFlow AI is an intelligent recruitment assistant designed for the Rooman Internship Challenge 2025, combining resume screening and automated voice/video interviews. It streamlines the hiring process by evaluating candidates through AI-powered resume analysis, generating tailored interview questions, and conducting real-time multi-modal interviews (text, voice, or video). The agent provides comprehensive scoring, feedback, and generates final PDF reports, with data stored in a cloud database for easy access and management.

## Features & Limitations
### Features
- **Resume Screening**: Upload PDF resumes and get AI-scored evaluations out of 100, including match percentage, strengths, gaps, and summary based on job descriptions.
- **Dynamic Interview Questions**: Generates exactly 5 behavioral and technical questions tailored to the candidate's resume and job description using AI.
- **Multi-Modal Interviews**: Supports text-based and voice interviews with real-time speech-to-text transcription using Whisper.
- **Real-Time Evaluation**: Provides instant feedback and scoring for each interview answer.
- **Final Report Generation**: Creates downloadable PDF reports summarizing resume scores, interview performance, and overall candidate assessment.
- **Database Storage**: Saves candidate data to Supabase for persistent storage and retrieval.
- **User-Friendly UI**: Built with Streamlit for an intuitive web interface.

### Limitations
- Requires a stable internet connection for AI API calls and real-time processing.
- Voice and video interviews depend on browser permissions for microphone/camera access.
- Speech-to-text accuracy may vary based on audio quality and accents.
- Currently supports only PDF resume uploads.
- Database operations may fail if Supabase RLS (Row Level Security) policies are not configured properly.
- Limited to 5 questions per interview; no customization for question count.

## Tech Stack & APIs Used
### Tech Stack
- **Frontend/UI**: Streamlit (for web app interface)
- **Backend**: Python
- **AI/ML**: Google Generative AI (Gemini 2.5 Flash for text generation and evaluation), OpenAI Whisper (for speech-to-text)
- **PDF Processing**: PyPDF2 (for extracting text from resumes)
- **Audio/Video Handling**: streamlit-webrtc (for real-time audio/video streaming), soundfile and numpy (for audio processing)
- **Database**: Supabase (for cloud storage)
- **Report Generation**: fpdf (for PDF report creation)
- **Other Libraries**: torch (for Whisper model)

### APIs Used
- **Google Generative AI (Gemini)**: For generating interview questions and evaluating answers.
- **Supabase API**: For storing and retrieving candidate data.
- **OpenAI Whisper API**: For transcribing audio from voice/video interviews.

## Setup & Run Instructions
### Prerequisites
- Python 3.8 or higher
- A Google Cloud account with Generative AI API enabled
- A Supabase account with a project set up
- Microphone and camera access (for voice/video interviews)

### Installation Steps
1. **Clone the Repository**:
   ```
   git clone https://github.com/srujanj18/Resume-Screening-Agent.git
   cd Resume-Screening-Agent
   ```

2. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Configure Secrets**:
   - Create a `.streamlit/secrets.toml` file in the project root.
   - Add your API keys:
     ```
     GEMINI_API_KEY = "your_google_generative_ai_api_key"
     SUPABASE_URL = "your_supabase_project_url"
     SUPABASE_KEY = "your_supabase_anon_key"
     SUPABASE_SERVICE_ROLE_KEY = "your_supabase_service_role_key"
     ```
   - **Note**: The `SUPABASE_SERVICE_ROLE_KEY` is required to bypass RLS policies when saving to the database. Get it from your Supabase project settings.

4. **Set Up Supabase Database**:
   - Create a table named `candidates` with columns: `name` (text), `resume_score` (int), `interview_score` (int), `final_score` (int), `created_at` (timestamp).
   - Row Level Security (RLS) can be enabled or disabled based on your setup. See `SUPABASE_SETUP.md` for detailed RLS configuration options.

### Running the Application
1. **Start the App**:
   ```
   streamlit run app.py
   ```

2. **Access the App**:
   - Open your browser and go to `http://localhost:8501`.
   - Follow the tabs: Resume Screening → Interview → Final Report.

### Live Demo
A live demo is available at: https://resumescreeningagent-fmuugwqybpqmxvphejkyb3.streamlit.app
                           https://8hg291mk-8501.inc1.devtunnels.ms/

## Potential Improvements
- **Enhanced AI Models**: Integrate more advanced LLMs for better question generation and evaluation accuracy.
- **Multi-Language Support**: Add support for interviews in multiple languages with translation capabilities.
- **Advanced Analytics**: Implement dashboards for HR analytics, such as candidate trends and performance metrics.
- **Integration with ATS**: Connect with Applicant Tracking Systems like Greenhouse or Lever for seamless data flow.
- **Video Analysis**: Add facial expression and body language analysis for video interviews.
- **Scalability**: Optimize for handling multiple concurrent interviews and larger datasets.
- **Security Enhancements**: Implement end-to-end encryption for sensitive candidate data.
- **Customizable Question Sets**: Allow users to define custom question templates or categories.
- **Offline Mode**: Enable offline processing for resume screening without internet dependency.
- **Feedback Loop**: Incorporate user feedback to continuously improve AI evaluations.
