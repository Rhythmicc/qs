"""
在终端预览图片 | 目前仅有MacOS下的iTerm可用, 你需要自行安装imgcat库

preview image on terminal | At present, only iTerm under MacOS is available,
you need to install imgcat library by yourself
"""
from imgcat import imgcat
from .. import headers


def image_preview(img, is_url=False):
    """
    在终端预览图片 | 目前仅有MacOS下的iTerm可用

    preview image on terminal | At present, only iTerm under MacOS is available

    :param is_url:
    :param img: opened file, numpy array, PIL.Image, matplotlib fig
    :return:
    """
    if is_url:
        from PIL import Image
        from io import BytesIO
        import requests
        res = requests.get(img, headers=headers).content
        img = Image.open(BytesIO(res))
    imgcat(img)
