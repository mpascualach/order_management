from flask import request, jsonify
from functools import wraps

def validate_order_id(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    data = request.json
    if not data or 'order_id' not in data:
      return jsonify({'error': 'Order ID is required'})
    try:
      order_id = int(data['order_id'])
      if order_id <= 0:
        raise ValueError
    except ValueError:
      return jsonify({'error': 'Invalid Order ID'}), 400
    return f(*args, **kwargs)
  return decorated_function