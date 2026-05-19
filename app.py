import streamlit as st
import pdfplumber
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from sklearn.feature_extraction.text import TfidfVectorizer
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

/* Main App */

.stApp {
    background: linear-gradient(
        to right,
        #0f172a,
        #111827
    );
    color: white;
}

/* Global Text */

html, body, [class*="css"] {
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

/* Skill Boxes */

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
st.sidebar.write("✅ Smart Skill Detection")
st.sidebar.write("✅ Missing Skills Analysis")
st.sidebar.write("✅ Resume Evaluation")
st.sidebar.write("✅ Dashboard Analytics")

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
# MASTER SKILL DATABASE
# ---------------------------------------------------

tech_skills = [

    # Programming

    "python",
    "java",
    "c++",
    "javascript",
    "sql",

    # Data Science

    "machine learning",
    "deep learning",
    "data science",
    "data analysis",
    "nlp",

    # Libraries

    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",

    # Visualization

    "power bi",
    "tableau",
    "excel",

    # Development

    "streamlit",
    "flask",
    "django",
    "react",
    "nodejs",

    # Database

    "mysql",
    "mongodb",

    # Cloud & DevOps

    "aws",
    "azure",
    "docker",

    # Tools

    "git",
    "github",
    "uipath",
    "etl",
    "automation"
]

# ---------------------------------------------------
# START ANALYSIS
# ---------------------------------------------------

analyze_button = st.button(
    "🚀 Analyze Resume"
)

if (
    analyze_button
    and uploaded_file is not None
    and job_description != ""
):

    text = ""

    # ---------------------------------------------------
    # PDF TEXT EXTRACTION
    # ---------------------------------------------------

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:

                text += extracted

    # ---------------------------------------------------
    # CLEAN TEXT
    # ---------------------------------------------------

    clean_text = text.lower()

    clean_jd = job_description.lower()

    # ---------------------------------------------------
    # EXTRACT JD SKILLS
    # ---------------------------------------------------

    jd_skills = []

    for skill in tech_skills:

        if skill in clean_jd:

            jd_skills.append(skill)

    # ---------------------------------------------------
    # EXTRACT RESUME SKILLS
    # ---------------------------------------------------

    resume_skills = []

    for skill in tech_skills:

        if skill in clean_text:

            resume_skills.append(skill)

    # ---------------------------------------------------
    # MATCHED SKILLS
    # ---------------------------------------------------

    matched_skills = []

    for skill in jd_skills:

        if skill in resume_skills:

            matched_skills.append(skill)

    # ---------------------------------------------------
    # MISSING SKILLS
    # ---------------------------------------------------

    missing_skills = []

    for skill in jd_skills:

        if skill not in resume_skills:

            missing_skills.append(skill)

    # ---------------------------------------------------
    # ATS SCORE
    # ---------------------------------------------------

    if len(jd_skills) > 0:

        ats_score = (
            len(matched_skills)
            / len(jd_skills)
        ) * 100

    else:

        ats_score = 0

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
        <h2>{len(matched_skills)}</h2>
        <p>Matched Skills</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class="metric-card">
        <h2>{len(missing_skills)}</h2>
        <p>Missing Skills</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # ---------------------------------------------------
    # ATS GAUGE CHART
    # ---------------------------------------------------

    st.subheader("📊 ATS Match Meter")

    gauge_chart = go.Figure(go.Indicator(

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

    st.plotly_chart(
        gauge_chart,
        use_container_width=True
    )

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
    # MATCHED & MISSING SKILLS
    # ---------------------------------------------------

    col4, col5 = st.columns(2)

    # MATCHED SKILLS

    with col4:

        st.subheader("✅ Matched Skills")

        if len(matched_skills) > 0:

            for skill in matched_skills:

                st.markdown(
                    f"""
                    <div class='skill-box'>
                    ✔ {skill}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.warning(
                "No matching skills found."
            )

    # MISSING SKILLS

    with col5:

        st.subheader("❌ Missing Skills")

        if len(missing_skills) > 0:

            for skill in missing_skills:

                st.markdown(
                    f"""
                    <div class='skill-box'>
                    ❌ {skill}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.success(
                "No major skills missing."
            )

    st.write("")

    # ---------------------------------------------------
    # SKILL DISTRIBUTION CHART
    # ---------------------------------------------------

    st.subheader("📌 Skill Distribution")

    chart_data = pd.DataFrame({

        "Category": [
            "Matched Skills",
            "Missing Skills"
        ],

        "Count": [
            len(matched_skills),
            len(missing_skills)
        ]
    })

    pie_chart = px.pie(

        chart_data,

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
        Add more technical skills from the
        job description into your projects,
        internships, and skills section.
        """)

    elif ats_score < 80:

        st.info("""
        Your resume is good but can be
        improved with more project-based
        achievements and technical keywords.
        """)

    else:

        st.success("""
        Your resume is highly optimized
        for this job role.
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
    # RESUME TEXT PREVIEW
    # ---------------------------------------------------

    with st.expander("📄 Resume Preview"):

        st.write(text[:4000])

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "🚀 Developed using Python • NLP • Streamlit • Machine Learning"
)