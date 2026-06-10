from .claim_url_extraction import google_news_search
from newspaper import Article
import requests

def content_extraction(url) ->str :
    ''''
    Extracts the main content from the given url and returns it as a string.
    '''

    response = requests.get(
        url,
        allow_redirects=True,
        timeout=10,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    print(response.url)

    try:
        article = Article(response.url)
        article.download()
        article.parse()
        print(f"Extracted content length: {len(article.text)}")
        return article.text
    except Exception as e:
        print(f"Error extracting content from {url}: {e}")
        return ""


    

