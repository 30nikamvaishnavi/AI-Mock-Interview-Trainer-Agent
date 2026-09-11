def detect_domain(text):

    text=text.lower()


    domains={


    "Technology":[

        "python",
        "java",
        "machine learning",
        "software",
        "developer",
        "sql",
        "ai"

    ],



    "Banking":[

        "bank",
        "finance",
        "loan",
        "account",
        "rbi"

    ],



    "Healthcare":[

        "medical",
        "hospital",
        "health",
        "pharma"

    ],



    "Marketing":[

        "marketing",
        "sales",
        "seo"

    ]


    }



    score={}



    for domain,words in domains.items():

        score[domain]=0


        for word in words:


            if word in text:

                score[domain]+=1



    return max(

        score,

        key=score.get

    )