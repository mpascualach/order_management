from app import create_app
from app.config import Config

if __name__ == '__main__':
  # app = create_app(init_database=True)
  print(f"Initialising database: {Config.SQLALCHEMY_DATABASE_URI}")
  # print("Database initialization complete")