import random

def recommend(level):

    exercises = {

    "Low":[
    "Hydrate and maintain posture",
    "Eye relaxation exercise"
    ],

    "Moderate":[
    "4-7-8 breathing technique",
    "3 minute walk"
    ],

    "High":[
    "5 minute meditation",
    "Neck and shoulder stretch",
    "Deep breathing cycles"
    ]

    }

    return random.choice(exercises[level])