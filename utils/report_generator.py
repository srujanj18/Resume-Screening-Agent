import google.generativeai as genai
from fpdf import FPDF
from datetime import datetime
import streamlit as st
import re

def generate_pdf_report(candidate, answers, final_score, include_special_chars=False, max_chars=1200):
    """
    Generate a short, clean hiring report PDF.

    - include_special_chars=False: strips non-printable and non-ASCII characters (neat & safe).
    - include_special_chars=True: allows extended Latin characters (tries to preserve accents).
    - max_chars: max characters for the generated detailed text (keeps report to 1-2 pages).
    Returns: PDF bytes (latin-1 encoded).
    """

    # Configure Gemini (do this once at startup ideally)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Short prompt so model returns a brief report (1-2 paragraph, bullet points)
    prompt = f"""
Write a concise hiring summary for a candidate. Keep it short (about 6-10 sentences and 3-6 bullet points),
professional, and suitable to fit in one page. Include:
- 1-line candidate summary (role fit & top skills)
- Short academic line (degree + key marks if present)
- 3 quick strengths (bulleted)
- 2 short improvement areas (bulleted)
- Final recommendation (one line)

Candidate name: {candidate.get('name','Unknown')}
Resume highlights: {candidate.get('resume_text','')}
Interview answers (short): {answers}
Final score: {final_score}/100
"""
    # Generate model output (defensive extraction)
    try:
        try:
            response = model.generate_content(prompt)
        except TypeError:
            response = model.generate_content(contents=prompt)

        # Common property
        if hasattr(response, "text") and response.text:
            report_content = response.text
        else:
            # fallback shapes
            report_content = ""
            try:
                report_content = response.candidates[0].content[0].text
            except Exception:
                try:
                    report_content = getattr(response, "output_text", "") or ""
                except Exception:
                    report_content = ""
    except Exception as e:
        # fallback short summary if model fails
        report_content = (
            f"Candidate: {candidate.get('name','Unknown')}\n"
            f"Resume Score: {candidate.get('resume_score','N/A')}/100\n"
            f"Interview Score: {candidate.get('interview_score', 'N/A')}/100\n"
            f"Final Score: {final_score}/100\n"
            f"Recommendation: {'STRONG HIRE' if final_score >= 75 else 'CONSIDER'}\n"
        )

    # Truncate to keep report compact
    if report_content and len(report_content) > max_chars:
        report_content = report_content[:max_chars].rstrip()
        # try to end cleanly at a sentence end
        last_period = report_content.rfind('.')
        last_newline = report_content.rfind('\n')
        cut_pos = max(last_period, last_newline)
        if cut_pos > int(max_chars*0.5):
            report_content = report_content[:cut_pos+1]

    # Sanitization:
    # - If include_special_chars False: keep printable ASCII + newline + basic punctuation
    # - If True: try to preserve Latin-1 characters (accents) and remove control chars
    def sanitize(s: str, allow_extended=False):
        if not s:
            return ""
        # normalize newlines
        s = s.replace("\r\n", "\n").replace("\r", "\n")

        if allow_extended:
            # remove C0 control chars (except newline and tab), keep others, then ensure latin-1 encodable
            s = ''.join(ch for ch in s if (ch == '\n' or ch == '\t' or (ord(ch) >= 32 and ord(ch) <= 255)))
            # encode-decode via latin-1 to ensure bytes are representable for FPDF, replacing unknowns
            s = s.encode('latin-1', errors='replace').decode('latin-1')
            return s
        else:
            # Keep common printable ASCII range plus newlines and basic punctuation
            # Allow ASCII 32-126 and newline
            s = ''.join(ch for ch in s if (ch == '\n' or 32 <= ord(ch) <= 126))
            # collapse multiple blank lines to single blank line
            s = re.sub(r'\n\s*\n+', '\n\n', s)
            # trim long runs of spaces
            s = re.sub(r' {2,}', ' ', s)
            return s.strip()

    sanitized = sanitize(report_content, allow_extended=include_special_chars)

    # Build the PDF (compact, readable layout)
    pdf = FPDF(format='A4')
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Header
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "TalentFlow AI - Hiring Summary", ln=1, align="C")
    pdf.ln(3)

    # Candidate basic info line
    pdf.set_font("Arial", size=11)
    name_line = f"Candidate: {candidate.get('name','')}"
    resume_score = f"Resume Score: {candidate.get('resume_score','N/A')}/100"
    interview_score = f"Interview Score: {candidate.get('interview_score', 85 + len(answers))}/100"
    pdf.cell(0, 7, f"{name_line}  |  {resume_score}  |  {interview_score}", ln=1)
    pdf.cell(0, 7, f"Final Score: {final_score}/100    Date: {datetime.now().strftime('%Y-%m-%d')}", ln=1)
    pdf.ln(4)

    # Short detailed content using MultiCell for wrapping
    pdf.set_font("Arial", size=10)
    if sanitized:
        # Ensure paragraphs split on double-newline; single newlines preserved as line breaks
        paragraphs = sanitized.split("\n\n")
        for p in paragraphs:
            # Avoid extremely long single-line paragraphs
            p = p.strip()
            if not p:
                continue
            pdf.multi_cell(0, 6, p)
            pdf.ln(2)
    else:
        pdf.cell(0, 8, "No detailed content available.", ln=1)

    # Compact footer recommendation (ensure obvious final line)
    pdf.ln(4)
    pdf.set_font("Arial", "B", 11)
    rec = "Recommendation: STRONG HIRE" if final_score >= 75 else "Recommendation: REVIEW"
    pdf.cell(0, 8, rec, ln=1)

    # Return bytes (latin-1)
    return pdf.output(dest="S").encode("latin-1")
