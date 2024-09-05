from app import db
from datetime import datetime

class Chat(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now())
  messages = db.relationship('Message', backref='chat', lazy=True)

  def to_dict(self):
    return {
      'id': self.id,
      'customer_id': self.customer_id,
      'created_at': self.created_at,
      'messages': [message.to_dict() for message in self.messages]
    }