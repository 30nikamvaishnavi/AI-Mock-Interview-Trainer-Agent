from agent import generate_interview


profile={

"name":"Vaishnavi",

"skills":[
"Python",
"Machine Learning",
"TensorFlow"
],

"projects":[
"Medical Image Diagnosis System using CNN"
]

}



result=generate_interview(

    profile,

    "AI Engineer",

    5,

    "Medium",

    "Detailed"

)


print(result)


for q in result:


    print("\nQUESTION:")
    print(
        q["question"]
    )


    print("\nANSWER:")
    print(
        q["expected_answer"]
    )