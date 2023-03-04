from . import pre_check, user_lang
import requests

url = pre_check("DeepLX")

def translate(text, target_lang=user_lang.lower()):
    """翻译文本"""
    res = requests.post(f"{url}/translate", json={
        'text': text,
        'source_lang': 'auto',
        'target_lang': target_lang,
    })
    if res.text.strip():
        return res.json().get('data')
    else:
        return None


if __name__ == "__main__":
    print(translate("Hello world!"))
 