from ... import user_lang, qs_default_console, qs_error_string, qs_config
import time

API_KEY = qs_config.basicSelect("gpt")["support"].get("alapi", None)
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

import requests
import json

class AlapiChatbot:
    def __init__(
            self, 
            system_prompt=f"You are ChatGPT, a large language model trained by OpenAI. Respond conversationally with Markdown format and using {lang_table[user_lang]} Language.",
        ):
        from ..alapi import v2_url

        self.api_key = API_KEY
        self.url = v2_url
        self.messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

    def ask(self, prompt):
        self.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )
        while res := (
            requests.post(
                self.url + "chatgpt/pro",
                json={
                    "token": self.api_key,
                    "message": self.messages,
                },
            )
            .json()
        ):
            if res['code'] == 422 or not res.get('data'):
                qs_default_console.print(qs_error_string, res)
                time.sleep(3)
                continue
            else:
                break
        res = res.get("data").get("content")
        if not self.no_record:
            self.messages.append(
                {
                    "role": "assistant",
                    "content": res,
                }
            )
        return res

    def ask_stream(self, prompt):  # not support now
        self.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )
        post_stream = requests.post(
            self.url + "chatgpt/stream",
            json={
                "token": self.api_key,
                "message": self.messages,
            },
            stream=True,
        )
        total_res = ""
        for line in post_stream.iter_lines(decode_unicode=True):
            line = line.strip()
            if not line:
                continue
            res = json.loads(line)
            if res['success']:
                total_res = res['text']
                yield total_res

        self.messages.append(
            {
                "role": "bot",
                "content": total_res,
            }
        )

def create_bot(
    model: str,
    system_prompt: str = f"You are ChatGPT, a large language model trained by OpenAI. Respond conversationally with Markdown format and using {lang_table[user_lang]} Language.",
):
    return AlapiChatbot(model, system_prompt)
