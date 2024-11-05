from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI()

# Define question sets for various issues
questions = {
    "depression": [
        "How often do you feel sad, down, or hopeless?",
        "How often do you have little interest or pleasure in doing things you used to enjoy?",
        "Do you feel fatigued or have little energy most days?",
        "How often do you have trouble falling asleep, staying asleep, or sleeping too much?",
        "How often do you feel bad about yourself or that you are a failure or have let yourself or your family down?",
        "Do you have trouble concentrating on things, such as reading or watching television?",
        "How often do you feel restless or find it hard to sit still?",
        "How often do you think about death or suicide?",
        "Have you experienced significant changes in your appetite or weight without trying?",
        "How often do you feel that your mood affects your ability to function at work, school, or in daily activities?"
    ],
    "anxiety": [
        "How often do you feel nervous, anxious, or on edge?",
        "How often do you worry excessively about different things?",
        "How often do you find it hard to control your worrying?",
        "How often do you feel restless or find it hard to relax?",
        "How often do you feel easily fatigued or tired?",
        "How often do you have difficulty concentrating or find your mind going blank?",
        "How often do you experience muscle tension or aches?",
        "How often do you experience physical symptoms such as sweating, trembling, or a rapid heartbeat?",
        "How often do you avoid situations or places because of anxiety or fear?",
        "How often do you feel a sense of impending doom or danger?"
    ],
    "eating_disorder": [
        "How often do you think about food or eating throughout the day?",
        "Do you feel out of control when you eat?",
        "How often do you eat large amounts of food in a short period?",
        "Do you ever make yourself vomit after eating or use laxatives to control your weight?",
        "How often do you skip meals or restrict the amount of food you eat to control your weight?",
        "Do you worry excessively about gaining weight or becoming fat?",
        "How often do you exercise excessively to lose weight or prevent weight gain?",
        "Do you feel guilty, ashamed, or distressed after eating?",
        "Do you feel that your self-worth is strongly influenced by your body weight or shape?",
        "How often do you lie about or hide your eating habits from others?"
    ]
}

# Define scoring for each option
options = {
    "A": 0,  # Never
    "B": 1,  # Rarely
    "C": 2,  # Sometimes
    "D": 3,  # Often
    "E": 4   # Always
}

# Define cognitive distortions
cognitive_distortions = {
    "Labeling": "e.g., 'I’m such a failure.'",
    "Emotional Reasoning": "e.g., 'I feel scared, so I must be in danger.'",
    "Catastrophizing": "e.g., 'Everything is going to go wrong.'",
    "Personalization": "e.g., 'It’s my fault that others are unhappy.'",
    "Mind Reading": "e.g., 'They probably don’t like me.'",
    "Mental Filtering": "e.g., focusing only on negatives."
}

# Define hobby suggestions
hobby_suggestions = [
    "Drawing or painting",
    "Reading books or writing stories",
    "Playing a musical instrument",
    "Going for a walk or jogging",
    "Cooking or baking new recipes",
    "Gardening",
    "Practicing yoga or meditation",
    "Playing video games or board games",
    "Crafting or DIY projects"
]

# Input data model
class UserInput(BaseModel):
    nickname: str
    issue: str = None
    answer: str = None


@app.post("/start_chatbot")
async def start_chatbot(user_input: UserInput):
    return {"message": f"Hello, {user_input.nickname}! I'm here to help you understand your feelings better."}


@app.post("/chat_about_day")
async def chat_about_day(user_input: UserInput):
    feeling = user_input.answer.strip().lower()
    response = ""

    if feeling in ["good", "happy", "great", "fantastic", "awesome"]:
        good_responses = [
            "That's fantastic to hear! What’s been the highlight of your day?",
            "I’m so happy for you! What are some things you’re grateful for right now?",
            "Great to hear you’re feeling good! Is there something special you’ve done today to boost your mood?"
        ]
        response = random.choice(good_responses)

    elif feeling in ["neutral", "okay", "fine"]:
        neutral_responses = [
            "Thanks for sharing that. Neutral days can be a great opportunity to reflect and recharge.",
            "Sometimes neutral days can feel like a pause. What’s one small thing you can do to bring a bit of joy?"
        ]
        response = random.choice(neutral_responses)

    elif feeling in ["sad", "down", "bad", "unhappy", "frustrated"]:
        response = "I'm sorry to hear that you're feeling sad. It's important to acknowledge these feelings."
        response += "\nHere are some activities that might help: Consider journaling or exploring mindfulness techniques."

    else:
        response = "That's an interesting feeling. Can you tell me more about it?"

    return {"response": response}


@app.post("/select_issue")
async def select_issue(user_input: UserInput):
    if user_input.issue not in questions:
        raise HTTPException(status_code=400, detail="Invalid issue selected.")
    return assess_feelings(user_input.issue, user_input.nickname)


def assess_feelings(issue, nickname):
    total_score = 0
    responses = []

    for question in questions[issue]:
        responses.append(question)
    
    return {"questions": responses}


@app.post("/submit_answers")
async def submit_answers(user_input: UserInput):
    if user_input.issue not in questions:
        raise HTTPException(status_code=400, detail="Invalid issue selected.")
    
    total_score = sum(options.get(answer.upper(), 0) for answer in user_input.answer.split(","))
    return analyze_score(total_score, user_input.nickname)


def analyze_score(score, nickname):
    if score <= 12:
        return {"message": f"Great job, {nickname}! Your score suggests you are experiencing mild feelings related to this issue."}
    elif score <= 24:
        return {"message": f"Your score indicates moderate feelings regarding this issue. It might be helpful to explore these feelings further."}
    else:
        return {"message": f"Your score suggests that you're experiencing severe feelings related to this issue. It’s important to seek support."}


@app.post("/analyze_thought")
async def analyze_thought(user_input: UserInput):
    thought = user_input.answer
    response = {"thought": thought, "cognitive_distortions": cognitive_distortions}
    
    return response


@app.post("/self_kindness")
async def self_kindness(user_input: UserInput):
    kindness_ideas = [
        "Remind yourself that it's okay to feel this way.",
        "Think of a friend who would comfort you; what would they say?",
        "Consider treating yourself to a favorite activity or hobby."
    ]
    suggestion = random.choice(kindness_ideas)
    
    return {"suggestion": suggestion}


@app.get("/hobby_suggestion")
async def hobby_suggestion():
    suggestion = random.choice(hobby_suggestions)
    return {"suggestion": suggestion}


@app.get("/end_chat")
async def end_chat(user_input: UserInput):
    return {"message": f"Thank you for talking with me today, {user_input.nickname}. Remember, it's okay to reach out for help if you need it."}

# Run the FastAPI application (this would typically be done in a separate command, not in this script)
# If running locally, you would use `uvicorn main:app --reload` in the terminal to start the server.
