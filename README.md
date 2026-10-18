# AI-Based Resume Skill Gap Analyzer

A beginner-friendly mini-project prototype built with Python, Gradio, pandas, and PyMuPDF.

## Features
- Upload a text-based PDF resume.
- Select Python Developer, Java Developer, or Web Developer.
- Detect predefined skill keywords in the resume.
- Compare detected skills with the sample requirements for the selected role.
- Show matched skills, missing skills, a simple match percentage, and learning suggestions.

## Project files
- `app.py` — application and Gradio interface.
- `requirements.txt` — Python packages required to run the app.
- `.gitignore` — files that should not be uploaded to GitHub.

## Run locally
Use Python 3.10 or newer if possible.

1. Open Terminal in this folder.
2. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open the local Gradio URL shown in Terminal.

## Important limitations
This is an educational prototype. It finds predefined skill keywords in selectable PDF text; it is not a full semantic AI resume parser. Scanned/image-only PDFs may require OCR. The sample job requirements and match percentage are illustrative and do not guarantee employability or job readiness.
