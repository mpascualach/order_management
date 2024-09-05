import os

db_user = os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD', 'newHills818')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'basf_order_management')

full_db = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

print(f"Openai API KEY: ", os.getenv('OPENAI_API_KEY'))

class Config:
  SQLALCHEMY_DATABASE_URI = full_db or 'postgresql://localhost/basf_chatbot'
  SQLALCHEMY_TRACK_MODIFICATIONS= False
  OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')