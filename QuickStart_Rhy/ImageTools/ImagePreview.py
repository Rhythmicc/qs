"""
在终端预览图片 | 目前仅有MacOS下的iTerm可用, 你需要自行安装imgcat库

preview image on terminal | At present, only iTerm under MacOS is available,
you need to install imgcat library by yourself
"""
from .. import headers, requirePackage
imgcat = requirePackage('imgcat', 'imgcat')


def image_preview(img, is_url=False, set_proxy: str = '', set_referer: str = '', qs_console_status=None):
    """
    在终端预览图片 | 目前仅有MacOS下的iTerm可用

    preview image on terminal | At present, only iTerm under MacOS is available

    :param is_url:
    :param img: opened file, numpy array, PIL.Image, matplotlib fig
    :param set_proxy: set proxy
    :param set_referer: set refer
    :param qs_console_status:
    :return:
    """
    try:
        if not is_url and isinstance(img, str):
            is_url = img.startswith('http')
        if is_url:
            from PIL import Image
            from io import BytesIO
            import requests
            if set_referer:
                headers['referer'] = set_referer
            proxies = {
                'http': 'http://' + set_proxy,
                'https': 'https://' + set_proxy
            } if set_proxy else {}
            res = requests.get(img, headers=headers, proxies=proxies).content
            if qs_console_status:
                qs_console_status.update(status='Opening')
            img = Image.open(BytesIO(res))
        if qs_console_status:
            qs_console_status.stop()
        imgcat(img)
    except Exception as e:
        if qs_console_status:
            from .. import qs_default_console, qs_error_string
            qs_default_console.print(qs_error_string, repr(e))
            qs_console_status.stop()
        return
