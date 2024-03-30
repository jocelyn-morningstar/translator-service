import os
from openai import OpenAI
client  = OpenAI(api_key = os.environ.get('OPENAI_API_KEY'))


def translate_content(content: str) -> tuple[bool, str]:
    prompt = "Translate the following text into English: "
    completion = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = [
        {"role": "user", "content": prompt + content}
        ])
    llmresponse = completion.choices[0].message
    translation = llmresponse.content
    #translation = "something"
    return True, translation
