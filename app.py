import streamlit as st
import fitz

st.set_page_config(
    page_title="AI Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI-Based Skill Gap Analyzer")
st.write("Analyze your resume and discover skills needed for your dream job.")

job_roles = {
    "Python Developer": ["Python", "SQL", "OOP", "DSA", "Git"],
    "Java Developer": ["Java", "SQL", "OOP", "DSA", "Git"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "SQL", "Git"]
}

learning_resources = {
    "Python": "Learn Python basics and practice coding.",
    "Java": "Learn Java fundamentals and object-oriented programming.",
    "SQL": "Practice SQL queries and database concepts.",
    "OOP": "Study classes, objects, inheritance, and polymorphism.",
    "DSA": "Practice arrays, strings, searching, and sorting.",
    "Git": "Learn Git commands and GitHub basics.",
    "HTML": "Learn HTML tags and page structure.",
    "CSS": "Practice styling, layouts, and responsive design.",
    "JavaScript": "Learn variables, functions, and DOM manipulation."
}

selected_role = st.selectbox(
    "Select your target job role",
    list(job_roles.keys())
)

uploaded_file = st.file_uploader(
    "Upload your resume (PDF only)",
    type=["pdf"]
)

if st.button("Analyze Resume"):
    if uploaded_file is None:
        st.warning("Please upload your resume PDF first.")
    else:
        pdf_document = fitz.open(
            stream=uploaded_file.read(),
            filetype="pdf"
        )

        resume_text = ""

        for page in pdf_document:
            resume_text += page.get_text()

        resume_text = resume_text.lower()
        required_skills = job_roles[selected_role]

        found_skills = []
        missing_skills = []

        for skill in required_skills:
            if skill.lower() in resume_text:
                found_skills.append(skill)
            else:
                missing_skills.append(skill)

        percentage = (len(found_skills) / len(required_skills)) * 100

        st.subheader("📊 Resume Analysis Result")
        st.write("**Selected Role:**", selected_role)
        st.progress(int(percentage))
        st.metric("Skill Match", f"{percentage:.0f}%")

        st.subheader("✅ Skills Found")

        if found_skills:
            st.write(", ".join(found_skills))
        else:
            st.write("No required skills detected.")

        st.subheader("📚 Skills to Improve")

        if missing_skills:
            for skill in missing_skills:
                st.write(f"**{skill}:** {learning_resources[skill]}")
        else:
            st.success("All listed skills were detected in your resume!")

        st.caption(
            "Note: This tool uses basic keyword matching. "
            "The percentage is an estimate, not a professional assessment."
        )
