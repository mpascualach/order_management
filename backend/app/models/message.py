from app import db
from datetime import datetime

class Message(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
  content = db.Column(db.Text, nullable=False)
  timestamp = db.Column(db.DateTime, default=datetime.now())
  is_from_user = db.Column(db.Boolean, default=True)

  def to_dict(self):
    return {
      'id': self.id,
      'chat_id': self.chat_id,
      'content': self.content,
      'timestamp': self.timestamp,
      'is_from_user': self.is_from_user,
    }