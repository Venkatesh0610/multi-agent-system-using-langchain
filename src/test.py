# from tools.tools import web_search,scrape_url
# from rich import print
# # result = web_search("tell me the latest news on india cricket schedule?")
# # result = scrape_url("https://www.ibm.com/think/topics/artificial-intelligence")
# result = scrape_url.invoke("https://www.cricbuzz.com/cricket-team/india/2/schedule")
# print(result)
import requests
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

print(response.json())