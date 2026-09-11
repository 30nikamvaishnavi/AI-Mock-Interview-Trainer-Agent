import streamlit as st
import json
import os
from voice import speech_to_text

from resume_parser import analyze_resume
from report_generator import create_report

from agent import (
    generate_interview,
    evaluate_answer,
    chat_with_agent
)


from history import (
    create_history_table,
    save_history,
    get_history,
    delete_history
)


from voice import speech_to_text





# =====================================
# PAGE CONFIG
# =====================================


st.set_page_config(

    page_title="AI Interview Trainer Agent",

    page_icon="🤖",

    layout="wide"

)





# =====================================
# DATABASE INIT
# =====================================


create_history_table()






# =====================================
# CSS THEME
# =====================================


st.markdown(

"""
<style>


.stApp{

background:

linear-gradient(

135deg,

#e3f2fd,

#fce4ec

);

}



.main-title{

font-size:45px;

font-weight:800;

text-align:center;

color:#1565c0;

}



.sub-title{

text-align:center;

font-size:20px;

color:#455a64;

}



.card{

background:white;

padding:25px;

border-radius:20px;

box-shadow:

0 5px 20px rgba(0,0,0,0.12);

margin-bottom:20px;

}



.question-box{

background:white;

padding:20px;

border-radius:15px;

border-left:8px solid #42a5f5;

}



.feedback{

background:#e8f5e9;

padding:20px;

border-radius:15px;

}



.stButton button{


background:

linear-gradient(

90deg,

#2196f3,

#9c27b0

);


color:white;

border-radius:15px;

font-weight:bold;


}



</style>

""",

unsafe_allow_html=True

)







# =====================================
# SESSION STATE
# =====================================


defaults={


"profile":{
    "name":"",
    "skills":[],
    "projects":[],
    "resume_text":""
},

"questions":[],

"current_question":0,

"answers":[],

"started":False,

"report":None,

"chat":[],

"voice_answer":"",

"role":"",

}


for key,value in defaults.items():


    if key not in st.session_state:


        st.session_state[key]=value







# =====================================
# SIDEBAR
# =====================================


with st.sidebar:


    st.markdown(

    """

    <h2 style="color:#1565c0">

    🤖 Interview Trainer

    </h2>

    """,

    unsafe_allow_html=True

    )



    page=st.radio(

        "Menu",

        [

            "🏠 Home",

            "📄 Resume",

            "💬 Chat Trainer",

            "🎤 Mock Interview",

            "📚 History"

        ]

    )









# =====================================
# HOME
# =====================================


if page=="🏠 Home":


    st.markdown(

    """

    <div class="main-title">

    🤖 AI Interview Trainer Agent

    </div>


    <div class="sub-title">

    IBM Granite + RAG + Resume Intelligence

    </div>


    """,

    unsafe_allow_html=True

    )



    st.write("")



    c1,c2,c3=st.columns(3)



    with c1:

        st.info(

        """

        📄 Resume Intelligence


        Extract:

        - Skills

        - Projects

        - Experience

        """

        )



    with c2:

        st.success(

        """

        🧠 IBM Granite


        Generates:

        - Technical questions

        - HR questions

        - Project questions

        """

        )



    with c3:

        st.warning(

        """

        🎤 Live Interview


        Supports:

        - Text

        - Voice

        - Evaluation

        """

        )
# =====================================
# 📄 RESUME PAGE
# =====================================


