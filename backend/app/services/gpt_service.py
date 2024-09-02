import openai
from app.config import Config

class GPTService:
  @staticmethod
  def generate_response(prompt):
    openai.api_key = Config.OPENAI_API_KEY
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      max_tokens=150,
      n=1,
      stop=None,
      temperature=0.5
    )
    return response.choices[0].text.strip()
  
  @staticmethod
  def format_order_status_prompt(order_data):
    prompt = f"Given the following order information:\n"
    prompt += f"Order ID: {order_data['id']}\n"
    prompt += f"Customer ID: {order_data['customer_id']}\n"
    prompt += f"Order Date: {order_data['order_date']}\n"
    prompt += f"Status: {order_data['status']}\n"
    prompt += f"Total Amount: ${order_data['total_amount']:.2f}\n\n"
    prompt += "Provide a concise summary of the order status in a friendly tone."
    return prompt