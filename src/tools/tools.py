from langchain.tools import tool
import requests
from dotenv import load_dotenv
import os
from tavily import TavilyClient
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
import re

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query:str) -> str:
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets."""

    results = tavily.search(query=query,max_result=5)

    output = []

    for r in results['results']:
        output.append(
        f"Title: {r['title']}\n URL:{r['url']}\n Data:{r['content'][:300]}\n"
        )

    return "\n-----\n".join(output)


@tool
def scrape_url(url: str) -> str:
    """Extract clean readable text from a webpage."""

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        text = trafilatura.extract(response.text)

        if not text:
            return "Could not extract meaningful content."

        return text[:5000]

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"