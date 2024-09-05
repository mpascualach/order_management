from flask import Blueprint, jsonify

health = Blueprint('health', __name__)

@health.route('/health', methods=['GET'])
def health_check():
  return jsonify({'status': 'OK'}), 200