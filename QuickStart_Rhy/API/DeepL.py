"""
DeepL 翻译 API
"""

import requests
from . import pre_check
from .. import user_lang


_token = pre_check("DeepL")


def translate(text, target_lang=user_lang.upper()):
    """翻译文本"""
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": _token,
        "text": text,
        "target_lang": target_lang,
    }
    res = requests.get(url, params=params)
    return res.json()["translations"][0]["text"]
