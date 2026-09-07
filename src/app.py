import streamlit as st
import time
from pipeline.pipeline import run_career_research_generator
import warnings

# Ignore all Python warnings in terminal
warnings.filterwarnings("ignore")

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Career Research Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================================================================
# CUSTOM CSS - DARK BLUE & CYAN PALETTE
# =============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&family=Syne:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: radial-gradient(circle at 10% 10%, rgba(56, 189, 248, 0.12), transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(59, 130, 246, 0.12), transparent 40%),
                linear-gradient(135deg, #030712 0%, #0f172a 50%, #020617 100%);
    color: #f3f4f6;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    max-width: 1200px;
    padding-top: 35px;
    padding-bottom: 80px;
}

/* HERO SECTION */
.hero { text-align: center; padding: 30px 20px 25px; }

.hero-eyebrow {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 6px 16px;
    border: 1px solid rgba(56, 189, 248, 0.3);
    border-radius: 50px;
    background: rgba(56, 189, 248, 0.1);
    color: #38bdf8;
    margin-bottom: 16px;
}

.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(38px, 5vw, 60px);
    font-weight: 800;
    line-height: 1.1;
    margin: 0;
    letter-spacing: -1.5px;
    color: #f9fafb;
}

.hero h1 span { color: #38bdf8; }

.hero-sub {
    max-width: 720px;
    margin: 16px auto 0;
    font-size: 15px;
    line-height: 1.6;
    color: #bae6fd;
    opacity: 0.8;
}

/* UI CARDS */
.glass-card {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(12px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    margin-bottom: 20px;
}

label {
    color: #38bdf8 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}

/* INPUT OVERRIDES */
.stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
    background: rgba(3, 7, 18, 0.8) !important;
    border: 1px solid rgba(56, 189, 248, 0.25) !important;
    border-radius: 8px !important;
    color: #f9fafb !important;
}

/* BUTTON */
.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 10px;
    border: 1px solid rgba(56, 189, 248, 0.5);
    background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
    color: white;
    font-size: 15px;
    font-weight: 700;
    transition: all 0.2s ease;
    box-shadow: 0 4px 20px rgba(2, 132, 199, 0.35);
}

.stButton > button:hover {
    transform: translateY(-2px);
    border-color: rgba(186, 230, 253, 0.6);
    box-shadow: 0 6px 24px rgba(2, 132, 199, 0.55);
}

/* PIPELINE CARDS & DYNAMIC COLORING */
.pipeline-card {
    min-height: 160px;
    padding: 18px;
    border-radius: 14px;
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.08);
    transition: all 0.3s ease;
}

/* RUNNING STATE - AMBER/GOLD */
.pipeline-card.running {
    border-color: #f59e0b !important;
    background: rgba(245, 158, 11, 0.15) !important;
    box-shadow: 0 0 20px rgba(245, 158, 11, 0.3) !important;
}

/* COMPLETE STATE - CYAN/BLUE */
.pipeline-card.complete {
    border-color: #38bdf8 !important;
    background: rgba(14, 116, 144, 0.4) !important;
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.3) !important;
}

.pipeline-number {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #38bdf8;
    font-weight: 500;
}

.pipeline-name {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    margin: 4px 0;
    color: #f3f4f6;
}

.pipeline-status-badge {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    margin-top: 10px;
    padding: 4px 10px;
    border-radius: 6px;
    display: inline-block;
    font-weight: 600;
}

