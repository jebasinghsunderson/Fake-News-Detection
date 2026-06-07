import streamlit as st
from urllib.parse import urlparse
from modules.extractor import process_article

st.title("Credibility of News Articles", text_alignment="center")
st.write("This application evaluates the credibility of news articles using a machine learning model.")

link = st.text_input("Enter the URL of a news article:")
if link:
    parsed = urlparse(link)
    
    if parsed.scheme and parsed.netloc:
        st.success(f"Valid URL: {link}")
        msg = st.empty()
        msg.write("Processing the article...")
        main_claim, result = process_article(link)
        msg.write("Done!")
        st.write("Extracted Information:")
        st.write(f"Main Claim: {main_claim}")
        st.write(f"Search Queries: {result}")

    else:
        st.error("Please enter a valid URL")

