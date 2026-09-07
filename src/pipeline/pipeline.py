import re
import warnings
warnings.filterwarnings("ignore")

from agents.agent import (
    build_career_search_agent,
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
    """

    print("[DEBUG] STEP 1/4: Invoking Search Agent API call...")
    search_result = search_agent.invoke({"messages": [("user", search_query)]})
    state["search_results"] = search_result["messages"][-1].content

    print(f"[DEBUG] STEP 1/4: Search Agent Completed. Output length: {len(state['search_results'])} characters.")
    print(f"[DEBUG] STEP 1/4 Output Preview:\n{state['search_results'][:300]}...\n")
    yield {"step": 1, "status": "complete", "msg": "✓ Search Agent completed research.", "data": state}

    # ========================================================
    # STEP 2 - DIRECT SCRAPING (OPTIMIZED: NO AGENT REASONING LOOP)
    # ========================================================
    print("\n[DEBUG] STEP 2/4: Extracting and Scraping Top URL directly...")
    yield {"step": 2, "status": "running", "msg": "📖 Scraping key resource page..."}
    
    # Extract the first valid HTTP/HTTPS URL from search results using regex
    urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', state["search_results"])

    if urls:
        target_url = urls[0].rstrip(".)")
        print(f"[DEBUG] STEP 2/4: Target URL found -> {target_url}")
        
        # Invoke tool directly to avoid agent loop latency
        scraped_data = scrape_url.invoke({"url": target_url})
        state["scraped_content"] = scraped_data
    else:
        print("[DEBUG] STEP 2/4: No URLs found in search output. Skipping scrape.")
        state["scraped_content"] = "No external URL available to scrape. Using search results."

    print(f"[DEBUG] STEP 2/4: Scraping Completed. Content length: {len(state['scraped_content'])} characters.")
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