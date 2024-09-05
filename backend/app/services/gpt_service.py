import os
from openai import OpenAI
from app.config import Config

client = OpenAI(
  api_key=os.environ.get('OPENAI_API_KEY')
)

class GPTService:
  @staticmethod
  def generate_welcome_message(customer_context):
    system_message = f"You are a helpful assistant for BASF's Order Management system. Here's some context about the customer:\n{customer_context}"
    messages = [
      {"role": "system", "content": system_message},
      {"role": "user", "content": "Generate a friendly welcome message for the customer"}
    ]
    return GPTService.generate_response(messages)

  @staticmethod
  def generate_response(messages):
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=messages,
      max_tokens=150,
      n=1,
      stop=None,
      temperature=0.5
    )
    return response.choices[0].message.content.strip()
  
  @staticmethod
  def format_messages(message_history, new_message, customer_context):
    formatted_messages = [
      {"role": "system", "content": "You are a helpful assistant for BASF's Order Management system. Here's some context about the customer:\n{customer_context}"}
    ]
    for msg in message_history:
      formatted_messages.append({"role": "user", "content": msg['user_message']})
      formatted_messages.append({"role": "assistant", "content": msg['ai_response']})
    formatted_messages.append({"role": "user", "content": new_message})
    return formatted_messages
  
  @staticmethod
  def format_order_status_prompt(order_data):
    prompt = f"Given the following order information:\n"
    prompt += f"Order ID: {order_data['id']}\n"
    prompt += f"Customer ID: {order_data['customer_id']}\n"
    prompt += f"Order Date: {order_data['order_date']}\n"
    prompt += f"Status: {order_data['status']}\n"
    prompt += f"Total Amount: ${order_data['total_amount']:.2f}\n\n"
    prompt += "Provide a concise summary of the order status in a friendly tone. If you don't know the answer to a follow-up question, tell the user that you don't know but offer to connect them with a customer representative."
    return prompt