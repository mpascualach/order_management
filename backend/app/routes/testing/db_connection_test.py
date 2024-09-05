from flask import Blueprint, jsonify
from app import db
from sqlalchemy import text
import traceback

db_test = Blueprint('db_test', __name__)

@db_test.route('/test-db-connection', methods=['GET'])
def test_db_connection():
  try:
    db.session.execute(text('SELECT 1'))
    return jsonify({"message": "Database connection successful!"}), 200
  except Exception as e:
    print(f"Database connection error: {str(e)}")
    print(traceback.format_exc())
    return jsonify({"error": "Database connection failed", "details": str(e)}), 500