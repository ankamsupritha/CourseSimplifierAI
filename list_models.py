import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("IBM_API_KEY")
URL = os.getenv("IBM_URL")

# Generate IAM Token
token = requests.post(
    "https://iam.cloud.ibm.com/identity/token",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data={
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY,
    },
).json()["access_token"]

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(
    f"{URL}/ml/v1/foundation_model_specs?version=2023-05-29",
    headers=headers
)

data = response.json()

print("\n===== AVAILABLE MISTRAL MODELS =====\n")

for model in data.get("resources", []):
    model_id = model.get("model_id", "")
    if "mistral" in model_id.lower():
        print(model_id)