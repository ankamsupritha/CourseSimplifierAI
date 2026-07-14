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
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": API_KEY,
        },
    )
    if response.status_code != 200:
        raise Exception("Failed to generate IAM Token:\n" + response.text)
    return response.json()["access_token"]


def build_system_prompt():
    return (
        "You are LearnEase AI, an expert educational assistant powered by IBM watsonx Orchestrate. "
        "Your job is to help students understand complex course material. "
        "You can:\n"
        "  • Explain concepts in simple, beginner-friendly language\n"
        "  • Generate summaries, key points, or revision notes on request\n"
        "  • Create MCQ practice questions on any topic\n"
        "  • Define technical terms clearly\n"
        "  • Answer follow-up questions about a document or topic\n\n"
        "Always keep explanations clear, concise, and easy to understand. "
        "Respond in plain text only — no Markdown symbols like **, ##, or ---."
    )


def chat_with_agent(conversation_history: list[dict], user_message: str) -> str:
    """
    Send a conversational message to the IBM watsonx LLM.

    `conversation_history` is a list of {"role": "user"|"assistant", "text": "..."}
    objects representing the prior turns of the conversation.

    Returns the assistant's reply as a plain string.
    """
    access_token = get_access_token()

    # Build the full prompt with conversation history
    history_text = ""
    for turn in conversation_history:
        role = "Student" if turn["role"] == "user" else "LearnEase AI"
        history_text += f"{role}: {turn['text']}\n"

    prompt = (
        f"{build_system_prompt()}\n\n"
        "Conversation so far:\n"
        f"{history_text}"
        f"Student: {user_message}\n"
        "LearnEase AI:"
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "model_id": "mistralai/mistral-small-3-1-24b-instruct-2503",
        "project_id": PROJECT_ID,
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "temperature": 0.3,
            "max_new_tokens": 1500,
            "repetition_penalty": 1.05,
            "stop_sequences": ["\nStudent:", "\n\nStudent:"],
        },
    }

    response = requests.post(
        f"{URL}/ml/v1/text/generation?version=2023-05-29",
        headers=headers,
        json=payload,
    )

    if response.status_code != 200:
        raise Exception(response.text)

    reply = response.json()["results"][0]["generated_text"]

    # Strip any stop-sequence leakage and stray Markdown
    reply = reply.replace("```", "").replace("###", "").replace("**", "").replace("---", "")
    reply = reply.strip()

    return reply
