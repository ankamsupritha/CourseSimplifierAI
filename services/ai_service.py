import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("IBM_PROJECT_ID")
URL = os.getenv("IBM_URL")


def get_access_token():

    response = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": API_KEY
        }
    )

    if response.status_code != 200:
        raise Exception("Failed to generate IAM Token:\n" + response.text)

    return response.json()["access_token"]


def simplify_course(text):

    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are LearnEase AI, an expert educational assistant.

Analyze the following course material.

IMPORTANT INSTRUCTIONS:

- Return ONLY plain text.
- Do NOT use Markdown.
- Do NOT use ###.
- Do NOT use **.
- Do NOT use ---.
- Leave one blank line between every section.
- Every bullet point must start on a new line.
- Keep the language simple and easy to understand.

Return EXACTLY in this format:

SUMMARY:

• Point 1

• Point 2

• Point 3

• Point 4

• Point 5

SIMPLIFIED NOTES:

Introduction:

• Point

• Point

Main Concepts:

• Point

• Point

Advantages:

• Point

• Point

KEY CONCEPTS:

• Concept 1

• Concept 2

• Concept 3

• Concept 4

• Concept 5

DEFINITIONS:

PLC: Programmable Logic Controller

SCADA: Supervisory Control and Data Acquisition

IoT: Internet of Things

Modbus: Industrial Communication Protocol

MCQS:

Question:
What is PLC?

A. Programming Language

B. Programmable Logic Controller

C. Personal Logic Circuit

D. Process Logic Code

Answer:
B

Explanation:
PLC stands for Programmable Logic Controller.

Question:
What is SCADA used for?

A. Gaming

B. Database

C. Industrial Monitoring

D. Networking

Answer:
C

Explanation:
SCADA is used for monitoring and controlling industrial processes.

Question:
Which protocol is commonly used in industrial communication?

A. Bluetooth

B. Modbus

C. HDMI

D. SMTP

Answer:
B

Explanation:
Modbus is a widely used industrial communication protocol.

REVISION NOTES:

• Important Point 1

• Important Point 2

• Important Point 3

• Important Point 4

• Important Point 5

Course Material:

{text[:10000]}
"""

    payload = {
        "model_id": "mistralai/mistral-small-3-1-24b-instruct-2503",
        "project_id": PROJECT_ID,
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "temperature": 0.2,
            "max_new_tokens": 3000,
            "repetition_penalty": 1.05
        }
    }

    response = requests.post(
        f"{URL}/ml/v1/text/generation?version=2023-05-29",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        raise Exception(response.text)

    output = response.json()["results"][0]["generated_text"]

    # Clean unwanted formatting
    output = output.replace("```", "")
    output = output.replace("###", "")
    output = output.replace("**", "")
    output = output.replace("---", "")
    output = output.strip()

    return {
        "summary": output
    }