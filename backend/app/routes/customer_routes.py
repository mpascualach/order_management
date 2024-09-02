from Flask import Blueprint, jsonify
from app.services.customer_service import CustomerService

customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route('/chats/<int:customer_id>')
def get_customer_chats(customer_id):
  chats = CustomerService.get_chats_for_customer(customer_id)
  if chats:
    return jsonify(chats)
  else:
    return "No chats found for this customer", 404
  
@customer_bp.route('/chats/<int:customer_id>/<int:chat_id>', methods=['DELETE'])
def delete_customer_chat(customer_id, chat_id):
  success = CustomerService.delete_chat(chat_id, customer_id)
  if success:
    return "Chat deleted successfully", 200
  else:
    return "Failed to delete chat or chat not found", 404