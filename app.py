import streamlit as st
import pdfplumber

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="ResumeXpert AI",
    page_icon="📄",
    layout="centered"
)

# -----------------------------------
# TITLE
# -----------------------------------

st.title("ResumeXpert - Smart ATS Resume Analyzer")

st.write(
    "Upload your resume and get ATS analysis instantly."
)

# -----------------------------------
# FILE UPLOAD
# -----------------------------------

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

# -----------------------------------
# SKILLS DATABASE
# -----------------------------------

skills = [
    "python",
    "java",
    "c++",
    "sql",
    "machine learning",
    "deep learning",
    "data science",
    "power bi",
    "tableau",
    "excel",
    "tensorflow",
    "pandas",
    "numpy",
    "scikit-learn",
    "html",
    "css",
    "javascript",
    "git",
    "github",
    "nlp",
    "streamlit"
]

# -----------------------------------
# RESUME ANALYSIS
# -----------------------------------

if uploaded_file is not None:

    text = ""

    # Extract Text From PDF

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

    # Convert To Lowercase

    clean_text = text.lower()

    # -----------------------------------
    # SKILL DETECTION
    # -----------------------------------

    found_skills = []

    for skill in skills:

        if skill in clean_text:

            found_skills.append(skill)

    # -----------------------------------
    # SHOW DETECTED SKILLS
    # -----------------------------------

    st.subheader("Detected Skills")

    if len(found_skills) > 0:

        for skill in found_skills:

            st.write("✔", skill)

    else:

        st.warning("No matching skills detected.")

    # -----------------------------------
    # SMART ATS SCORE
    # -----------------------------------

    score = 0

    # Skills Score (40 Marks)

    skills_score = (
        len(found_skills) / len(skills)
    ) * 40

    score += skills_score

    # Education Score (20 Marks)

    education_keywords = [
        "bachelor",
        "engineering",
        "computer",
        "degree",
        "university",
        "b.tech",
        "student"
    ]

    for word in education_keywords:

        if word in clean_text:

            score += 20
            break

    # Projects Score (20 Marks)

    project_keywords = [
        "project",
        "projects",
        "internship",
        "developed",
        "application"
    ]

    for word in project_keywords:

        if word in clean_text:

            score += 20
            break

    # Experience Score (20 Marks)

    experience_keywords = [
        "experience",
        "internship",
        "work",
        "training"
    ]

    for word in experience_keywords:

        if word in clean_text:

            score += 20
            break

    # Limit Score To 100

    if score > 100:

        score = 100

    # -----------------------------------
    # SHOW ATS SCORE
    # -----------------------------------

    st.subheader("ATS Score")

    st.success(f"{round(score,2)} %")

    # -----------------------------------
    # RESUME STRENGTH
    # -----------------------------------

    st.subheader("Resume Strength")

    if score >= 80:

        st.success("Strong Resume ✅")

    elif score >= 60:

        st.warning("Good Resume 👍")

    else:

        st.error("Needs Improvement ⚠")

    # -----------------------------------
    # MISSING SKILLS
    # -----------------------------------

    st.subheader("Recommended Skills To Add")

    missing_skills = []

    for skill in skills:

        if skill not in found_skills:

            missing_skills.append(skill)

    top_missing = missing_skills[:8]

    for skill in top_missing:

        st.write("❌", skill)

    # -----------------------------------
    # RESUME TEXT PREVIEW
    # -----------------------------------

    with st.expander("View Extracted Resume Text"):

        st.write(text[:3000])

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    "Developed using Python, Streamlit, NLP and Machine Learning"
)