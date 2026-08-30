from tools.tools import web_search,scrape_url
from rich import print
# result = web_search("tell me the latest news on india cricket schedule?")
# result = scrape_url("https://www.ibm.com/think/topics/artificial-intelligence")
result = scrape_url.invoke("https://www.cricbuzz.com/cricket-team/india/2/schedule")
print(result)