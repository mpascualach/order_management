from flask import Blueprint, Response
from app.services.order_service import OrderService

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/download-orders/<int:customer_id>')
def download_orders_csv(customer_id):
  csv_data = OrderService.get_orders_csv(customer_id)
  if csv_data:
    return Response(
      csv_data,
      mimetype="text/csv",
      headers={"Content-disposition": "attachment; filename=customer_orders.csv"}
    )
  else:
    return "No orders found for this customer", 404