.badge-idle { background: rgba(255, 255, 255, 0.08); color: #9ca3af; }
.badge-running { background: rgba(245, 158, 11, 0.3); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.5); }
.badge-complete { background: rgba(56, 189, 248, 0.25); color: #7dd3fc; border: 1px solid rgba(56, 189, 248, 0.5); }

/* REPORT READABILITY */
.report-wrapper {
    background: rgba(3, 7, 18, 0.75);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 14px;
    padding: 28px;
    color: #f3f4f6;
    line-height: 1.7;
    font-size: 15px;
}

.report-wrapper h1, .report-wrapper h2, .report-wrapper h3 {
    color: #38bdf8 !important;
    font-family: 'Syne', sans-serif;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# HERO
# =============================================================================
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">LangChain · Groq / Gemini · Multi-Agent AI</div>
    <h1>Career <span>Intelligence Suite</span></h1>
    <p class="hero-sub">Autonomous multi-agent market research and career evaluation system.</p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# INPUT SECTION
# =============================================================================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

role_options = [
    "Generative AI Engineer", "LLM Solutions Architect", "Data Scientist", 
    "Machine Learning Engineer", "Backend Developer (Python/FastAPI)", 
    "DevOps / MLOps Engineer", "Full Stack Developer", "Other (Custom Input)"
]

exp_options = ["0-1 years (Junior)", "2-4 years (Mid-Level)", "5-8 years (Senior)", "8+ years (Lead/Principal)", "Other (Custom Input)"]
loc_options = ["Hyderabad, India", "Bengaluru, India", "Remote (Global)", "San Francisco, CA", "London, UK", "Other (Custom Input)"]

with col1:
    selected_role = st.selectbox("Target Role", role_options, index=0)
    role = st.text_input("Specify Role", placeholder="e.g. Quantum Computing Researcher") if selected_role == "Other (Custom Input)" else selected_role

    selected_exp = st.selectbox("Experience Level", exp_options, index=2)
    experience = st.text_input("Specify Experience", placeholder="e.g. 12 years") if selected_exp == "Other (Custom Input)" else selected_exp

with col2:
    selected_loc = st.selectbox("Preferred Location", loc_options, index=0)
    location = st.text_input("Specify Location", placeholder="e.g. Berlin, Germany") if selected_loc == "Other (Custom Input)" else selected_loc

    skills = st.text_area(
        "Current Skills",
        value="Python, LangChain, RAG, LLMs, FastAPI, Docker, GCP",
        height=100,
        key="skills"
    )

analyze_button = st.button("🚀 Run Career Intelligence Pipeline", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# PIPELINE STATUS TRACKER (DYNAMIC BLUE & GOLD UI)
# =============================================================================
if "step_states" not in st.session_state:
    st.session_state["step_states"] = {
        1: {"status": "idle", "msg": "Waiting..."},
        2: {"status": "idle", "msg": "Waiting..."},
        3: {"status": "idle", "msg": "Waiting..."},
        4: {"status": "idle", "msg": "Waiting..."}
    }

pipeline_meta = [
    (1, "🔎", "Search Agent", "Discovers market trends & postings"),
    (2, "📖", "Reader Agent", "Extracts deep page insights"),
    (3, "✍️", "Writer Agent", "Synthesizes intelligence report"),
    (4, "🧐", "Critic Agent", "Audits for precision & accuracy")
]

pipeline_placeholder = st.empty()

def render_pipeline_ui():
    cols = pipeline_placeholder.columns(4)
    for col, (step_num, icon, name, desc) in zip(cols, pipeline_meta):
        step_info = st.session_state["step_states"][step_num]
        status = step_info["status"]
        
        badge_class = f"badge-{status}"
        card_class = f"pipeline-card {status}"
        
        if status == "running":
            status_label = "⚡ RUNNING..."
        elif status == "complete":
            status_label = "✓ DONE"
        else:
            status_label = "IDLE"

        with col:
            st.markdown(f"""
            <div class="{card_class}">
                <div class="pipeline-number">STEP 0{step_num}</div>
                <div style="font-size: 22px; margin: 4px 0;">{icon}</div>
                <div class="pipeline-name">{name}</div>
                <div style="font-size:11px; color:#bae6fd; opacity:0.7;">{desc}</div>
                <div class="pipeline-status-badge {badge_class}">{status_label}</div>
            </div>
            """, unsafe_allow_html=True)

render_pipeline_ui()

# =============================================================================
# EXECUTE PIPELINE WITH REAL-TIME UPDATES
# =============================================================================
if analyze_button:
    if not role or not experience or not skills or not location:
        st.error("Please ensure all profile inputs are completed.")
    else:
        # Reset States
        for key in st.session_state["step_states"]:
            st.session_state["step_states"][key] = {"status": "idle", "msg": "Waiting..."}
        
        generator = run_career_research_generator(
            role=role, experience=experience, skills=skills, location=location
        )

        for update in generator:
            step_num = update["step"]
            st.session_state["step_states"][step_num]["status"] = update["status"]
            st.session_state["step_states"][step_num]["msg"] = update["msg"]
            
            # Refresh live status grid
            render_pipeline_ui()

            if update["status"] == "complete" and "data" in update:
                st.session_state["career_result"] = update["data"]

# =============================================================================
# RESULTS DISPLAY
# =============================================================================
if "career_result" in st.session_state:
    result = st.session_state["career_result"]
    
    st.markdown("---")
    st.markdown("### 🧠 Generated Intelligence Output")

    tab_report, tab_search, tab_reader, tab_critic = st.tabs([
        "✍️ Career Report", "🔎 Search Data", "📖 Scraped Content", "🧐 Critic Review"
    ])

    with tab_report:
        st.markdown('<div class="report-wrapper">', unsafe_allow_html=True)
        st.markdown(result.get("report", "No report generated."))
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_search:
        st.code(result.get("search_results", ""), language="text")

    with tab_reader:
        st.code(result.get("scraped_content", ""), language="text")

    with tab_critic:
        st.markdown('<div class="report-wrapper">', unsafe_allow_html=True)
        st.markdown(result.get("feedback", "No feedback available."))
        st.markdown('</div>', unsafe_allow_html=True)

    # DOWNLOAD BUTTON
    markdown_report = f"""# Career Intelligence Report
**Role:** {role}
**Experience:** {experience}
**Location:** {location}

## Report
{result.get('report', '')}

## Critic Review
{result.get('feedback', '')}
"""

    st.download_button(
        label="📥 Download Full Report (.md)",
        data=markdown_report,
        file_name=f"career_report_{role.replace(' ', '_').lower()}.md",
        mime="text/markdown",
        use_container_width=True
    )