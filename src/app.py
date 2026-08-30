import streamlit as st
import time
from io import BytesIO

from pipeline.pipeline import run_job_analysis_pipeline


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Job Fit Advisor",
    page_icon="🧑‍💻",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');


/* ==========================================================
   BASE
   ========================================================== */

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #edf3ff;
}

.stApp {
    background: #07111f;
    background-image:
        radial-gradient(
            circle at top left,
            rgba(0,191,255,0.14),
            transparent 32%
        ),
        radial-gradient(
            circle at bottom right,
            rgba(124,58,237,0.12),
            transparent 30%
        ),
        linear-gradient(
            180deg,
            #07111f 0%,
            #0a1729 100%
        );
}

#MainMenu,
footer,
header {
    visibility: hidden;
}

.block-container {
    padding: 2rem 3rem 4rem;
    max-width: 1250px;
}


/* ==========================================================
   HERO
   ========================================================== */

.hero {
    text-align: center;
    padding: 3.2rem 0 2.2rem;
}

.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #38bdf8;
    margin-bottom: 1rem;
}

.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.03em;
    color: #f8fbff;
    margin: 0 0 1rem;
}

.hero h1 span {
    background: linear-gradient(
        135deg,
        #38bdf8,
        #8b5cf6
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #b5c3d9;
    max-width: 650px;
    margin: 0 auto;
    line-height: 1.65;
}


/* ==========================================================
   DIVIDER
   ========================================================== */

.divider {
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(56,189,248,0.35),
        transparent
    );

    margin: 2rem 0;
}


/* ==========================================================
   INPUT CARD
   ========================================================== */

.input-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(56,189,248,0.18);
    border-radius: 22px;
    padding: 2rem 2.3rem;
    margin-bottom: 2rem;
    backdrop-filter: blur(14px);
    box-shadow: 0 10px 40px rgba(0,0,0,0.28);
}


/* ==========================================================
   INPUTS
   ========================================================== */

.stTextInput > div > div > input,
.stTextArea textarea {

    background: rgba(255,255,255,0.06) !important;

    border: 1px solid rgba(56,189,248,0.25) !important;

    border-radius: 12px !important;

    color: #f8fbff !important;

    font-family: 'DM Sans', sans-serif !important;

    font-size: 0.95rem !important;

    padding: 0.8rem 1rem !important;
}


.stTextInput > label,
.stTextArea > label,
.stFileUploader > label {

    font-family: 'DM Mono', monospace !important;

    font-size: 0.72rem !important;

    letter-spacing: 0.15em !important;

    text-transform: uppercase !important;

    color: #38bdf8 !important;

    font-weight: 500 !important;
}


/* ==========================================================
   FILE UPLOADER
   ========================================================== */

[data-testid="stFileUploader"] {

    background: rgba(255,255,255,0.03);

    border: 1px dashed rgba(56,189,248,0.25);

    border-radius: 14px;

    padding: 0.8rem;
}


/* ==========================================================
   BUTTON
   ========================================================== */

.stButton > button {

    background: linear-gradient(
        135deg,
        #38bdf8 0%,
        #8b5cf6 100%
    ) !important;

    color: white !important;

    font-family: 'Syne', sans-serif !important;

    font-weight: 700 !important;

    font-size: 0.95rem !important;

    letter-spacing: 0.04em !important;

    border: none !important;

    border-radius: 12px !important;

    padding: 0.8rem 2.2rem !important;

    transition: all 0.18s ease !important;

    box-shadow: 0 8px 30px rgba(56,189,248,0.22) !important;

    width: 100%;
}


.stButton > button:hover {

    transform: translateY(-2px) scale(1.01) !important;

    box-shadow:
        0 12px 35px rgba(56,189,248,0.32) !important;
}


/* ==========================================================
   SECTION HEADING
   ========================================================== */

.section-heading {

    font-family: 'Syne', sans-serif;

    font-size: 1.35rem;

    font-weight: 700;

    color: #f8fbff;

    margin: 2rem 0 1rem;
}


/* ==========================================================
   PIPELINE CARDS
   ========================================================== */

.step-card {

    background: rgba(255,255,255,0.035);

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 18px;

    padding: 1.25rem 1.5rem;

    margin-bottom: 1rem;

    position: relative;

    overflow: hidden;

    backdrop-filter: blur(10px);
}


.step-card.done {

    border-color: rgba(34,197,94,0.28);

    background: rgba(34,197,94,0.05);
}


