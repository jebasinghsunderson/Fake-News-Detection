import requests
from bs4 import BeautifulSoup
from ollama import chat

url = "https://www.thehindu.com/news/national/karnataka/shivakumars-elevation-as-karnataka-cm-poses-existential-challenge-for-jds/article71036564.ece"

html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")
for tag in soup(["script", "style", "footer", "nav", "header", "aside"]):
    tag.decompose()

text = soup.get_text(" ", strip=True)


prompt = f"""
Extract:
1. Main claim
2. 3 unique Search query generted from the main claim 
(dont not return the search query as none or dont know)
Article:
{text}
"""


response = chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content":prompt
        }
    ]
)

print(response["message"]["content"])