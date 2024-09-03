from flask import Blueprint, jsonify, request
from app.services.customer_service import CustomerService
from app.services.gpt_service import GPTService

customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route('/chats/<int:customer_id>/<int:chat_id>/messages', methods=['POST'])
def send_message(customer_id, chat_id):
  message_content = request.json.get('message')
  if not message_content:
    return "Message content is required", 400
  
  chat_history = CustomerService.get_chat_history(customer_id, chat_id)

  formatted_messages = GPTService.format_messages(chat_history, message_content)
  
  ai_response = GPTService.generate_response(formatted_messages)

  success = CustomerService.add_message(customer_id, chat_id, message_content, ai_response)

  if success:
    return jsonify({
      "customer_message": message_content,
      "ai_response": ai_response
    }), 201
  else:
    return "Failed to save messages or chat not found"

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