.step-card.active {

    border-color: rgba(56,189,248,0.45);

    background: rgba(56,189,248,0.06);
}


.step-card::before {

    content: '';

    position: absolute;

    left: 0;

    top: 0;

    bottom: 0;

    width: 4px;

    background: rgba(255,255,255,0.06);
}


.step-card.done::before {
    background: #22c55e;
}


.step-card.active::before {
    background: #38bdf8;
}


.step-header {

    display: flex;

    align-items: center;

    gap: 0.8rem;
}


.step-num {

    font-family: 'DM Mono', monospace;

    font-size: 0.68rem;

    color: #38bdf8;
}


.step-title {

    font-family: 'Syne', sans-serif;

    font-size: 0.95rem;

    font-weight: 700;

    color: #f8fbff;
}


.step-status {

    margin-left: auto;

    font-family: 'DM Mono', monospace;

    font-size: 0.65rem;

    letter-spacing: 0.1em;
}


.status-waiting {
    color: #64748b;
}


.status-running {
    color: #38bdf8;
}


.status-done {
    color: #22c55e;
}


.step-desc {

    font-size: 0.78rem;

    color: #94a3b8;

    margin-top: 0.4rem;

    padding-left: 2rem;
}


/* ==========================================================
   RESULT PANELS
   ========================================================== */

.result-panel {

    background: rgba(255,255,255,0.03);

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 18px;

    padding: 1.5rem 1.8rem;

    margin-bottom: 1rem;

    backdrop-filter: blur(12px);
}


.result-title {

    font-family: 'DM Mono', monospace;

    font-size: 0.7rem;

    letter-spacing: 0.2em;

    text-transform: uppercase;

    color: #38bdf8;

    padding-bottom: 0.7rem;

    margin-bottom: 1rem;

    border-bottom:
        1px solid rgba(56,189,248,0.15);
}


/* ==========================================================
   SCORE CARD
   ========================================================== */

.score-card {

    background:
        linear-gradient(
            135deg,
            rgba(56,189,248,0.10),
            rgba(139,92,246,0.10)
        );

    border:
        1px solid rgba(56,189,248,0.25);

    border-radius: 20px;

    padding: 2rem;

    text-align: center;

    margin-bottom: 1.5rem;
}


.score-label {

    font-family: 'DM Mono', monospace;

    font-size: 0.7rem;

    letter-spacing: 0.2em;

    text-transform: uppercase;

    color: #94a3b8;
}


.score-value {

    font-family: 'Syne', sans-serif;

    font-size: 4rem;

    font-weight: 800;

    color: #f8fbff;

    line-height: 1.1;

    margin: 0.4rem 0;
}


/* ==========================================================
   NOTICE
   ========================================================== */

