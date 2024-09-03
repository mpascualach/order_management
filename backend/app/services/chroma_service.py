import chromadb
from chromadb.config import Settings
import PyPDF2
import openai
import os

class ChromaDBService:
  client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_db"
  ))
  collection = client.get_or_create_collection("order_pdfs")
  
  openai.api_key = os.getenv('OPENAI_API_KEY')

  @classmethod
  def get_embedding(cls, text):
    response = openai.Embedding.create(
      input=text,
      model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

  @classmethod
  def store_pdf_content(cls, pdf_path, order_id):
    with open(pdf_path, "rb") as file:
      reader = PyPDF2.PdfReader(file)
      text = ""
      for page in reader.pages:
        text += page.extract_text()
    
    vector = cls.get_embedding(text)

    cls.collection.add(
      documents=[text],
      metadatas=[{"order_id": str(order_id), "file_path": pdf_path}],
      ids=[f"Order_{order_id}"],
      embeddings=[vector]
    )

    cls.collection.add(
      documents=[text],
      metadatas=[{"order_id": str(order_id), "file_path": pdf_path}],
      ids=[f"order_{order_id}"],
      embeddings=[vector]
    )
  
  @classmethod
  def search_pdf_content(cls, query, n_results=5):
    query_vector = cls.get_embedding(query)
    results = cls.collection.query(
      query_embeddings=[query_vector],
      n_results=n_results
    )
    return results