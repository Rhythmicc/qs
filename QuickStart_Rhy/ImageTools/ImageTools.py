from PIL import Image


def topng(imgPath: str):
    """
    将图片路径所指的图片转为jpg格式

    transform image to jpg

    :param imgPath: 图片路径 | image path
    :return:
    """
    Image.open(imgPath).save(imgPath + '.png', quality=100)


def tojpg(imgPath: str):
    """
    将图片路径所指的图片转为jpg格式

    transform image to jpg

    :param imgPath: 图片路径 | image path
    :return:
    """
    Image.open(imgPath).convert("RGB").save(imgPath + '.jpg', quality=100)
