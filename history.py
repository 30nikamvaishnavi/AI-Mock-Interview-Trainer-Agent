import sqlite3
import json
import os
from datetime import datetime





# ======================================
# DATABASE
# ======================================


DB_FOLDER="interview_db"


os.makedirs(

    DB_FOLDER,

    exist_ok=True

)



DB_PATH=os.path.join(

    DB_FOLDER,

    "history.db"

)






# ======================================
# CONNECTION
# ======================================


def connect():


    return sqlite3.connect(

        DB_PATH

    )







# ======================================
# CREATE TABLE
# ======================================


def create_history_table():


    conn=connect()


    cursor=conn.cursor()



    cursor.execute(

    """

    CREATE TABLE IF NOT EXISTS interviews

    (

        id INTEGER PRIMARY KEY AUTOINCREMENT,


        candidate TEXT,


        role TEXT,


        profile TEXT,


        questions TEXT,


        answers TEXT,


        feedback TEXT,


        score TEXT,


        created_at TEXT


    )

    """

    )



    conn.commit()


    conn.close()







# ======================================
# SAVE INTERVIEW
# ======================================


def save_history(

        candidate,

        role,

        profile,

        questions,

        answers,

        feedback,

        score

):



    conn=connect()


    cursor=conn.cursor()



    cursor.execute(

    """

    INSERT INTO interviews

    (

    candidate,

    role,

    profile,

    questions,

    answers,

    feedback,

    score,

    created_at

    )



    VALUES (?,?,?,?,?,?,?,?)

    """,



    (

    candidate,

    role,

    json.dumps(profile),


    json.dumps(questions),


    json.dumps(answers),


    json.dumps(feedback),


    score,


    datetime.now().strftime(

        "%d-%m-%Y %H:%M"

    )


    )



    )



    conn.commit()


    conn.close()







# ======================================
# GET ALL HISTORY
# ======================================


def get_history():


    conn=connect()


    cursor=conn.cursor()



    cursor.execute(

    """

    SELECT *

    FROM interviews

    ORDER BY id DESC

    """

    )


    data=cursor.fetchall()


    conn.close()



    return data







# ======================================
# GET SINGLE INTERVIEW
# ======================================


def get_interview(interview_id):


    conn=connect()


    cursor=conn.cursor()



    cursor.execute(

    """

    SELECT *

    FROM interviews

    WHERE id=?

    """,

    (interview_id,)

    )



    data=cursor.fetchone()



    conn.close()



    return data






# ======================================
# DELETE HISTORY
# ======================================


def delete_history(interview_id):


    conn=connect()


    cursor=conn.cursor()



    cursor.execute(

    """

    DELETE FROM interviews

    WHERE id=?

    """,

    (interview_id,)

    )



    conn.commit()


    conn.close()







# ======================================
# UPDATE HISTORY
# ======================================


def update_feedback(

        interview_id,

        feedback

):


    conn=connect()


    cursor=conn.cursor()



    cursor.execute(

    """

    UPDATE interviews

    SET feedback=?

    WHERE id=?

    """,

    (

    json.dumps(feedback),

    interview_id

    )

    )



    conn.commit()


    conn.close()






# ======================================
# TEST
# ======================================


if __name__=="__main__":


    create_history_table()


    print(

        "History database created"

    )