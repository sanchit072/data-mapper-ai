from app.apis.data_feed_manager import create_connection, create_trial, deploy_connection, update_interaction
from dsl.dslMapping import DslMapping
from dsl_llm_call import VertexStructuredAgent
from llm_call import LLMCaller


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
        self.stage = "initial"
        self.carrier_latest_message = ""
        self.complete_chat = []
        self.carrier_data = ""
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
            - initial
            - ask_permission_for_sftp_server
            - validate_credentials
            - get_carrier_file
            - generate_mapping
            - validate_mapping
            - generate_dsl
            - complete

            The current stage is: {current_stage}
            This is the complete chat history: {self.complete_chat}

            Return only the stage as plain text and nothing else.
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
        create_connection()
        return response
    
    def ask_permission_for_sftp_server(self):
        prompt = """
            You are a helpful assistant that greets the freight carrier who is going to establish an SFTP connection to share the shipment status updates.
            You have to ask the carrier for their SCAC permission to create the SFTP server for the connection.
"""
        # LLM call
        response = self.llm_caller.get_llm_response(prompt)
        self.update_complete_chat("system", response)
        return response

    def validate_credentials(self):
        prompt = """
            You have to ask the carrier if these credentials for the SFTP connection are acceptable:
            - Username: {username}
            - Password: {password}
            - Host: {host}
            - Port: {port}
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
    
    def generate_dsl(self):
        with open('prompt_store/dsl_mapping_prompt.txt', 'r') as file:
            prompt = file.read().format(carrier_data=self.carrier_data, suggested_mapping=self.suggested_mapping)
        # LLM call to generate DSL
        response = self.dsl_llm_caller.get_structured_response(prompt, DslMapping)
        update_interaction(response)
        create_trial()
        deploy_connection()
        return "Connection has been deployed - {connection_link} and activated. Please validate the mapping and upload data to the mentioned server for end-to-end testing."
        # Take the response and make the API calls
        # return the connection link to the carrier through the prompt
