import os
from openai import OpenAI
client  = OpenAI(api_key = os.environ.get('OPENAI_API_KEY'))


def translate_content(inContent: str) -> 'tuple[bool, str]':
    content = inContent.strip()
    if len(content) == 0:
        return True, content
    prompt = "True or false is the following text written entirely in English: "
    completion = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = [
        {"role": "user", "content": prompt + content}
        ])
    llmresponse = completion.choices[0].message
    isEnglish = llmresponse.content == "True"

    if (not isEnglish):
        prompt = "Translate the following text into English: "
        completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "user", "content": prompt + content}
            ])
        llmresponse = completion.choices[0].message
        translation = llmresponse.content
    else:
        translation = content
    return isEnglish, translation
