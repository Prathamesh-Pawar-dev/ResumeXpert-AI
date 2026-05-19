import streamlit as st
import pdfplumber

from sklearn.feature_extraction.text import (
    TfidfVectorizer,
    ENGLISH_STOP_WORDS
)

from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="ResumeXpert AI",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>

/* Main App */

.stApp {
    background-color: #0E1117;
    color: white;
}

/* Global Text */

html, body, [class*="css"] {
    color: white;
}

/* Headings */

h1, h2, h3, h4, h5, h6 {
    color: white !important;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: #161B22;
    color: white;
}

/* Text Area */

textarea {
    background-color: #1c1f26 !important;
    color: white !important;
    border-radius: 10px;
}

/* File Uploader */

[data-testid="stFileUploader"] {
    background-color: #1c1f26;
    border-radius: 12px;
    padding: 15px;
}

/* Metric Cards */

.metric-card {
    background: linear-gradient(
        135deg,
        #1f77ff,
        #00c6ff
    );

    padding: 25px;

    border-radius: 18px;

    color: white;

    text-align: center;

    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

/* Skill Boxes */

.skill-box {
    background-color: #1c1f26;

    padding: 12px;

    border-radius: 12px;

    margin-bottom: 10px;

    border-left: 5px solid #00c6ff;

    color: white;
}

/* Footer */

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HEADER
# -----------------------------------

st.markdown(
    """
    <h1 style='text-align:center;'>
    🚀 ResumeXpert AI
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h4 style='text-align:center;color:gray;'>
    Smart ATS Resume Analyzer
    </h4>
    """,
    unsafe_allow_html=True
)

st.write("")

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("ResumeXpert AI")

st.sidebar.info(
    """
    Upload your resume and compare it
    with the job description.
    """
)

st.sidebar.markdown("---")

st.sidebar.write("### Features")

st.sidebar.write("✅ ATS Match Score")
st.sidebar.write("✅ Keyword Analysis")
st.sidebar.write("✅ Missing Keywords")
st.sidebar.write("✅ Resume Evaluation")
st.sidebar.write("✅ Smart Dashboard")

# -----------------------------------
# FILE UPLOAD
# -----------------------------------

uploaded_file = st.file_uploader(
    "📄 Upload Resume PDF",
    type=["pdf"]
)

# -----------------------------------
# JOB DESCRIPTION
# -----------------------------------

job_description = st.text_area(
    "📝 Paste Job Description Here",
    height=220
)

# -----------------------------------
# START ANALYSIS
# -----------------------------------

if uploaded_file is not None and job_description != "":

    text = ""

    # -----------------------------------
    # PDF TEXT EXTRACTION
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
    # KEYWORD EXTRACTION
    # -----------------------------------

    job_keywords = clean_jd.split()

    job_keywords = list(set(job_keywords))

    filtered_keywords = []

    for word in job_keywords:

        if (
            word not in ENGLISH_STOP_WORDS
            and len(word) > 3
            and word.isalpha()
        ):

            filtered_keywords.append(word)

    job_keywords = filtered_keywords

    # -----------------------------------
    # MATCHING KEYWORDS
    # -----------------------------------

    found_keywords = []

    for word in job_keywords:

        if word in clean_text:

            found_keywords.append(word)

    # -----------------------------------
    # MISSING KEYWORDS
    # -----------------------------------

    missing_keywords = []

    for word in job_keywords:

        if word not in clean_text:

            missing_keywords.append(word)

    # -----------------------------------
    # ATS SCORE
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
    # DASHBOARD METRICS
    # -----------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
                <h2>{round(ats_score,2)}%</h2>
                <p>ATS Match Score</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card">
                <h2>{len(found_keywords)}</h2>
                <p>Matched Keywords</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-card">
                <h2>{len(missing_keywords)}</h2>
                <p>Missing Keywords</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # -----------------------------------
    # ATS PROGRESS BAR
    # -----------------------------------

    st.subheader("📊 ATS Match Progress")

    st.progress(int(ats_score))

    st.write("")

    # -----------------------------------
    # RESUME EVALUATION
    # -----------------------------------

    st.subheader("📈 Resume Evaluation")

    if ats_score >= 80:

        st.success("Excellent Match ✅")

    elif ats_score >= 60:

        st.warning("Good Match 👍")

    else:

        st.error("Low Match ❌")

    st.write("")

    # -----------------------------------
    # MATCHED & MISSING KEYWORDS
    # -----------------------------------

    col4, col5 = st.columns(2)

    # MATCHED

    with col4:

        st.subheader("✅ Matching Keywords")

        if len(found_keywords) > 0:

            for keyword in found_keywords:

                st.markdown(
                    f"""
                    <div class='skill-box'>
                    ✔ {keyword}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.warning(
                "No matching keywords found."
            )

    # MISSING

    with col5:

        st.subheader("❌ Missing Keywords")

        if len(missing_keywords) > 0:

            top_missing = missing_keywords[:15]

            for keyword in top_missing:

                st.markdown(
                    f"""
                    <div class='skill-box'>
                    ❌ {keyword}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.success(
                "No major keywords missing."
            )

    st.write("")

    # -----------------------------------
    # RESUME TEXT PREVIEW
    # -----------------------------------

    with st.expander(
        "📄 View Extracted Resume Text"
    ):

        st.write(text[:3000])

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    "🚀 Developed using Python • NLP • Streamlit • Machine Learning"
)