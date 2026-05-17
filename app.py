from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import pandas as pd
import os
API_KEY = "AIzaSyCdhbvQSlzswmWt7TGPTIuz2SguThhKlqE"

app = Flask(__name__)
CORS(app)

# READ DATASET
df = pd.read_excel("2000 DATASET HOSPITAL VA.xlsx")

# CREATE DATA SUMMARY
summary = f"""
Total Patients: {len(df)}

Average Billing Amount:
{df['Billing Amount'].mean():.2f}

Average Length of Stay:
{df['Length of Stay'].mean():.2f}

Patient Count by Medical Condition:
{df['Medical Condition'].value_counts().to_string()}

Patient Count by Insurance Provider:
{df['Insurance Provider'].value_counts().to_string()}

Patient Count by Admission Type:
{df['Admission Type'].value_counts().to_string()}

Top Hospitals:
{df['Hospital'].value_counts().head(5).to_string()}
"""

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():

    data = request.json

    question = data.get("question")

    prompt = f"""
    You are an AI healthcare business analyst.

    Dataset Summary:
    {summary}

    User Question:
    {question}

    IMPORTANT:
    - Answer ONLY based on dataset summary.
    - Give concise business insights.
    - Mention exact numbers when possible.
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }

    response = requests.post(url, json=payload)

    result = response.json()

    try:
        answer = result['candidates'][0]['content']['parts'][0]['text']
    except:
        answer = str(result)

    return jsonify({
        "answer": answer
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
