from langchain_huggingface import HuggingFaceEmbeddings


from langchain_chroma import Chroma




VECTOR_PATH="vector_db"





def get_retriever():



    embeddings=HuggingFaceEmbeddings(

        model_name=

        "sentence-transformers/all-MiniLM-L6-v2"

    )



    db=Chroma(

        persist_directory=VECTOR_PATH,

        embedding_function=embeddings

    )


    return db.as_retriever(

        search_kwargs={

            "k":5

        }

    )








def retrieve_context(query):


    retriever=get_retriever()



    docs=retriever.invoke(

        query

    )



    context=""



    for doc in docs:


        context += doc.page_content+"\n\n"



    return context