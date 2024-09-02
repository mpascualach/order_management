from app import db, create_app
from app.models.order import Order

def init_db()
  app = create_app()
  with app.app_context():
    db.create_all()

if __name__ == 'main':
  init_db()
  print("Database initialized.")