if page=="📄 Resume":
   # Initialize candidate profile
    if "profile" not in st.session_state:

        st.session_state.profile = {

            "name": "",

            "skills": [],

            "projects": [],

            "resume_text": ""

        }



    st.markdown(
    """
    <div class="main-title">

    📄 Resume Intelligence

    </div>


    <div class="sub-title">

    Upload resume and create your interview profile

    </div>

    """,
    unsafe_allow_html=True
    )



    uploaded_file = st.file_uploader(

        "Upload Resume (PDF/DOCX)",

        type=[

            "pdf",

            "docx"

        ]

    )





    if uploaded_file:



        # Save file temporarily


        file_path=os.path.join(

            "uploads",

            uploaded_file.name

        )



        os.makedirs(

            "uploads",

            exist_ok=True

        )



        with open(

            file_path,

            "wb"

        ) as f:


            f.write(

                uploaded_file.getbuffer()

            )




        if st.button(

            "🔍 Analyze Resume"

        ):



            with st.spinner(

                "Extracting resume information..."

            ):


                profile = analyze_resume(

                    file_path

                )


                st.session_state.profile = profile



            st.success(

                "Resume analyzed successfully"

            )







    # =================================
    # SHOW PROFILE
    # =================================


    if "profile" in st.session_state:



        profile=st.session_state.profile



        st.divider()



        st.header(

            "👤 Candidate Profile"

        )




        name=st.text_input(

            "Candidate Name",

            value=profile.get(

                "name",

                ""

            )

        )




        skills=st.text_area(

            "Skills",

            value=", ".join(

                profile.get(

                    "skills",

                    []

                )

            )

        )




        projects=st.text_area(

            "Projects",

            value="\n".join(

                profile.get(

                    "projects",

                    []

                )

            )

        )






        resume_text=st.text_area(

            "Resume Text",

            value=profile.get(

                "resume_text",

                ""

            ),

            height=200

        )







        if st.button(

            "💾 Save Profile"

        ):



            st.session_state.profile={


                "name":

                name,



                "skills":

                [

                    x.strip()

                    for x in skills.split(",")

                ],



                "projects":

                [

                    x.strip()

                    for x in projects.split("\n")

                    if x.strip()

                ],



                "resume_text":

                resume_text

            }



            st.success(

                "Profile updated"

            )







        st.divider()



        st.subheader(

            "Preview"

        )



        col1,col2,col3=st.columns(3)




        with col1:


            st.metric(

                "Skills",

                len(

                    st.session_state.profile.get("skills", [])

                )

            )



        with col2:


            st.metric(

                "Projects",

                len(

                    st.session_state.profile.get("projects", [])

                )

            )



        with col3:


            st.metric(

                "Resume Loaded",

                "Yes"

            )





        st.write(

            "### Extracted Skills"

        )


        skills = st.session_state.profile.get(
            "skills",
            []
        )


        for skill in skills:

             st.success(
                 "✔ " + skill
         )



        st.write(

            "### Extracted Projects"

        )


        projects = st.session_state.profile.get(
             "projects",
             []
        )


        for project in projects:

             st.info(
               "📌 " + project
        )

# =====================================
# 💬 CHAT TRAINER PAGE
# =====================================


if page == "💬 Chat Trainer":


    st.markdown(
    """
    <div class="main-title">

    💬 AI Interview Trainer Chat

    </div>


    <div class="sub-title">

    Chat with your resume-aware interview assistant

    </div>

    """,
    unsafe_allow_html=True
    )



    # -----------------------------
    # Check Resume
    # -----------------------------

    if "profile" not in st.session_state or not st.session_state.profile:


        st.warning(
            "Please upload and analyze resume first."
        )


        st.stop()





    # -----------------------------
    # Initialize Chat Memory
    # -----------------------------


    if "chat_history" not in st.session_state:


        st.session_state.chat_history=[]





    # -----------------------------
    # Sidebar Actions
    # -----------------------------


    with st.sidebar:


        st.subheader(
            "Chat Options"
        )


        if st.button(
            "🗑 Clear Chat"
        ):


            st.session_state.chat_history=[]


            st.rerun()





        st.divider()



        st.write(
            "Quick Prompts"
        )


        prompts=[


            "Generate interview questions from my projects",


            "Review my resume for AI Engineer role",


            "Ask difficult ML interview questions",


            "Improve my interview answers",


            "Prepare HR questions"

        ]



        for p in prompts:


            if st.button(
                p,
                key=p
            ):


                st.session_state.selected_prompt=p


                st.rerun()





    # -----------------------------
    # Display Chat History
    # -----------------------------


    for chat in st.session_state.chat_history:



        if chat["role"]=="user":



            st.markdown(
            f"""

            <div style="
            background:#DCF8C6;
            padding:15px;
            border-radius:15px;
            margin:10px 0;
            ">


            👤 <b>Candidate</b>


            <br><br>


            {chat["message"]}


            </div>


            """,
            unsafe_allow_html=True
            )



        else:



            st.markdown(
            f"""

            <div style="
            background:#F1F1F1;
            padding:15px;
            border-radius:15px;
            margin:10px 0;
            ">


            🤖 <b>AI Interview Trainer</b>


            <br><br>


            {chat["message"]}


            </div>


            """,
            unsafe_allow_html=True
            )







    # -----------------------------
    # Input
    # -----------------------------


    user_input=None



    if "selected_prompt" in st.session_state:


        user_input=st.session_state.selected_prompt


        del st.session_state.selected_prompt




    else:


        user_input=st.chat_input(

            "Ask your interview trainer..."

        )





    if user_input:



        # Save user message


        st.session_state.chat_history.append(

            {

            "role":"user",

            "message":user_input

            }

        )



        with st.spinner(

            "AI Trainer thinking..."

        ):



            response=chat_with_agent(

                user_input,

                st.session_state.profile

            )




        # Save AI response


        st.session_state.chat_history.append(

            {

            "role":"assistant",

            "message":response

            }

        )



        st.rerun()






    # -----------------------------
    # Resume Information
    # -----------------------------


    with st.expander(

        "📄 Candidate Profile Used By AI"

    ):



        profile=st.session_state.profile



        st.write(

            "Name:",

            profile.get(

                "name",

                ""

            )

        )


        st.write(

            "Skills:",

            profile.get(

                "skills",

                ""

            )

        )


        st.write(

            "Projects:",

            profile.get(

                "projects",

                ""

            )

        )
