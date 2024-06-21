import os
import time
import random
from google.oauth2 import service_account
from google.cloud import aiplatform
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# Set the path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/suyogbala/documents/codinglanguages/python.py/ARI_Timesheet/peaceful-signer-427117-m6-517775fa497c.json"

# Initialize the Vertex AI client
project_id = "peaceful-signer-427117-m6"  # Replace with your Google Cloud project ID
location = "us-central1"
aiplatform.init(project=project_id, location=location)

# Configure the genai API with your API key
genai.configure(api_key="AIzaSyBSV0XbpWUbxE0qmrTxZlqd1o2VJKpWfYA")  # Replace with your Generative AI API key

# Define the generation configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 200,
}

# Define the safety settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Start a new conversation
convo = model.start_chat(history=[])
responses = []

table = {}

patient_info = [
    "Admit Date:\nWhen did you get admit at the hospital?",
    "Date of Birth (DOB):\nWhen is your birthday?",
    "Nephrologist:\nWho is your kidney doctor?",
    "Frame Size:\nHow would you describe your body frame? How big you are? Depending on height and weight(Options: Small - 5 to 5.7 ft, Medium - 5.8 to 5.11 ft, Large - over 6 ft)",
    "Height:\nHow tall are you?",
    "Weight Assessment:\nSince your last visit, has your weight increased, decreased, or stayed the same? (Options: Increased, Decreased, Stayed the same)",
    "Target Weight (TW):\nWhat is your target weight according to your doctor?",
]

nutition_assessment_ques = [
    "Current Weight:\nWhat is your current weight?",
    "Standard Body Weight Index (SBWI):\nDo you know your standard body weight index?",
    "Dietitian:\nDo you have a dietitian? If yes, what's their name?",
    "Amputee:\nHave you had any amputations?\n☐ Yes\n☐ No\nIf yes, what is your adjusted body weight?",
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

medications_coverage_ques = [
    "Medications:\nWhat medications are you taking right now?",
    "Coverage:\nHow is your medication coverage?\n☐ Full\n☐ Limited/No coverage",
    "Bundled:\nAre your medications included in your overall care package?\n☐ Yes\n☐ No",
    "Prior Diet Counseling:\nHave you had any advice or counseling about your diet before?\n☐ Yes\n☐ No\nIf yes, who gave you the advice?",
    "Previous Diet(s):\nWhat types of diets have you tried in the past?"
]

dental_swallowing_ques = [
    "Dental Status:\nHow are your teeth and gums?\n☐ Own teeth\n☐ Dentures\n☐ Toothache\n☐ Missing teeth\n☐ Gum problems\n☐ Chewing difficulty\n☐ Bridge/Partial",
    "Access to a Dentist:\nDo you have access to a dentist?\n☐ Yes\n☐ No",
    "Appointment Scheduled:\nDo you have an upcoming dentist appointment?\n☐ Yes\n☐ No",
    "Difficulty Swallowing:\nDo you have any trouble swallowing your food?\n☐ Yes\n☐ No"
]

appetite_gi_assessment_ques = [
    "Current Appetite:\nOn a scale of 1 (worst) to 10 (best), how would you rate your current appetite?",
    "Appetite Trend:\nHas your appetite changed recently?\n☐ No change\n☐ Declining\n☐ Improving",
    "GI Symptoms (> 2 weeks):\nHave you had any of these symptoms for more than 2 weeks?\n☐ Nausea/Vomiting\n☐ Constipation/Diarrhea\n☐ Obesity\n☐ Heartburn\n☐ Pica (craving non-food items)\n☐ Hiccups\n☐ Indigestion\n☐ Altered/Metallic taste\n☐ GI Ulcer\n☐ Abdominal pain\n☐ Blood in stool\n☐ Colostomy\n☐ Anorexia (loss of appetite)\n☐ Coffee ground emesis (vomiting with a coffee ground appearance)\n☐ TPN/IDPN/IPN (special nutritional feeding methods)\n☐ Tube feeding\n☐ Other:\n☐ No identified problems",
    "Frequency of Symptoms:\nHow often do you experience these symptoms?\n☐ Very few (1x per day)\n☐ Some (2-3x per day) - Improving\n☐ Some (2-3x per day) - No change\n☐ Some (2-3x per day) - Getting worse\n☐ Frequent (>3x per day)\n☐ Constant (All day)",
    "Symptom Treatments:\nHow are these symptoms being treated?\n☐ No treatments\n☐ Diet\n☐ Over-the-counter medications\n☐ Prescribed medications"
]

functional_capacity_ques = [
    "Adequate Cooking Facilities:\nDo you have what you need to cook at home?\n☐ Yes\n☐ No",
    "Grocery Shopping:\nHow do you usually get your groceries?\n☐ I shop myself\n☐ Family helps\n☐ From an extended care facility\n☐ Delivery service\n☐ A caregiver shops for me",
    "Type of Eater:\nHow would you describe your eating habits?\n☐ I prefer easy cooking\n☐ I grab and go\n☐ I’m hardly ever home\n☐ I like home-cooked meals\n☐ I live in an extended care facility",
    "Meals Away From Home:\nHow often do you eat out or have meals away from home?\n☐ 1-2 times per week\n☐ 3-4 times per week\n☐ Rarely\n☐ Usually",
    "Changes in Living Situation Affecting Food Access:\nHas anything changed in your living situation that makes it harder for you to get food?\n☐ Yes\n☐ No",
    "Food Preparation:\nWho usually prepares your meals?\n☐ I cook myself\n☐ Family cooks\n☐ Extended care facility cooks\n☐ Friends cook\n☐ Meals are delivered to my home",
    "Activity Level (Exercise equal to 30 minutes):\nHow active are you on a daily basis?\n☐ Inactive\n☐ Light activity\n☐ Active",
    "Smoker:\nDo you smoke?\n☐ Yes\n☐ No",
    "Alcohol Use:\nDo you drink alcohol?\n☐ Yes\n☐ No",
    "Drug Use:\nDo you use any recreational drugs?\n☐ Yes\n☐ No",
    "Functional Capacity:\nHow would you describe your ability to perform daily activities?\n☐ Fully functional\n☐ Some loss of stamina\n☐ Severe"
]

all_questions = [patient_info, nutition_assessment_ques, medications_coverage_ques, dental_swallowing_ques, appetite_gi_assessment_ques, functional_capacity_ques]

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
                new = convo.send_message(f"Please ask this question {part_question[i]} in a human way so that patient understands it in a friendly way.")
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
    
def summary(table):
    all_answers = ''
    for question, answer in table.items():
        try:
            ask = convo.send_message(f"{question} is the question, and {answer} is the answer for that question. Now I want you to understand that and create me a sentence of that.")
            sentence = ask.text.strip()
            all_answers += sentence
        except ResourceExhausted:
            print("API quota exceeded. Retrying in 30 seconds...")
            time.sleep(30)
            continue
    
    final_summary = convo.send_message(f"Use the information {sentence} provided to tailor and adjust a patient dialysis treatment to suite their specific needs")
    print(final_summary)
gather_patient_info()