.notice {

    font-family: 'DM Mono', monospace;

    font-size: 0.7rem;

    color: #64748b;

    text-align: center;

    margin-top: 3rem;

    letter-spacing: 0.08em;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "results" not in st.session_state:
    st.session_state.results = {}

if "running" not in st.session_state:
    st.session_state.running = False


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def extract_resume_text(uploaded_file):

    """
    Extract text from PDF or DOCX resume.
    """

    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name.lower()

    # --------------------------------------------------------
    # PDF
    # --------------------------------------------------------

    if file_name.endswith(".pdf"):

        try:

            from pypdf import PdfReader

            pdf_bytes = uploaded_file.read()

            reader = PdfReader(
                BytesIO(pdf_bytes)
            )

            text = ""

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

            return text.strip()

        except Exception as e:

            st.error(
                f"Could not read PDF: {str(e)}"
            )

            return ""


    # --------------------------------------------------------
    # DOCX
    # --------------------------------------------------------

    elif file_name.endswith(".docx"):

        try:

            from docx import Document

            doc_bytes = uploaded_file.read()

            document = Document(
                BytesIO(doc_bytes)
            )

            text = "\n".join(
                paragraph.text
                for paragraph in document.paragraphs
            )

            return text.strip()

        except Exception as e:

            st.error(
                f"Could not read DOCX: {str(e)}"
            )

            return ""


    else:

        st.error(
            "Please upload a PDF or DOCX resume."
        )

        return ""


def pipeline_step(
    number,
    title,
    description,
    status
):

    status_map = {

        "waiting": (
            "WAITING",
            "status-waiting"
        ),

        "running": (
            "● RUNNING",
            "status-running"
        ),

        "done": (
            "✓ DONE",
            "status-done"
        )
    }

    label, status_class = status_map[status]

    card_class = ""

    if status == "running":
        card_class = "active"

    elif status == "done":
        card_class = "done"


    st.markdown(
        f"""
        <div class="step-card {card_class}">

            <div class="step-header">

                <span class="step-num">
                    {number}
                </span>

                <span class="step-title">
                    {title}
                </span>

                <span class="step-status {status_class}">
                    {label}
                </span>

            </div>

            <div class="step-desc">
                {description}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-eyebrow">
            Multi-Agent Career Intelligence
        </div>

        <h1>
            Job Fit <span>Advisor</span>
        </h1>

        <p class="hero-sub">
            Upload your resume and provide a job opportunity.
            Specialized AI agents analyze the role, research
            the company, identify skill gaps and help you
            decide whether the opportunity is right for you.
        </p>

    </div>

    <div class="divider"></div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MAIN INPUT AREA
# ============================================================

col_input, col_pipeline = st.columns(
    [5, 4],
    gap="large"
)


# ============================================================
# LEFT - INPUT
# ============================================================

with col_input:

    st.markdown(
        '<div class="input-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-heading" style="margin-top:0;">'
        '📌 Job Opportunity'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Job URL
    # --------------------------------------------------------

    job_url = st.text_input(
        "Job URL",
        placeholder=(
            "https://company.com/careers/"
            "senior-ai-engineer"
        )
    )


    st.markdown(
        """
        <div style="
            text-align:center;
            color:#64748b;
            font-family:'DM Mono',monospace;
            font-size:0.7rem;
            margin:0.6rem 0;
        ">
            OR
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Job Description
    # --------------------------------------------------------

    job_description = st.text_area(
        "Job Description",
        placeholder=(
            "Paste the complete job description here..."
        ),
        height=220
    )


    st.markdown(
        '<div class="section-heading">'
        '👤 Your Resume'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Resume upload
    # --------------------------------------------------------

    resume_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"],
        help="Upload your resume in PDF or DOCX format."
    )


    if resume_file:

        st.caption(
            f"📄 {resume_file.name}"
        )


    # --------------------------------------------------------
    # Run button
    # --------------------------------------------------------

    run_button = st.button(
        "⚡ Analyze Job Fit",
        use_container_width=True
    )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Example
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="
            font-family:'DM Mono',monospace;
            font-size:0.7rem;
            color:#64748b;
            line-height:1.7;
        ">

        <b style="color:#38bdf8;">HOW IT WORKS</b><br><br>

        1. Provide a job URL or paste the JD<br>
        2. Upload your resume<br>
        3. AI analyzes both profiles<br>
        4. Company information is researched<br>
        5. Skill gaps are identified<br>
        6. AI recommends whether you should apply

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RIGHT - PIPELINE
# ============================================================

with col_pipeline:

    st.markdown(
        '<div class="section-heading" style="margin-top:0;">'
        'AI Pipeline'
        '</div>',
        unsafe_allow_html=True
    )


    results = st.session_state.results


    pipeline_step(
        "01",
        "Job Analyzer Agent",
        "Extracts requirements, skills and responsibilities",
        "done" if "job_analysis" in results
        else "waiting"
    )


    pipeline_step(
        "02",
        "Resume Analyzer Chain",
        "Builds a structured candidate profile",
        "done" if "candidate_profile" in results
        else "waiting"
    )


    pipeline_step(
        "03",
        "Company Research Agent",
        "Researches company and recent developments",
        "done" if "company_research" in results
        else "waiting"
    )


    pipeline_step(
        "04",
        "Skill Gap Analyzer",
        "Compares candidate skills against requirements",
        "done" if "skill_gap_analysis" in results
        else "waiting"
    )


    pipeline_step(
        "05",
        "Career Advisor",
        "Generates job-fit score and recommendation",
        "done" if "career_advice" in results
        else "waiting"
    )


    pipeline_step(
        "06",
        "Critic",
        "Reviews the recommendation for accuracy",
        "done" if "critic_feedback" in results
        else "waiting"
    )


# ============================================================
# RUN PIPELINE
# ============================================================

if run_button:

    # --------------------------------------------------------
    # Validate job input
    # --------------------------------------------------------

    if not job_url.strip() and not job_description.strip():

        st.error(
            "Please provide a Job URL or Job Description."
        )

        st.stop()


    # --------------------------------------------------------
    # Validate resume
    # --------------------------------------------------------

    if resume_file is None:

        st.error(
            "Please upload your resume."
        )

        st.stop()


    # --------------------------------------------------------
    # Extract resume
    # --------------------------------------------------------

    with st.spinner(
        "📄 Reading your resume..."
    ):

        resume_text = extract_resume_text(
            resume_file
        )


    if not resume_text:

        st.error(
            "Could not extract text from the resume."
        )

        st.stop()


    # --------------------------------------------------------
    # Prepare job input
    # --------------------------------------------------------

    if job_url.strip():

        job_input = job_url.strip()

    else:

        job_input = job_description.strip()


    # --------------------------------------------------------
    # Clear previous results
    # --------------------------------------------------------

    st.session_state.results = {}
    st.session_state.running = True


    # --------------------------------------------------------
    # Run pipeline
    # --------------------------------------------------------

    try:

        with st.status(
            "🚀 Running AI Job Fit Analysis...",
            expanded=True
        ) as status:

            st.write(
                "🤖 Running Job Analyzer..."
            )

            st.write(
                "👤 Analyzing candidate resume..."
            )

            st.write(
                "🏢 Researching the company..."
            )

            st.write(
                "🛠️ Comparing skills and identifying gaps..."
            )

            st.write(
                "🎯 Generating career recommendation..."
            )

            st.write(
                "🧐 Reviewing the recommendation..."
            )


            results = run_job_analysis_pipeline(
                job_description=job_input,
                resume_text=resume_text
            )


            st.session_state.results = results
            st.session_state.running = False


            status.update(
                label="✅ Job analysis completed!",
                state="complete",
                expanded=False
            )


    except Exception as e:

        st.session_state.running = False

        st.error(
            f"Pipeline failed: {str(e)}"
        )

        st.stop()


    st.rerun()


# ============================================================
# RESULTS
# ============================================================

results = st.session_state.results


if results:

    st.markdown(
        '<div class="divider"></div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="section-heading">'
        '🎯 Job Fit Analysis'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # CAREER ADVICE - MAIN RESULT
    # ========================================================

    if "career_advice" in results:

        st.markdown(
            """
            <div class="result-panel">

                <div class="result-title">
                    🎯 AI Career Recommendation
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            results["career_advice"]
        )


    # ========================================================
    # ANALYSIS TABS
    # ========================================================

    tabs = st.tabs([
        "📌 Job Analysis",
        "👤 Candidate",
        "🏢 Company",
        "🛠️ Skill Gap",
        "🧐 Critic"
    ])


    # --------------------------------------------------------
    # JOB ANALYSIS
    # --------------------------------------------------------

    with tabs[0]:

        if "job_analysis" in results:

            st.markdown(
                results["job_analysis"]
            )


    # --------------------------------------------------------
    # CANDIDATE
    # --------------------------------------------------------

    with tabs[1]:

        if "candidate_profile" in results:

            st.markdown(
                results["candidate_profile"]
            )


    # --------------------------------------------------------
    # COMPANY
    # --------------------------------------------------------

    with tabs[2]:

        if "company_research" in results:

            st.markdown(
                results["company_research"]
            )


    # --------------------------------------------------------
    # SKILL GAP
    # --------------------------------------------------------

    with tabs[3]:

        if "skill_gap_analysis" in results:

            st.markdown(
                results["skill_gap_analysis"]
            )


    # --------------------------------------------------------
    # CRITIC
    # --------------------------------------------------------

    with tabs[4]:

        if "critic_feedback" in results:

            st.markdown(
                results["critic_feedback"]
            )


    # ========================================================
    # DOWNLOAD
    # ========================================================

    st.markdown(
        '<div class="section-heading">'
        '📥 Export'
        '</div>',
        unsafe_allow_html=True
    )


    # Combine all outputs into markdown report

    report = f"""
# AI Job Fit & Career Analysis

## Job Analysis

{results.get("job_analysis", "")}


## Candidate Profile

{results.get("candidate_profile", "")}


## Company Research

{results.get("company_research", "")}


## Skill Gap Analysis

{results.get("skill_gap_analysis", "")}


## Career Recommendation

{results.get("career_advice", "")}


## Critic Feedback

{results.get("critic_feedback", "")}
"""


    st.download_button(
        label="⬇ Download Complete Analysis",
        data=report,
        file_name=(
            f"job_fit_analysis_{int(time.time())}.md"
        ),
        mime="text/markdown",
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="notice">
        Job Fit Advisor · Powered by LangChain · Gemini ·
        Multi-Agent AI
    </div>
    """,
    unsafe_allow_html=True
)