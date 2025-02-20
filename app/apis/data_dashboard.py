import requests
from flask import jsonify
from http import HTTPStatus
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from app.config.constants import APP_CONFIG

# Load environment variables from .env file
load_dotenv()

def send_email(recipient_email, carrier_name):
    """
    Send email with carrier data using project44 SMTP server
    """
    try:
        # Get email password from environment variables
        email_password = os.getenv('EMAILPASSWORD')
        if not email_password:
            raise ValueError("Email password not found in environment variables")

        message = MIMEMultipart()
        message["Subject"] = f"Self onboarding at Project44 - {carrier_name}"
        message["From"] = "Project44 <upload@p44-fileserver.com>"
        message["Reply-To"] = "queries@project44.com"
        message["To"] = recipient_email

        # Create HTML email body
        html = f"""
        <html>
        <head>
            <style>
                a {{
                    color: #0066cc;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
        <p>Hello,<br><br>
        Here is the link attached for self onboarding information at project44: <a href="http://localhost:3003/" target="_blank">http://localhost:3003/</a><br><br>
        
        Thanks,<br>
        project44
        </p></body></html>
        """

        body_part = MIMEText(html, "html")
        message.attach(body_part)

        # Connect to SMTP server
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        
        # Use the email password from environment variables
        server.login("upload@p44-fileserver.com", email_password)
        
        # Send email
        server.sendmail(
            "upload@p44-fileserver.com",
            [recipient_email],
            message.as_string()
        )
        
        server.quit()
        return True

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

def search_carrier_and_send_email(carrier_name=None):
    """
    Function to call the external partners search API and optionally send email for specific carrier
    """
    try:
        # API endpoint
        url = "http://customer-partner-service.integration.project44.com/internal/v1/partners/search"
        
        # Headers
        headers = {
            'accept': '*/*',
            'X-Tenant-Id': APP_CONFIG["user"]["tenant_id"],
            'X-Tenant-Uuid': APP_CONFIG["user"]["tenant_uuid"],
            'X-User-Id': APP_CONFIG["user"]["user_id"],
            'Content-Type': 'application/json'
        }
        
        # Request body with default parameters
        payload = {
            "paginationParameters": {
                "pageSize": 20,
                "pageNumber": 1
            },
            "performanceTimeFrame": "LAST_3_MONTHS",
            "searchText": carrier_name if carrier_name else "",
            "sortParameters": [
                {
                    "fieldName": "TOTAL_CREATED_SHIPMENTS",
                    "direction": "DESC"
                }
            ],
            "connectionInsightCriteria": {}
        }

        # Make the API call
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        print(data)

        # If carrier_name is provided, find the specific carrier and send email
        if carrier_name:
            for carrier in data.get('results', []):
                if carrier['name'].lower() == carrier_name.lower():
                    # Extract email from carrier data
                    carrier_email = carrier.get('connectionInsights', [{}])[0].get('implementation', {}).get('partnerContact', {}).get('email')
                    
                    if carrier_email:
                        # Send email
                        email_sent = send_email(carrier_email, carrier_name)
                        if email_sent:
                            carrier['email_status'] = 'Email sent successfully'
                        else:
                            carrier['email_status'] = 'Failed to send email'
                    else:
                        carrier['email_status'] = 'No email found for carrier'
                    
                    return {'carrier_data': carrier}
            
            return {
                'error': f'Carrier with name {carrier_name} not found'
            }, HTTPStatus.NOT_FOUND

        return data

    except requests.exceptions.RequestException as e:
        return {
            'error': f'API request failed: {str(e)}'
        }, HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        return {
            'error': f'Internal server error: {str(e)}'
        }, HTTPStatus.INTERNAL_SERVER_ERROR