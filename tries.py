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

patient_info = [
    "Admit Date:\nWhen did you get admit at the hospital?",
    "Nephrologist:\nWho is your kidney doctor?",
    "Frame Size:\nHow would you describe your body frame? How big you are? Depending on height and weight(Options: Small - 5 to 5.7 ft, Medium - 5.8 to 5.11 ft, Large - over 6 ft)",
    "Height:\nHow tall are you?",
    "Weight Assessment:\nSince your last visit, has your weight increased, decreased, or stayed the same? (Options: Increased, Decreased, Stayed the same)",
    "Target Weight (TW):\nWhat is your target weight according to your doctor?",
    "Date of Birth (DOB):\nWhen is your birthday?"
]

nutition_assessment_ques = [
    "Current Weight:\nWhat is your current weight?",
    "Recent Weight Changes:\nHas your weight recently:\n☐ Increased\n☐ Decreased\n☐ Stayed the same",
    "Usual Body Weight (UBW):\nWhat is your typical weight on most days?",
    "Standard Body Weight Index (SBWI):\nDo you know your standard body weight index?",
    "Ideal Body Weight (IBW):\nWhat is your goal weight?",
    "Dietitian:\nDo you have a dietitian? If yes, what's their name?",
    "Amputee:\nHave you had any amputations?\n☐ Yes\n☐ No\nIf yes, what is your adjusted body weight?",
    "Weight Change:\nIf your weight has changed, how much and over what time period?",
    "Medications:\nWhat medications are you currently taking for your kidneys or other conditions?",
    "Diet Intake (past 2 weeks):\nHow would you describe your diet over the past two weeks?\n☐ Good\n☐ Borderline\n☐ Poor",
    "Intake Compared to Usual Meal:\nHow much of your usual meal are you eating?\n☐ 100% (all)\n☐ 75-99%\n☐ 50-75% but increasing\n☐ 50-75% with no change or decreasing\n☐ <50% but increasing\n☐ <50% with no change or decreasing\n☐ ≤ 25% (very little)",
    "Meals:\nWhat did you eat for:\n- Breakfast:\n- Lunch:\n- Dinner:\n- Snacks:",
    "Food/Cultural Preferences/Dislikes:\nAre there any foods you particularly like or dislike?",
    "Food Allergies/Intolerances:\nDo you have any food allergies or things you can’t eat?",
    "Nutrition/Vitamin/Herbal Supplements:\nAre you taking any vitamins or herbal supplements?",
    "Food Accessibility:\nAre you able to afford the food you need?\n☐ Yes\n☐ No\n☐ Need assistance",
    "Food Stamps/Food Program:\nAre you on any food stamps or food assistance programs?\n☐ Yes\n☐ No"
]

all_questions = [patient_info, nutition_assessment_ques]

def is_question(response):
    try:
        ask = convo.send_message(f"Do you think '{response}' is a question? Type 'yes' or 'no'.")
        response = ask.text.strip()
        print(f"is_question: {response}")
        return "yes" in response.lower()
    except ResourceExhausted:
        print("API quota exceeded. Retrying in 30 seconds...")
        time.sleep(30)
        return is_question(response)

def is_understandable(response, question):
    try:
        ask = convo.send_message(f"Is the following response '{response}' understandable for the question '{question}'? Type 'yes' or 'no'.")
        response = ask.text.strip()
        print(f"is_understandable: {response}")
        return "yes" in response.lower()
    except ResourceExhausted:
        print("API quota exceeded. Retrying in 30 seconds...")
        time.sleep(30)
        return is_understandable(response, question)

def is_answer(response, question):
    try:
        ask = convo.send_message(f"Does the response '{response}' appropriately answer the question '{question}'? Type 'yes' or 'no'.")
        response = ask.text.strip()
        print(f"is_answer: {response}")
        return "yes" in response.lower()
    except ResourceExhausted:
        print("API quota exceeded. Retrying in 30 seconds...")
        time.sleep(30)
        return is_answer(response, question)

def human_like_delay():
    time.sleep(random.uniform(1, 3)) 

def gather_patient_info():
    for part_question in all_questions:
        i = 0
        while i < len(part_question):
            try:
                new = convo.send_message(f"Please ask this question {part_question[i]} in friendly way. You can make your own question.")
                print(f'\nQuestion: {new.text.strip()}')
                response = input('Your Response: ').strip()
                human_like_delay()
            except ResourceExhausted:
                print("API quota exceeded. Retrying in 30 seconds...")
                time.sleep(30)
                continue

            while True:
                if not is_answer(response, part_question[i]):
                    try:
                        ai_response = convo.send_message(f"The patient responded '{response}' for the question: '{part_question[i]}'. Please ask a follow-up question to clarify.")
                        human_like_delay()
                        print(f"AI Response: {ai_response.text.strip()}")
                        response = input('Your Response: ').strip()
                        human_like_delay()
                        continue
                    except ResourceExhausted:
                        print("API quota exceeded. Retrying in 30 seconds...")
                        time.sleep(30)
                        return not is_answer(response, part_question[i])
                    
                elif is_question(response):
                    try:
                        ai_response = convo.send_message(f"The patient asked a question: '{response} for the question: {part_question[i]}'. Please respond to it in the context of kidney health.")
                        human_like_delay()
                        print(f"AI Response: {ai_response.text.strip()}")
                        response = input('Your Response: ').strip()
                        human_like_delay()
                        continue
                    except ResourceExhausted:
                        print("API quota exceeded. Retrying in 30 seconds...")
                        time.sleep(30)
                        return is_question(response)
                    
                elif not is_understandable(response, part_question[i]):
                    try:
                        ai_response = convo.send_message(f"The patient responded '{response}' for the question: '{part_question[i]}'. Please ask a follow-up question to clarify.")
                        human_like_delay()
                        print(f"AI Response: {ai_response.text.strip()}")
                        response = input('Your Response: ').strip()
                        human_like_delay()
                        continue
                    except ResourceExhausted:
                        print("API quota exceeded. Retrying in 30 seconds...")
                        time.sleep(30)
                        return not is_understandable(response, part_question[i])


                else:
                    table[part_question[i]] = response
                    break

            i += 1

    print("\nSummary of Patient Information:")
    for key, value in table.items():
        print(f"{key}: {value}")

gather_patient_info()