# =====================================
# 🎤 MOCK INTERVIEW PAGE
# =====================================

if page == "🎤 Mock Interview":

    st.title("🎤 AI Mock Interview")


    # -------------------------
    # Initialize Session
    # -------------------------

    if "questions" not in st.session_state:
        st.session_state.questions = []

    if "current_question" not in st.session_state:
        st.session_state.current_question = 0

    if "answers" not in st.session_state:
        st.session_state.answers = []

    if "started" not in st.session_state:
        st.session_state.started = False


    # ==================================================
    # INTERVIEW SETUP
    # ==================================================

    if not st.session_state.started:


        st.markdown(
        """
        <div class="card">
        ⚙️ Customize Your Interview
        </div>
        """,
        unsafe_allow_html=True
        )


        role = st.selectbox(
            "🎯 Target Role",
            [
                "AI Engineer",
                "Machine Learning Engineer",
                "Data Analyst",
                "Software Developer",
                "Data Scientist"
            ],
            key="mock_role"
        )


        question_type = st.multiselect(
            "Question Type",
            [
                "Technical",
                "Project Based",
                "HR",
                "Coding"
            ],
            default=[
                "Technical",
                "Project Based"
            ],
            key="mock_question_type"
        )


        number = st.slider(
            "Number of Questions",
            1,
            10,
            5,
            key="mock_number"
        )


        difficulty = st.selectbox(
            "Difficulty",
            [
                "Easy",
                "Medium",
                "Hard"
            ],
            key="mock_difficulty"
        )


        answer_style = st.selectbox(
            "Answer Style",
            [
                "Short",
                "Medium",
                "Detailed"
            ],
            key="mock_answer_style"
        )



        if st.button(
            "🚀 Start Interview",
            key="mock_start"
        ):


            with st.spinner(
                "🤖 Generating interview questions..."
            ):


                result = generate_interview(
                    role=role,
                    profile=st.session_state.profile,
                    number=number,
                    difficulty=difficulty,
                    answer_style=answer_style
                )


            if isinstance(result,dict) and "questions" in result:


                st.session_state.questions = result["questions"]

                st.session_state.role = role

                st.session_state.current_question = 0

                st.session_state.answers = []

                st.session_state.started = True


                st.rerun()


            else:

                st.error(
                    "❌ AI response format incorrect"
                )



    # ==================================================
    # RUN INTERVIEW
    # ==================================================

    else:


        questions = st.session_state.questions


        if not questions:

            st.warning(
                "No questions generated"
            )

            st.session_state.started=False

            st.stop()



        total = len(questions)

        index = st.session_state.current_question



        # ==================================================
        # COMPLETED
        # ==================================================

        if index >= total:


            st.success(
                "🎉 Interview Completed"
            )


            st.subheader(
                "📊 Interview Summary"
            )



            for i,item in enumerate(
                st.session_state.answers
            ):


                st.markdown(
                    f"### Question {i+1}"
                )

                st.write(
                    item["question"]
                )


                st.write(
                    "**Your Answer:**"
                )

                st.write(
                    item["answer"]
                )


                if "feedback" in item:

                    st.write(
                        "**AI Feedback:**"
                    )

                    st.json(
                        item["feedback"]
                    )


                st.divider()



            # SAVE HISTORY

            if st.button(
                "💾 Save Interview",
                key="save_interview"
            ):


                save_history(

                    candidate=
                    st.session_state.profile.get(
                        "name",
                        "Candidate"
                    ),

                    role=
                    st.session_state.role,

                    profile=
                    st.session_state.profile,

                    questions=
                    st.session_state.questions,

                    answers=
                    st.session_state.answers,

                    feedback="Completed",

                    score="Generated"

                )


                st.success(
                    "Interview saved successfully"
                )




            if st.button(
                "🔄 Restart Interview"
            ):


                st.session_state.started=False

                st.session_state.questions=[]

                st.session_state.answers=[]

                st.session_state.current_question=0


                st.rerun()




        # ==================================================
        # CURRENT QUESTION
        # ==================================================

        else:


            question_data = questions[index]


            question = question_data.get(
                "question",
                ""
            )


            st.progress(
                (index+1)/total
            )


            st.subheader(
                f"Question {index+1}/{total}"
            )


            st.info(
                question
            )

            # =========================
