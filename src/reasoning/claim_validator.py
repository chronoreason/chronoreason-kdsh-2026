import os
import sys
from dotenv import load_dotenv
from openai import APIError, OpenAI, RateLimitError

load_dotenv()
client = OpenAI()
FALLBACK_LABEL = os.getenv("CLAIM_VALIDATOR_FALLBACK_LABEL", "neutral").lower()

def validate_claim(claim, evidence_list):
    prompt = f"""
Claim:
{claim}

Evidence:
{evidence_list}

Does the evidence SUPPORT, CONTRADICT, or is it NEUTRAL?
Answer in one word.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return response.choices[0].message.content.strip().lower()
    except RateLimitError:
        print("OpenAI rate limit/quota hit; returning fallback label", file=sys.stderr)
    except APIError as err:
        print(f"OpenAI API error ({getattr(err, 'status_code', 'unknown')}): {err}", file=sys.stderr)

    return FALLBACK_LABEL
