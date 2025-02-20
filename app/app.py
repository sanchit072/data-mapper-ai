from flask import Flask, request, jsonify
from apis.data_dashboard import search_carrier_and_send_email
from apis.data_feed_manager import create_connection, update_interaction
from http import HTTPStatus
from config.constants import APP_CONFIG
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True)

@app.route("/")
def home():
    return "Welcome to Data Dashboard API"

@app.route("/api/carrier/send-email", methods=['POST'])
def send_carrier_email():
    try:
        request_data = request.get_json()
        
        if not request_data or 'carrier_name' not in request_data:
            return jsonify({
                'error': 'carrier_name is required in request body'
            }), HTTPStatus.BAD_REQUEST
            
        carrier_name = request_data['carrier_name']
        result = search_carrier_and_send_email(carrier_name)
        
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
            
        return jsonify(result), HTTPStatus.OK
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to process request: {str(e)}'
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route("/api/carrier/create-connection", methods=['POST'])
def create_carrier_connection():
    try:
        request_data = request.get_json()
        
        if not request_data or 'carrier_scac' not in request_data:
            return jsonify({
                'error': 'carrier_scac is required in request body'
            }), HTTPStatus.BAD_REQUEST
            
        carrier_scac = request_data['carrier_scac']
        APP_CONFIG["connection"]["entity_id"] = carrier_scac
        result = create_connection()
        
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
            
        return jsonify(result), HTTPStatus.OK
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to process request: {str(e)}'
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route("/api/carrier/update-interaction", methods=['POST'])
def update_carrier_interaction():
    try:
        # Get template values from request body
        request_data = request.get_json()
        
        if not request_data:
            return jsonify({
                'error': 'Request body is required'
            }), HTTPStatus.BAD_REQUEST
            
        # Check if we have a connection_id
        if not APP_CONFIG["connection"]["connection_id"]:
            return jsonify({
                'error': 'No connection_id found. Please create a connection first.'
            }), HTTPStatus.BAD_REQUEST
            
        response_body_template_value = request_data.get('response_body_template_value')
        
        if not response_body_template_value:
            return jsonify({
                'error': 'response_body_template_value is required'
            }), HTTPStatus.BAD_REQUEST
            
        result = update_interaction(response_body_template_value)
        
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
            
        return jsonify(result), HTTPStatus.OK
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to process request: {str(e)}'
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@socketio.on('message')
def handle_message(message):
    print(f"Received: {message}")
    socketio.emit('response', f"Echo: {message}")
    return f"Echo: {message}"