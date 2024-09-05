from app import db
from datetime import datetime

class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
  item = db.Column(db.String(20), nullable=False)
  measurement = db.Column(db.String(20), nullable=False)
  order_date = db.Column(db.DateTime, default=datetime.now(),nullable=False)
  total_amount = db.Column(db.Float, nullable=False)
  currency = db.Column(db.String(3), nullable=False)
  status = db.Column(db.String(20), nullable=False)
  pdf_path = db.Column(db.String(255), nullable=True)

  def to_dict(self):
    return {
      'id': self.id,
      'customer_id': self.customer_id,
      'item': self.item,
      'measurement': self.measurement,
      'order_date': self.order_date,
      'status': self.status,
      'total_amount': self.total_amount,
    }