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


questions_info = {
    "Do you have any existing medical conditions or illnesses?": "pre-existing medical conditions such as chronic kidney disease (CKD), hypertension, diabetes mellitus, or other conditions that may contribute to or result from kidney failure.",
    "Could you please provide more details about the specific conditions you've been diagnosed with?": "Details regarding the stage of kidney failure, etiology (e.g., diabetic nephropathy, hypertensive nephrosclerosis, glomerulonephritis), presence of complications (e.g., anemia, bone disease, cardiovascular disease), and any concurrent illnesses that may impact dialysis treatment or prognosis.",
    "Have there been any recent changes or developments in your medical history that we should be aware of?": "Updates on changes in kidney function (e.g., decline in glomerular filtration rate), development of new complications (e.g., electrolyte imbalances, fluid overload), or any significant events such as hospitalizations, infections, or vascular access issues."
}

responses = ''

def check_information(response, conditions):
    global responses
    query = f'Given the response: "{response}", do you think there are any indicators of {conditions}? If so, identify the specific condition.'
    try:
        convo.send_message(query)
        answer = convo.last.text
        if "yes" in answer.lower() or "indicator" in answer.lower():
            responses += response
            return
        else:
            print('Moving to another section')
    except ResourceExhausted:
        print("API quota exceeded in checking_info. Please try again later.")
        return


def ask_and_check_questions():
    for question, conditions in questions_info.items():
        print(f'Question: {question}')
        response = input('Your Response: ')
        ai_response = check_information(response, conditions)


def summarize_responses():
    global responses
    print(f'Responses from the patients: {responses}')
    try:
        convo.send_message(f"Based on the {responses}, please provide me the summary of the patient's information that doctor's need to know.")
        print(convo.last.text)
    except ResourceExhausted:
        print("API quota exceeded in summary. Please try again later.")


ask_and_check_questions()
summarize_responses()
