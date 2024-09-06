import traceback
from flask import jsonify

def register_error_handlers(app):
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': str(error)}), 400
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({'error': 'Not Found', 'message': str(error)}), 404
  
  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({'error': 'Internal Server Error', 'message': str(error)}), 500
  
  @app.errorhandler(Exception)
  def handle_exception(e):
    tb = traceback.format_exc().splitlines()[-1]
    return jsonify(error=str(e), traceback=tb), 500