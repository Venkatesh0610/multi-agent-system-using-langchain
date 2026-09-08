import re
import warnings
warnings.filterwarnings("ignore")

from agents.agent import (
    build_career_search_agent,
    build_job_reader_agent,
    writer_chain,
    critic_chain
)
from tools.tools import scrape_url

def run_career_research_generator(
    role: str,
    experience: str,
    skills: str,
    location: str
):
    """
    Generator function that yields status updates and partial results
    after each pipeline stage for real-time UI updates, with console logging for debugging.
    """
    print("\n" + "=" * 70)
    print("🚀 PIPELINE INITIATED")
    print(f"   Role       : {role}")
    print(f"   Experience : {experience}")
    print(f"   Skills     : {skills}")
    print(f"   Location   : {location}")
    print("=" * 70)

    state = {
        "role": role,
        "experience": experience,
        "skills": skills,
        "location": location
    }

    # ========================================================
    # STEP 1 - SEARCH AGENT
    # ========================================================
    print("\n[DEBUG] STEP 1/4: Launching Search Agent...")
    yield {"step": 1, "status": "running", "msg": "🔎 Search Agent is querying job market trends..."}
    
    search_agent = build_career_search_agent()
    search_query = f"""
    Find recent and reliable information about:
    Job Role: {role}
    Experience: {experience}
    Skills: {skills}
    Location: {location}

    Search for:
    - Current job opportunities
    - Required technical skills
    - Required experience
    - Common job responsibilities
    - Technologies used
    - Industry trends
    - Relevant companies

    IMPORTANT: Always include the direct HTTP/HTTPS source URLs as explicit links in your response.
    You are strictly allowed to execute AT MOST ONE web search before providing your final answer.
    """

    print("[DEBUG] STEP 1/4: Invoking Search Agent API call...")
    search_result = search_agent.invoke({"messages": [("user", search_query)]})
    print(search_result)
    print("========================================")
    state["search_results"] = search_result["messages"][-1].content

    print(f"[DEBUG] STEP 1/4: Search Agent Completed. Output length: {len(state['search_results'])} characters.")
    print(f"[DEBUG] STEP 1/4 Output Preview:\n{state['search_results']}...\n")
    yield {"step": 1, "status": "complete", "msg": "✓ Search Agent completed research.", "data": state}

    # ========================================================
    # STEP 2 - JOB READER AGENT (AGENTIC SCRAPING)
    # ========================================================
    print("\n[DEBUG] STEP 2/4: Launching Job Reader Agent...")
    yield {"step": 2, "status": "running", "msg": "📖 Job Reader Agent is inspecting target resource..."}
    
    # 1. First priority: Check extracted_urls array populated from ToolMessages in Step 1
    # 2. Fallback: Parse state["search_results"] if extracted_urls is missing or empty
    urls = state.get("extracted_urls", [])
    if not urls and state.get("search_results"):
        raw_urls = re.findall(r'https?://[^\s<>"\'\`\)]+|www\.[^\s<>"\'\`\)]+', state["search_results"])
        urls = [u.rstrip(".,;:)]}") for u in raw_urls if u]

    if urls:
        target_url = urls[0].rstrip(".,;:)]}")
        print(f"[DEBUG] STEP 2/4: Target URL found -> {target_url}")
        
        # Instantiate and invoke the Job Reader Agent directly
        job_reader_agent = build_job_reader_agent()
        reader_prompt = f"Scrape and extract all relevant content from this page using scrape_url: {target_url}"
        
        print("[DEBUG] STEP 2/4: Invoking Job Reader Agent API call...")
        reader_result = job_reader_agent.invoke({"messages": [("user", reader_prompt)]})
        
        # Capture agent's final message output
        state["scraped_content"] = reader_result["messages"][-1].content
    else:
        print("[DEBUG] STEP 2/4: No URLs found across search output or execution trace. Skipping scrape.")
        state["scraped_content"] = "No external URL available to scrape. Using search results."

    print(f"[DEBUG] STEP 2/4: Reader Agent Completed. Content length: {len(state['scraped_content'])} characters.")
    print(f"[DEBUG] STEP 2/4 Output Preview:\n{state['scraped_content'][:300]}...\n")
    yield {"step": 2, "status": "complete", "msg": "✓ Extracted deep research content.", "data": state}

    # ========================================================
    # STEP 3 - WRITER
    # ========================================================
    print("\n[DEBUG] STEP 3/4: Launching Writer Chain...")
    yield {"step": 3, "status": "running", "msg": "✍️ Writer Agent is synthesizing the career report..."}
    
    research_combined = f"""
    SEARCH RESULTS:
    {state['search_results']}

    DETAILED JOB INFORMATION:
    {state['scraped_content']}
    """

    print("[DEBUG] STEP 3/4: Invoking Writer Chain LLM...")
    state["report"] = writer_chain.invoke({
        "role": role,
        "experience": experience,
        "skills": skills,
        "location": location,
        "research": research_combined
    })

    print(f"[DEBUG] STEP 3/4: Writer Completed. Report length: {len(state['report'])} characters.")
    yield {"step": 3, "status": "complete", "msg": "✓ Writer Agent drafted career report.", "data": state}

    # ========================================================
    # STEP 4 - CRITIC
    # ========================================================
    print("\n[DEBUG] STEP 4/4: Launching Critic Chain...")
    yield {"step": 4, "status": "running", "msg": "🧐 Critic Agent is auditing the final findings..."}
    
    print("[DEBUG] STEP 4/4: Invoking Critic Chain LLM...")
    state["feedback"] = critic_chain.invoke({"report": state["report"]})

    print(f"[DEBUG] STEP 4/4: Critic Completed. Feedback length: {len(state['feedback'])} characters.")
    print("=" * 70)
    print("✅ PIPELINE EXECUTION FINISHED SUCCESSFULLY")
    print("=" * 70 + "\n")
    
    yield {"step": 4, "status": "complete", "msg": "✓ Critic Agent finished quality review.", "data": state}