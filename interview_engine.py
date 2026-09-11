def evaluate_answer(answer,question):


    score=0

    feedback=[]


    if len(answer)>100:
        score+=40
        feedback.append(
        "Good explanation"
        )

    else:
        feedback.append(
        "Explain with more details"
        )



    if "example" in answer.lower():

        score+=20

        feedback.append(
        "Good practical example"
        )



    if "project" in answer.lower():

        score+=20

        feedback.append(
        "Project understanding shown"
        )


    return {

    "score":score,

    "feedback":feedback,

    "suggestion":
    "Improve technical depth and add measurable results"

    }