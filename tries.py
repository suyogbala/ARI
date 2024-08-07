import google.generativeai as genai
import time
import random
from datetime import date
from google.generativeai.types.generation_types import StopCandidateException

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
current_date = date.today()

important_not_in_file = {
    # "Patient Information": [
    #     "Usual Body Weight (UBW): What is your usual weight?",
    #     "Standard Body Weight Index (SBWI): What is your standard body weight index?"
    # ],
    # "Comprehensive Nutrition Assessment": [
    #     "Food Accessibility: Can you afford food?\n   - ☐ Yes\n   - ☐ No",
    #     "Food Stamps/Food Program: Are you on any food stamps or food assistance programs?\n   - ☐ Yes\n   - ☐ No"
    # ],
    # "Dental and Swallowing Assessment": [
    #     "Dental Status: How are your teeth and gums?",
    #     "Access to a Dentist: Do you have access to a dentist?\n   - ☐ Yes\n   - ☐ No",
    #     "Appointment Scheduled: Do you have an upcoming dentist appointment?\n   - ☐ Yes\n   - ☐ No"
    # ],
    # "Appetite and GI Assessment": [
    #     "Appetite Trend: Is your appetite changing?\n   - ☐ No Change\n   - ☐ Declining\n   - ☐ Improving",

    #  ],
    "Functional Capacity": [
        "Grocery Shopping: How do you usually get your groceries? ☐ Self ☐ Family ☐ Extended Care Facility ☐ Delivery Service ☐ Caregiver",
        "Type of Eater: How would you describe your eating habits? ☐ Easy Cooking ☐ Grab-and-Go ☐ Hardly Home ☐ Home Cooking☐ Extended Care Facility",
        "Meals Away From Home: How often do you eat out or have meals away from home? ☐ 1-2x per week ☐ 3-4x per week ☐ Rarely ☐ Usually",
        "Food Preparation: Who usually prepares your meals? ☐ Self ☐ Family ☐ Extended Care Facility ☐ Friends ☐ Prepared Meals Delivered to Home",
        "Changes in Living Situation Affecting Food Access: Have changes in your living situation affected your food access?"
    ]
}

important_in_file = {
    "Patient Information": [
        "Admit Date: When were you admitted?",
        "Nephrologist: Who is your kidney doctor?",
        "Frame Size: (Select one)\n   - ☐ Small (5 - 5.7 ft)\n   - ☐ Medium (5.8 - 5.11 ft)\n   - ☐ Large (over 6 ft)",
        "Height: How tall are you?",
        "Weight Assessment: Since your last visit, has your weight changed?\n   - ☐ Increased\n   - ☐ Decreased\n   - ☐ Stayed the same",
        "Target Weight (TW): What is your target weight?",
        "Current Weight: Has your weight changed?\n   - ☐ Increased\n   - ☐ Decreased\n   - ☐ Stayed the same",
        "Date of Birth (DOB): What is your date of birth?",
        "Amputee: Have you had any amputations?\n   - ☐ Yes\n   - ☐ No\n   - If Yes, Adjusted Body Weight (Adj BW): What is your adjusted body weight?"
    ],
    "Comprehensive Nutrition Assessment": [
        "Ideal Body Weight (IBW): What is your ideal body weight?",
        "Dietitian: Do you have a dietitian? If yes, what's their name?",
        "Nutrition/Vitamin/Herbal Supplements: Are you taking any vitamins or herbal supplements?"
    ],
    "Medications and Coverage": [
        "Medications: What medications are you taking right now? Just the coverage name is fine",
        "Coverage: How is your medication coverage?\n   - ☐ Full\n   - ☐ Limited/No Coverage"
    ],
    "Prior Diet Counseling": [
        "Have you had any advice or counseling about your diet before?\n   - ☐ Yes\n   - ☐ No\n   - If Yes, By whom?: Who provided the diet counseling?"
    ],
    "Dental and Swallowing Assessment": [
        "Difficulty Swallowing: Do you have any trouble swallowing your food?\n   - ☐ Yes\n   - ☐ No"
    ],
    "Appetite and GI Assessment": [
        "Current Appetite: Rate your current appetite.",
        "GI Symptoms (> 2 weeks): Have you had any of these symptoms for more than 2 weeks?\n   - ☐ Nausea/Vomiting\n   - ☐ Constipation/Diarrhea\n   - ☐ Obese\n   - ☐ Heartburn\n   - ☐ Pica\n   - ☐ Hiccups\n   - ☐ Indigestion\n   - ☐ Altered/Metallic Taste\n   - ☐ GI Ulcer\n   - ☐ Abdominal Pain\n   - ☐ Blood in Stool\n   - ☐ Colostomy\n   - ☐ Anorexia\n   - ☐ Coffee Ground Emesis\n   - ☐ TPN/IDPN/IPN\n   - ☐ Tube Feeding\n   - ☐ Other:\n   - ☐ No Identified Problems. If other issues then that is not the answer."
    ],
    "Functional Capacity": [
        "Adequate Cooking Facilities: Do you have what you need to cook at home?\n   - ☐ Yes\n   - ☐ No",
        "Activity Level (Exercise equal to 30 minutes): How active are you on a daily basis?\n   - ☐ Inactive\n   - ☐ Light\n   - ☐ Active",
        "Smoker: Do you smoke?\n   - ☐ Yes\n   - ☐ No",
        "Alcohol Use: Do you drink alcohol?\n   - ☐ Yes\n   - ☐ No"
    ]
}

