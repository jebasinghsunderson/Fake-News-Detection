from modules.content_extraction import content_extraction
from modules.verify_claim import verify_claim
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import os
import uuid

os.environ["HF_HUB_DISABLE_XET"] = "1"
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"

from langchain_chroma import Chroma

#Embedding model
model_name=HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

# Directory to store the chunks
persist_directory = 'docs/chroma/'
os.makedirs(persist_directory, exist_ok=True)

# ChromaDB
chroma_db = Chroma(
    collection_name="claim_verification",
    embedding_function=model_name,
    persist_directory=persist_directory
)

# Text splitter
r_spliter =RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            " ",
            ""
            ]
)
def claim_content_points(url, title, publisher, main_claim) -> list[int]:
    '''
    Extracts the text from the articles and returns a list of points that can be used for claim verification.
    '''
    print("Processing URL: ", url)
    
    #Extract the content
    url_content = content_extraction(url)
    content = url_content[0]
    print("Extracted content length:", len(content))
    url = url_content[1]
    #Load the content to a document object
    docs = [
        Document(
            page_content=content,
            metadata={
                "url": url,
                "title": title,
                "publisher": publisher
            }
        )
    ]

    print("docs object created successfully.")
    print(f"Number of documents before splitting: {len(docs)}", f"content length: {len(content)}" ,sep ="\n")
   
    # split the documents into chunks
    
    # for i, chunk in enumerate(split_docs):
    #     print(i, chunk.page_content)

    # Embedding the chunks
    
    print("Embeddings created successfully.")
    
    
    # Persisting the embedded chunks to ChromaDB
    print("Count after add:", chroma_db._collection.count())
    existing = chroma_db.get(
        where={"url": url},
        include=[]
    )
    
    if not existing["ids"]:

        print("Splitting documents...")
        
        split_docs = r_spliter.split_documents(docs)
        split_docs = [
            d for d in split_docs
            if len(d.page_content.strip()) > 100
        ]
        print(f"Chunks: {len(split_docs)}")
        #Adding chunks to chroma db
        chroma_db.add_documents(
            split_docs,
            ids=[str(uuid.uuid4()) for _ in split_docs]
        )

        print("Documents added to ChromaDB successfully.")
    

    #Search for similar chunks to the main claim  
    search_results = chroma_db.similarity_search(
        query=main_claim,
        k=2,
        filter={"url": url}
    )

    points = verify_claim(main_claim, search_results[0].page_content, url)
    print("Points:", points )
    return points
