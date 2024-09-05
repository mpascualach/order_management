import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from app import create_app, db
from app.models.customer import Customer
from app.models.order import Order
from datetime import datetime

def add_order_to_first_customer(email):
  app = create_app()
  with app.app_context():
    user = Customer.query.filter_by(email=email).first()
    if not user:
      print("User not found.")
      return
    
    new_order = Order(
      customer_id=user.id,
      item="Sample Item",
      measurement="50mg",
      order_date=datetime.now(),
      total_amount=99.99,
      currency="USD",
      status="Pending"
    )

    db.session.add(new_order)
    db.session.commit()

    print(f"Order added for user: {user.name}")


if __name__ == '__main__':
  add_order_to_first_customer('test.user@example.com')