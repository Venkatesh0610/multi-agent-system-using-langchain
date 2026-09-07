import os
import requests
import trafilatura
from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles, URLs, and snippets."""
    results = tavily.search(query=query, max_results=3)

    output = []
    for r in results.get('results', []):
        output.append(
            f"Title: {r['title']}\nURL: {r['url']}\nData: {r['content'][:300]}\n"
        )

    return "\n-----\n".join(output)


@tool
def scrape_url(url: str) -> str:
    """Extract clean readable text from a webpage."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=8)
        response.raise_for_status()

        text = trafilatura.extract(response.text)

        if not text:
            return "Could not extract meaningful content from the page."

        # Truncate to 3000 chars to speed up downstream LLM token processing
        return text[:3000]

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"