semi_important_not_in_file = {
    "Patient Information": [
        "Usual Body Weight (UBW): What is your usual weight?",
        "Weight change: If your weight changed, how much?",
        "Standard Body Weight Index (SBWI): What is your standard body weight index?"
    ],
    "Comprehensive Nutrition Assessment": [
        "Food Accessibility: Can you afford food?\n   - ☐ Yes\n   - ☐ No",
        "Food Stamps/Food Program: Are you on any food stamps or food assistance programs?\n   - ☐ Yes\n   - ☐ No"
    ],
    "Appetite and GI Assessment": [
        "Appetite Trend: Is your appetite changing?\n   - ☐ No Change\n   - ☐ Declining\n   - ☐ Improving",
        "Frequency of Symptoms: How often do you experience symptoms?\n   - ☐ Very Few (1x per day)\n   - ☐ Some (2-3x per day)",
        "Symptom Treatments: What treatments are you using?\n   - ☐ No Treatments\n   - ☐ Diet\n   - ☐ OTC Medications\n   - ☐ Prescribed Medications"
    ],
    "Functional Capacity": [
        "Grocery Shopping: How do you usually get your groceries?\n   - ☐ Self\n   - ☐ Family\n   - ☐ Extended Care Facility\n   - ☐ Delivery Service\n   - ☐ Caregiver",
        "Type of Eater: How would you describe your eating habits?\n   - ☐ Easy Cooking\n   - ☐ Grab-and-Go\n   - ☐ Hardly Home\n   - ☐ Home Cooking\n   - ☐ Extended Care Facility",
        "Meals Away From Home: How often do you eat out or have meals away from home?\n   - ☐ 1-2x per week\n   - ☐ 3-4x per week\n   - ☐ Rarely\n   - ☐ Usually",
        "Food Preparation: Who usually prepares your meals?\n   - ☐ Self\n   - ☐ Family\n   - ☐ Extended Care Facility\n   - ☐ Friends\n   - ☐ Prepared Meals Delivered to Home",
        "Changes in Living Situation Affecting Food Access: Have changes in your living situation affected your food access?\n   - ☐ Yes\n   - ☐ No"
    ]
}

