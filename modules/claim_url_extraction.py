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