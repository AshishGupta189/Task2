import json
import pdfplumber
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS,cross_origin

app = Flask(__name__)
CORS(app)

# Your OpenAI API key
api_key = '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'

# Define the API endpoint
GPT3_API_URL = "https://api.openai.com/v1/chat/completions"


@app.route("/route_with_cors", methods=["GET"])
@cross_origin()  # Apply CORS to this route
def route_with_cors():
    data = {"message": "CORS is enabled for this route"}
    return jsonify(data)


# Maintain context between user interactions
conversation_history = []
@app.route('/generate-text', methods=['POST'])
def generate_text():
    global conversation_history
    print("function called")
    try:
        # Get the user's message from the request
        print("function try")
        user_message = request.get_json()
        mess=user_message['userMessage']
        print("function called")
        # Add the user's message to the conversation history
        conversation_history.append({"role": "user", "content": mess})
        print(mess)
        # Generate a response using GPT-3.5-turbo

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
                "messages": conversation_history,
                "model": "gpt-3.5-turbo"
        }
        response = requests.post(GPT3_API_URL, headers=headers, data=json.dumps(payload))
        print(conversation_history)
        print(response)
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            print("success")
            assistant_reply = data["choices"][0]["message"]["content"]
            # Add the assistant's reply to the conversation history if needed
            print("suces1")
            conversation_history.append({"role": "assistant", "content": assistant_reply})
            # print("succ2")
            print(assistant_reply)
            return jsonify({"assistant_reply": assistant_reply})
        else:
            print("Error:", response.status_code, response.text)
            return jsonify({"error": "An error occurred"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/summarize', methods=['POST'])
def summarize():
    uploaded_file = request.files['file']

    input_text=''
    uploaded_files = request.files.getlist('file')
    summaries = []

    for uploaded_file in uploaded_files:
        if uploaded_file.content_type == "text/plain":
            # Handle plain text file
            input_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.content_type == "application/pdf":
            # Handle PDF file
            pdf_text = extract_text_from_pdf(uploaded_file)
            input_text = pdf_text
        else:
            return jsonify({"error": "Invalid input. Provide either 'pdf' or 'text'."})
    print(input_text)
    headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    payload = {
        "messages": [ 
            {
                "role": "system",
                "content": f"You are a summarization assistant."
            },
            {
                "role": "user",
                "content": f"please make the summary of the {input_text} "
            }
        ],
        "model": "gpt-3.5-turbo"
    }

    # Generate a summary using GPT-3.5-turbo
    response = requests.post(GPT3_API_URL, headers=headers, data=json.dumps(payload))

    # Get the generated summary
    if response.status_code == 200:
        data=response.json()
        summary = data['choices'][0]['message']['content']
        return jsonify({"summary": summary})
    else:
        return jsonify({"summary": "error"})


@app.route('/analyze', methods=['POST'])
def analyze_text():

    try:
        # Get the user's message from the request
        user_message = request.get_json()
        mess=user_message['message']
        
        # Generate a response using GPT-3.5-turbo

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
                "messages": [
                    {
                        "role":"system",
                        "content":"You are an emotion recognition assistant."
                    },
                    { "role": 'user', "content": f"analyze the text and give me only one word response for this {mess}" }
                ],
                "model": "gpt-3.5-turbo"
        }
        response = requests.post(GPT3_API_URL, headers=headers, data=json.dumps(payload))
        
        print(response)
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            assistant_reply = data["choices"][0]["message"]["content"]
            return jsonify({"message": assistant_reply})
        else:
            print("Error:", response.status_code, response.text)
            return jsonify({"error": "An error occurred"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500




def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

if __name__ == '__main__':
    app.run(debug=True)


