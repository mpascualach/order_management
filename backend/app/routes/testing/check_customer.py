import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from app import create_app, db
from app.models.customer import Customer

def check_customer_by_email(email):
  app = create_app()
  with app.app_context():
    customer = Customer.query.filter_by(email=email).first()
    if customer:
      print(f"Customer found: ID={customer.id}, Name={customer.name}")
    else:
      print("Customer not found")

if __name__ == "__main__":
  check_customer_by_email("test.user@example.com")