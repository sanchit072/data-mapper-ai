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
        # self.stage = "validated_mapping"
        self.stage = "initial_ask_for_scac"
        self.carrier_latest_message = ""
        self.complete_chat = []
        # self.carrier_data = "Load,PRO,BOL,SCAC,field_4,field_5,Time_Stamp,Location_City,Location_State,Delivered_Date,CUST_ID\n,119958687,,TXOK,44.8833,-93.1333,1/13/2021 9:45,EAGAN,MN,,REYROIL"
        self.carrier_data = ""
        self.scac = ""
        # self.suggested_mapping = """I\'ll help you map the data from your CSV to match the schema format. Based on the provided data and following the pattern from previous examples:\n\n{\n"carrierIdentifier": {\n"type": "SCAC",\n"value": "TXOK, taken from SCAC field"\n},\n"shipmentIdentifiers": [{\n"type": "ORDER",\n"value": "119958687, taken from Load field"\n}],\n"latitude": "44.8833, taken from field_4 field",\n"longitude": "-93.1333, taken from field_5 field",\n"utcTimestamp": "2021-01-13T09:45:00, taken from Time_Stamp field and formatted to ISO 8601",\n"customerId": "REYROIL, taken from CUST_ID field",\n"eventType": "POSITION",\n"shipmentStops": [{\n"address": {\n"city": "EAGAN, taken from Location_City field",\n"state": "MN, taken from Location_State field",\n"country": "US"\n}\n}]\n}\n\nNote:\n1. I\'ve mapped the Load number as an ORDER type identifier since it appears to be the primary shipment reference\n2. The timestamp has been converted to ISO 8601 format\n3. I\'ve defaulted the country to "US" based on the presence of a US state\n4. I\'ve set eventType to "POSITION" since this appears to be a location update\n5. I\'ve included the city and state information in the shipmentStops section\n6. The BOL field was empty in the input, so I didn\'t include it in the shipmentIdentifiers array'"""
        self.suggested_mapping = ""
        self.llm_caller = LLMCaller()
        self.dsl_llm_caller = VertexStructuredAgent()

        
        # self.complete_chat.extend([{'role': 'system', 'stage': 'initial_ask_for_scac', 'content': "Hello! I'm here to help you set up an SFTP connection for sharing shipment status updates. Could you please provide your SCAC (Standard Carrier Alpha Code)? This will help us properly identify your organization in our system."}, {'role': 'carrier', 'stage': 'initial_ask_for_scac', 'content': 'ABTE'}])
        # self.complete_chat.extend([{'role': 'system', 'stage': 'received_scac_from_carrier', 'content': "Hello! I hope you're having a good day. I understand you'll be sharing shipment status updates with us via SFTP connection. Before we proceed with setting up the SFTP server, I would need your permission and confirmation to create the SFTP server for establishing this connection. \n\nCould you please confirm if we can go ahead with creating the SFTP server for this purpose? Once confirmed, we can proceed with the technical setup and share the necessary credentials and connection details with you.\n\nWould you also like to know any specific details about the SFTP server setup or have any particular requirements we should consider?"}, {'role': 'carrier', 'stage': 'received_scac_from_carrier', 'content': 'Yes looks good'}])
        # self.complete_chat.extend([{'role': 'system', 'stage': 'received_permission_for_sftp_server', 'content': '\n            These are your credentials for the SFTP connection:\n            - Username: abte_tl\n            - Password: 12342avr323\n            - Host: sftp://p44-fileserver.com\n            - Port: 2222\n\n            Please let us know if there are any issues\n'}, {'role': 'carrier', 'stage': 'received_permission_for_sftp_server', 'content': 'Yes looks good'}])
        # self.complete_chat.extend([{'role': 'system', 'stage': 'received_validation_for_credentials', 'content': '\n            ABTE, Could you please provide us with the CSV file containing the shipment status updates?\n            Additionally, please confirm:\n \n            1. Does the file include headers/column names?\n \n            2. What delimiter is used in the file (comma, semicolon, tab, etc.)? This information will help us process the data correctly.\n\n        '}, {'role': 'carrier', 'stage': 'received_validation_for_credentials', 'content': 'Load,PRO,BOL,SCAC,field_4,field_5,Time_Stamp,Location_City,Location_State,Delivered_Date,CUST_ID ,119958687,,TXOK,44.8833,-93.1333,1/13/2021 9:45,EAGAN,MN,,REYROIL'}])
        # self.complete_chat.extend([{'role': 'system', 'stage': 'received_carrier_file', 'content': 'I\'ll help you map the data from your CSV to match the schema format. Based on the provided data and following the pattern from previous examples:\n\n{\n"carrierIdentifier": {\n"type": "SCAC",\n"value": "TXOK, taken from SCAC field"\n},\n"shipmentIdentifiers": [{\n"type": "ORDER",\n"value": "119958687, taken from Load field"\n}],\n"latitude": "44.8833, taken from field_4 field",\n"longitude": "-93.1333, taken from field_5 field",\n"utcTimestamp": "2021-01-13T09:45:00, taken from Time_Stamp field and formatted to ISO 8601",\n"customerId": "REYROIL, taken from CUST_ID field",\n"eventType": "POSITION",\n"shipmentStops": [{\n"address": {\n"city": "EAGAN, taken from Location_City field",\n"state": "MN, taken from Location_State field",\n"country": "US"\n}\n}]\n}\n\nNote:\n1. I\'ve mapped the Load number as an ORDER type identifier since it appears to be the primary shipment reference\n2. The timestamp has been converted to ISO 8601 format\n3. I\'ve defaulted the country to "US" based on the presence of a US state\n4. I\'ve set eventType to "POSITION" since this appears to be a location update\n5. I\'ve included the city and state information in the shipmentStops section\n6. The BOL field was empty in the input, so I didn\'t include it in the shipmentIdentifiers array'}, {'role': 'carrier', 'stage': 'received_carrier_file', 'content': 'Yes this mapping is good. Please proceed'}])


    def update_complete_chat(self, role, message):
        self.complete_chat.append({"role": role, "stage": self.stage, "content": message})

    def determine_stage(self):
        self.update_complete_chat("carrier", self.carrier_latest_message)
        print(self.complete_chat)
        stage_determination_prompt = f"""
            You are a helpful assistant that determines the stage of the conversation.
            There are 2 users. One is the carrier and the other is the system. You are the system.
            We are trying to configure a data connection with the carrier. Initially, the carrier
            will send an empty message and you have to start with initial_ask_for_scac.

            Based on the chat history, determine the stage of the conversation accurately.

            The stages are:
            - initial_ask_for_scac
            - received_scac_from_carrier
            - received_permission_for_sftp_server
            - received_validation_for_credentials
            - received_carrier_file
            - generated_mapping
            - validated_mapping
            - generated_dsl
            - complete

            This is the latest chat messages: {self.complete_chat[-2:]}

            Return only the stage as plain text and nothing else. If stage is complete, return "complete".
        """
        # Make LLM call to determine the stage
        print("Stage determination prompt " + stage_determination_prompt)
        response = self.llm_caller.get_llm_response(stage_determination_prompt)
        print("Stage determination result " + response)
        self.stage = response
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
            You have to ask the carrier for permission to create the SFTP server for the connection.
