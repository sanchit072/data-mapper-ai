import vertexai
from vertexai.generative_models import GenerativeModel
import os

# TODO(developer): Update and un-comment below line
PROJECT_ID = "hackathon-2025-450908"
vertexai.init(project=PROJECT_ID, location="us-central1")
model = GenerativeModel("gemini-2.0-pro-exp-02-05")

# go from src/main to the root directory
os.chdir("..")
os.chdir("..")

with open("prompt_store/mapping_prompt.txt", "r") as file:
    prompt = file.read()

    response = model.generate_content(
        prompt
    )
    print(response.text)