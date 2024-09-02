from app import db

class Customer(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20), nullable=False)
  email = db.Column(db.String(20), nullable=False)
  phone = db.Column(db.String(20), nullable=False)
  address = db.Column(db.String(20), nullable=False)
  orders = db.relationship('Order', backref='customer', lazy=True),
  chats = db.relationship('Chat', backref='customer', lazy=True),
