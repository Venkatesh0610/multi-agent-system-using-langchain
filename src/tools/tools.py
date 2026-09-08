import os
import requests
import trafilatura
from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient
from bs4 import BeautifulSoup

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles, URLs, and snippets."""
    results = tavily.search(query=query, max_results=3)

    output = []
    for r in results.get('results', []):
        print(r['url'])
        output.append(
            f"Title: {r['title']}\nURL: {r['url']}\nData: {r['content'][:300]}\n"
        )

    return "\n-----\n".join(output)

@tool
def scrape_url(url: str) -> str:
    """Extract clean readable text from a webpage."""

    # 1. THE "FAKE IDENTITY" (USER-AGENT)
    # Websites often block computer programs/bots.
    # This header tricks the website into thinking a real person using Google Chrome on Windows is visiting.
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }

    try:
        # 2. VISITING THE WEBSITE
        # Send a request to open the webpage. Wait up to 8 seconds. If it takes longer, give up.
        response = requests.get(url, headers=headers, timeout=8)

        # Check if the page loaded successfully (e.g., error 404 means "Page Not Found").
        response.raise_for_status()

        # 3. PLAN A: THE SMART CLEANER (Trafilatura)
        # Trafilatura is a smart tool that automatically knows what is main content and what is an ad or menu.
        text = trafilatura.extract(response.text)

        # 4. PLAN B: THE BACKUP CLEANER (BeautifulSoup)
        # If Plan A fails and extracts nothing, we switch to Plan B.
        if not text:
            # Load the raw web code (HTML) into BeautifulSoup to manually inspect it.
            soup = BeautifulSoup(response.text, "html.parser")

            # Throw away useless clutter: code scripts, styles, header bars, footers, and menus.
            for element in soup(
                ["script", "style", "nav", "footer", "header", "noscript"]
            ):
                element.decompose()  # Delete these parts from the page structure

            # Grab whatever text is left over and join it together.
            text = " ".join(soup.stripped_strings)

        # 5. QUALITY CHECK
        # If no text was found, or if it's super short (less than 50 letters), it means scraping failed.
        if not text or len(text.strip()) < 50:
            return "Could not extract meaningful content from the page."

        # 6. CUTTING IT DOWN TO SIZE
        # Keep only the first 3,000 characters so the text isn't too long to read or process.
        return text[:3000]

    except Exception as e:
        # 7. SAFETY NET (ERROR HANDLING)
        # If the internet is down, the website blocks us, or the link is broken, show an error message instead of crashing.
        return f"Could not scrape URL: {str(e)}"