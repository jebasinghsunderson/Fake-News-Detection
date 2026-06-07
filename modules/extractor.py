import requests
from bs4 import BeautifulSoup
from ollama import chat
import json
#url = "https://www.thehindu.com/news/national/karnataka/shivakumars-elevation-as-karnataka-cm-poses-existential-challenge-for-jds/article71036564.ece"
def process_article(url) -> tuple[str, list[str]]:
    '''
    Extracts questions from the given article url using beautiful soup and process questions using llama3
    RETURN FORMAT: (main claim, [search_query1, search_query2, search_query3])
    '''
    
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "footer", "nav", "header", "aside"]):
        tag.decompose()

    article_text = soup.get_text(" ", strip=True)


    prompt = f"""
    
    Main claim is the most important claim in the article.
    Generate 3 unique search queries based on the main claim. Search queries are the queries that can be used to search for evidence to support the main claim.Search queries shouldn't be short sentence.(Also add punctuation to the search queries if needed)
    Return the format ONLY as a JSON object and ONLY 3 search queries.
    Format:
    {{
    "main_claim": "",
    "search_queries": [
        "",
        "",
        ""
    ]
    }}

    Article:
    {article_text}
    """
    response = chat(
        model="llama3.2:1b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    content = response["message"]["content"]

    result = json.loads(content)

    main_claim = result["main_claim"]
    queries = result["search_queries"]

    print(main_claim)
    for query in queries:
        print(query)

    return (main_claim, queries)