from .. import requirePackage
from . import pre_check

ENGINE = "gpt-3.5-turbo"
API_KEY = pre_check("openai", ext=False)


_chatbot = None


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
        _chatbot = requirePackage("revChatGPT.V3", "Chatbot", "revChatGPT")(
            API_KEY, ENGINE
        ) if API_KEY else requirePackage("revChatGPT.V1", "Chatbot", "revChatGPT")(
            {
                "email": pre_check("openai-email"),
                "password": pre_check("openai-password"),
                "paid": pre_check("openai-paid"),
            }
        )
    if wait_all or not API_KEY:
        return _chatbot.ask(prompt)
    else:
        return _chatbot.ask_stream(prompt)
