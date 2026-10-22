import streamlit as st
import fitz
import re
import io
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

st.set_page_config(
    page_title="AI Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide"
)
st.markdown("""
<style>
.stApp {
    background: #f3f6fc !important;
    color: #1e293b !important;
}

.stApp, .stApp p, .stApp label,
.stApp span, .stApp div {
    color: #1e293b;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #263b80 !important;
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #475569 !important;
    font-size: 17px;
}

div[data-testid="stMetric"] {
    background: #ffffff !important;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #dce5ff;
}

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #1e293b !important;
}

.stButton > button {
    background: #4357d8 !important;
    color: #ffffff !important;
    border-radius: 10px;
    border: none;
    padding: 10px 22px;
    font-weight: 600;
}

.stButton > button p,
.stDownloadButton > button p {
    color: #ffffff !important;
}

.stDownloadButton > button {
    background: #16805d !important;
    color: #ffffff !important;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


st.markdown(
    '<div class="main-title">🎯 AI-Based Skill Gap Analyzer</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Analyze your resume, discover skill gaps, and prepare for your dream job.</div>',
    unsafe_allow_html=True
)
st.write("")
st.divider()

job_roles = {
    "Python Developer": [
        "Python", "SQL", "OOP", "DSA", "Git", "Problem Solving"
    ],
    "Java Developer": [
        "Java", "SQL", "OOP", "DSA", "Git", "Problem Solving"
    ],
    "Web Developer": [
        "HTML", "CSS", "JavaScript", "SQL", "Git", "Responsive Design"
    ],
    "Data Analyst": [
        "Python", "SQL", "Excel", "Power BI", "Statistics", "Data Visualization"
    ],
    "Data Scientist": [
        "Python", "SQL", "Statistics", "Machine Learning", "Pandas", "Data Visualization"
    ],
    "Machine Learning Engineer": [
        "Python", "Machine Learning", "Statistics", "Pandas", "NumPy", "Scikit-learn"
    ],
    "Software Developer": [
        "Programming", "OOP", "DSA", "SQL", "Git", "Problem Solving"
    ],
    "Frontend Developer": [
        "HTML", "CSS", "JavaScript", "React", "Git", "Responsive Design"
    ],
    "Backend Developer": [
        "Python", "Java", "SQL", "APIs", "Git", "Database Design"
    ],
    "SQL/Database Developer": [
        "SQL", "Database Design", "Joins", "Normalization", "Indexes", "Stored Procedures"
    ]
}

learning_resources = {
    "Python": "Practice Python basics, functions, and coding problems.",
    "Java": "Study Java fundamentals, classes, and object-oriented programming.",
    "SQL": "Practice SELECT queries, joins, grouping, and subqueries.",
    "OOP": "Learn classes, objects, inheritance, and polymorphism.",
    "DSA": "Practice arrays, strings, searching, sorting, and basic data structures.",
    "Git": "Learn Git commands and how to manage projects using GitHub.",
    "Problem Solving": "Solve beginner programming problems regularly.",
    "HTML": "Learn HTML tags, forms, and webpage structure.",
    "CSS": "Practice layouts, styling, Flexbox, and CSS Grid.",
    "JavaScript": "Learn variables, functions, events, and DOM manipulation.",
    "Responsive Design": "Practice making websites work on mobile and desktop screens.",
    "Excel": "Learn formulas, sorting, filtering, and pivot tables.",
    "Power BI": "Create dashboards and practice data visualization.",
    "Statistics": "Study mean, median, probability, distributions, and basic statistics.",
    "Data Visualization": "Practice presenting data through clear charts and graphs.",
    "Machine Learning": "Learn supervised learning, model training, and model evaluation.",
    "Pandas": "Practice cleaning, filtering, and analyzing datasets with Pandas.",
    "NumPy": "Learn arrays and numerical operations using NumPy.",
    "Scikit-learn": "Practice building and evaluating ML models with Scikit-learn.",
    "Programming": "Strengthen programming fundamentals and write small programs.",
    "React": "Learn components, props, state, and basic React applications.",
    "APIs": "Understand REST APIs, HTTP methods, and JSON responses.",
    "Database Design": "Learn tables, relationships, keys, and database design.",
    "Joins": "Practice INNER JOIN, LEFT JOIN, RIGHT JOIN, and related queries.",
    "Normalization": "Study database normalization and how it reduces data duplication.",
    "Indexes": "Learn how database indexes help improve query performance.",
    "Stored Procedures": "Learn how to create and use stored procedures in SQL."
}

# Resume mein skill ke alternative words ko bhi pehchanne ke liye
skill_aliases = {
    "OOP": ["oop", "object oriented programming", "object-oriented programming"],
    "DSA": ["dsa", "data structures and algorithms", "data structure and algorithms"],
    "Git": ["git", "github"],
    "Machine Learning": ["machine learning", "machine-learning", "ml"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy", "num py"],
    "Scikit-learn": ["scikit-learn", "scikit learn", "sklearn"],
    "Power BI": ["power bi", "powerbi"],
    "Responsive Design": ["responsive design", "responsive web design"],
    "APIs": ["api", "apis", "rest api", "restful api"],
    "Database Design": ["database design", "database schema"],
    "Problem Solving": ["problem solving", "problem-solving"],
    "Data Visualization": ["data visualization", "data visualisation"],
    "Stored Procedures": ["stored procedure", "stored procedures"]
}

st.subheader("📝 Resume and Job Details")

col1, col2 = st.columns(2)

with col1:
    selected_role = st.selectbox(
        "Choose your target job role",
        list(job_roles.keys())
    )

with col2:
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF only)",
        type=["pdf"]
    )

st.caption(
    "Your resume is analyzed using keyword matching. "
    "The match percentage is an estimate, not a hiring guarantee."
)

if st.button("🔍 Analyze Resume", use_container_width=True):

    if uploaded_file is None:
        st.warning("Please upload your resume in PDF format.")

    else:
        try:
            pdf_document = fitz.open(
                stream=uploaded_file.getvalue(),
                filetype="pdf"
            )

            resume_text = ""

            for page in pdf_document:
                resume_text += page.get_text() + "\n"

            pdf_document.close()
            resume_text = resume_text.lower()

            if not resume_text.strip():
                st.error(
                    "No readable text was found. Please upload a text-based PDF resume."
                )
                st.stop()

            required_skills = job_roles[selected_role]
            found_skills = []
            missing_skills = []

            for skill in required_skills:
                possible_names = skill_aliases.get(
                    skill, [skill.lower()]
                )

                skill_found = False

                for name in possible_names:
                    pattern = r"(?<![a-z0-9])" + re.escape(name) + r"(?![a-z0-9])"

                    if re.search(pattern, resume_text):
                        skill_found = True
                        break

                if skill_found:
                    found_skills.append(skill)
                else:
                    missing_skills.append(skill)

            percentage = (
                len(found_skills) / len(required_skills)
            ) * 100

            st.session_state["analysis"] = {
                "role": selected_role,
                "found": found_skills,
                "missing": missing_skills,
                "percentage": percentage
            }

        except Exception as error:
            st.error(
                "Unable to read this PDF. Please try another PDF resume."
            )

if "analysis" in st.session_state:
    result = st.session_state["analysis"]

    st.divider()
    st.subheader("📊 Your Resume Analysis Dashboard")

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric("Skill Match", f"{result['percentage']:.0f}%")

    with metric2:
        st.metric("Skills Found", len(result["found"]))

    with metric3:
        st.metric("Skills to Improve", len(result["missing"]))

    st.progress(int(result["percentage"]))

    st.write(f"**Selected Job Role:** {result['role']}")

    left, right = st.columns(2)

    with left:
        st.markdown("### ✅ Matched Skills")

        if result["found"]:
            for skill in result["found"]:
                st.success(f"✓ {skill}")
        else:
            st.info("No required skills detected yet.")

    with right:
        st.markdown("### 📚 Skills to Improve")

        if result["missing"]:
            for skill in result["missing"]:
                st.warning(f"**{skill}**")
                st.write(learning_resources.get(
                    skill,
                    "Search for beginner tutorials and practice projects."
                ))
        else:
            st.success("All listed skills were detected in your resume!")

    st.divider()
    st.subheader("📈 Skill Match Visualization")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.pie(
            [result["percentage"], 100 - result["percentage"]],
            labels=["Matched", "Gap"],
            autopct="%1.0f%%",
            startangle=90
        )
        ax.set_title("Resume Skill Match")
        st.pyplot(fig)
        plt.close(fig)

    with chart_col2:
        fig, ax = plt.subplots(figsize=(5, 3))

        labels = ["Matched", "Missing"]
        values = [len(result["found"]), len(result["missing"])]

        ax.bar(labels, values)
        ax.set_ylabel("Number of Skills")
        ax.set_title("Skills Overview")
        ax.set_ylim(0, max(len(result["found"]) + len(result["missing"]), 1) + 1)

        st.pyplot(fig)
        plt.close(fig)

    st.divider()
    st.subheader("📥 Download Your Analysis Report")

    def create_pdf_report(data):
        buffer = io.BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            textColor=colors.HexColor("#263b80"),
            spaceAfter=18
        )

        story = [
            Paragraph("AI Skill Gap Analyzer Report", title_style),
            Paragraph(f"<b>Target Job Role:</b> {data['role']}", styles["Normal"]),
            Spacer(1, 12),
            Paragraph(
                f"<b>Estimated Skill Match:</b> {data['percentage']:.0f}%",
                styles["Heading2"]
            ),
            Paragraph(
                f"<b>Skills Found:</b> {len(data['found'])}",
                styles["Normal"]
            ),
            Paragraph(
                f"<b>Skills to Improve:</b> {len(data['missing'])}",
                styles["Normal"]
            ),
            Spacer(1, 16),
            Paragraph("Matched Skills", styles["Heading2"])
        ]

        found_text = ", ".join(data["found"]) if data["found"] else "None detected"
        story.append(Paragraph(found_text, styles["Normal"]))
        story.append(Spacer(1, 16))
        story.append(Paragraph("Skills to Improve and Recommendations", styles["Heading2"]))

        if data["missing"]:
            table_data = [["Skill", "Learning Recommendation"]]

            for skill in data["missing"]:
                table_data.append([
                    Paragraph(skill, styles["Normal"]),
                    Paragraph(
                        learning_resources.get(skill, "Practice this skill."),
                        styles["Normal"]
                    )
                ])

            report_table = Table(
                table_data,
                colWidths=[120, 350],
                repeatRows=1
            )

            report_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4357d8")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 8)
            ]))

            story.append(report_table)
        else:
            story.append(
                Paragraph("No missing skills detected in the listed skill set.", styles["Normal"])
            ) 
            story.append(Spacer(1, 20))
        story.append(Paragraph(
            "This report highlights the skills identified in your resume "
            "and provides learning recommendations to support your career preparation.",
            styles["Italic"]
        ))
        

        document.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    try:
        report_bytes = create_pdf_report(result)

        st.download_button(
            label="⬇️ Download PDF Report",
            data=report_bytes,
            file_name="skill_gap_analysis_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    except Exception:
        st.error(
            "The report could not be generated. Please check that ReportLab is installed."
        )

st.divider()
st.caption(
    "AI Skill Gap Analyzer | Educational project | "
    "Results depend on the skills detected in the uploaded resume."
)
