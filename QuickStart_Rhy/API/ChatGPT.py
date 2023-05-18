from .. import requirePackage, user_lang, qs_default_console, qs_error_string
from . import pre_check
import time

lang_table = {
    'zh': 'Chinese',
    'en': 'English',
    'fra': 'French',
    'ru': 'Russian',
    'spa': 'Spanish',
    'ara': 'Arabic',
}

API_KEY = pre_check("openai", ext=False)
ALAPI = pre_check("openai-alapi", ext=False)
if ALAPI:
    import requests
    import json


_chatbot = None


class AlapiChatbot:
    def __init__(
            self, 
            system_prompt=f"You are ChatGPT, a large language model trained by OpenAI. Respond conversationally with Markdown format and using {lang_table[user_lang]} Language.",
            no_record: bool = False
        ):
        from .alapi import alapi_token, v2_url

        self.no_record = no_record
        self.api_key = alapi_token
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

        if not self.no_record:
            self.messages.append(
                {
                    "role": "assistant",
                    "content": total_res,
                }
            )


def create_bot(no_record: bool = False):
    if ALAPI:
        return AlapiChatbot(no_record=no_record)
    else:
        return (
            requirePackage("revChatGPT.V3", "Chatbot", "revChatGPT")(
                API_KEY,
                system_prompt=f"You are ChatGPT, a large language model trained by OpenAI. Respond conversationally with Markdown format and using {lang_table[user_lang]} Language.",
            )
            if API_KEY
            else requirePackage("revChatGPT.V1", "Chatbot", "revChatGPT")(
                {
                    "email": pre_check("openai-email"),
                    "password": pre_check("openai-password"),
                    "paid": pre_check("openai-paid"),
                }
            )
        )


def chatGPT(
    prompt: str,
    wait_all: bool = False,
    no_record: bool = False,
):
    """
    使用OpenAI的GPT-3 API进行聊天

    :param prompt: 聊天内容
    :param wait_all: 是否等待所有内容
    :param no_record: 是否不记录聊天内容
    """
    global _chatbot
    if _chatbot is None:
        _chatbot = create_bot(no_record=no_record)
    if wait_all:
        return _chatbot.ask(prompt)
    else:
        return _chatbot.ask_stream(prompt)
