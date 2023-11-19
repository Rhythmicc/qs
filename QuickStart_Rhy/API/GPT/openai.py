from ... import requirePackage, user_lang, qs_config

API_KEY = qs_config.basicSelect("gpt")["support"].get("openai", None)
if not API_KEY:
    raise RuntimeError("No API key for POE Chatbot.")

lang_table = {
    'zh': 'Chinese',
    'en': 'English',
    'fra': 'French',
    'ru': 'Russian',
    'spa': 'Spanish',
    'ara': 'Arabic',
}

client = requirePackage("openai", "OpenAI", real_name="openai")(api_key=API_KEY)

class OpenAIChatBot:
    def __init__(self, model, system_prompt):
        self.model = model
        self.messages = [{
            "role": "system",
            "content": system_prompt,
        }]
    
    def ask_stream(self, prompt):
        self.messages.append({
            "role": "user",
            "content": prompt,
        })
        res = client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=True
        )
        _total = ""
        for i in res:
            _cur = i.choices[0].text or ""
            _total += _cur
            yield _cur
        self.messages.append({
            "role": "bot",
            "content": _total,
        })
          

def create_bot(model: str, system_prompt: str = f"You are ChatGPT, a large language model trained by OpenAI. Respond conversationally with Markdown format and using {lang_table[user_lang]} Language."):
    return OpenAIChatBot(model, system_prompt)
