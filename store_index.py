# Import functions from src.helper.py file
from src.helper import load_pdf_file, text_split, download_embeddings
from pinecone import Pinecone
from dotenv import load_dotenv
from langchain_openai import OpenAI
import os


extracted_data = load_pdf_file("data")
text_chunks=text_split(extracted_data)
embeddings=download_embeddings()

# Pre-requisite: create index in pinecone
load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("lucho715")
# Upsert documents
#vector_store = Pinecone.from_documents(documents=text_chunks, index_name="lucho715", embedding=embeddings)

