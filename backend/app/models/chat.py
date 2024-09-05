from app import db
from datetime import datetime

class Chat(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now())
  messages = db.relationship('Message', backref='chat', lazy=True)