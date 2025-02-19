from dsl.mapping import Mapping
from pydantic import BaseModel, Field
from typing import List, Optional
from anthropic import AnthropicVertex
import json

prompt = """
This is the carrier file that we have to map to the output format.

<record>
	<Load>
	</Load>
	<PRO>
		119958687
	</PRO>
	<BOL>
	</BOL>
	<SCAC>
		TXOK
	</SCAC>
	<field4>
		44.8833
	</field4>
	<field5>
		-93.1333
	</field5>
	<TimeStamp>
		1/13/2021 9:45
	</TimeStamp>
	<LocationCity>
		EAGAN
	</LocationCity>
	<LocationState>
		MN
	</LocationState>
	<DeliveredDate>
	</DeliveredDate>
	<CUSTID>
		REYROIL
	</CUSTID>
</record>

This is the JSON mapping.
{
	"latitude":"44.8833",
	"longitude":"-93.1333",
	"utcTimestamp":"2021/11/01T09:45:00",
	"customerId":"REYROIL",
	"carrierIdentifier":{
		"type":"SCAC",
		"value":"TXOK"
	},
	"shipmentIdentifiers":[{
		"type":"ORDER",
		"value":"119958687"
	},
	{
		"type":"BILL_OF_LADING",
		"value":""
	}
	]
}

Use my python models and generate the DSL output.
"""

def format_model_schema(model_class: type[BaseModel]) -> str:
    """Convert Pydantic model to a prompt-friendly schema description"""
    schema = model_class.model_json_schema()
    return json.dumps(schema, indent=2)

class VertexStructuredAgent:
    def __init__(self, location: str, project_id: str):
        self.client = AnthropicVertex(
            region=location,
            project_id=project_id
        )
        
    def get_structured_response(self, 
                              user_input: str, 
                              response_model: type[BaseModel]) -> BaseModel:
        """Get a response from Claude that conforms to the given Pydantic model"""
        
        prompt = f"""Please provide your response in JSON format that exactly matches this schema:
        
        {format_model_schema(response_model)}
        
        The JSON must be valid and match all types and constraints.
        
        User input: {user_input}"""
        
        response = self.client.messages.create(
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": prompt
            }],
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

# Example usage
agent = VertexStructuredAgent(
    location="us-east5",
    project_id="hackathon-2025-450908"
)

try:
    response = agent.get_structured_response(
        prompt,
        Mapping
    )
    print(response)
        
except ValueError as e:
    print(f"Error getting structured response: {e}")