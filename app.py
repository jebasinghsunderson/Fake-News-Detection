import streamlit as st
from urllib.parse import urlparse

st.title("Credibility of News Articles", text_alignment="center")
st.write("This application evaluates the credibility of news articles using a machine learning model.")

link = st.text_input("Enter the URL of a news article:")
if link:
    parsed = urlparse(link)
    
    if parsed.scheme and parsed.netloc:
        st.success(f"Valid URL: {link}")
    else:
        st.error("Please enter a valid URL")