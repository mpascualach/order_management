import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from app.utils.error_handlers import register_error_handlers
from app.utils.logger import setup_logger
from app.utils.limiter import init_limiter

db = SQLAlchemy()

def init_db(app):
  with app.app_context():
    from app.models.customer import Customer
    from app.models.order import Order
    from app.models.chat import Chat
    from app.models.message import Message
    db.create_all()
  print("Database tables created.")

def create_app(init_database=False):
  os.environ.clear()

  load_dotenv()
  
  app = Flask(__name__)
  CORS(app)
  app.config.from_object(Config)

  db.init_app(app)
  init_limiter(app)

  from app.routes.chatbot import chatbot
  from app.routes.testing.health import health
  from app.routes.customer_routes import customer_bp
  from app.routes.order_routes import order_bp
  from app.routes.test_routes import test_bp  # Add this line
  from app.routes.testing.db_connection_test import db_test

  app.register_blueprint(chatbot, url_prefix='/chatbot')
  app.register_blueprint(health, url_prefix='/')
  app.register_blueprint(customer_bp, url_prefix='/')
  app.register_blueprint(order_bp, url_prefix='/')
  app.register_blueprint(db_test, url_prefix='/')
  app.register_blueprint(test_bp, url_prefix='/test')

  register_error_handlers(app)
  setup_logger(app)

  if init_database:
    init_db(app)

  return app