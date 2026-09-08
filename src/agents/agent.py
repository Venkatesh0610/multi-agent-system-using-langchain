import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools.tools import web_search, scrape_url

load_dotenv()

# ============================================================
# OPEN-SOURCE MODEL INITIALIZATION (GROQ)
# ============================================================

llm = ChatGroq(
    model_name="openai/gpt-oss-120b",
    temperature=0
)

# ============================================================
# AGENT 1 - CAREER SEARCH AGENT
# ============================================================

def build_career_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )

# ============================================================
# AGENT 2 - JOB READER AGENT
# ============================================================

def build_job_reader_agent():
    system_prompt = (
        "You are an expert web scraping and reader agent. "
        "When given a URL, immediately call the `scrape_url` tool to extract "
        "and clean the page contents, then return the extracted information concisely."
    )
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt=system_prompt
    )

# ============================================================
# WRITER CHAIN
# ============================================================

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert AI career research analyst.

        Analyze the research collected by other agents
        and create a useful career intelligence report.

        Do not invent information.
        Use only the research provided.
        """
    ),
    (
        "human",
        """
        Create a career intelligence report for the following user.

        Target Role:
        {role}

        Experience:
        {experience}

        Current Skills:
        {skills}

        Preferred Location:
        {location}


        RESEARCH:

        {research}


        Structure the report as:

        1. Career Market Overview

        2. Most In-Demand Skills

        3. Common Job Responsibilities

        4. Technologies Employers Are Looking For

        5. Skill Gaps

        6. Recommended Learning Path

        7. Career Recommendations

        Keep the report factual, practical and easy to understand.
        """
    )
])

writer_chain = writer_prompt | llm | StrOutputParser()

# ============================================================
# CRITIC CHAIN
# ============================================================

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a strict and constructive career research critic.

        Review the report and identify:

        - Accuracy problems
        - Missing information
        - Unsupported claims
        - Weak recommendations
        - Irrelevant information
        - Structural problems
        """
    ),
    (
        "human",
        """
        Review the following career research report.

        REPORT:

        {report}


        Respond exactly in this format:

        Score: X/10

        Strengths:
        - ...
        - ...
        - ...

        Areas to Improve:
        - ...
        - ...
        - ...

        Missing Information:
        - ...
        - ...

        One Line Verdict:
        - ...
        """
    )
])

critic_chain = critic_prompt | llm | StrOutputParser()