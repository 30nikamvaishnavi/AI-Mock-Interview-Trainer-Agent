from dotenv import load_dotenv
import os

from ibm_watsonx_ai.foundation_models import ModelInference


load_dotenv()

api_key = os.getenv("IBM_API_KEY")


# Read profile
with open("profile.txt", "r") as file:
    profile = file.read()


model = ModelInference(
    model_id="ibm/granite-4-h-small",
    params={
        "max_new_tokens": 500,
        "temperature": 0.7
    },
    credentials={
        "apikey": api_key,
        "url": "https://us-south.ml.cloud.ibm.com"
    },
    project_id="42eb43a2-2bbf-4b94-a112-39c75d7461ae"
)


prompt = f"""
You are an AI Interview Trainer Agent.

Analyze this candidate profile:

{profile}


Generate:

1. Technical interview questions
2. HR interview questions
3. Project-based questions
4. Expected answers
5. Improvement tips

Target role:
AI Engineer Fresher
"""


response = model.generate_text(prompt)

print(response)