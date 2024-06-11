import time
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

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings
)

convo = model.start_chat(history=[])

responses = []

def generate_follow_up_question(last_response):
    query = f"Based on the patient's response '{last_response}', what is the next follow-up question to gather general information about their medical history related to kidney failure? Respond with only the question."
    try:
        convo.send_message(query)
        follow_up_question = convo.last.text.strip()
        return follow_up_question
    except ResourceExhausted:
        print("API quota exceeded. Retrying in 60 seconds...")
        time.sleep(30) 
        return generate_follow_up_question(last_response)

def has_gathered_enough_info(combined_responses):
    query = f"Based on the collected responses '{combined_responses}', do we have enough information about the patient's medical history related to kidney failure? Reply with 'yes' or 'no' and provide a brief reason."
    try:
        convo.send_message(query)
        response = convo.last.text.strip().lower()
        print(response)
        return "yes" in response
    except ResourceExhausted:
        print("API quota exceeded. Retrying in 60 seconds...")
        time.sleep(60) 
        return has_gathered_enough_info(combined_responses)

def gather_patient_info():
    initial_question = "Please describe your current medical history related to kidney failure."
    print(f'Question: {initial_question}')
    response = input('Your Response: ')
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

def summary():
    combined_responses = " ".join(responses)   
    try:
        convo.send_message(f"Based on the responses '{combined_responses}', please provide a summary of the patient's medical history that is relevant to kidney failure.")
        print("\nSummary of the patient's medical history:")
        print(convo.last.text)
    except ResourceExhausted:
        print("API quota exceeded in summary. Retrying in 60 seconds...")
        time.sleep(60) 
        gather_patient_info() 

gather_patient_info()
summary()