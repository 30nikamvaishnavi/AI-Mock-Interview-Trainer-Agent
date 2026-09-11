from dotenv import load_dotenv
import os

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from ibm_watsonx_ai.foundation_models import ModelInference


load_dotenv()

api_key = os.getenv("IBM_API_KEY")


# Load candidate profile
with open("profile.txt", "r") as file:
    profile = file.read()


# Load embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Load vector database
db = Chroma(
    persist_directory="interview_db",
    embedding_function=embeddings
)


# User request
query = "Prepare AI Engineer interview questions for this candidate"


# Retrieve knowledge
docs = db.similarity_search(
    query,
    k=3
)


context = "\n\n".join(
    [doc.page_content for doc in docs]
)


# IBM Granite model

model = ModelInference(
    model_id="ibm/granite-4-h-small",
    params={
        "max_new_tokens": 700,
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

Candidate Profile:

{profile}


Use this interview knowledge:

{context}


Generate:

1. Technical interview questions
2. Project-based questions
3. HR questions
4. Expected answers
5. Improvement suggestions

Target role:
AI Engineer Fresher

"""


response = model.generate_text(prompt)

print(response)