from .GPT import ChatGPT
from .. import user_lang

def translate(text, target_lang=user_lang.lower()):
    prompt = f"Please translate into {target_lang} (avoid explaining the original text): {text}"
    response = ChatGPT(prompt, system_prompt="You are a professional, authentic translation engine. You only return the translated text, without any explanations.", record_history=False)
    return response
