from src.dsl.dslMapping import DslMapping
from pydantic import BaseModel, Field
from typing import List, Optional
from anthropic import AnthropicVertex
import json
import os

mapping_prompt = """
"""

class VertexStructuredAgent:
    def __init__(self, project_id="hackathon-2025-450908", location="us-east5"):
        self.client = AnthropicVertex(
            region=location,
            project_id=project_id
        )
        
    @staticmethod
    def format_model_schema(model_class: type[BaseModel]) -> str:
        """Convert Pydantic model to a prompt-friendly schema description"""
        schema = model_class.model_json_schema()
        return json.dumps(schema, indent=2)

    def get_structured_response(self, 
                              user_input: str, 
                              response_model: type[BaseModel]) -> BaseModel:
        """Get a response from Claude that conforms to the given Pydantic model"""

        # Load example carrier files from directory
        carrier_examples = []
        carrier_input_path = "../carrier_input_data"
        
        for root, dirs, files in os.walk(carrier_input_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        carrier_examples.append(f.read())
                except Exception as e:
                    print(f"Error reading file {file_path}: {str(e)}")
        
        # Load DSL response body examples
        dsl_json_examples = []
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        dsl_response_body_path = os.path.join(script_dir, "..", "dsl_response_body")
        
        for root, dirs, files in os.walk(dsl_response_body_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        dsl_json_examples.append(f.read())
                except Exception as e:
                    print(f"Error reading file {file_path}: {str(e)}")

        connector_output_examples = []
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        connector_output_path = os.path.join(script_dir, "..", "connector_output_data")

        for root, dirs, files in os.walk(connector_output_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        connector_output_examples.append(f.read())
                except Exception as e:
                    print(f"Error reading file {file_path}: {str(e)}")

        sample_mapping_for_prompt = ""
        for index, dsl_json_example in enumerate(dsl_json_examples):
            sample_mapping_for_prompt += f"Example {index+1}:\n mapping - {connector_output_examples[index]}\n\n json output - {dsl_json_example}\n\n"
        
        prompt = f"""Please provide your response in JSON format that exactly matches this schema:
        
        {VertexStructuredAgent.format_model_schema(response_model)}
        
        The JSON must be valid and match all types and constraints. A few examples to show you how to do it:

        {sample_mapping_for_prompt}
        
        User input: {user_input}"""
        
        response = self.client.messages.create(
            max_tokens=4096,
            system="You are a helpful data mapping AI solution for the supply chain world",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="claude-3-5-sonnet-v2@20241022"
        )
        
        try:
            print(response.content[0].text)
            print("\n\n\n")
            # Extract JSON from response (handles cases where Claude might add explanatory text)
            json_str = self._extract_json(response.content[0].text)
            # Parse and validate against the model
            return response_model.model_validate_json(json_str)
        except Exception as e:
            raise ValueError(f"Failed to parse response into expected model: {str(e)}")
            
    def _extract_json(self, text: str) -> str:
        """Extract JSON object from text that might contain other content"""
        try:
            # Find JSON-like content between curly braces
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > 0:
                possible_json = text[start:end]
                # Validate it's actually JSON
                json.loads(possible_json)
                return possible_json
            raise ValueError("No JSON object found in response")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON in response")