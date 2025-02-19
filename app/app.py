from flask import Flask, request, jsonify
from apis.data_dashboard import search_carrier_and_send_email
from http import HTTPStatus

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Data Dashboard API"

@app.route("/api/carrier/send-email", methods=['POST'])
def send_carrier_email():
    try:
        # Get carrier name from request body
        request_data = request.get_json()
        
        if not request_data or 'carrier_name' not in request_data:
            return jsonify({
                'error': 'carrier_name is required in request body'
            }), HTTPStatus.BAD_REQUEST
            
        carrier_name = request_data['carrier_name']
        
        # Example tenant values - you might want to move these to environment variables
        tenant_id = "1730790390858"
        tenant_uuid = "85fbe0ad-a6e0-4e03-bbae-2b2c7005c60b"
        user_id = "0"
        
        # Call search_partners with carrier name
        result = search_carrier_and_send_email(tenant_id, tenant_uuid, user_id, carrier_name)
        
        # If result is a tuple, it means there was an error
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
            
        return jsonify(result), HTTPStatus.OK
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to process request: {str(e)}'
        }), HTTPStatus.INTERNAL_SERVER_ERROR

if __name__ == '__main__':
    app.run(debug=True)