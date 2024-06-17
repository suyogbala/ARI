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


questions = [
    "Admit Date: When did you first admit to the doctor's place?",
    "Nephrologist: Who is your nephrologist (kidney specialist)?",
    "Frame Size: What is your frame size? (Options: Small - 5 to 5.7 ft, Medium - 5.8 to 5.11 ft, Large - over 6 ft)",
    "Height: What is your current height?",
    "Weight Assessment: Since visiting the doctor, have you experienced any changes in weight? (Options: Gain, Loss, Stable)",
    "Target Weight (TW): What is your target weight as recommended by your doctor?",
    "Date of Birth (DOB): When were you born?",
    "Current weight: Have you gained, lost, or maintained weight since visiting the doctor? (Options: Gain, Loss, Maintain)",
    "Usual Body Weight (UBW): What is your usual day-to-day weight in general?",
    "Standard Body Weight Index (SBWI): What is your standard body weight index?",
    "Ideal Body Weight (IBW): What is your targeted weight for dialysis?",
    "Dietitian: Who is your dietitian?",
    "Amputee: Do you have any amputations? (Options: Yes, No)",
    "If Yes, Adjusted Body Weight (Adj BW): What is your adjusted body weight?",
    "Weight Change: If you have gained or lost weight, how much?",
    "Timeframe: Over what timeframe did you experience this weight change?",
    "Medications (Binders, Active Vitamin D, Calcimimetics): Are you taking any of these medications?",
    "Diet Intake (past 2 weeks): How would you rate your diet intake over the past 2 weeks? (Options: Good, Borderline, Poor)",
    "Intake Compared to Usual Meal: How does your current intake compare to your usual meal intake?",
    "Meals: What did you eat for breakfast, lunch, dinner, and snacks?",
    "Food/Cultural Preferences/Dislikes: What are your food preferences or dislikes?",
    "Food Allergies/Intolerances: What are your food allergies or intolerances?",
    "Nutrition/Vitamin/Herbal Supplements: Are you taking any nutrition, vitamin, or herbal supplements?",
    "Food Accessibility: Can you afford food? (Options: Yes, No, Needs Assistance)",
    "Food Stamps/Food Program: Are you receiving food stamps or part of a food program? (Options: Yes, No)",
    "Medications: What medications are you currently taking?",
    "Coverage: Do you have full, limited, or no coverage for your medications? (Options: Full, Limited/No Coverage)",
    "Bundled: Are your medications bundled? (Options: Yes, No)",
    "Prior Diet Counseling: Have you received prior diet counseling? (Options: Yes, No)",
    "By whom?: Who provided the diet counseling?",
    "Previous Diet(s): What is your usual diet?",
    "Dental Status: What is your dental status? (Options: Own, Dentures, Toothache, Missing Teeth, Gum Problems, Chewing Difficulty, Bridge/Partial)",
    "Access to a Dentist: Do you have access to a dentist? (Options: Yes, No)",
    "Appointment Scheduled: Do you have a dentist appointment scheduled? (Options: Yes, No)",
    "Difficulty Swallowing: Do you have difficulty swallowing? (Options: Yes, No)",
    "Current Appetite (1 worst, 10 best): How would you rate your current appetite on a scale of 1 to 10?",
    "Appetite Trend: How has your appetite changed recently? (Options: No Change, Declining, Improving)",
    "GI Symptoms (> 2 weeks): Have you experienced any GI symptoms for more than 2 weeks? (Options: Nausea/Vomiting, Constipation/Diarrhea, Obese, Heartburn, Pica, Hiccups, Indigestion, Altered/Metallic Taste, GI Ulcer, Abdominal Pain, Blood in Stool, Colostomy, Anorexia, Coffee Ground Emesis, TPN/IDPN/IPN, Tube Feeding, Other, No Identified Problems)",
    "Frequency of Symptoms: How often do you experience these symptoms? (Options: Very Few, Some, Frequent, Constant)",
    "Symptom Treatments: What treatments are you using for these symptoms? (Options: No Treatments, Diet, OTC Medications, Prescribed Medications)",
    "Adequate Cooking Facilities: Do you have adequate cooking facilities? (Options: Yes, No)",
    "Grocery Shopping: How do you get your groceries? (Options: Self, Family, Extended Care Facility, Delivery Service, Caregiver)",
    "Type of Eater: What type of eater are you? (Options: Easy Cooking, Grab-and-Go, Hardly Home, Home Cooking, Extended Care Facility)",
    "Meals Away From Home: How often do you eat meals away from home? (Options: 1-2x per week, 3-4x per week, Rarely, Usually)",
    "Changes in Living Situation Affecting Food Access: Have changes in your living situation affected your access to food? (Options: Yes, No)",
    "Food Preparation: Who prepares your food? (Options: Self, Family, Extended Care Facility, Friends, Prepared Meals Delivered to Home)",
    "Activity Level (Exercise equal to 30 minutes): What is your activity level? (Options: Inactive, Light, Active)",
    "Smoker: Do you smoke? (Options: Yes, No)",
    "Alcohol Use: Do you use alcohol? (Options: Yes, No)",
    "Drug Use: Do you use drugs? (Options: Yes, No)",
    "Functional Capacity: How would you describe your functional capacity? (Options: Fully Functional, Some Loss of Stamina, Severe Loss of Functional Ability)",
    "Functional Capacity Rating: How would you rate your functional capacity? (Options: Fully Functional - No Dysfunction, Improvement in Dysfunction, Mild to Moderate Loss of Stamina, Light Activity, Change in Function, Difficulty with Ambulation, Severe Loss of Functional Ability, Difficulty with Activity, Bed/Chair Ridden with Little or No Activity)",
    "Edema (Nutrition Related): Do you experience edema related to nutrition? (Options: None, Mild, Moderate, Severe)",
    "Fat Stores: How would you describe your fat stores? (Options: None, Mild, Moderate, Severe)",
    "Muscle Wasting: How would you describe your muscle wasting? (Options: None, Mild, Moderate, Severe)",
    "Hospitalization in the Past 30 Days: Have you been hospitalized in the past 30 days? (Options: Yes, No)",
    "If Yes: Did hospitalization impact your ability to shop/prepare food? (Options: Yes, No)",
    "Did hospitalization change quantity of intake? (Options: Yes, No)",
    "Did hospitalization have a nutritional impact? (Options: Yes, No)",
    "Does the patient have diabetes? (Options: Yes, No)",
    "If Yes: What type of diabetes do you have? (Options: Type 1, Type 2)",
    "Diet Controlled Only?: Is your diabetes diet controlled only? (Options: Yes, No)",
    "Does the patient take insulin or oral agents at home? (Options: Yes, No)",
    "Does the patient utilize an insulin pump? (Options: Yes, No)",
    "Does the patient check blood sugar at home? (Options: Yes, No)",
    "Usual Glucose Ranges: What are your usual glucose ranges?",
    "Does the patient have a working glucometer and supplies? (Options: Yes, No)",
    "Is there a provider managing their diabetes care? (Options: Yes, No)",
    "Name of Provider: What is the name of your diabetes care provider?",
    "Eye Exam in the Last Year: Have you had an eye exam in the last year? (Options: Yes, No)",
    "Date: When was the last eye exam?"
]


