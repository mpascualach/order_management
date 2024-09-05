from app.models.chat import Chat
from app import db
from app.models.customer import Customer
from app.models.order import Order
from app.models.message import Message
from sqlalchemy import desc, func

class CustomerService:
  @staticmethod
  def create_new_chat(customer_id):
    try:
      new_chat = Chat(customer_id=customer_id)
      db.session.add(new_chat)
      db.session.commit()
      return new_chat.id
    except Exception as e:
      print(f"Error creating chat: {str(e)}")
      db.session.rollback()
      return None
  
  @staticmethod
  def add_message(customer_id, chat_id, user_message, ai_response):
    try:
      chat = Chat.query.filter_by(id=chat_id, customer_id=customer_id).first()
      if not chat:
        return False
      
      if user_message:
        user_msg = Message(chat_id=chat_id, content=user_message, is_from_user=True)
        db.session.add(user_msg)

      ai_msg = Message(chat_id=chat_id, content=ai_response, is_from_user=False)
      db.session.add(ai_msg)

      db.session.commit()
      return True
    except Exception as e:
      print(f"Error adding message: {str(e)}")
      db.session.rollback()
      return False

  @staticmethod
  def get_chat_history(customer_id, chat_id):
    try:
      chat = Chat.query.filter_by(id=chat_id, customer_id=customer_id).first()
      if not chat:
        return None
      
      messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.timestamp).all()
      history = []
      for msg in messages:
        if msg.is_from_user:
          history.append({"user_message": msg.content})
        else:
          history.append({"ai_response": msg.content})
      return history
    except Exception as e:
      print(f"Error retrieving chat history: {str(e)}")
      return None
  
  @staticmethod
  def get_customer_context(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
      return None
    
    orders = Order.query.filter_by(customer_id=customer_id).all()

    context = f"Customer ID: {customer_id}\n"
    context += f"Customer Name: {customer.name}\n"
    context += f"Recent Orders:\n"
    for order in orders[:5]:
      context += f"Order ID: {order.id}, Order item: {order.item}, Order measurement: {order.measurement}, Order date: {order.order_date}, Status: {order.status}\n"

    return context

  @staticmethod
  def get_chats_for_customer(customer_id):
    print(f"Customer id: {customer_id}")
    try:
      chats = Chat.query.filter_by(customer_id=customer_id).all()

      chat_data = []

      for chat in chats:
        latest_message = Message.query.filter_by(chat_id=chat.id).order_by(Message.timestamp.desc()).first()

        if latest_message:
          chat_data.append({
            'chat': chat.to_dict(),
            'latest_message_timestamp': latest_message.timestamp
          })

        # Sort the chat_data list by the latest message timestamp
        chat_data.sort(key=lambda x: x['latest_message_timestamp'], reverse=True)
        
        # Return only the chat data, maintaining the sorted order
        return [item['chat'] for item in chat_data]
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