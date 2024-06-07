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

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[])

categories_info = {
    "Medical History": [
        "existing medical conditions such as chronic kidney disease (CKD)", 
        "hypertension", 
        "diabetes mellitus", 
        "history of heart disease", 
        "previous surgeries or hospitalizations",
        "family history of kidney disease"
    ],
    "Medications and Supplements": [
        "current prescription medications", 
        "over-the-counter medications",
        "vitamins or supplements", 
        "herbal remedies", 
        "any recent changes in medication"
    ],
    "Lifestyle Factors": [
        "dietary habits", 
        "exercise routine", 
        "smoking history", 
        "alcohol consumption", 
        "stress levels"
    ],
    "Symptoms": [
        "fatigue", 
        "swelling in the legs or feet", 
        "changes in urination", 
        "shortness of breath", 
        "nausea or vomiting", 
        "itching"
    ]
}

responses = {category: [] for category in categories_info}

def generate_follow_up_question(missing_info, category):
    query = f"Based on the {category} section, what follow-up question should I ask to gather information about {missing_info}?"
    try:
        convo.send_message(query)
        follow_up_question = convo.last.text
        return follow_up_question
    except ResourceExhausted:
        print("API quota exceeded. Please try again later.")
        return None

def check_information(response, required_info, category):
    global responses
    relevant_info = []
    for info in required_info:
        if info.lower() in response.lower():
            relevant_info.append(info)
    if relevant_info:
        responses[category].append(response)
    return relevant_info

def ask_and_check_questions(category):
    required_info = categories_info[category]
    collected_info = set()
    
    initial_question = f"Tell me about {category.lower()}?"
    print(f'Question: {initial_question}')
    response = input('Your Response: ')
    relevant_info = check_information(response, required_info, category)
    collected_info.update(relevant_info)
    
    # Continue asking follow-up questions until all necessary data is collected
    while len(collected_info) < len(required_info):
        missing_info = [info for info in required_info if info not in collected_info]
        follow_up_question = generate_follow_up_question(", ".join(missing_info), category)
        if follow_up_question:
            print(f'AI Generated Question: {follow_up_question}')
            response = input('Your Response: ')
            relevant_info = check_information(response, required_info, category)
            collected_info.update(relevant_info)

def summarize_responses():
    for category, response_list in responses.items():
        if response_list:
            combined_responses = " ".join(response_list)
            print(f'Responses from the {category.lower()} section: {combined_responses}')
            try:
                convo.send_message(f"Based on the {combined_responses}, please provide a summary of the patient's {category.lower()} that is relevant to kidney failure.")
                print(convo.last.text)
            except ResourceExhausted:
                print("API quota exceeded in summary. Please try again later.")

# Start the interaction
for category in categories_info.keys():
    print(f'\n--- {category} Section ---')
    ask_and_check_questions(category)

summarize_responses()
