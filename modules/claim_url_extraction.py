# from .extractor import process_article
# import os

# newsdata.io API key: os.getenv("NEWS_API_KEY")
# format :  https://newsdata.io/api/1/latest?apikey=pub_b459818a0c364eb193feca066802e633&q=???
import feedparser
from urllib.parse import quote_plus

def google_news_search(query, limit=5) -> list[dict[str, str]]:
    '''
    Searches Google news for the given query and returns a list of results with title, url, and published date.
    '''
    rss_url = (
        f"https://news.google.com/rss/search?"
        f"q={quote_plus(query)}"
    )

    feed = feedparser.parse(rss_url)

    results = []
    for entry in feed.entries[:limit]:
        results.append({
            "title": entry.title,
            "url": entry.link,
            "published": entry.published
        })
    
    return results