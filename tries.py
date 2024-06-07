import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# Configure the Gemini AI API
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
    query = f"Based on the patient's response '{last_response}', what is a follow-up question to gather more information about their kidney failure condition? Only provide the question."
    try:
        convo.send_message(query)
        follow_up_question = convo.last.text.strip()
        return follow_up_question
    except ResourceExhausted:
        print("API quota exceeded. Please try again later.")
        return None

def gather_patient_info():
    initial_question = "Please describe your current condition related to kidney failure."
    print(f'Question: {initial_question}')
    response = input('Your Response: ')
    responses.append(response)
    
    while True:
        follow_up_question = generate_follow_up_question(response)
        if not follow_up_question:
            break
        print(f'AI Generated Question: {follow_up_question}')
        response = input('Your Response: ')
        if response.lower() in ["no", "none", "that's all", "nothing else"]:
            break
        responses.append(response)
    
    combined_responses = " ".join(responses)
    try:
        convo.send_message(f"Based on the responses '{combined_responses}', please provide a summary of the patient's condition relevant to kidney failure.")
        print("\nSummary of the patient's condition:")
        print(convo.last.text)
    except ResourceExhausted:
        print("API quota exceeded in summary. Please try again later.")

gather_patient_info()
