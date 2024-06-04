import google.generativeai as genai

# Configure the Gemini AI with your API key
genai.configure(api_key="AIzaSyBSV0XbpWUbxE0qmrTxZlqd1o2VJKpWfYA")

# Set up the model
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

# Define questions and information needed
questions_info = {
    "Do you have any existing medical conditions or illnesses?": "Information Needed: Confirmation of any pre-existing medical conditions such as chronic kidney disease (CKD), hypertension, diabetes mellitus, or other conditions that may contribute to or result from kidney failure.",

    "Could you please provide more details about the specific conditions you've been diagnosed with?": [
        "stage of kidney failure", "diabetic nephropathy", "hypertensive nephrosclerosis", "glomerulonephritis",
        "anemia", "bone disease", "cardiovascular disease", "concurrent illnesses"]
}

# Function to check for relevant medical conditions using Gemini AI
def check_information(response, conditions):
    convo.send_message(f'By seeing the answer {response} provided, do you think that are the causes of {conditions} over here? If so point out me the disease that patient have in {conditions}')
    answer = convo.last.text
    print(answer)
    if "matches" in answer.lower():
        return
    else:
        print('Moving to another section.')


# Function to handle the interaction
def ask_and_check_questions():
    for question, conditions in questions_info.items():
        print(f'Question: {question}')
        response = input('Your Response: ')
        has_info = check_information(response, conditions)



# Start the interaction
ask_and_check_questions()