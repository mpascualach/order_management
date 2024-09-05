import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
sys.path.append(project_root)

from app import create_app, db
from app.models.customer import Customer
# from app.models.order import Order
# from app.models.chat import Chat
# from app.models.message import Message

def reset_database():
  app = create_app()
  with app.app_context():
    db.drop_all()
    print("All tables dropped")

    db.create_all()
    print("All tables recreated.")

    test_customer = Customer(
      name="Test User",
      email="test.user@example.com",
      password="password",
      phone='1234567890',
      address='123 Test St, Test City, TS 12345'
    )
    db.session.add(test_customer)
    db.session.commit()
    print("Test customer created.")

    print("Database reset complete.")

if __name__ == '__main__':
  reset_database()