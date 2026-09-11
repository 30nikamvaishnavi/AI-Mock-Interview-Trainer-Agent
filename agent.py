import os
import json
from dotenv import load_dotenv


from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import ModelInference
from rag_agent import retrieve_context


# =====================================
# LOAD ENV
# =====================================


load_dotenv()



IBM_API_KEY = os.getenv(
    "IBM_API_KEY"
)


IBM_PROJECT_ID = os.getenv(
    "IBM_PROJECT_ID"
)



if not IBM_API_KEY:

    raise ValueError(
        "IBM_API_KEY missing in .env"
    )


if not IBM_PROJECT_ID:

    raise ValueError(
        "IBM_PROJECT_ID missing in .env"
    )





# =====================================
# IBM GRANITE CONFIG
# =====================================


MODEL_ID = (

    "ibm/granite-4-h-small"

)





# =====================================
# CREATE MODEL
# =====================================


def get_model():


    model = ModelInference(


        model_id=MODEL_ID,


        params={

            "max_new_tokens":1200,

            "temperature":0.3

        },


        project_id=IBM_PROJECT_ID,


        credentials={

            "apikey":IBM_API_KEY,


            "url":

            "https://us-south.ml.cloud.ibm.com"

        }

    )


    return model






import json


# =====================================
# GENERATE INTERVIEW QUESTIONS
# =====================================

def generate_interview(
        role,
        profile,
        number,
        difficulty,
        answer_style
):

    try:

        model = get_model()


        # ==========================
        # RAG CONTEXT
        # ==========================

        knowledge = retrieve_context(role)



        # ==========================
        # PROFILE DATA
        # ==========================

        name = profile.get(
            "name",
            "Candidate"
        )

        skills = profile.get(
            "skills",
            []
        )

        projects = profile.get(
            "projects",
            []
        )


        # ==========================
        # PROMPT
        # ==========================

        prompt = f"""

You are an expert AI interviewer.

Create a personalized mock interview.

Candidate Information:

Name:
{name}

Skills:
{skills}

Projects:
{projects}


Target Role:
{role}


Difficulty:
{difficulty}


Answer Style:
{answer_style}


Knowledge Base:
{knowledge}


Generate exactly {number} questions.


Return ONLY JSON.

No markdown.
No explanation.

JSON FORMAT:

{{
"questions":[
    {{
        "question":"",
        "expected_answer":"",
        "evaluation_points":[
            "",
            ""
        ]
    }}
]
}}

"""


        # ==========================
        # MODEL RESPONSE
        # ==========================

        response = model.generate_text(
            prompt
        )


        if not response:

            return {
                "questions":[]
            }



        response = response.strip()



        # Remove markdown

        if "```json" in response:

            response = response.replace(
                "```json",
                ""
            )

            response = response.replace(
                "```",
                ""
            )


        elif "```" in response:

            response=response.replace(
                "```",
                ""
            )


        # Extract JSON

        start=response.find("{")

        end=response.rfind("}")+1


        if start == -1 or end == 0:

            return {
                "questions":[]
            }


        json_response=response[start:end]


        result=json.loads(
            json_response
        )


        return result



    except Exception as e:

        print(
            "Generate Interview Error:",
            e
        )

        return {
            "questions":[]
        }





# =====================================
# EVALUATE ANSWER
# =====================================


def evaluate_answer(
        question,
        candidate_answer
):

    try:

        model=get_model()



        prompt=f"""

You are an expert technical interview evaluator.


Question:

{question}



Candidate Answer:

{candidate_answer}



Evaluate the answer based on:

- Technical correctness
- Explanation quality
- Communication
- Completeness


Return ONLY JSON.


FORMAT:


{{
"score":0,

"technical_accuracy":0,

"communication":0,


"strengths":[
""
],


"missing_points":[
""
],


"improved_answer":"",

"feedback":""

}}


Score range: 0-10.

"""


        response=model.generate_text(
            prompt
        )


        if not response:

            return {
                "score":0,
                "feedback":"No evaluation generated"
            }



        response=response.strip()



        if "```json" in response:

            response=response.replace(
                "```json",
                ""
            )

            response=response.replace(
                "```",
                ""
            )


        start=response.find("{")

        end=response.rfind("}")+1



        if start!=-1:

            json_text=response[start:end]

            return json.loads(
                json_text
            )



        return {
            "feedback":response
        }



    except Exception as e:

        print(
            "Evaluation Error:",
            e
        )


        return {

            "score":0,

            "feedback":
            "Evaluation failed"

        }



# =====================================
# CHAT INTERVIEW TRAINER
# =====================================


def chat_with_agent(message, profile):


    context = retrieve_context(message)


    prompt=f"""

You are an AI Interview Trainer.


Candidate Profile:

Name:
{profile.get("name")}


Skills:
{profile.get("skills")}


Projects:
{profile.get("projects")}



Relevant Knowledge:

{context}



Candidate Request:

{message}



Give practical interview guidance.

"""


    model=get_model()


    response=model.generate_text(prompt)


    return response


# =====================================
# TEST
# =====================================


if __name__=="__main__":


    print(

        "IBM Granite Interview Agent Ready"

    )