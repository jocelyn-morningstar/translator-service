import os
from openai import OpenAI
client  = OpenAI(api_key = os.environ.get('OPENAI_API_KEY'))

#this translates foreign language in inContent to English
def translate_content(inContent: str) -> tuple[bool, str]:
    content = inContent.strip()
    if len(content) == 0:
        return True, content
    prompt = "Is the following text written entirely in English? (True or False):"
    completion = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = [
        {"role": "user", "content": prompt + content}
        ])
    llmresponse = completion.choices[0].message
    isEnglish = llmresponse.content == "True"

    if (not isEnglish):
        prompt = "Translate the following text into English (give only the English translation): "
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
