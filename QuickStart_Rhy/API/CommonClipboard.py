# coding=utf-8
"""
通过网络硬盘的本地文件系统实现的共享剪切板

Shared cutting board realized by local file system of network hard disk
"""
from . import pre_check
from .. import requirePackage
pyperclip = requirePackage('pyperclip')


class CommonClipboard:
    def __init__(self, path: str = pre_check('commonClipboardFilePath')):
        """
        通过网络硬盘的本地文件系统实现的共享剪切板

        Shared cutting board realized by local file system of network hard disk

        :param path: 用于设备间沟通的共享文件路径
        """
        self.path = path

    def get_msg(self):
        """
        获取信息到剪切板

        Get the information to the clipboard

        :return: None
        """
        with open(self.path, 'rb') as f:
            try:
                pyperclip.copy(f.read().decode('utf-8'))
            except pyperclip.PyperclipException:
                from .. import open_file
                open_file([self.path])

    def post_msg(self, msg: str = pyperclip.paste()):
        """
        发送信息

        Get the information to the clipboard

        :param msg: 信息内容（缺省时使用粘贴板中的内容）
        :return: None
        """
        if not msg:
            raise IndexError
        with open(self.path, 'wb') as f:
            f.write(msg.encode('utf-8'))
