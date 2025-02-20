import requests
from flask import jsonify
from http import HTTPStatus
import os
from dotenv import load_dotenv
from config.constants import APP_CONFIG

load_dotenv()

data_feed_manager_base_url = "http://data-feed-manager.integration.project44.com/"

def create_connection():
    """
    Create a connection for a carrier using the data feed manager API
    """
    try:
        # API endpoint
        create_connection_url = data_feed_manager_base_url + "onramp/staged/connections"
        
        # Headers
        headers = {
            'accept': 'application/json',
            'X-User-Id': APP_CONFIG["user"]["user_id"],
            'Content-Type': 'application/json'
        }
        
        # Request body
        payload = {
            "configKey": {
                "mode": APP_CONFIG["connection"]["mode"],
                "service": APP_CONFIG["connection"]["service"],
                "interactionType": APP_CONFIG["connection"]["interaction_type"],
                "entityId": APP_CONFIG["connection"]["entity_id"]
            },
            "processorStrategy": APP_CONFIG["connection"]["connection_strategy"],
            "doCreateDefaultInteraction": True
        }

        # Make the API call
        response = requests.post(create_connection_url, headers=headers, json=payload)
        response.raise_for_status()
        
        # Save connectionId to APP_CONFIG
        response_data = response.json()
        if 'connectionId' in response_data:
            APP_CONFIG["connection"]["connection_id"] = response_data["connectionId"]
        
        return response_data

    except requests.exceptions.RequestException as e:
        return {
            'error': f'API request failed: {str(e)}'
        }, HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        return {
            'error': f'Internal server error: {str(e)}'
        }, HTTPStatus.INTERNAL_SERVER_ERROR

def update_interaction(response_body_template_value=None):
    """
    Update an interaction with new template values
    """
    try:
        # API endpoint
        update_interaction_url = data_feed_manager_base_url + f"onramp/staged/connections/{APP_CONFIG['connection']['connection_id']}/interactions/1"
        
        # Headers
        headers = {
            'accept': 'application/json',
            'X-User-Id': APP_CONFIG["user"]["user_id"],
            'Content-Type': 'application/json'
        }
        
        # Get current interaction metadata
        interaction_metadata = APP_CONFIG["interaction"]
        
        # Update template values if provided
        if response_body_template_value:
            interaction_metadata["metaData"]["responseBodyTemplate"]["dslTemplateValue"] = response_body_template_value
        

        # Make the API call
        response = requests.put(update_interaction_url, headers=headers, json=interaction_metadata)
        response.raise_for_status()
        print(response.json())
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            'error': f'API request failed: {str(e)}'
        }, HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        return {
            'error': f'Internal server error: {str(e)}'
        }, HTTPStatus.INTERNAL_SERVER_ERROR

def create_trial():
    """
    Create a trial for a connection using the data feed manager API
    """
    try:
        # API endpoint
        create_trial_url = data_feed_manager_base_url + f"onramp/staged/connections/{APP_CONFIG['connection']['connection_id']}/trials"
        
        # Headers
        headers = {
            'accept': 'application/json',
            'X-User-Id': APP_CONFIG["user"]["user_id"],
            'Content-Type': 'application/json'
        }
        
        # Request body from APP_CONFIG
        payload = {
            "description": APP_CONFIG["trials"]["description"],
            "displayName": APP_CONFIG["trials"]["displayName"],
            "interactions": APP_CONFIG["trials"]["interactions"]
        }

        # Make the API call
        response = requests.post(create_trial_url, headers=headers, json=payload)
        response.raise_for_status()
        
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            'error': f'API request failed: {str(e)}'
        }, HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        return {
            'error': f'Internal server error: {str(e)}'
        }, HTTPStatus.INTERNAL_SERVER_ERROR
    
def deploy_connection():
    return ""
