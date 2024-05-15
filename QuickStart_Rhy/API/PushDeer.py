from . import pre_check
from .. import requirePackage

pushdeer_api_info = pre_check('pushdeer')

server = pushdeer_api_info["url"]
key = pushdeer_api_info['key']
pushdeer = requirePackage('pypushdeer', 'PushDeer')(server=server, pushkey=key)


def send_text(text):
    """
    推送文本消息
    :param text: 文本内容
    :return:
    """
    return pushdeer.send_text(text)


def send_image(image_path):
    """
    推送图片消息
    :param image_path: 图片路径
    :return:
    """
    return pushdeer.send_image(image_path)

def send_markdown(content):
    """
    推送Markdown消息
    :param title: 标题
    :param content: 内容
    :return:
    """
    return pushdeer.send_markdown(content)
