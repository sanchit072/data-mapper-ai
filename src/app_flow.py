import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import base64
from app.apis.data_feed_manager import create_connection, create_trial, update_interaction, publish_connection
from src.dsl.dslMapping import DslMapping
from src.dsl_llm_call import VertexStructuredAgent
from src.llm_call import LLMCaller


class AppFlow:
    # Possible stages:
    # initial
    # ask_permission_for_sftp_server
    # validate_credentials
    # get_carrier_file
    # generate_mapping
    # validate_mapping
    # generate_dsl
    # complete

    def __init__(self):
        self.stage = "initial_ask_for_scac"
        self.carrier_latest_message = ""
        self.complete_chat = []
        self.carrier_data = ""
        self.scac = ""
        self.suggested_mapping = ""
        self.llm_caller = LLMCaller()
        self.dsl_llm_caller = VertexStructuredAgent()

    def update_complete_chat(self, role, message):
        self.complete_chat.append({"role": role, "content": message})

    def determine_stage(self):
        self.update_complete_chat("carrier", self.carrier_latest_message)
        stage_determination_prompt = """
            You are a helpful assistant that determines the stage of the conversation.
            The stages are:
            - initial_ask_for_scac
            - received_scac
            - received_permission_for_sftp_server
            - received_validation_for_credentials
            - received_carrier_file
            - generated_mapping
            - validated_mapping
            - generated_dsl
            - complete

            The current stage is: {current_stage}
            This is the complete chat history: {self.complete_chat}

            Return only the stage as plain text and nothing else. If stage is complete, return "complete".
        """
        # Make LLM call to determine the stage
        self.stage = self.llm_caller.get_llm_response(stage_determination_prompt)
        return self.stage

    def greet_carrier(self):
        prompt = """
            You are a helpful assistant that greets the freight carrier who is going to establish an SFTP connection to share the shipment status updates.
            You have to ask the carrier for their SCAC.
"""
        # LLM call
        response = self.llm_caller.get_llm_response(prompt)
        self.update_complete_chat("system", response)
        return response
    
    def ask_permission_for_sftp_server(self):
        self.scac = self.carrier_latest_message
        prompt = """
            You are a helpful assistant that greets the freight carrier who is going to establish an SFTP connection to share the shipment status updates.
            You have to ask the carrier for their SCAC permission to create the SFTP server for the connection.
"""
        # LLM call
        response = self.llm_caller.get_llm_response(prompt)
        self.update_complete_chat("system", response)
        create_connection(self.scac)
        return response

    def validate_credentials(self):
        prompt = """
            You have to ask the carrier if these credentials for the SFTP connection are acceptable:
            - Username: abte_tl
            - Password: 12342avr323
            - Host: sftp://p44-fileserver.com
            - Port: 2222
"""
        # LLM call
        response = self.llm_caller.get_llm_response(prompt)
        self.update_complete_chat("system", response)
        return response
    
    def get_carrier_file(self):
        prompt = """
            You have to ask the carrier for the CSV file that contains the shipment status updates.
            Also ask the carrier if the file contains headers and what is the delimiter used in the file.
"""
        # LLM call
        response = self.llm_caller.get_llm_response(prompt)
        self.update_complete_chat("system", response)
        self.carrier_data = response
        return response

    def generate_mapping(self):
        with open('prompt_store/mapping_prompt.txt', 'r') as file:
            prompt = file.read().format(carrier_data=self.carrier_data)
        response = self.llm_caller.get_llm_response(prompt)
        self.suggested_mapping = response
        self.update_complete_chat("system", response)
        return response
    
    def validate_mapping(self):
        prompt = """
            You have to validate the mapping from the carrier.
            The mapping is: {suggested_mapping}

            Ask the carrier if the mapping is correct and if they have any changes to make.
        """
        response = self.llm_caller.get_llm_response(prompt)
        return response
    
    def generate_dsl(self):
        with open('prompt_store/dsl_mapping_prompt.txt', 'r') as file:
            prompt = file.read().format(carrier_data=self.carrier_data, suggested_mapping=self.suggested_mapping)
        # LLM call to generate DSL
        response = self.dsl_llm_caller.get_structured_response(prompt, DslMapping)
        update_interaction(response)
        # Convert carrier data to base64 string for trial
        carrier_data_bytes = self.carrier_data.encode('utf-8')
        carrier_data_base64 = base64.b64encode(carrier_data_bytes).decode('utf-8')
        create_trial(carrier_data_base64)
        self.stage = "complete"
        connection_link = publish_connection()
        return f"Connection has been deployed - {connection_link} and activated. Please validate the mapping and upload data to the mentioned server for end-to-end testing."