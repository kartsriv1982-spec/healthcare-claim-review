import json
import os

from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_answer(prompt):

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