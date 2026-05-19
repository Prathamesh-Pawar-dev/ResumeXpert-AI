import streamlit as st
import pdfplumber

# -----------------------------------
# Page Title
# -----------------------------------

st.title("ResumeXpert - Smart ATS Resume Analyzer")

st.write("Upload your resume and get ATS analysis instantly.")

# -----------------------------------
# Upload Resume
# -----------------------------------

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

# -----------------------------------
# Skills Database
# -----------------------------------

skills = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "power bi",
    "tableau",
    "excel",
    "git",
    "github",
    "data science",
    "numpy",
    "pandas",
    "tensorflow"
]

# -----------------------------------
# Resume Analysis
# -----------------------------------

if uploaded_file is not None:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

    clean_text = text.lower()

    # -----------------------------------
    # Skill Detection
    # -----------------------------------

    found_skills = []

    for skill in skills:

        if skill in clean_text:

            found_skills.append(skill)

    # -----------------------------------
    # Display Skills
    # -----------------------------------

    st.subheader("Detected Skills")

    for skill in found_skills:

        st.write("✔", skill)

    # -----------------------------------
    # ATS Score
    # -----------------------------------

    score = (
        len(found_skills) / len(skills)
    ) * 100

    st.subheader("ATS Score")

    st.success(f"{round(score,2)} %")

    # -----------------------------------
    # Resume Strength
    # -----------------------------------

    if score >= 70:

        st.success("Strong Resume ✅")

    elif score >= 40:

        st.warning("Good Resume 👍")

    else:

        st.error("Needs Improvement ⚠")