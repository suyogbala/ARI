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

# Predefined questions to gather patient information
questions = [
    "Admit Date: Date of patient’s admission to the doctor's place.",
    "Nephrologist: Name of the doctor.",
    "Frame Size: Please select one of the following options:\n- Small (5 - 5.7 ft)\n- Medium (5.8 - 5.11 ft)\n- Large (over 6 ft)",
    "Height: What is your height?",
    "Weight Assessment: Since visiting the doctor, has your weight:\n- Gained\n- Lost\n- Remained Stable",
    "Target Weight (TW): This information should already be provided by the doctor. If you know it, please provide it.",
    "Date of Birth (DOB): What is your date of birth?"
]

def generate_ai_response(patient_question):
    query = f"The patient asked: '{patient_question}'. How should I respond?"
    try:
        convo.send_message(query)
        ai_response = convo.last.text.strip()
        return ai_response
    except ResourceExhausted:
        print("API quota exceeded. Retrying in 30 seconds...")
        time.sleep(30)
        return generate_ai_response(patient_question)

def gather_patient_info():
    for question in questions:
        print(f'Question: {question}')
        response = input('Your Response: ').strip()
        
        while response.lower().startswith("question:"):
            patient_question = response[9:].strip()
            ai_response = generate_ai_response(patient_question)
            print(f'AI Response: {ai_response}')
            # Ask the same question again since it was not answered
            print(f'Question: {question}')
            response = input('Your Response: ').strip()

        responses.append(f'{question} {response}')
        print(f'Patient Response: {response}')
        
        time.sleep(1)  # Simulate delay in patient response

    print("Thank you for providing the information. We have gathered all the necessary details.")

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
    gather_patient_info()
    generate_summary()

if __name__ == "__main__":
    main()
