from google import genai
from google.genai import types
import json
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()

def verify_claim(main_claim, contents, url):

    prompt = f"""
Claim:
{main_claim}

Content:
{contents}

Classify the claim using ONLY one of these labels:

- supports
- refutes
- insufficient_evidence
 
Rate the claim on a scale of 0 to 10. (based on the claim you made)

Definitions:
supports = content directly confirms the claim
refutes = content directly contradicts the claim
insufficient_evidence = content neither confirms nor contradicts

Return valid JSON only:

{{
  "score":"...",
  "verdict": "supports",
   "evidence": "..."
}}
"""
    client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema = {
            "type": "object",
            "properties": {
                "score": {
                    "type": "number"
                },
                "verdict": {
                    "type": "string",
                    "enum": [
                        "supports",
                        "refutes",
                        "insufficient_evidence"
                    ]
                },
                "evidence": {
                    "type": "string"
                },
                "justification": {
                    "type": "string"
                }
            },
            "required": [
                "verdict",
                "evidence",
                "justification"
            ]
        },
            temperature=0.1
        )
    )

    result = json.loads(response.text)

    verdict_scores = {
        "supports": 5,
        "refutes": -5,
        "insufficient_evidence": 0
    }

    st.write("Verdict:", result["verdict"])
    st.write("Evidence:", result["evidence"])
    st.write("Justification:", result["justification"])
    st.write("Evidence link:", url)

    return result["score"]