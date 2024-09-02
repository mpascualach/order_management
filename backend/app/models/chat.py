from app import db

class Chat(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  customer_id = db.Column(db.Integer, nullable=False)
  created_at = db.Column(db.DateTime, nullable=False)
  messages = db.relationship('Message', backref='chat', lazy=True)