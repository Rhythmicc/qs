from . import pre_check, user_lang
import requests

url = pre_check("DeepLX")

def translate(text, target_lang=user_lang.lower()):
    """翻译文本"""
    if target_lang == 'en':
        target_lang = 'en-us'
    return requests.post(f"{url}/translate", json={
        'text': text,
        'source_lang': 'auto',
        'target_lang': target_lang,
    }).json()['data']
