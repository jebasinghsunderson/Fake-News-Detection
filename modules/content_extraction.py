from newspaper import Article, Config   
from playwright.sync_api import sync_playwright



def content_extraction(url) ->list[str,str] :
    ''''
    Extracts the main content from the given url and returns it as a string.
    '''
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500
        )
        context = browser.new_context(
            locale="en-IN",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            )
        )

        page = context.new_page()

        page.goto(url)
        page.wait_for_timeout(10000)
        print(page.title())
        print("final url: ", page.url)
        url = page.url
        browser.close()
    try:
        
        config = Config()
        config.browser_user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0 Safari/537.36"
        )
       
        article = Article(url, config=config)
        article.download()
        article.parse()

        print(f"Extracted content length: {len(article.text)}")
        return [article.text, url]
    
    except Exception as e:
        print(f"Error extracting content from {url}: {e}")
        return ""