semi_important_in_file = {
    "Patient Information": [
        "Weight Assessment: What is your target weight according to your doctor?",
        "Dietitian: Do you have a dietitian? If yes, what's their name?"
    ],
    "Dental and Swallowing Assessment": [
        "Dental Status: How are your teeth and gums?",
        "Access to a Dentist: Do you have access to a dentist?\n   - ☐ Yes\n   - ☐ No",
        "Appointment Scheduled: Do you have an upcoming dentist appointment?\n   - ☐ Yes\n   - ☐ No"
    ],
    "Appetite and GI Assessment": [
        "Appetite Trend: Is your appetite changing?\n   - ☐ No Change\n   - ☐ Declining\n   - ☐ Improving",
        "Frequency of Symptoms: How often do you experience symptoms?\n   - ☐ Very Few (1x per day)\n   - ☐ Some (2-3x per day)",
        "Symptom Treatments: What treatments are you using?\n   - ☐ No Treatments\n   - ☐ Diet\n   - ☐ OTC Medications\n   - ☐ Prescribed Medications"
    ],
    "Functional Capacity": [
        "Grocery Shopping: How do you usually get your groceries?\n   - ☐ Self\n   - ☐ Family\n   - ☐ Extended Care Facility\n   - ☐ Delivery Service\n   - ☐ Caregiver",
        "Type of Eater: How would you describe your eating habits?\n   - ☐ Easy Cooking\n   - ☐ Grab-and-Go\n   - ☐ Hardly Home\n   - ☐ Home Cooking\n   - ☐ Extended Care Facility",
        "Meals Away From Home: How often do you eat out or have meals away from home?\n   - ☐ 1-2x per week\n   - ☐ 3-4x per week\n   - ☐ Rarely\n   - ☐ Usually",
        "Food Preparation: Who usually prepares your meals?\n   - ☐ Self\n   - ☐ Family\n   - ☐ Extended Care Facility\n   - ☐ Friends\n   - ☐ Prepared Meals Delivered to Home",
        "Changes in Living Situation Affecting Food Access: Have changes in your living situation affected your food access?\n   - ☐ Yes\n   - ☐ No"
    ]
}

least_important_not_in_file = {
    "Dental and Swallowing Assessment": [
        "Missing teeth",
        "Gum problems",
        "Chewing difficulty",
        "Toothache",
        "Bridge/Partial"
    ]
}

least_important_in_file = {
    "Comprehensive Nutrition Assessment": [
        "Food Allergies/Intolerances: Do you have any food allergies or intolerances?",
        "Food/Cultural Preferences/Dislikes: What foods do you prefer or dislike?",
        "Diet Intake (past 2 weeks): How would you describe your diet over the past two weeks?"
    ],
    "Medications and Coverage": [
        "Bundled: Are your medications included in your overall care package?"
    ],
    "Prior Diet Counseling": [
        "Previous Diet(s): What types of diets have you tried in the past?"
    ]
}

all_questions = [important_not_in_file, important_in_file, semi_important_not_in_file, semi_important_in_file, least_important_not_in_file, least_important_in_file]

def is_unsure(response, question):
    try:
        ask = convo.send_message(f"The patient responded with '{response}' to the question '{question}'. Does this response indicate that the patient's response is unsure or doesn't remember the answer? Type 'yes' or 'no'.")
        ai_response = ask.text.strip()
        print(f"is_unsure: {ai_response.lower()}")
        return "yes" in ai_response.lower()
    except StopCandidateException as e:
        is_unsure(response, question)

def convert_answer(response, question):
    try:
        ask = convo.send_message(f"The patient responded {response} to the question {question}. Please give one line answer what patient is trying to say from the patient's POV. Staring with I.")
        ai_response = ask.text.strip()
        print(ai_response)
        return ai_response
    except StopCandidateException as e:
        convert_answer(response, question)

def is_answer(response, question):
    try:
        prompt = f"The patient said {response} for the question {question}, Do you think the {response} comes under the examples answers {is_match(question)}. Even a slight answer could be fine.Typ 'yes' or 'no"
        ask = convo.send_message(prompt)
        ai_response = ask.text.strip()
        print(f"is_answer: {ai_response.lower()}")
        return "yes" in ai_response.lower()
    except StopCandidateException as e:
        is_answer(response, question)

def generate_follow_up_question(initial_question, all_followup_ques, all_followup_ans):
    try:
        prompt = f"""
        The patient seems unsure about their answer to the initial question: "{initial_question}".
        Here are the questions that have been asked so far: {' '.join(all_followup_ques)}.
        Here are the responses to those questions: {' '.join(all_followup_ans)}.
        Considering the {' '.join(all_followup_ans)}, and the {' '.join(all_followup_ques)}, Please generate one casual follow-up questions that helps the patient recall their answer to the initial question: "{initial_question}".
        Please ask the logical question that human would ask, and add some expression according to their last response.
        """
        ai_response = convo.send_message(prompt)
        follow_up_question = ai_response.text.strip()
        return follow_up_question
    except StopCandidateException as e:
        generate_follow_up_question(initial_question, all_followup_ques, all_followup_ans)

def is_important(key, value):
    return key in important_not_in_file and value in important_not_in_file[key]

