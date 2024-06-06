from ... import requirePackage, user_lang, qs_config

OPENAI_SETTING = qs_config.basicSelect("gpt")["support"].get("openai", None)
if not OPENAI_SETTING:
    OPENAI_SETTING = {"API_KEY": "", "API_URL": ""}
    qs_config.config["basic"]["gpt"]["support"]["openai"] = OPENAI_SETTING
    qs_config.update()

API_KEY = OPENAI_SETTING.get("API_KEY", None)
API_URL = OPENAI_SETTING.get("API_URL", None)

if not API_KEY:
    raise RuntimeError("No API key for OpenAI Chatbot.")

lang_table = {
    "zh": "Chinese",
    "en": "English",
    "fra": "French",
    "ru": "Russian",
    "spa": "Spanish",
    "ara": "Arabic",
}


class OpenAIChatBot:
    def __init__(self, model, system_prompt, record_history=True):
        self.model = model
        self.messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]
        self.client = requirePackage("openai", "OpenAI", real_name="openai")(
            api_key=API_KEY, base_url=API_URL
        )
        self.record_history = record_history

    def ask_stream(self, prompt):
        self.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )
        res = self.client.chat.completions.create(
            model=self.model, messages=self.messages, stream=True
        )
        _total = ""
        for i in res:
            _cur = i.choices[0].delta.content or ""
            _total += _cur
            yield _total
        if self.record_history:
            self.messages.append(
                {
                    "role": "assistant",
                    "content": _total,
                }
            )


def create_bot(
    model: str,
    system_prompt: str = f"You are ChatGPT, a large language model trained by OpenAI. Respond conversationally with Markdown format and using {lang_table[user_lang]} Language.",
    record_history=True
):
    return OpenAIChatBot(model, system_prompt, record_history)
