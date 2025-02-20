class AppFlow:
    def __init__(self):
        self.stage = "initial"
        self.carrier_data = {}

    def greet_carrier(self):
        prompt = """
            You are a helpful assistant that greets the freight carrier who is going to establish an SFTP connection to share the shipment status updates.
            You have to ask the carrier for the permission to create the SFTP server for the connection.
"""
        return prompt, "initial"

    def validate_credentials(self):
        prompt = """
            You have to ask the carrier if these credentials for the SFTP connection are acceptable:
            - Username: {username}
            - Password: {password}
            - Host: {host}
            - Port: {port}
"""
        return prompt, "credentials"

    def get_carrier_file(self):
        prompt = """
            You have to ask the carrier for the CSV file that contains the shipment status updates.
            Also ask the carrier if the file contains headers and what is the delimiter used in the file.
"""
        return prompt, "file_request"

    def generate_mapping(self):
        prompt = """
            Based on the carrier's file format and specifications, suggest a mapping between their fields
            and our standardized fields. Ask for confirmation of the mapping.
"""
        return prompt, "mapping"
    
    def generate_dsl(self):
        # LLM call to generate DSL
        # Take the response and make the API calls
        # return the connection link to the carrier through the prompt

    def process_response(self, carrier_response, current_stage):
        # Update stage based on carrier response
        if current_stage == "initial" and self._is_permission_granted(carrier_response):
            self.stage = "credentials"
        elif current_stage == "credentials" and self._is_credentials_accepted(carrier_response):
            self.stage = "file_request"
        elif current_stage == "file_request" and self._is_file_info_provided(carrier_response):
            self.stage = "mapping"
            
        # Return the next prompt based on current stage
        if self.stage == "credentials":
            return self.validate_credentials()
        elif self.stage == "file_request":
            return self.get_carrier_file()
        elif self.stage == "mapping":
            return self.generate_mapping()
        
        return None, self.stage

    def _is_permission_granted(self, response):
        # LLM will analyze if carrier granted permission
        return True  # Placeholder

    def _is_credentials_accepted(self, response):
        # LLM will analyze if credentials were accepted
        return True  # Placeholder

    def _is_file_info_provided(self, response):
        # LLM will analyze if file information was provided
        return True  # Placeholder
