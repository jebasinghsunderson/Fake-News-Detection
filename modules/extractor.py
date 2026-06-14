from newspaper import Article, Config
import json
from google import genai
from .claim_url_extraction import google_news_search
from .claim_content_extraction import claim_content_points
from google.genai import types
from dotenv import load_dotenv
import os
load_dotenv()

def process_article(url) -> tuple[str, list[str]]:
    """
    Returns:
    (
        main_claim,
        [query1, query2, query3]
    )
    """
    # Extract article text

    config = Config()
    config.browser_user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )

    article = Article(url, config=config)
    article.download()
    article.parse()

    article_text = article.text[:5000]

    # Prompt

    prompt = f"""
You are a fact-checking search assistant.

Your task:

1. Identify the main factual claim in the article.
2. Generate EXACTLY 3 Google News search queries that can help verify the claim.

Search Query Rules:

- Queries should resemble real news headlines.
- Include important entities, organizations, places, dates and events.
- Do not copy entire sentences from the article.
- Do not include website navigation text.
- Do not include unrelated information.
- Do not ask questions.
- Each query must target a different angle:

    Query 1 → exact event
    Query 2 → organization/entity angle
    Query 3 → verification/security/context angle

- Each query should contain 5-15 words.
- Return ONLY valid JSON.

Output:

{{
    "main_claim": "...",
    "search_queries": [
        "...",
        "...",
        "..."
    ]
}}

Article:

{article_text}
"""
    # LLM
    client = genai.Client(api_key= os.getenv("GENAI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema = {
        "type": "object",
        "properties": {
            "main_claim": {
                "type": "string"
            },
            "search_queries": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": ["main_claim", "search_queries"]
    },
        temperature=0.2
        )
    )

    # Parse
    content = response.text
    result = json.loads(content)

    main_claim = result["main_claim"]
    queries = result["search_queries"]

    # -------------------------
    # Validate queries
    # -------------------------

    clean_queries = []

    for q in queries:
        q = q.strip()

        if len(q) < 10:
            continue

        if len(q.split()) < 3:
            continue

        clean_queries.append(q)

    queries = clean_queries
    amount = len(queries)
    point=0
    print("Main Claim:", main_claim)
    for query in queries:
        print(f"\nQUERY: {query}")

        try:
            results = google_news_search(query)
            point += claim_content_points(results[0]["url"], results[0]["title"], results[0]["published"], main_claim)

        except Exception as e:
            print(e)

    print("Average Points:", point/amount)
    
    return main_claim, queries
