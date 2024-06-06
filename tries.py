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


med_ques = {
    "Do you have any existing medical conditions or illnesses?": "pre-existing medical conditions such as chronic kidney disease (CKD), hypertension, diabetes mellitus, or other conditions that may contribute to or result from kidney failure.",
    "Could you please provide more details about the specific conditions you've been diagnosed with?": "Details regarding the stage of kidney failure, etiology (e.g., diabetic nephropathy, hypertensive nephrosclerosis, glomerulonephritis), presence of complications (e.g., anemia, bone disease, cardiovascular disease), and any concurrent illnesses that may impact dialysis treatment or prognosis.",
    "Have there been any recent changes or developments in your medical history that we should be aware of?": "Updates on changes in kidney function (e.g., decline in glomerular filtration rate), development of new complications (e.g., electrolyte imbalances, fluid overload), or any significant events such as hospitalizations, infections, or vascular access issues."
}

med_supp_ques = {
    "Are you currently taking any medications or supplements?" : "Confirmation of current use of medications and supplements, including prescription drugs, over-the-counter medications, and dietary supplements.", 
    "Could you please list the medications you're taking and their dosages?" : "Detailed list of all medications being taken, including dosage strength, frequency of administration, and route of administration. This includes medications for managing kidney failure (e.g., phosphate binders, erythropoiesis-stimulating agents, vitamin D analogs), as well as medications for coexisting conditions (e.g., antihypertensive agents, insulin or oral hypoglycemic agents for diabetes mellitus, medications for cardiovascular disease).", 
    "Have you experienced any side effects or difficulties with your current medications?" : "Details about any adverse reactions, side effects, or difficulties experienced with the prescribed medications, including symptoms such as nausea, vomiting, diarrhea, dizziness, rash, or changes in laboratory parameters. Pay particular attention to potential complications related to kidney function, such as electrolyte imbalances, hypotension, or medication accumulation due to impaired renal clearance."

}
responses = ''

def check_information(response, conditions):
    global responses
    query = f'We are checking up the patient who have kidney failure. The expected answer is {conditions}. So, based on the {response}, do you it is important to for us to note these answers for the doctor? If you think it is above minor thing then only note and please begin with "Yes".'
    try:
        convo.send_message(query)
        answer = convo.last.text
        print(answer)
        if "yes" in answer.lower():
            responses += response
            return
        else:
            print('Moving to another section')
    except ResourceExhausted:
        print("API quota exceeded in checking_info. Please try again later.")
        return


def medical_question():
    for question, conditions in med_ques.items():
        print(f'Question: {question}')
        response = input('Your Response: ')
        check_information(response, conditions)

def medications_and_supplements():
    for question, conditions in med_supp_ques.items():
        print(f'Question: {question}')
        response = input('Your response: ')
        check_information(response, conditions)

def summarize_responses():
    global responses
    print(f'Responses from the patients: {responses}')
    try:
        convo.send_message(f"Based on the {responses}, please provide me the summary of the patient's information that doctor's need to know.")
        print(convo.last.text)
    except ResourceExhausted:
        print("API quota exceeded in summary. Please try again later.")


medical_question()
medications_and_supplements()
summarize_responses()
