from agents.agent import (
    build_job_analyzer_agent,
    build_company_research_agent,
    resume_chain,
    skill_gap_chain,
    career_advisor_chain,
    critic_chain
)


def run_job_analysis_pipeline(
    job_description: str,
    resume_text: str
) -> dict:

    state = {}

    # =========================================================
    # STEP 1 - JOB ANALYZER
    # =========================================================

    print("\n" + "=" * 60)
    print("STEP 1 - Job Analyzer Agent")
    print("=" * 60)

    job_analyzer = build_job_analyzer_agent()

    job_result = job_analyzer.invoke({
        "messages": [
            (
                "user",
                f"""
Analyze the following job opportunity.

JOB INPUT:
{job_description}

Extract all important requirements and provide
a structured job analysis.
"""
            )
        ]
    })

    state["job_analysis"] = job_result["messages"][-1].content

    print("\nJOB ANALYSIS:\n")
    print(state["job_analysis"])


    # =========================================================
    # STEP 2 - RESUME ANALYZER
    # =========================================================

    print("\n" + "=" * 60)
    print("STEP 2 - Resume Analyzer")
    print("=" * 60)

    state["candidate_profile"] = resume_chain.invoke({"resume": resume_text})

    print("\nCANDIDATE PROFILE:\n")
    print(state["candidate_profile"])


    # =========================================================
    # STEP 3 - COMPANY RESEARCH
    # =========================================================

    print("\n" + "=" * 60)
    print("STEP 3 - Company Research Agent")
    print("=" * 60)

    company_agent = build_company_research_agent()

    company_result = company_agent.invoke({
        "messages": [
            (
                "user",
                f"""
Research the company associated with this job.

JOB ANALYSIS:
{state["job_analysis"]}

Find reliable information about:

- Company overview
- Products and services
- Industry
- Technology areas
- Recent developments
- AI / ML / GenAI initiatives
- Relevant information for a candidate

Include source URLs.
"""
            )
        ]
    })

    state["company_research"] = (
        company_result["messages"][-1].content
    )

    print("\nCOMPANY RESEARCH:\n")
    print(state["company_research"])


    # =========================================================
    # STEP 4 - SKILL GAP ANALYSIS
    # =========================================================

    print("\n" + "=" * 60)
    print("STEP 4 - Skill Gap Analyzer")
    print("=" * 60)

    state["skill_gap_analysis"] = skill_gap_chain.invoke({
        "job_analysis": state["job_analysis"],
        "candidate_profile": state["candidate_profile"]
    })

    print("\nSKILL GAP ANALYSIS:\n")
    print(state["skill_gap_analysis"])


    # =========================================================
    # STEP 5 - CAREER ADVISOR
    # =========================================================

    print("\n" + "=" * 60)
    print("STEP 5 - Career Advisor")
    print("=" * 60)

    state["career_advice"] = career_advisor_chain.invoke({
        "job_analysis": state["job_analysis"],
        "candidate_profile": state["candidate_profile"],
        "company_research": state["company_research"],
        "skill_gap": state["skill_gap_analysis"]
    })

    print("\nCAREER ADVICE:\n")
    print(state["career_advice"])


    # =========================================================
    # STEP 6 - CRITIC
    # =========================================================

    print("\n" + "=" * 60)
    print("STEP 6 - Critic")
    print("=" * 60)

    state["critic_feedback"] = critic_chain.invoke({
        "job_analysis": state["job_analysis"],
        "candidate_profile": state["candidate_profile"],
        "skill_gap": state["skill_gap_analysis"],
        "career_advice": state["career_advice"]
    })

    print("\nCRITIC FEEDBACK:\n")
    print(state["critic_feedback"])


    # =========================================================
    # RETURN FINAL STATE
    # =========================================================

    return state