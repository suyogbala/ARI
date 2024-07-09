import google.generativeai as genai
import time
import random
from datetime import datetime

genai.configure(api_key="AIzaSyBSV0XbpWUbxE0qmrTxZlqd1o2VJKpWfYA")

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[])

responses = []
table = {}
current_date = datetime.now().strftime("%Y-%m-%d")

patient_info = [
    "Admit Date:\nWhat date did you get admit at the hospital?, we need the date",
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

def is_unsure(response, question):
    ask = convo.send_message(f"The patient responded with '{response}' to the question '{question}'. Does this response indicate that the patient is unsure or doesn't remember the answer? Type 'yes' or 'no'.")
    ai_response = ask.text.strip()
    print(f"is_unsure: {ai_response.lower()}")
    return "yes" in ai_response.lower()

def is_answer(response, question):
    ask = convo.send_message(f"Does the response '{response}' provide the answer we needed for the question '{question}'? Please answer 'yes' or 'no'.")
    ai_response = ask.text.strip()
    print(f"is_answer: {ai_response.lower()}")
    return "yes" in ai_response.lower()

def human_like_delay():
    time.sleep(random.uniform(1, 3)) 

def gather_patient_info():
    for part_question in all_questions:
        i = 0
        while i < len(part_question):
            new = convo.send_message(f"Please ask this question {part_question[i]} in a human way so that patient understands it in a friendly way. Please just ask the question.")
            print(f'\nQuestion: {new.text.strip()}')
            response = input('Your Response: ').strip()
            human_like_delay()
            new_hashmap = {new: response}
            asking = convo.send_message(f"This is the answer; {response} for the question: {part_question[i]}. write me a one answer that states the patient response for the question in a way that patient response is understandable according to the question. ")
            answers = asking.text.strip()
            all_ans = asking.text.strip()
            print(all_ans)
            count = 0
            while True:
                if not is_answer(all_ans, part_question[i]):
                    followup_resp = all_ans
                    followup_ques = part_question[i]
                    if is_unsure(all_ans, part_question[i]):
                        while True:
                            all_followup_ques = convo.send_message(f"Combine all these questions into one: {followup_ques}")
                            all_followup_ans = convo.send_message(f"Combine all these answers into one: {followup_resp}")
                            print('First')
                            prom = f"""
                                These are the questions that I have asked {all_followup_ques} that I have asked to get the answer from the patient.
                                The patient response {all_followup_ans} to the {all_followup_ques}.
                                The initial question was: {part_question[i]}. So, Do you think the patient might remember after few other questions.
                                Type 'Yes' or 'No'
                                """
                            resp_for_prom = convo.send_message(prom)
                            print(resp_for_prom.text.strip())
                            if 'yes' in resp_for_prom.text.strip().lower():
                                prompt = f"""
                                    The patient seems unsure about their answer. The initial question was: "{part_question[i]}"
                                    The patient responded with: "{all_ans}"
                                    Please generate one follow-up questions that human would ask to help the patient recall about the {part_question[i]}. Consider that {followup_ques} are already asked, and the provided response are {followup_resp}.
                                    Provide only the questions, without any explanations or headers.
                                """
                                ai_response = convo.send_message(prompt)
                                human_like_delay()
                                questions = ai_response.text.strip()
                                print(f"Followup_Ques: {questions}")
                                response = input(f'Your Response: ').strip()
                                followup_ques += questions
                                followup_resp += response
                                new_hashmap[questions] = response
                                for ques, ans in new_hashmap.items():
                                    asking = convo.send_message(f"This is the answer; {ans} for the question: {ques}. write me a one answer that states the patient response for the question ")
                                    answers += asking.text.strip()
                                    
                                final = convo.send_message(f"From these {answers}, write me a one answer that states the patient response for the question {part_question[i]}")
                                all_ans = final.text.strip()
                                if is_unsure(all_ans, part_question[i]):
                                    continue
                            else:
                                table[part_question[i]] = "Patient doesn't remember the answer, should look at time file."
                                ask = convo.send_message(f"{part_question[i]} is the question, and {all_ans} is the answer for that question. Now I want you to understand that and create me a sentence of that.")
                                print(ask.text.strip())
                                break
                        break

                    else:
                        print('Second')
                        ai_response = convo.send_message(f"The patient responded '{all_ans}' for the question: '{part_question[i]}. Please tell the patient what you meant by the question, and Please ask a follow-up question to clarify.")
                        human_like_delay()
                        print(f"AI Response: {ai_response.text.strip()}")
                        response = input('Your Response: ').strip()
                        new_hashmap[ai_response] = response
                        human_like_delay()
                            
                        for ques, ans in new_hashmap.items():
                            asking = convo.send_message(f"This is the answer; {ans} for the question: {ques}. write me a one answer that states the patient response for the question ")
                            answers += asking.text.strip()
                            
                        final = convo.send_message(f"From these {answers}, write me a one answer that states the patient response for the question {part_question[i]}")
                        all_ans = final.text.strip()

                else:       
                    print('Third')
                    table[part_question[i]] = all_ans
                    ask = convo.send_message(f"{part_question[i]} is the question, and {all_ans} is the answer for that question. Now I want you to understand that and create me a sentence of that.")
                    print(ask.text.strip())
                    break

            i += 1
    
def summary(table):
    all_answers = ''
    for question, answer in table.items():
        print(question, answer)
        ask = convo.send_message(f"{question} is the question, and {answer} is the answer for that question. Now I want you to understand that and create me a sentence of that.")
        sentence = ask.text.strip()
        all_answers += sentence
    
    final_summary = convo.send_message(f"Use the information {sentence} provided to tailor and adjust a patient dialysis treatment to suite their specific needs")
    print(final_summary)
gather_patient_info()