def is_response_correct(response, question):
    prompt = f"The patient was asked: {question}. They responded: {response}. Is this response correct for the question?, just check if it is correct or not"
    ai_judgment = convo.send_message(prompt)
    judgment = ai_judgment.text.strip().lower()
    return 'yes' in judgment


def gather_patient_info():
    i = 0
    while i < len(questions):
        print(f'\nQuestion: {questions[i]}')
        response = input('Your Response: ').strip()
        responses.append(response)
        
        if not is_response_correct(response, questions[i]):
            try:
                ai_response = convo.send_message(f"The patient's response was: {response}. Please provide the correct information or clarify.")
                print(f"AI Response: {ai_response.text.strip()}")
                responses.pop()
            except ResourceExhausted:
                print("API quota exceeded. Retrying in 60 seconds...")
                time.sleep(60)
                continue
        
        patient_has_question = True
        while patient_has_question:
            follow_up_response = input('Do you have any questions or need clarification on anything? (Type "no" to proceed): ').strip().lower()
            if follow_up_response == 'no':
                patient_has_question = False
            else:
                try:
                    ai_response = convo.send_message(follow_up_response)
                    print(f"AI Response: {ai_response.text.strip()}")
                except ResourceExhausted:
                    print("API quota exceeded. Retrying in 60 seconds...")
                    time.sleep(60)
        
        if is_response_correct(response, questions[i]) or not response:
            i += 1

gather_patient_info()
