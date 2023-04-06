from .. import requirePackage, user_lang
from . import pre_check

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
    def __init__(self):
        from .alapi import alapi_token, v2_url

        self.api_key = alapi_token
        self.url = v2_url
        self.messages = [
            {
                "role": "system",
                "content": "You are ChatGPT, a large language model trained by OpenAI. Respond conversationally with Markdown Language.",
            }
        ]

    def ask(self, prompt):
        self.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )
        res = (
            requests.post(
                self.url + "chatgpt/pro",
                json={
                    "token": self.api_key,
                    "message": self.messages,
                },
            )
            .json()
            .get("data")
            .get("content")
        )
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
            self.url + "chatgpt/pro",
            json={
                "token": self.api_key,
                "message": self.messages,
            },
            stream=True,
        )
        total_res = ""
        for line in post_stream.iter_lines():
            if not line:
                continue
            line = line.decode("utf-8")
            if line == "[DONE]":
                break
            resp: dict = json.loads(line)
            choices = resp.get("data")
            if not choices:
                continue
            delta = choices.get("content")
            if not delta:
                continue
            total_res += delta
            yield delta

        self.messages.append(
            {
                "role": "assistant",
                "content": total_res,
            }
        )


def create_bot():
    if ALAPI:
        return AlapiChatbot()
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
):
    """
    使用OpenAI的GPT-3 API进行聊天

    :param prompt: 聊天内容
    :param wait_all: 是否等待所有内容
    """
    global _chatbot
    if _chatbot is None:
        _chatbot = create_bot()
    if wait_all or ALAPI:
        return _chatbot.ask(prompt)
    else:
        return _chatbot.ask_stream(prompt)
