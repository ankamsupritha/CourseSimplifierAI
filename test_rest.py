import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("IBM_PROJECT_ID")
URL = os.getenv("IBM_URL")

# ----------------------------------------
# STEP 1: GET IAM ACCESS TOKEN
# ----------------------------------------

print("Generating IAM Token...")

token_response = requests.post(
    "https://iam.cloud.ibm.com/identity/token",
    headers={
        "Content-Type": "application/x-www-form-urlencoded"
    },
    data={
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY
    }
)

if token_response.status_code != 200:
    print("❌ Failed to generate token")
    print(token_response.text)
    exit()

access_token = token_response.json()["access_token"]

print("✅ Token Generated Successfully")

# ----------------------------------------
# STEP 2: CALL GRANITE MODEL
# ----------------------------------------

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

payload = {
    "model_id": "mistralai/mistral-small-3-1-24b-instruct-2503",
    "project_id": "28fedc43-055d-4026-a719-4620b1b42c3c",
    "input": "Explain Artificial Intelligence in simple words.",
    "parameters": {
        "decoding_method": "greedy",
        "max_new_tokens": 150,
        "temperature": 0.7
    }
}

print("\nCalling Granite Model...\n")

response = requests.post(
    f"{URL}/ml/v1/text/generation?version=2023-05-29",
    headers=headers,
    json=payload
)

print("Status Code:", response.status_code)

try:
    print(response.json())
except Exception:
    print(response.text)