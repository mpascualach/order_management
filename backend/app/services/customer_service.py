from app.models.chat import Chat
from app import db

class CustomerService:
  @staticmethod
  def get_chats_for_customer(customer_id):
    try:
      chats = Chat.query.filter_by(customer_id=customer_id).order_by(Chat.timestamp).all()
      return [chat.to_dict() for chat in chats]
    except Exception as e:
      print(f"Error retrieving chats: {str(e)}")
      return None
    
  @staticmethod
  def delete_chat(chat_id, customer_id):
    try:
      chat = Chat.query.filter_by(id=chat_id, customer_id=customer_id.id).first()
      if chat:
        db.session.delete(chat)
        db.session.commit()
        return True
      return False
    except Exception as e:
      print(f"Error deleting chat: {str(e)}")
      db.session.rollback()
      return False