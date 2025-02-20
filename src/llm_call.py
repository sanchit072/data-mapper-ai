from anthropic import AnthropicVertex

class LLMCaller:
    def __init__(self, project_id="hackathon-2025-450908", location="europe-west1"):
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
            return message.content[0].text
        except Exception as e:
            print(f"Failed to get LLM response: {str(e)}")
            return ""
