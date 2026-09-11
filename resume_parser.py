import os
import re

import fitz   # PyMuPDF
from docx import Document





# ======================================
# Extract text from PDF
# ======================================


def extract_pdf_text(file_path):


    text=""


    pdf=fitz.open(file_path)


    for page in pdf:


        text += page.get_text()



    return text






# ======================================
# Extract text from DOCX
# ======================================


def extract_docx_text(file_path):


    doc=Document(file_path)


    text="\n".join(

        para.text

        for para in doc.paragraphs

    )


    return text






# ======================================
# Main Resume Text Extraction
# ======================================


def extract_resume_text(file_path):


    if file_path.endswith(".pdf"):


        return extract_pdf_text(

            file_path

        )


    elif file_path.endswith(".docx"):


        return extract_docx_text(

            file_path

        )


    else:


        return ""







# ======================================
# Extract Name
# ======================================


def extract_name(text):


    lines=text.split("\n")


    for line in lines[:10]:


        line=line.strip()


        if len(line.split())<=4 and len(line)>3:


            return line



    return "Candidate"








# ======================================
# Extract Skills
# ======================================


def extract_skills(text):


    skill_list=[


        "Python",

        "Java",

        "C++",

        "C",

        "SQL",

        "Machine Learning",

        "Deep Learning",

        "TensorFlow",

        "PyTorch",

        "LangChain",

        "RAG",

        "LLM",

        "Generative AI",

        "Power BI",

        "Data Analysis",

        "Flask",

        "Django",

        "React",

        "HTML",

        "CSS",

        "JavaScript",

        "Git",

        "Linux"

    ]



    found=[]



    for skill in skill_list:


        if skill.lower() in text.lower():


            found.append(skill)



    return found








# ======================================
# Extract Projects
# ======================================


def extract_projects(text):


    projects=[]


    pattern=re.compile(

        r"(projects?|academic projects?)",

        re.I

    )



    match=pattern.search(text)



    if match:


        section=text[

            match.start():

            match.start()+1500

        ]



        lines=section.split("\n")



        for line in lines:


            line=line.strip()


            if len(line)>10:


                projects.append(line)



    return projects[:5]









# ======================================
# Complete Resume Analysis
# ======================================


def analyze_resume(file_path):


    text=extract_resume_text(

        file_path

    )


    profile={


        "name":

        extract_name(text),



        "skills":

        extract_skills(text),



        "projects":

        extract_projects(text),



        "resume_text":

        text

    }



    return profile