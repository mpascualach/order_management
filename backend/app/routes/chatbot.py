from flask import Blueprint, request, jsonify
from app.services.order_service import OrderService
from app.services.gpt_service import GPTService
from app.services.chroma_service import ChromaDBService
from app.utils.validators import validate_order_id #define validate_order_id
from app.utils.limiter import limiter

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

order_status_template = PromptTemplate(
  input_variables=["order_data"],
  template="Given the following order data: {order_data}\nProvide a summary of the order status."
)

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
  
  prompt = GPTService.format_order_status_prompt(order_data)
  response = GPTService.generate_response(prompt)

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

  chroma_results = ChromaDBService.search_pdf_content(query)

  if order_id:
    filtered_results = [r for r in chroma_results['metadatas'][0] if r['order_id'] == str(order_id)]
  else:
    filtered_results = chroma_results['metadatas'][0]

  context = "\n".join([f"Order {r['order_id']}: {chroma_results['documents'][0][i]}" for i, r in enumerate(filtered_results)])

  prompt = f"Given the following context about orders:\n{context}\n\nAnswer the following question: {query}"
  response = GPTService.generate_response(prompt)

  return jsonify({
    'query': query,
    'ai_response': response,
    'relevant_orders': [r['order_id'] for r in filtered_results]
  })
  