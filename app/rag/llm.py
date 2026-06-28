import json
import os

from openai import OpenAI


def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def generate_answer(prompt):
    client = get_client()

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        temperature=0,

        response_format={
            "type": "json_object"
        },

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    try:

        return json.loads(content)

    except json.JSONDecodeError:

        raise Exception(
            f"LLM returned invalid JSON:\n{content}"
        )