import os


from langchain_community.document_loaders import TextLoader


from langchain_text_splitters import RecursiveCharacterTextSplitter


from langchain_huggingface import HuggingFaceEmbeddings


from langchain_chroma import Chroma





DATA_PATH="knowledge_base"


VECTOR_PATH="vector_db"





def create_vector_db():



    documents=[]



    for file in os.listdir(DATA_PATH):


        if file.endswith(".txt"):


            loader=TextLoader(

                os.path.join(

                    DATA_PATH,

                    file

                ),

                encoding="utf-8"

            )


            documents.extend(

                loader.load()

            )





    splitter=RecursiveCharacterTextSplitter(

        chunk_size=500,

        chunk_overlap=100

    )



    chunks=splitter.split_documents(

        documents

    )




    embeddings=HuggingFaceEmbeddings(

        model_name=

        "sentence-transformers/all-MiniLM-L6-v2"

    )




    db=Chroma.from_documents(

        chunks,

        embeddings,

        persist_directory=VECTOR_PATH

    )



    print(

        "Vector database created successfully"

    )





if __name__=="__main__":


    create_vector_db()