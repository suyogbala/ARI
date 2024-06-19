import time
import random
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

genai.configure(api_key="AIzaSyBSV0XbpWUbxE0qmrTxZlqd1o2VJKpWfYA")

generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 200,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings
)

convo = model.start_chat(history=[])
responses = []

table = {}
questions = [
    "Admit Date: When did you start seeing your current doctor?",
    "Nephrologist: Who is your kidney doctor?",
    "Frame Size: How would you describe your body frame? (Options: Small - 5 to 5.7 ft, Medium - 5.8 to 5.11 ft, Large - over 6 ft)",
    "Height: How tall are you?",
    "Weight Assessment: Since your last visit, has your weight increased, decreased, or stayed the same? (Options: Increased, Decreased, Stayed the same)",
    "Target Weight (TW): What is your target weight according to your doctor?",
    "Date of Birth (DOB): When is your birthday?"
]

def is_question(response):
    try:
        ask = convo.send_message(f"Do you think '{response}' is a question? Type 'yes' or 'no'.")
        response = ask.text.strip()
        print(f"is_question: {response}")
        return "yes" in response.lower()
    except ResourceExhausted:
        print("API quota exceeded. Retrying in 60 seconds...")
        time.sleep(60)
        return is_question(response)

def is_understandable(response, question):
    try:
        ask = convo.send_message(f"Is the following response '{response}' understandable for the question '{question}'? Type 'yes' or 'no'.")
        response = ask.text.strip()
        print(f"is_understandable: {response}")
        return "yes" in response.lower()
    except ResourceExhausted:
        print("API quota exceeded. Retrying in 60 seconds...")
        time.sleep(60)
        return is_understandable(response, question)

def is_answer(response, question):
    try:
        ask = convo.send_message(f"Does the response '{response}' appropriately answer the question '{question}'? Type 'yes' or 'no'.")
        response = ask.text.strip()
        print(f"if_answer: {response}")
        return "yes" in response.lower()
    except ResourceExhausted:
        print("API quota exceeded. Retrying in 60 seconds...")
        time.sleep(60)
        return is_answer(response, question)

def human_like_delay():
    time.sleep(random.uniform(1, 3)) 

def gather_patient_info():
    i = 0
    while i < len(questions):
        print(f'\nQuestion: {questions[i]}')
        response = input('Your Response: ').strip()
        human_like_delay()

        while True:
            if is_question(response):
                try:
                    ai_response = convo.send_message(f"The patient asked a question: '{response} for the question: {questions[i]}'. Please respond to it in the context of kidney health.")
                    human_like_delay()
                    print(f"AI Response: {ai_response.text.strip()}")
                    response = input('Your Response: ').strip()
                    human_like_delay()
                    continue
                except ResourceExhausted:
                    print("API quota exceeded. Retrying in 60 seconds...")
                    time.sleep(60)
                    continue

            if not is_understandable(response, questions[i]):
                try:
                    ai_response = convo.send_message(f"The patient responded '{response}' for the question: '{questions[i]}'. Please ask a follow-up question to clarify.")
                    human_like_delay()
                    print(f"AI Response: {ai_response.text.strip()}")
                    response = input('Your Response: ').strip()
                    human_like_delay()
                    continue
                except ResourceExhausted:
                    print("API quota exceeded. Retrying in 60 seconds...")
                    time.sleep(60)
                    continue

            if not is_answer(response, questions[i]):
                try:
                    ai_response = convo.send_message(f"The patient responded '{response}' for the question: '{questions[i]}'. Please ask a follow-up question to clarify.")
                    human_like_delay()
                    print(f"AI Response: {ai_response.text.strip()}")
                    response = input('Your Response: ').strip()
                    human_like_delay()
                    continue
                except ResourceExhausted:
                    print("API quota exceeded. Retrying in 60 seconds...")
                    time.sleep(60)
                    continue

            table[questions[i]] = response
            break

        i += 1

    print("\nSummary of Patient Information:")
    for key, value in table.items():
        print(f"{key}: {value}")

gather_patient_info()
