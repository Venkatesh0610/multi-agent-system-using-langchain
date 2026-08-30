import sys
import os
from pathlib import Path

# ---------------------------------------------------------
# Fix module import paths
# ---------------------------------------------------------

SRC_DIR = Path(__file__).resolve().parent.parent

if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))


# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools.tools import web_search, scrape_url


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

load_dotenv()


# =========================================================
# LLM
# =========================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0.1,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    transport="rest"
)


# =========================================================
# 1. JOB ANALYZER AGENT
# =========================================================

def build_job_analyzer_agent():

    return create_agent(
        model=llm,
        tools=[scrape_url],

        system_prompt="""
You are an expert Job Description Analyst.

Your job is to analyze a job opportunity and extract
important information from the job description.

If the user provides a URL, use the scrape_url tool
to retrieve the job description.

Extract the following information:

1. Job Title
2. Company Name
3. Location
4. Required Years of Experience
5. Required Technical Skills
6. Preferred Technical Skills
7. Key Responsibilities
8. Education Requirements
9. Certifications
10. Cloud / DevOps Requirements
11. AI / ML / Generative AI Requirements
12. Important soft skills

Do not invent information.

Only include information that is present in the
job description or can be directly inferred.

Return a clear and structured job analysis.
"""
    )


# =========================================================
# 2. RESUME ANALYZER CHAIN
# =========================================================

resume_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        """
You are an expert Resume Analyzer.

Analyze the candidate's resume and create a structured
candidate profile.

Extract:

1. Total Years of Experience
2. Current / Recent Job Role
3. Technical Skills
4. Programming Languages
5. AI / ML Skills
6. Generative AI Skills
7. Cloud Technologies
8. Backend Technologies
9. Databases
10. DevOps / Deployment Skills
11. Major Projects
12. Education
13. Certifications
14. Domain / Industry Experience

Do not invent skills, experience or qualifications.

Only use information explicitly present in the resume.
"""
    ),

    (
        "human",
        """
Analyze the following candidate resume.

RESUME:
{resume}

Create a structured candidate profile.
"""
    )
])


resume_chain = resume_prompt | llm | StrOutputParser()


# =========================================================
# 3. COMPANY RESEARCH AGENT
# =========================================================

def build_company_research_agent():

    return create_agent(
        model=llm,
        tools=[web_search],

        system_prompt="""
You are an expert Company Research Agent.

Your responsibility is to research the company associated
with a job opportunity.

Use the web_search tool to find reliable information.

Research:

1. Company overview
2. Main products and services
3. Industry
4. Technology areas
5. Recent developments
6. AI / ML / Generative AI initiatives
7. Relevant information for a job candidate

Prefer reliable and recent sources.

Do not invent information.

Include the URLs of the sources used in your research.
"""
    )


# =========================================================
# 4. SKILL GAP ANALYZER CHAIN
# =========================================================

skill_gap_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        """
You are an expert Technical Skill Gap Analyst.

Your job is to compare a candidate's profile against
the requirements of a job.

Analyze:

1. Matching skills
2. Partial matches
3. Missing required skills
4. Missing preferred skills
5. Experience match
6. AI / ML / GenAI match
7. Cloud / DevOps match
8. Major candidate strengths
9. Major weaknesses

Categorize important skills as:

MATCH
PARTIAL MATCH
GAP

Important rules:

- Do not invent candidate skills.
- Do not assume experience that is not present.
- Give more importance to required skills than preferred skills.
- Consider equivalent technologies where reasonable.
"""
    ),

    (
        "human",
        """
Perform a detailed skill-gap analysis.

JOB REQUIREMENTS:
{job_analysis}

CANDIDATE PROFILE:
{candidate_profile}

Compare the candidate against the job requirements.

Provide a clear explanation of the matches,
partial matches and gaps.
"""
    )
])


skill_gap_chain = skill_gap_prompt | llm | StrOutputParser()


# =========================================================
# 5. CAREER ADVISOR CHAIN
# =========================================================

career_advisor_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        """
You are an experienced Technology Career Advisor.

Your responsibility is to evaluate whether a candidate
should apply for a particular job.

Use the provided job analysis, candidate profile,
company research and skill-gap analysis.

Your response must include:

1. AI-estimated Job Fit Score out of 100
2. Recommendation
3. Strongest matching skills
4. Major skill gaps
5. Experience assessment
6. Skills to prioritize
7. Resume improvement suggestions
8. Interview preparation topics
9. Expected interview questions
10. Final career advice

Use one of these recommendations:

- STRONGLY APPLY
- APPLY
- APPLY WITH PREPARATION
- LOW MATCH

Important:

The job-fit score is an AI-estimated assessment,
not an objective measurement.

Base the recommendation only on the information provided.

Do not invent candidate experience or company information.
"""
    ),

    (
        "human",
        """
Evaluate this job opportunity for the candidate.

========================
JOB ANALYSIS
========================

{job_analysis}


========================
CANDIDATE PROFILE
========================

{candidate_profile}


========================
COMPANY RESEARCH
========================

{company_research}


========================
SKILL GAP ANALYSIS
========================

{skill_gap}


Provide a detailed career recommendation.
"""
    )
])


career_advisor_chain = (
    career_advisor_prompt
    | llm
    | StrOutputParser()
)


# =========================================================
# 6. CRITIC CHAIN
# =========================================================

critic_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        """
You are a strict and constructive Career Analysis Critic.

Review the complete job-fit analysis.

Check whether:

1. Job requirements were correctly interpreted.
2. Candidate skills were correctly interpreted.
3. Skill gaps are reasonable.
4. The job-fit score is justified.
5. The recommendation is supported by the evidence.
6. There are unsupported assumptions.
7. Important requirements were missed.
8. Career recommendations are practical.
9. Interview preparation is relevant.

Respond in exactly this format:

Score: X/10

Strengths:
- ...
- ...
- ...

Issues:
- ...
- ...
- ...

Recommended Improvements:
- ...
- ...
- ...

Final Verdict:
...

Be honest, specific and constructive.
"""
    ),

    (
        "human",
        """
Review the following complete career analysis.

JOB ANALYSIS:
{job_analysis}

CANDIDATE PROFILE:
{candidate_profile}

SKILL GAP ANALYSIS:
{skill_gap}

CAREER ADVICE:
{career_advice}

Provide your critical evaluation.
"""
    )
])


critic_chain = critic_prompt | llm | StrOutputParser()