from app.models.order import Order
from app import db
from app.services.pdf_service import PDFService
# from app.services.chroma_service import ChromaDBService

import csv
from io import StringIO

class OrderService:
  @staticmethod
  def get_order_status(order_id):
    try:
      order = Order.query.get(order_id)
      if order:
        return order.to_dict()
      return None
    except Exception as e:
      print(f"Error retrieving order sattus: {str(e)}")
      return None
    
  @staticmethod
  def create_order(customer_id, item, measurement, status, total_amount):
    try:
      new_order = Order(
        customer_id=customer_id,
        item=item,
        measurement=measurement,
        status=status,
        total_amount=total_amount
      )
      db.session.add(new_order)
      db.session.flush()

      pdf_path = PDFService.generate_order_pdf(new_order)
      new_order.pdf_path = pdf_path

      db.session.commit()

      return new_order.to_dict()
    except Exception as e:
      print(f"Error creating order: {str(e)}")
      db.session.rollback()
      return None
    
  @staticmethod
  def update_order_status(order_id, new_status):
    try:
      order = Order.query.get(order_id)
      if order:
        order.status = new_status
        db.session.commit()
        return order.to_dict()
      return None
    except Exception as e:
      print(f"Error updating order status: {str(e)}")
      db.session.rollback()
      return None
    
  @staticmethod
  def get_order_pdf(order_id):
    try:
      order = Order.query.get(order_id)
      if order and order.pdf_path:
        return order.pdf_path
      return None
    except Exception as e:
      print(f"Error retrieving order PDF: {str(e)}")
      return None
    
  @staticmethod
  def get_orders_csv(customer_id):
    try:
      orders = Order.query.filter_by(customer_id=customer_id).all()
      if not orders:
        return None
      
      si = StringIO()
      cw = csv.writer(si)
      cw.writerow(['ID', 'Item', 'Measurement', 'Status', 'Total Amount'])
      for order in orders:
        cw.writerow([order.id, order.item, order.measurement, order.status, order.total_amount])

      return si.getvalue()
    except Exception as e:
      print(f"Error generating orders CSV: {str(e)}")
      return None
