from app import create_app, db
from app.models.customer import Customer
from sqlalchemy.exc import SQLAlchemyError

def create_first_user():
  app = create_app(init_database=True)
  with app.app_context():
    try:
      existing_user = Customer.query.filter_by(email="first-user@example.com").first()
      if existing_user:
        print("User already exists.")
        return
      
      first_user = Customer(
        name="First User",
        email="first.user@example.com",
        password="password",
        phone="123456789",
        address="123 Fake St., Anytown, England",
        orders=[],
        chats=[]
      )

      db.session.add(first_user)
      db.session.commit()

      print("First user created successfully.")

      created_user = Customer.query.filter_by(email="first-user@example.com").first()
      if created_user:
        print(f"User verified: {created_user.name} (ID: {created_user.id})")
      else:
        print("Failed to verify user creation.")
        
    except SQLAlchemyError as e:
      db.session.rollback()
      print(f"An error occurred: {str(e)}")
    

if __name__ == "__main__":
  create_first_user()