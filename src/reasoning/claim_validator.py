import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def validate_claim(claim, evidence_list):
    prompt = f"""
Claim:
{claim}

Evidence:
{evidence_list}

Does the evidence SUPPORT, CONTRADICT, or is it NEUTRAL?
Answer in one word.
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message["content"].strip().lower()
