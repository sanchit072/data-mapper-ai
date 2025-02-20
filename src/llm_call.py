from anthropic import AnthropicVertex

class LLMCaller:
    def __init__(self, project_id="hackathon-2025-450908", location="us-east5"):
        self.client = AnthropicVertex(region=location, project_id=project_id)

    def get_llm_response(self, prompt: str) -> str:
        try:
            message = self.client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="claude-3-5-sonnet-v2@20241022",
            )
            print(message.model_dump_json(indent=2))
            return message.content[0].text
        except Exception as e:
            raise Exception(f"Failed to get LLM response: {str(e)}")
