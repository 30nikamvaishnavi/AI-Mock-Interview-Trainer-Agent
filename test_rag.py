from vector_store import search_questions


result = search_questions(
    "Machine Learning Engineer"
)


for item in result:

    print("----------------")
    print(item)