from .GPT import ChatGPT
from .. import user_lang, qs_config

translate_model = qs_config.basicSelect("gpt").get("translate", None)
if not translate_model:
    from .. import qs_default_console
    qs_default_console.print("You can set \".qsrc['basic_settings']['gpt']['translate']\" to specify the translation model.")


def translate(text, target_lang=user_lang.lower()):
    prompt = f"Please translate into {target_lang} (avoid explaining the original text): {text}"
    response = ChatGPT(prompt, system_prompt="You are a professional, authentic translation engine. You only return the translated text, without any explanations.", record_history=False, model=translate_model)
    return response
