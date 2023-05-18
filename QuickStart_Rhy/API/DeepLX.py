from . import pre_check, user_lang
import requests
import random

url = pre_check("DeepLX")

if isinstance(url, list):
    _load_balancer_ = random.randint(0, len(url) - 1)

def get_url():
    """获取当前使用的API地址"""
    if isinstance(url, list):
        global _load_balancer_
        _load_balancer_ = (_load_balancer_ + 1) % len(url)
        return url[_load_balancer_]
    else:
        return url


def translate(text, target_lang=user_lang.lower()):
    """翻译文本"""
    _url = get_url()
    res = requests.post(f"{_url}/translate", json={
        'text': text,
        'source_lang': 'auto',
        'target_lang': target_lang,
    })
    if res.text.strip():
        # return res.json().get('data')
        # get json data
        try:
            return res.json().get('data')
        except Exception as e:
            from .. import qs_default_console, qs_error_string
            qs_default_console.print(qs_error_string, f"DeepLX: {_url}")
            return None
    else:
        from .. import qs_default_console, qs_error_string
        qs_default_console.print(qs_error_string, f"DeepLX: {_url}")
        return None


if __name__ == "__main__":
    print(translate("Hello world!"))
 