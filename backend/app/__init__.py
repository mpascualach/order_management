from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from app.utils.error_handlers import register_error_handlers
from app.utils.logger import setup_logger
from app.utils.limiter import init_limiter

db = SQLAlchemy()

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  init_limiter(app)

  from app.routes.chatbot import chatbot
  from app.routes.health import health
  from app.routes.customer_routes import customer_bp
  from app.routes.order_routes import order_bp

  app.register_blueprint(chatbot, url_prefix='/api/chatbot')
  app.register_blueprint(health, url_prefix='/api')
  app.register_blueprint(customer_bp, url_prefix='/orders')
  app.register_blueprint(order_bp, url_prefix='/customers')

  register_error_handlers(app)
  setup_logger(app)

  return app