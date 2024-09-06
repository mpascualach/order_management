from flask import Blueprint, request, jsonify
from app.services.order_service import OrderService
# from app.services.gpt_service import GPTService
# from app.services.chroma_service import ChromaDBService
from app.utils.validators import validate_order_id #define validate_order_id
from app.utils.limiter import limiter
import json

from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.chains import create_qa_with_sources_chain
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chat_models import ChatOpenAI

chatbot = Blueprint('chatbot', __name__)

# Initialise LangChain components
llm = ChatOpenAI(temperature=0.2)
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(embedding_function=embeddings)

# Structure prompt for providing order status
order_status_template = PromptTemplate(
  input_variables=["order_data"],
  template="Given the following order data: {order_data}\nProvide a summary of the order status."
)

# Structure prompt for providing order query
order_query_template = PromptTemplate(
  input_variables=["context", "query"],
  template="Given the following context about orders:\n{context}\n\nAnswer the following question: {query}"
)

order_analysis_template = PromptTemplate(
  input_variables=["query", "orders"],
  template="""
    Analyze the following user query about their orders:
    Query: {query}

    Here are the user's orders:
    {orders}

    Provide a brief and to-the-point response addressing the user's question.
    Focus only on the most relevant information.
    Limit your response to 2-3 sentences maximum.
    Follow your answer with a suggestion as to how you can help or, if there is no help in particular to follow up with, just offer your help.
  """
)

order_status_chain = LLMChain(llm=llm, prompt=order_status_template)
order_analysis_chain = LLMChain(llm=llm, prompt=order_analysis_template)

@chatbot.route('/order_status', methods=['POST'])
@limiter.limit("5 per minute")
def get_order_status():
  data = request.json
  order_id = data['order_id']

  if not validate_order_id(order_id):
    return jsonify({'error': 'Order ID is required'})
  
  order_data = OrderService.get_order_status(order_id)

  if not order_data:
    return jsonify({'error': 'Order not found'})
  
  order_data_str=json.dumps(order_data)
  print(f"Order data string: {order_data_str}")
  
  response = order_status_chain.run(order_data=order_data_str)
  print(f"Response: {response}")

  return jsonify({
    'order_data': order_data,
    'ai_response': response
  })

@chatbot.route('/order_query', methods=['POST'])
@limiter.limit("5 per minute")
def query_order():
  data = request.json
  query = data['query']
  user_id = data.get('user_id')

  # Fetch all current orders for the user
  current_orders = OrderService.get_user_orders()

  if not current_orders:
    return jsonify({'error': 'No orders found for this user'})
  
  orders_str = json.dumps(current_orders, indent=2)

  response = order_analysis_chain.run(query=query, orders=orders_str)

  return jsonify({
    'query': query,
    'ai_response': response,
    'orders_analyzed': len(current_orders)
  })
  