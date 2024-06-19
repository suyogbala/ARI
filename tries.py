import time
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

genai.configure(api_key="AIzaSyBSV0XbpWUbxE0qmrTxZlqd1o2VJKpWfYA")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
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

def check_if_question(response, question):
    try:
        ask = convo.send_message(f"Do you think '{response}' is a question? Type 'yes' or 'no'.")
        response = ask.text.strip()
        print(response)
        if "yes" in response.lower():
            return True
        else:
            table[question] = response

    except ResourceExhausted:
        print("API quota exceeded. Retrying in 60 seconds...")
        time.sleep(60)

def check_if_understandable(response, question):
    try:
        ask = convo.send_message(f"Is the following response {response} understandable? for the question {question}'. Type 'yes' or 'no'.")
        response = ask.text.strip()
        print(response)
        if "yes" in response.lower():
            return True
        else:
            table[question] = response
    
    except ResourceExhausted:
        print("API quota exceeded. Retrying in 60 seconds...")
        time.sleep(60)
    

def gather_patient_info():
    i = 0
    while i < len(questions):
        print(f'\nQuestion: {questions[i]}')
        response = input('Your Response: ').strip()
        while True:
            if check_if_question(response, questions[i]):
                try:
                    ai_response = convo.send_message(f"The patient asked a question: '{response}'. Please respond to it.")
                    print(f"AI Response: {ai_response.text.strip()}")
                    response = input('Your Response: ').strip()
                except ResourceExhausted:
                    print("API quota exceeded. Retrying in 60 seconds...")
                    time.sleep(60)
                    continue

            elif not check_if_understandable(response, questions[i]):
                try:
                    ai_response = convo.send_message(f"The patient responded '{response}' for the question: {questions[i]}. Ask a follow-up question to clarify.")
                    print(f"AI Response: {ai_response.text.strip()}")
                    response = input('Your Response: ').strip()
                    continue
                except ResourceExhausted:
                    print("API quota exceeded. Retrying in 60 seconds...")
                    time.sleep(60)
                    continue

            elif not check_if_question(response, questions[i]) or check_if_understandable(response, questions[i]):
                table[questions[i]] = response
                break
                
            else:
                try:
                    ai_response = convo.send_message(f"The patient responded '{response}' for the question: '{questions[i]}'. Please provide a suitable follow-up or response in the context of kidney health. The patient has a kidney failure.")
                    print(f"AI Response: {ai_response.text.strip()}")
                    response = input('Your Response: ').strip()
                except ResourceExhausted:
                    print("API quota exceeded. Retrying in 60 seconds...")
                    time.sleep(60)
                    continue
        i += 1

gather_patient_info()
print(table)
