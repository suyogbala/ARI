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

def generate_follow_up_question(last_response):
    query = f"Based on the patient's response '{last_response}', what is the next follow-up question to gather additional information about their medical history to decide on the type of dialysis treatment? Respond with only the question."
    try:
        convo.send_message(query)
        follow_up_question = convo.last.text.strip()
        return follow_up_question
    except ResourceExhausted:
        print("API quota exceeded. Retrying in 60 seconds...")
        time.sleep(30)
        return generate_follow_up_question(last_response)

def has_gathered_enough_info(combined_responses):
    query = f"Based on the collected responses '{combined_responses}', do we have enough information to decide on the type of dialysis treatment for the patient? Reply with 'yes' or 'no'."
    try:
        convo.send_message(query)
        response = convo.last.text.strip().lower()
        print(response)
        return "yes" in response
    except ResourceExhausted:
        print("API quota exceeded. Retrying in 60 seconds...")
        time.sleep(60)
        return has_gathered_enough_info(combined_responses)

def gather_patient_info(initial_response):
    response = initial_response
    responses.append(response)
    
    while True:
        follow_up_question = generate_follow_up_question(response)
        if not follow_up_question:
            print("Thank you for providing the information. We have gathered all the necessary details.")
            break
        print(f'AI Generated Question: {follow_up_question}')
        response = input('Your Response: ')
        
        responses.append(response)
        combined_responses = " ".join(responses)
        
        if has_gathered_enough_info(combined_responses):
            print("Thank you for providing the information. We have gathered all the necessary details.")
            break

def generate_summary():
    combined_responses = " ".join(responses)
    try:
        convo.send_message(f"Based on the responses '{combined_responses}', please provide a summary of the patient's medical history and the recommended type of dialysis treatment.")
        print("\nSummary of the patient's medical history and recommended treatment:")
        print(convo.last.text)
    except ResourceExhausted:
        print("API quota exceeded in summary. Retrying in 60 seconds...")
        time.sleep(60)
        generate_summary()

def main():
    patient_info = """
    Patient Information:
    Full Name: John Smith
    Date of Birth: April 20, 1965
    Age: 59
    Gender: Male
    Contact Information: 123 Elm Street, Anytown, USA, (555) 123-4567

    Chief Complaint (CC):
    "I’m feeling very fatigued and have swelling in my legs and ankles. My doctor said my kidney function is worsening."

    History of Present Illness (HPI):
    John Smith has a history of chronic kidney disease (CKD), which has progressively worsened over the past five years. He was diagnosed with CKD stage 3 in 2019. Over the last six months, his symptoms have included:
    Fatigue: Persistent and increasing over the past few months.
    Edema: Noticeable swelling in the lower extremities, worsening in the past three months.
    Decreased Urine Output: John has noticed a reduction in the volume of urine over the last four weeks.
    Nausea: Occasional nausea, especially in the mornings.
    Itching: Persistent itching that is not relieved by over-the-counter medications.
    Recent blood tests indicate a significant decrease in kidney function with an eGFR (estimated glomerular filtration rate) dropping below 15 mL/min/1.73m², indicating CKD stage 5. His nephrologist recommended starting dialysis.

    Past Medical History (PMH):
    Chronic Kidney Disease (CKD): Diagnosed in 2019, initially stage 3, now progressed to stage 5.
    Hypertension (High Blood Pressure): Diagnosed in 2005, currently managed with medication.
    Type 2 Diabetes Mellitus: Diagnosed in 2000, controlled with oral medications and diet.
    Congestive Heart Failure (CHF): Diagnosed in 2021, under regular cardiology follow-up.
    Obesity: Body Mass Index (BMI) of 32.
    Hyperlipidemia (High Cholesterol): Diagnosed in 2008, managed with statins.
    Peripheral Neuropathy: Associated with diabetes, diagnosed in 2015.

    Medications:
    Lisinopril: 20 mg, once daily (for hypertension and CKD management).
    Metformin: 1000 mg, twice daily (for diabetes).
    Furosemide: 40 mg, once daily (for edema).
    Atorvastatin: 40 mg, once daily (for high cholesterol).
    Aspirin: 81 mg, once daily (preventive for cardiovascular disease).
    Gabapentin: 300 mg, twice daily (for peripheral neuropathy).

    Allergies:
    Sulfa Drugs: Causes rash and difficulty breathing.

    Family Medical History:
    Father: Heart disease, died at age 65.
    Mother: Type 2 diabetes, currently 82 years old.
    Brother: Hypertension, age 61.
    Sister: No significant health issues, age 55.

    Social History:
    Occupation: Retired, formerly a construction manager.
    Marital Status: Married, with two adult children.
    Tobacco Use: Smoked 1 pack per day for 20 years, quit in 2010.
    Alcohol Use: Drinks occasionally, about 2-3 beers per week.
    Drug Use: No history of recreational drug use.
    Exercise: Limited due to fatigue and swelling, previously enjoyed walking.
    Diet: Low-sodium, diabetic-friendly diet but struggles with weight control.

    Preventive and Screening History:
    Last Tetanus Booster: 2022
    Last Flu Vaccine: October 2023
    Pneumonia Vaccine (Pneumovax): Received in 2020
    Colonoscopy: Last done in 2020, no abnormalities.
    Mammogram: N/A (male patient)
    Eye Exam: Annual check-ups for diabetic retinopathy, last done in February 2024.

    Review of Systems (ROS):
    General: Significant fatigue, recent weight loss of 10 lbs over 2 months.
    Cardiovascular: Shortness of breath with minimal exertion, occasional chest discomfort.
    Respiratory: No cough or wheezing.
    Gastrointestinal: Reduced appetite, occasional nausea.
    Genitourinary: Decreased urine output, nocturia.
    Musculoskeletal: Muscle cramps, joint pain in the knees and back.
    Neurological: Tingling in feet, no recent headaches or dizziness.
    Psychiatric: Feels anxious about health, occasional low mood but no depression.
    Skin: Persistent itching, no rashes.
    Hematologic: Bruises easily, no unusual bleeding.
    Endocrine: Increased thirst, consistent with diabetes.
    EENT (Eyes, Ears, Nose, Throat): Blurred vision, wears glasses, no hearing issues.

    Recent Laboratory Results:
    eGFR: 12 mL/min/1.73m² (indicating stage 5 CKD).
    Creatinine: 5.4 mg/dL (elevated, indicating kidney dysfunction).
    Hemoglobin A1c: 7.2% (indicating controlled diabetes).
    Blood Pressure: 145/85 mmHg (slightly elevated).
    Potassium: 5.2 mEq/L (slightly elevated, monitored due to CKD).

    Summary and Plan:
    John Smith’s medical history and current symptoms indicate he is in advanced stages of CKD, now requiring dialysis. His treatment plan includes:
    Initiation of Hemodialysis: Scheduled for next week.
    Continued Management of Hypertension and Diabetes: With adjustments to medications as needed.
    Regular Follow-up: With nephrology, cardiology, and endocrinology.
    Dietary Adjustments: To manage CKD, including reduced potassium and phosphorus intake.
    Social Support: Referral to a dietitian and social worker for assistance with lifestyle adjustments and coping with dialysis.
    """
    
    gather_patient_info(patient_info)
    generate_summary()

if __name__ == "__main__":
    main()
