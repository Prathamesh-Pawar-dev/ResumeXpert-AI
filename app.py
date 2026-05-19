import streamlit as st
import pdfplumber
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from sklearn.feature_extraction.text import (
    TfidfVectorizer,
    ENGLISH_STOP_WORDS
)

from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="ResumeXpert AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

/* Main Background */

.stApp {
    background: linear-gradient(
        to right,
        #0f172a,
        #111827
    );
    color: white;
}

/* Global Text */

html, body, [class*="css"]  {
    color: white;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Metric Cards */

.metric-card {
    background: linear-gradient(
        135deg,
        #2563eb,
        #06b6d4
    );

    padding: 25px;

    border-radius: 18px;

    text-align: center;

    color: white;

    box-shadow: 0px 6px 25px rgba(0,0,0,0.3);
}

/* Skill Box */

.skill-box {
    background-color: #1e293b;

    padding: 12px;

    border-radius: 12px;

    margin-bottom: 10px;

    border-left: 5px solid #06b6d4;

    color: white;
}

/* Text Area */

textarea {
    background-color: #1e293b !important;
    color: white !important;
}

/* Hide Footer */

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown("""
<h1 style='text-align:center;'>
🚀 ResumeXpert AI
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<h4 style='text-align:center;color:lightgray;'>
Professional ATS Resume Analyzer
</h4>
""", unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("ResumeXpert AI")

st.sidebar.info("""
Upload your resume and compare
it with the Job Description.
""")

st.sidebar.markdown("---")

st.sidebar.write("### Features")

st.sidebar.write("✅ ATS Match Score")
st.sidebar.write("✅ Resume Analytics")
st.sidebar.write("✅ AI Suggestions")
st.sidebar.write("✅ Skill Analysis")
st.sidebar.write("✅ Dashboard Visualization")

# ---------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    "📄 Upload Resume PDF",
    type=["pdf"]
)

# ---------------------------------------------------
# JOB DESCRIPTION
# ---------------------------------------------------

job_description = st.text_area(
    "📝 Paste Job Description",
    height=220
)

# ---------------------------------------------------
# START ANALYSIS
# ---------------------------------------------------

if uploaded_file is not None and job_description != "":

    text = ""

    # ---------------------------------------------------
    # EXTRACT PDF TEXT
    # ---------------------------------------------------

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:

                text += extracted

    clean_text = text.lower()

    clean_jd = job_description.lower()

    # ---------------------------------------------------
    # KEYWORD EXTRACTION
    # ---------------------------------------------------

    job_keywords = clean_jd.split()

    job_keywords = list(set(job_keywords))

    # ---------------------------------------------------
    # CUSTOM STOPWORDS
    # ---------------------------------------------------

    custom_stopwords = {

        "looking",
        "candidate",
        "candidates",
        "ideal",
        "required",
        "preferred",
        "responsibilities",
        "qualification",
        "skills",
        "knowledge",
        "apply",
        "related",
        "degree",
        "junior",
        "senior",
        "teams",
        "team",
        "work",
        "working",
        "generate",
        "development",
        "business",
        "understanding",
        "strong",
        "good",
        "excellent",
        "present",
        "using",
        "experience",
        "role",
        "opportunity",
        "ability",
        "problem",
        "solving",
        "communication",
        "management"
    }

    # ---------------------------------------------------
    # FILTER KEYWORDS
    # ---------------------------------------------------

    filtered_keywords = []

    for word in job_keywords:

        if (
            word not in ENGLISH_STOP_WORDS
            and word not in custom_stopwords
            and len(word) > 3
            and word.isalpha()
        ):

            filtered_keywords.append(word)

    job_keywords = filtered_keywords

    # ---------------------------------------------------
    # MATCHED KEYWORDS
    # ---------------------------------------------------

    found_keywords = []

    for word in job_keywords:

        if word in clean_text:

            found_keywords.append(word)

    # ---------------------------------------------------
    # MISSING KEYWORDS
    # ---------------------------------------------------

    missing_keywords = []

    for word in job_keywords:

        if word not in clean_text:

            missing_keywords.append(word)

    # ---------------------------------------------------
    # ATS SCORE
    # ---------------------------------------------------

    documents = [clean_text, clean_jd]

    tfidf = TfidfVectorizer()

    matrix = tfidf.fit_transform(documents)

    similarity = cosine_similarity(
        matrix[0:1],
        matrix[1:2]
    )

    ats_score = similarity[0][0] * 100

    # ---------------------------------------------------
    # DASHBOARD METRICS
    # ---------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(f"""
        <div class="metric-card">
        <h2>{round(ats_score,2)}%</h2>
        <p>ATS Match Score</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="metric-card">
        <h2>{len(found_keywords)}</h2>
        <p>Matched Skills</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class="metric-card">
        <h2>{len(missing_keywords)}</h2>
        <p>Missing Skills</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # ---------------------------------------------------
    # ATS GAUGE CHART
    # ---------------------------------------------------

    st.subheader("📊 ATS Match Meter")

    fig = go.Figure(go.Indicator(

        mode = "gauge+number",

        value = ats_score,

        title = {'text': "ATS Score"},

        gauge = {

            'axis': {'range': [0, 100]},

            'bar': {'color': "#06b6d4"},

            'steps': [

                {'range': [0, 40], 'color': "#ef4444"},

                {'range': [40, 70], 'color': "#f59e0b"},

                {'range': [70, 100], 'color': "#22c55e"}

            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------------------------------
    # RESUME EVALUATION
    # ---------------------------------------------------

    st.subheader("📈 Resume Evaluation")

    if ats_score >= 80:

        st.success("Excellent Match ✅")

    elif ats_score >= 60:

        st.warning("Good Match 👍")

    else:

        st.error("Low Match ❌")

    # ---------------------------------------------------
    # KEYWORD ANALYSIS
    # ---------------------------------------------------

    col4, col5 = st.columns(2)

    # MATCHED

    with col4:

        st.subheader("✅ Matching Keywords")

        for keyword in found_keywords:

            st.markdown(
                f"""
                <div class='skill-box'>
                ✔ {keyword}
                </div>
                """,
                unsafe_allow_html=True
            )

    # MISSING

    with col5:

        st.subheader("❌ Missing Keywords")

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

    st.write("")

    # ---------------------------------------------------
    # PIE CHART
    # ---------------------------------------------------

    st.subheader("📌 Skill Distribution")

    pie_data = pd.DataFrame({

        "Category": [
            "Matched",
            "Missing"
        ],

        "Count": [
            len(found_keywords),
            len(missing_keywords)
        ]
    })

    pie_chart = px.pie(

        pie_data,

        names="Category",

        values="Count",

        hole=0.5
    )

    st.plotly_chart(
        pie_chart,
        use_container_width=True
    )

    # ---------------------------------------------------
    # AI SUGGESTIONS
    # ---------------------------------------------------

    st.subheader("🤖 AI Suggestions")

    if ats_score < 60:

        st.info("""
        Add more technical keywords from the
        job description into your projects,
        skills, and internship sections.
        """)

    elif ats_score < 80:

        st.info("""
        Your resume is good but can be improved
        by adding measurable achievements and
        more domain-specific keywords.
        """)

    else:

        st.success("""
        Your resume is highly optimized for
        this job role.
        """)

    # ---------------------------------------------------
    # SECTION ANALYSIS
    # ---------------------------------------------------

    st.subheader("📋 Resume Section Analysis")

    sections = {

        "Skills": "skills" in clean_text,
        "Projects": "project" in clean_text,
        "Experience": "experience" in clean_text,
        "Education": "education" in clean_text,
        "Certifications": "certification" in clean_text
    }

    for section, status in sections.items():

        if status:

            st.success(f"✅ {section} Section Found")

        else:

            st.warning(f"⚠ {section} Section Missing")

    # ---------------------------------------------------
    # RESUME PREVIEW
    # ---------------------------------------------------

    with st.expander("📄 Resume Text Preview"):

        st.write(text[:4000])

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "🚀 Developed using Python • NLP • Streamlit • Machine Learning"
)