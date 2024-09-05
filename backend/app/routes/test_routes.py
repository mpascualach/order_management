from flask import Blueprint, jsonify
from app.services.gpt_service import GPTService

test_bp = Blueprint('test_bp', __name__)

@test_bp.route('/test-openai-connection', methods=['GET'])
def test_openai_connection():
  try:
    test_prompt = "Say 'Hello, OpenAI!' if you can hear me."
    response = GPTService.generate_response([{"role": "user", "content": test_prompt}])

    return jsonify({
      "status": "success",
      "message": "Successfully connected to OpenAI API",
      "response": response
    })
  except Exception as e:
    return jsonify({
      "status": "error",
      "message": f"Failed to connect to OpenAI API: {str(e)}"
    }), 500