def is_question(response, questions):
    try:
        prompt = f"The patient responded {response} for the question: {questions}. Do you think the patient is asking question. Type 'yes' or 'no'"
        ask = convo.send_message(prompt)
        ai_response = ask.text.strip()
        print(f"is_question:  {ai_response.lower()}")
        return "yes" in ai_response.lower()
    except StopCandidateException as e:
        is_question(response, questions)

def is_match(questions):
    try:
        prompt = f"""
            "We are asking these questions to the dialysis patient. "
            "What should be the definite answer of this question: {questions}, when it is asked to the patient? 
            "Just give me definite answers only. For example: if the question is about a date, respond with a date; 
            "if it's about a name, respond with a name; if it's {questions} is about medication, just a category of medication can be the answer.
            "Provide only the exact answer, without any additional information."
            """
        ask = convo.send_message(prompt)
        ai_response = ask.text.strip()
        print(f"Answer_should_be: {ai_response.lower().strip()}")
        return ai_response
    except StopCandidateException as e:
        is_match(questions)

def human_like_delay():
    time.sleep(random.uniform(1, 3)) 

start_time = time.time()
alert_time = 1 * 60
print(start_time)
def gather_patient_info():
    all_ans = ''
    for three in all_questions:
        for key, value in three.items():
            i = 0
            while i < len(value):
                print(time.time())
                print(f"Real Question: {value[i]}")
                last_resp = all_ans
                if time.time() - start_time < alert_time:
                    try:
                        new = convo.send_message(f"""
                        We are asking about the patient about their {key}, and we want to ask patient about their {value[i]}, so can you ask patient the question to get the answer of {value[i]}. Please just ask the question.
                        Also, this is the last respose from the patien {last_resp}, give one sentence showing your exoression to the patient, and ask the question. If there is nothing in the {last_resp} then that is the first question.
                        """)
                        print(f'\nQuestion: {new.text.strip()}')
                    except StopCandidateException as e:
                        print(f"Question: {value[i]}")
                else:
                    if is_important(key, value[i]):
                        try:
                            new = convo.send_message(f"We are asking about the {key}, and we need the {value[i]}, so can you ask patient the question to get the answer of {value[i]}")
                            print(f'\nQuestion: {new.text.strip()}')
                        except StopCandidateException as e:
                            print(f"Question: {value[i]}")
                    else:
                        print(f"The time is Finished")
                        return 

                response = input('Your Response: ').strip()
                human_like_delay()
                new_hashmap = {new: response}
                answers = convert_answer(response, value[i])
                all_ans = answers
                count = 0
                while True:
                    if not is_answer(all_ans, value[i]):
                        if is_important(key, value[i]):
                            if is_unsure(all_ans, value[i]):
                                followup_ques = []
                                followup_resp = []
                                while True:
                                    print('First')
                                    check_recall = f"""
                                        These are the questions that have been asked: {' '.join(followup_ques)}.
                                        These are the responses: {' '.join(followup_resp)}.
                                        The initial question was: {value[i]}.
                                        Keep the questions light and casual. If the patient still doesn't remember, we can always check the file and skip the question.
                                        If there are no any {followup_ques} then we should ask.
                                        Do you think the patient might remember the answer after a few followup questions? Type 'Yes' or 'No'
                                        """
                                    resp_for_prom = convo.send_message(check_recall)
                                    if 'yes' in resp_for_prom.text.strip().lower():
                                        follow_up_question = generate_follow_up_question(value[i], followup_ques, followup_resp)
                                        count += 1
                                        print(f"Follow-up Question: {follow_up_question}")
                                        response = input(f'Your Response: ').strip()
                                        followup_ques.append(follow_up_question)
                                        followup_resp.append(response)
                                        new_hashmap[follow_up_question] = response    
                                        answers = ""
                                        for ques, ans in new_hashmap.items():
                                            try:
                                                asking = convo.send_message(f"This is the answer: '{ans}' for the question: '{ques}'. Write me a one-sentence answer that states the patient's response for the question.")
                                            except StopCandidateException as e:
                                                continue
                                            answers += asking.text.strip()
                                                
                                        final = convo.send_message(f"From these responses: {answers}, write me a one-sentence answer that states the patient's response for the question: '{value[i]}'")
                                        all_ans = final.text.strip()
                                        print(f"all_ans:  {all_ans}")
                                        if is_unsure(all_ans, value[i]):
                                            continue
                                        else:
                                            print('pat remember')
                                            table[value[i]] = all_ans
                                            ask = convo.send_message(f"{value[i]} is the question, and {all_ans} is the answer for that question. Now I want you to understand that and create me a sentence of that.")
                                            print(ask.text.strip())
                                            break
                                    else:
                                        if count >= 1:
                                            print(f"Question: So, after these questions, do you happen to remember the answer?")
                                            response = input(f'Your response: ')
                                            all_ans += response
                                            if is_unsure(all_ans, value[i]):
                                                print('pat dont rem')
                                                table[value[i]] = "Patient doesn't remember the answer, should look at time file."
                                                break
                                            else:
                                                print('pat remember')
                                                table[value[i]] = all_ans
                                                ask = convo.send_message(f"{value[i]} is the question, and {all_ans} is the answer for that question. Now I want you to understand that and create me a sentence of that.")
                                                print(ask.text.strip())
                                                break
                                        else:
                                            if count == 0:
                                                ask = convo.send_message(f"The patient said {all_ans} for the question {value[i]}, so give an appropriate response making them clear about the question {value[i]}")
                                                ques = ask.text.strip()
                                                print(f"Followup-ques: {ques}")
                                                response = input(f"Your Response: ")
                                                followup_ques.append(follow_up_question)
                                                followup_resp.append(response)
                                                new_hashmap[follow_up_question] = response    
                                                answers = ""
                                                for ques, ans in new_hashmap.items():
                                                    try:
                                                        asking = convo.send_message(f"This is the answer: '{ans}' for the question: '{ques}'. Write me a one-sentence answer that states the patient's response for the question.")
                                                    except StopCandidateException as e:
                                                        continue
                                                answers += asking.text.strip()

                                                final = convo.send_message(f"From these responses: {answers}, write me a one-sentence answer that states the patient's response for the question: '{value[i]}'")
                                                all_ans = final.text.strip()
                                                if is_unsure(all_ans, value[i]):
                                                    continue
                                            else:
                                                table[value[i]] = "Patient doesn't remember the answer, should look at time file."
                                                break

                                break
                            else:
                                print('Second')
                                ai_response = convo.send_message(f"The patient responded '{all_ans}' for the question: '{value[i]}. Please tell the patient what you meant by the question, and Please ask a follow-up question to clarify.")
                                human_like_delay()
                                print(f"AI Response: {ai_response.text.strip()}")
                                response = input('Your Response: ').strip()
                                new_hashmap[ai_response] = response
                                human_like_delay()
                                    
                                for ques, ans in new_hashmap.items():
                                    asking = convo.send_message(f"This is the answer; {ans} for the question: {ques}. write me a one answer that states the patient response for the question ")
                                    answers += asking.text.strip()
                                    
                                final = convo.send_message(f"From these {answers}, write me a one answer that states the patient response for the question {value[i]}")
                                all_ans = final.text.strip()
                        else:
                            if is_question(response, value[i]):
                                print("Third")
                                ask = convo.send_message(f"The patient said {response} for the questions: {value[i]}, please respond accordingly")
                                ai_response = ask.text.strip()
                                print(f"Clarification Ques: {ai_response}")
                                response = input(f"Your Response: ")
                                all_ans += response
                            
                            else:
                                table[value[i]] = f"Patient doesn't remember the answer, should look at time file for the patient's {value[i]}."
                                break

                    else:       
                        print('Fourth')
                        table[value[i]] = all_ans
                        ask = convo.send_message(f"{value[i]} is the question, and {all_ans} is the answer for that question. Now I want you to understand that and create me a sentence of that.")
                        print(ask.text.strip())
                        break

                i += 1

    
def summary(table):
    all_answers = ''
    for question, answer in table.items():
        ask = convo.send_message(f"{question} is the question, and {answer} is the answer for that question. Now I want you to understand that and create me a sentence of that.")
        sentence = ask.text.strip()
        all_answers += sentence
    
    final_summary = convo.send_message(f"Use this information {sentence} provided to tailor and adjust a patient dialysis treatment to suite their specific needs")
    print(final_summary.text.strip())
gather_patient_info()
summary(table)

endtime = time.time()
finish_time = (endtime - start_time) / 60
print(finish_time)