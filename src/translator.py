import os
from openai import OpenAI
client  = OpenAI(api_key = os.environ.get('OPENAI_API_KEY'))

#  Translate any foreign language in "inContent" to English; leave alone if
#  already English or cannot be translated into valid English.  Returns a
#  tuple: (bool, string)   If the bool is true, the string will just be
#  the original text in "inContent"; if the bool is false, the string will
#  be a translated text.  In other words, the first "bool" returned indicates
#  if "inContent" was return unchanged

def translate_content(inContent: str) -> tuple[bool, str]:

    content = inContent.strip()
    if len(content) == 0:
        return (True, content)
    try:
       prompt = "What is the language used in the following text: "
       completion = client.chat.completions.create(
       model = "gpt-3.5-turbo",
       messages = [
           {"role": "user", "content": prompt + content}
           ])
       llmresponse = completion.choices[0].message
       noChange = ("english" in llmresponse.content.lower())
       if (not noChange):
           prompt = "Translate the text or sequence of words after the first colon into English if "
           prompt += "possible, else return only 'Not possible': "
           completion = client.chat.completions.create(
           model = "gpt-3.5-turbo",
           messages = [
               {"role": "user", "content": prompt + content}
               ])
           llmresponse = completion.choices[0].message
           translation = llmresponse.content
           if (translation.strip().lower() == "not possible"):
               noChange = True
               translation = content
       else:
           translation = content
       return (noChange, translation)

    except Exception as e:
       return (False, f"Error: {str(e)}")
      