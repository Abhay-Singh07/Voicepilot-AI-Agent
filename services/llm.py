
import json
from groq import Groq

from config import GROQ_API_KEY, LLM_MODEL

from services.prompts import (
    INTENT_PARSER_PROMPT,
    VOICE_CORRECTION_PROMPT,
    CODE_GENERATION_PROMPT,
    SUMMARY_PROMPT,
    CHAT_PROMPT
)


client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = LLM_MODEL


#  MODEL CALL


def ask_llm(prompt, temperature=0.2):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temperature
    )

    return response.choices[0].message.content.strip()


# VOICE CORRECTIO

def clean_transcript(text):

    prompt = VOICE_CORRECTION_PROMPT + f"\n\nInput:\n{text}"

    return ask_llm(prompt, temperature=0)




def parse_user_request(user_text):

    prompt = INTENT_PARSER_PROMPT + f"\n\nInput:\n{user_text}"

    raw_output = ask_llm(prompt, temperature=0)

    try:
        parsed = json.loads(raw_output)

        if "commands" not in parsed:
            raise Exception("Missing commands key")

        return parsed

    except Exception:

        return {
            "commands": [
                {
                    "intent": "chat",
                    "filename": "",
                    "content": user_text
                }
            ]
        }




def generate_code(requirement):

    prompt = CODE_GENERATION_PROMPT.format(
        requirement=requirement
    )

    return ask_llm(prompt, temperature=0.2)



def summarize_text(text):

    prompt = SUMMARY_PROMPT.format(
        text=text
    )

    return ask_llm(prompt, temperature=0.3)




def chat_response(text):

    prompt = CHAT_PROMPT.format(
        text=text
    )

    return ask_llm(prompt, temperature=0.5)
