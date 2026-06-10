from modules.content_extraction import content_extraction
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_embeddings.openai import OpenAIEmbeddings

import os


def claim_content_points(url, title, publisher, main_claim) -> list[int]:
    '''
    Extracts the text from the articles and returns a list of points that can be used for claim verification.
    '''

    #Content extraction
    content = content_extraction(url)
    print("Extracted content length:", len(content))
    
    #Load the content to a document object
    docs = [Document(page_content=content)]
    print("docs object created successfully.")
    print(f"Number of documents before splitting: {len(docs)}", f"content length: {len(content)}" ,sep ="\n")
   
    # split the documents into chunks
    r_spliter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20 ,separators=["\n\n", "\n"," ", ""])
    print("Splitting documents...")
    split_docs = r_spliter.split_documents(docs)
    print(f"Chunks: {len(split_docs)}")
    print("First 4 chunk content:", [doc.page_content for doc in split_docs[:4]])

    # Embedding the chunks
    embeddings = OpenAIEmbeddings()
    embedded_docs = [embeddings.embed_query(doc.page_content) for doc in split_docs]
    print("Embeddings created successfully.")
    return []

if __name__ == "__main__":
    url = "https://www.thehindu.com/news/international/west-asia-conflict-iran-us-israel-war-strait-of-hormuz-live-updates-june-9-2026/article71079114.ece"
    title = "Russia-Ukraine war: Russia's Wagner mercenaries 'surrender' in Bakhmut"
    publisher = "BBC"
    main_claim = "Wagner mercenaries have surrendered in Bakhmut"
    print(claim_content_points(url, title, publisher, main_claim))