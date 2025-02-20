from flask import Flask, request, jsonify
from app.apis.data_dashboard import search_carrier_and_send_email
from app.apis.data_feed_manager import create_connection, update_interaction, create_trial, publish_connection
from http import HTTPStatus
from app.config.constants import APP_CONFIG
from flask_socketio import SocketIO
from flask_cors import CORS
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.app_flow import AppFlow

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True)
flow = AppFlow()

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
        result = create_connection(carrier_scac)
        
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

@app.route("/api/carrier/create-trial", methods=['POST'])
def create_carrier_trial():
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
            
        result = create_trial(request_data.get('mock_file_payload'))
        
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
            
        return jsonify(result), HTTPStatus.OK
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to process request: {str(e)}'
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route("/api/carrier/publish-connection", methods=['POST'])
def publish_carrier_connection():
    try:
        # Check if we have a connection_id
        if not APP_CONFIG["connection"]["connection_id"]:
            return jsonify({
                'error': 'No connection_id found. Please create a connection first.'
            }), HTTPStatus.BAD_REQUEST
            
        result = publish_connection()
        
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
            
        return jsonify(result), HTTPStatus.OK
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to process request: {str(e)}'
        }), HTTPStatus.INTERNAL_SERVER_ERROR

# @socketio.on('connect')
# def handle_connect():
#     socketio.emit('message', {
#         'message': chat_response(""),
#         'sender': 'agent'
#     })

@socketio.on('message')
def handle_message(message):
    print(f"Received: {message}")
    socketio.emit('message', {
        'message': chat_response(message),
        'sender': 'agent'
    })
    return f"Echo: {message}"

def chat_response(carrier_latest_message):
    flow.carrier_latest_message = carrier_latest_message
    return flow.generate_dsl()
    match flow.determine_stage():
        case "initial_ask_for_scac":
            return flow.greet_carrier()
        case "received_scac_from_carrier":
            return flow.ask_permission_for_sftp_server()
        case "received_permission_for_sftp_server":
            return flow.validate_credentials()
        case "received_validation_for_credentials":
            return flow.get_carrier_file()
        case "received_carrier_file":
            return flow.generate_mapping()
        case "generated_mapping":
            return flow.validate_mapping()
        case "validated_mapping":
            return flow.generate_dsl()
        case "generated_dsl":
            return flow.generate_dsl()
        case "complete":
            return "Chat is now closed. Thank you."