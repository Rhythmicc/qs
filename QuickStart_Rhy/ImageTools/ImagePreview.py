from imgcat import imgcat


def image_preview(img, is_url=False):
    """
    在终端预览图片

    preview image on terminal

    :param is_url:
    :param img: opened file, numpy array, PIL.Image, matplotlib fig
    :return:
    """
    if is_url:
        from PIL import Image
        from io import BytesIO
        import requests
        res = requests.get(img).content
        img = Image.open(BytesIO(res))
    imgcat(img)