"""
        # LLM call
        response = self.llm_caller.get_llm_response(prompt)
        self.update_complete_chat("system", response)
        create_connection(self.scac)
        return response

    def validate_credentials(self):
        prompt = """
            These are your credentials for the SFTP connection:
            - Username: abte_tl
            - Password: 12342avr323
            - Host: sftp://p44-fileserver.com
            - Port: 2222

            Please let us know if there are any issues
"""
        # LLM call
        # response = self.llm_caller.get_llm_response(prompt)
        self.update_complete_chat("system", prompt)
        return prompt
    
    def get_carrier_file(self):
        prompt = f"""
            {self.scac}, Could you please provide us with the CSV file containing the shipment status updates?
            Additionally, please confirm:\n 
            1. Does the file include headers/column names?\n 
            2. What delimiter is used in the file (comma, semicolon, tab, etc.)? This information will help us process the data correctly.\n
        """
        # LLM call
        # response = self.llm_caller.get_llm_response(prompt)
        self.update_complete_chat("system", prompt)
        return prompt

    def generate_mapping(self):
        self.carrier_data = self.carrier_latest_message
        try:
            with open('prompt_store/mapping_prompt.txt', 'r') as file:
                prompt_template = file.read()
                # Replace the placeholder directly instead of using format()
                prompt = prompt_template.replace("{carrier_data}", self.carrier_data)
            
            response = self.llm_caller.get_llm_response(prompt)
            self.suggested_mapping = response
            self.update_complete_chat("system", response)
            return response
        except Exception as e:
            print(f"Error in generate_mapping: {str(e)}")
            return "I apologize, but I encountered an error while generating the mapping. Could you please provide the file data again?"
    
    def validate_mapping(self):
        prompt = f"""
            You have to validate the mapping from the carrier.
            The mapping is: {self.suggested_mapping}

            Ask the carrier if the mapping is correct and if they have any changes to make.
        """
        response = self.llm_caller.get_llm_response(prompt)
        return response
    
    def generate_dsl(self):
        with open('prompt_store/dsl_mapping_prompt.txt', 'r') as file:
            prompt = file.read().format(carrier_data=self.carrier_data, suggested_mapping=self.suggested_mapping)
        # LLM call to generate DSL
        response = self.dsl_llm_caller.get_structured_response(prompt, DslMapping)
        print(response)
        update_interaction(response["dsl"])
        # Convert carrier data to base64 string for trial
        carrier_data_bytes = self.carrier_data.encode('utf-8')
        carrier_data_base64 = base64.b64encode(carrier_data_bytes).decode('utf-8')
        # create_trial(carrier_data_base64)
        self.stage = "complete"
        # connection_link = publish_connection()
        return f"Connection has been created - please activate and deploy and validate the mapping and upload data to the mentioned server for end-to-end testing."