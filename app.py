import streamlit as st
import pdfplumber

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
    "Upload your resume and compare it with the job description."
)

# -----------------------------------
# RESUME UPLOAD
# -----------------------------------

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

# -----------------------------------
# JOB DESCRIPTION INPUT
# -----------------------------------

job_description = st.text_area(
    "Paste Job Description Here"
)

# -----------------------------------
# START ANALYSIS
# -----------------------------------

if uploaded_file is not None and job_description != "":

    text = ""

    # -----------------------------------
    # EXTRACT TEXT FROM PDF
    # -----------------------------------

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:

                text += extracted

    # -----------------------------------
    # CLEAN TEXT
    # -----------------------------------

    clean_text = text.lower()

    clean_jd = job_description.lower()

    # -----------------------------------
    # EXTRACT KEYWORDS FROM JOB DESCRIPTION
    # -----------------------------------

    job_keywords = clean_jd.split()

    # Remove duplicates

    job_keywords = list(set(job_keywords))

    # -----------------------------------
    # FIND MATCHING KEYWORDS
    # -----------------------------------

    found_keywords = []

    for word in job_keywords:

        if len(word) > 3 and word in clean_text:

            found_keywords.append(word)

    # -----------------------------------
    # SHOW MATCHING KEYWORDS
    # -----------------------------------

    st.subheader("Matching Keywords")

    if len(found_keywords) > 0:

        for keyword in found_keywords:

            st.write("✔", keyword)

    else:

        st.warning("No matching keywords detected.")

    # -----------------------------------
    # ATS MATCH SCORE
    # -----------------------------------

    documents = [clean_text, clean_jd]

    tfidf = TfidfVectorizer()

    matrix = tfidf.fit_transform(documents)

    similarity = cosine_similarity(
        matrix[0:1],
        matrix[1:2]
    )

    ats_score = similarity[0][0] * 100

    # -----------------------------------
    # SHOW ATS SCORE
    # -----------------------------------

    st.subheader("ATS Match Score")

    st.success(f"{round(ats_score,2)} %")

    # -----------------------------------
    # RESUME EVALUATION
    # -----------------------------------

    st.subheader("Resume Evaluation")

    if ats_score >= 80:

        st.success("Excellent Match ✅")

    elif ats_score >= 60:

        st.warning("Good Match 👍")

    else:

        st.error("Low Match ❌")

    # -----------------------------------
    # MISSING KEYWORDS
    # -----------------------------------

    st.subheader("Missing Keywords")

    missing_keywords = []

    for word in job_keywords:

        if len(word) > 3 and word not in clean_text:

            missing_keywords.append(word)

    if len(missing_keywords) > 0:

        top_missing = missing_keywords[:15]

        for keyword in top_missing:

            st.write("❌", keyword)

    else:

        st.success(
            "No major keywords missing."
        )

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
    "Developed using Python, NLP, Streamlit and Machine Learning"
)