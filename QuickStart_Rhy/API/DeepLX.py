from . import pre_check, user_lang
import requests
import random

url = pre_check("DeepLX", ext=False)

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
    from .. import qs_default_console

    if url:
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
                data = res.json().get('data')
                if not data:
                    from .. import qs_default_console, qs_error_string
                    qs_default_console.print(qs_error_string, f"DeepLX: {_url}")
                    return None
                return data.strip()
            except Exception as e:
                from .. import qs_default_console, qs_error_string
                qs_default_console.print(qs_error_string, f"DeepLX: {_url}")
                return None
        else:
            from .. import qs_default_console, qs_error_string
            qs_default_console.print(qs_error_string, f"DeepLX: {_url}")
            return None
    else:
        from .. import requirePackage

        translator = requirePackage("PyDeepLX", "PyDeepLX")
        if translator:
            return translator.translate(text, targetLang=target_lang)
        else:
            from .. import qs_default_console, qs_error_string
            qs_default_console.print(qs_error_string, "Get PyDeepLX failed!")
            return None

def available():
    """检查API是否可用"""
    for _ in range(len(url)):
        print(translate("Passed!"))

if __name__ == "__main__":
    # print(translate("Hello world!"))
    available()
