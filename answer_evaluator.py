import os

from dotenv import load_dotenv

from ibm_watsonx_ai.foundation_models import ModelInference



load_dotenv()



def evaluate_answer(question,answer):


    model=ModelInference(

    model_id="ibm/granite-4-h-small",


    credentials={

    "url":
    "https://us-south.ml.cloud.ibm.com",

    "apikey":
    os.getenv("IBM_API_KEY")

    },


    project_id=os.getenv("PROJECT_ID")

    )



    prompt=f"""

Evaluate this interview answer.


Question:

{question}



Candidate Answer:

{answer}



Give:


Score /10


Strengths


Weaknesses


Improvement Tips


Better Answer



"""



    result=model.chat(

    messages=[

    {

    "role":"user",

    "content":prompt

    }

    ]

    )


    return result["choices"][0]["message"]["content"]