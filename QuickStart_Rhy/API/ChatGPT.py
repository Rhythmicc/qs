from .. import requirePackage
from . import pre_check

_openai = None


def chatGPT(
    prompt: str,
):
    """
    使用OpenAI的GPT-3 API进行聊天
    """
    global _openai
    if _openai is None:
        _openai = requirePackage("openai")
        _openai.api_key = pre_check("openai")
    response = _openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        temperature=0.5,
    )
    return response["choices"][0]["text"].strip()
