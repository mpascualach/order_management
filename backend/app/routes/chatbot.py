from flask import Blueprint, request, jsonify
from app.services.order_service import OrderService
from app.services.gpt_service import GPTService
from app.services.chroma_service import ChromaDBService
from app.utils.validators import validate_order_id #define validate_order_id
from app.utils.limiter import limiter
import json

from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
from langchain.chains import create_qa_with_sources_chain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
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

order_status_chain = LLMChain(llm=llm, prompt=order_status_template)
order_query_chain = create_qa_with_sources_chain(llm)

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
  
  response = order_status_chain.run(order_data=order_data_str)

  return jsonify({
    'order_data': order_data,
    'ai_response': response
  })

@chatbot.route('/order_query', methods=['POST'])
@limiter.limit("5 per minute")
def query_order():
  data = request.json
  query = data['query']
  order_id = data.get('order_id')

  docs = vectorstore.similarity_search(query)

  if order_id:
    docs = [doc for doc in docs if doc.metadata['order_id'] == str(order_id)]

  context = "\n".join([doc.page_content for doc in docs])

  response = order_query_chain.run(context=context, query=query)

  return jsonify({
    'query': query,
    'ai_response': response,
    'relevant_orders': [doc.metadata['order_id'] for doc in docs]
  })
  