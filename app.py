import gradio as gr
import pandas as pd
import fitz

# Job roles and the skills commonly required for each role.
job_data = {
    "Job_Role": (
        ["Python Developer"] * 5
        + ["Java Developer"] * 5
        + ["Web Developer"] * 5
    ),
    "Skill": [
        "Python", "SQL", "OOP", "DSA", "Git",
        "Java", "SQL", "OOP", "DSA", "Git",
        "HTML", "CSS", "JavaScript", "SQL", "Git",
    ],
}
jobs_df = pd.DataFrame(job_data)

learning_resources = {
    "Python": "Practise Python fundamentals and problem solving.",
    "Java": "Learn Java fundamentals and object-oriented programming.",
    "SQL": "Learn SQL queries, joins and database management.",
    "OOP": "Learn classes, objects, inheritance and polymorphism.",
    "DSA": "Practise arrays, strings, stacks, queues and algorithms.",
    "Git": "Learn version control, Git commands and GitHub basics.",
    "HTML": "Learn webpage structure using HTML.",
    "CSS": "Learn webpage styling using CSS.",
    "JavaScript": "Learn JavaScript fundamentals and DOM manipulation.",
}

ALL_SKILLS = [
    "Python", "Java", "SQL", "OOP", "DSA",
    "Git", "HTML", "CSS", "JavaScript",
]


def analyze_resume_job(pdf_file, job_role):
    """Extract supported skill keywords from a PDF and compare with a job role."""
    if pdf_file is None:
        return "Please upload your PDF resume."

    if not job_role:
        return "Please select a target job role."

    try:
        with fitz.open(pdf_file) as document:
            resume_text = " ".join(page.get_text() for page in document)
    except Exception as exc:
        return f"Could not read this PDF. Please try another PDF file. Details: {exc}"

    # Basic keyword matching (not a full semantic AI resume parser).
    text_lower = resume_text.lower()
    resume_skills = [
        skill for skill in ALL_SKILLS
        if skill.lower() in text_lower
    ]

    required = jobs_df.loc[jobs_df["Job_Role"] == job_role, "Skill"].tolist()
    if not required:
        return "The selected job role was not found."

    resume_skills_lower = {skill.lower() for skill in resume_skills}
    matched = [skill for skill in required if skill.lower() in resume_skills_lower]
    missing = [skill for skill in required if skill.lower() not in resume_skills_lower]
    percentage = (len(matched) / len(required)) * 100

    recommendations = [
        f"- {skill}: {learning_resources.get(skill, 'Find beginner learning resources.')}"
        for skill in missing
    ]

    return (
        f"Selected Job Role: {job_role}\n\n"
        f"Skills Found in Resume: {', '.join(resume_skills) if resume_skills else 'None of the supported keywords found'}\n\n"
        f"Required Skills: {', '.join(required)}\n\n"
        f"Matched Skills: {', '.join(matched) if matched else 'None'}\n\n"
        f"Missing Skills: {', '.join(missing) if missing else 'None'}\n\n"
        f"Skill Match Percentage: {percentage:.2f}%\n\n"
        f"Learning Recommendations:\n"
        + ("\n".join(recommendations) if recommendations else "No missing skills found for this role.")
        + "\n\nNote: This prototype searches for predefined skill keywords in selectable PDF text. "
          "A scanned/image-only PDF may not work without OCR. The match percentage is a simple "
          "comparison with this project's sample requirements, not a guarantee of job readiness."
    )


with gr.Blocks(title="AI-Based Resume Skill Gap Analyzer") as demo:
    gr.Markdown("# AI-Based Resume Skill Gap Analyzer")
    gr.Markdown(
        "Upload a text-based PDF resume and select a target role to view supported skills, "
        "matched skills, missing skills, a match percentage, and learning suggestions."
    )
    with gr.Row():
        resume_input = gr.File(
            label="Upload Your Resume (PDF)",
            file_types=[".pdf"],
            type="filepath",
        )
        job_input = gr.Dropdown(
            choices=jobs_df["Job_Role"].drop_duplicates().tolist(),
            label="Select Your Target Job Role",
            value="Python Developer",
        )
    analyze_button = gr.Button("Analyze Resume")
    report_output = gr.Textbox(label="Your Skill Gap Report", lines=18)
    analyze_button.click(
        fn=analyze_resume_job,
        inputs=[resume_input, job_input],
        outputs=report_output,
    )

if __name__ == "__main__":
    demo.launch()