# ANSWER METHOD
# =========================

        mode = st.radio(
            "Answer Method",
            [
                "⌨️ Text Answer",
                "🎤 Voice Answer"
            ],
            horizontal=True,
            key=f"mode_{index}"
        )


        answer = ""

# =========================
# ANSWER METHOD
# =========================

mode = st.radio(

    "Answer Method",

    [
        "⌨️ Text Answer",
        "🎤 Voice Answer"
    ],

    horizontal=True,

    key=f"mode_{index}"

)



answer = ""



# -------------------------
# Text Answer
# -------------------------

if mode == "⌨️ Text Answer":


    answer = st.text_area(

        "✍️ Your Answer",

        height=200,

        key=f"text_answer_{index}"

    )



# -------------------------
# Voice Answer
# -------------------------

else:


    if "voice_answer" not in st.session_state:

        st.session_state.voice_answer = ""



    if st.button(

        "🎤 Record Answer",

        key=f"record_{index}"

    ):


        with st.spinner(

            "Listening..."

        ):


            voice_text = speech_to_text()


            st.session_state.voice_answer = voice_text



    answer = st.session_state.get(

        "voice_answer",

        ""

    )



    st.text_area(

        "🎤 Converted Voice Answer",

        value=answer,

        height=200,

        key=f"voice_display_{index}"

    )



# =========================
# BUTTONS
# =========================


col1, col2 = st.columns(2)



# -------------------------
# SUBMIT
# -------------------------

with col1:


    if st.button(

        "✅ Submit",

        key=f"submit_{index}"

    ):


        if not answer.strip():


            st.warning(

                "Please enter answer"

            )


        else:


            with st.spinner(

                "🤖 AI Evaluating..."

            ):


                feedback = evaluate_answer(

                    question,

                    answer

                )



            st.session_state.answers.append(

                {

                    "question": question,

                    "answer": answer,

                    "feedback": feedback

                }

            )


            # clear voice after submit

            st.session_state.voice_answer = ""


            st.session_state.current_question += 1


            st.rerun()



# -------------------------
# SKIP
# -------------------------

with col2:


    if st.button(

        "⏭ Skip",

        key=f"skip_{index}"

    ):


        st.session_state.answers.append(

            {

                "question": question,

                "answer": "Skipped",

                "feedback": "Not evaluated"

            }

        )


        st.session_state.voice_answer = ""


        st.session_state.current_question += 1


        st.rerun()