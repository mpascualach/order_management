from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from app.config import Config

def test_db_connection():
  try:
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

    with engine.connect() as connection:
      result = connection.execute("SELECT 1")
      print("Connection successful!")
      print(f"Result of SELECT 1: {result.fetchone()[0]}")
  
  except SQLAlchemyError as e:
    print(f"An error has occurred while connecting to the database")

if __name__ == "__main__":
  test_db_connection()