import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment.")

def ask_groq(query, context):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"""
You are a financial analyst assistant. The user may ask about specific section numbers or bullet points (e.g. '5.3.3', 'Section 6', etc.).
Use the document structure to find and answer the question clearly.

Context:
{context}

Question:
{query}

If the user references a section number or pointer, locate the relevant content and explain it step-by-step.
"""
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that answers questions based on context."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Groq API Error: {response.status_code} - {response.text}")
