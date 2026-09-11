from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet




def create_report(
        filename,
        candidate,
        role,
        answers
):


    doc = SimpleDocTemplate(

        filename

    )


    styles=getSampleStyleSheet()


    content=[]



    content.append(

        Paragraph(

            "AI Interview Trainer Report",

            styles["Title"]

        )

    )


    content.append(

        Spacer(

            1,

            20

        )

    )



    content.append(

        Paragraph(

            f"Candidate: {candidate}",

            styles["Normal"]

        )

    )



    content.append(

        Paragraph(

            f"Role: {role}",

            styles["Normal"]

        )

    )



    content.append(

        Spacer(

            1,

            20

        )

    )



    for i,item in enumerate(answers):


        content.append(

            Paragraph(

                f"Question {i+1}",

                styles["Heading3"]

            )

        )


        content.append(

            Paragraph(

                item["question"],

                styles["Normal"]

            )

        )


        content.append(

            Paragraph(

                "Candidate Answer: "

                +

                item["answer"],

                styles["Normal"]

            )

        )


        content.append(

            Paragraph(

                "AI Feedback: "

                +

                str(item["feedback"]),

                styles["Normal"]

            )

        )


        content.append(

            Spacer(

                1,

                15

            )

        )


    doc.build(content)