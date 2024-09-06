# order_management

## Backend

### What's included:

1. Order Repository:

   - CRUD operations for orders using SQLAlchemy (Order model)
   - Methods to retrieve order status, create orders, update order status, and get order PDFs

2. Vectorized PDFs:

   - Integration with ChromaDB for storing and searching PDF content
   - PDF content is vectorized using OpenAI's text-embedding-ada-002 model

3. Routes:

   - Chatbot routes for querying order status and general order queries
   - Order routes for downloading customer orders as CSV

4. Services:

   - OrderService: Handles order-related operations
   - PDFService: Generates PDF files for orders
   - ChromaDBService: Manages vectorized PDF content and search functionality
   - GPTService: Integrates with GPT for generating responses (implementation not shown in the provided code)

5. Rate Limiting:
   - Implemented using Flask-Limiter to prevent abuse of the API

### What's missing:

1. LangChain Integration:

   - The current implementation doesn't use LangChain, which could potentially simplify and enhance the LLM integration

2. Refined Prompt Engineering:
   - While there's a basic prompt structure in place, more sophisticated prompt engineering techniques could be implemented to improve the quality of AI responses

## Frontend

### What's included:

- A minimalist chatbot interface (implementation details not provided in the given code snippets)

### What's missing:

1. Connection with a Deployed Backend:

   - The frontend code to connect with the backend API is not shown in the provided snippets

2. Refinement:
   - User interface for selecting pre-defined questions
   - Display of chat history
   - Table view for requested orders from a specific customer
   - Interface for downloading Excel/CSV files

You may access a deployed (provisional) version of the chatbot here: https://ordermanagement2.netlify.app/
