from newspaper import Article
from ollama import chat
import json

from .claim_url_extraction import google_news_search
from .content_extraction import content_extraction
from .claim_content_extraction import claim_content_points

def process_article(url) -> tuple[str, list[str]]:
    """
    Returns:
    (
        main_claim,
        [query1, query2, query3]
    )
    """
    # Extract article text
    article_text =content_extraction(url)

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
   
    response = chat(
        model="llama3.2:1b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format={
            "type": "object",
            "properties": {
                "main_claim": {
                    "type": "string"
                },
                "search_queries": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "minItems": 3,
                    "maxItems": 3
                }
            },
            "required": [
                "main_claim",
                "search_queries"
            ]
        },
        options={
            "temperature": 0
        }
    )

    # Parse
    content = response["message"]["content"]

    #try:
    result = json.loads(content)
    # except Exception:
    #     print("RAW MODEL OUTPUT:")
    #     print(content)
    #     raise

    main_claim = result["main_claim"]

    queries = result["search_queries"][:3]

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


    for query in queries:
        print(f"\nQUERY: {query}")

        try:
            results = google_news_search(query)

            for r in results[:3]:
                print(r["title"])
                print(r["url"])
                print(r["published"])
                point = claim_content_points(r["url"], r["title"],r["published"], main_claim)
                print(point)

        except Exception as e:
            print(e)

    return main_claim, queries