import chromadb
from chromadb.config import Settings
import PyPDF2

class ChromaDBService:
  client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_db"
  ))
  collection = client.get_or_create_collection("order_pdfs")

  @classmethod
  def store_pdf_content(cls, pdf_path, order_id):
    with open(pdf_path, "rb") as file:
      reader = PyPDF2.PdfReader(file)
      text = ""
      for page in reader.pages:
        text += page.extract_text()

    cls.collection.add(
      documents=[text],
      metadatas=[{"order_id": str(order_id), "file_path": pdf_path}],
      ids=[f"order_{order_id}"]
    )
  @classmethod
  def search_pdf_content(cls, query, n_results=5):
    results = cls.collection.query(
      query_texts=[query],
      n_results=n_results
    )
    return results