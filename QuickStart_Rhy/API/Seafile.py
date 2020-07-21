from QuickStart_Rhy.API import pre_check
import pyperclip


class Seafile:
    def __init__(self, path=pre_check('seafile_communicate_path')):
        """
        利用Seafile实现的共享剪切板

        :param path: 用于设备间沟通的共享文件路径
        """
        self.path = path

    def get_msg(self):
        """
        获取信息到剪切板

        :return: None
        """
        with open(self.path, 'rb') as f:
            try:
                pyperclip.copy(f.read().decode('utf-8'))
            except pyperclip.PyperclipException:
                from QuickStart_Rhy import open_file
                open_file([self.path])

    def post_msg(self, msg=pyperclip.paste()):
        """
        发送信息

        :param msg: 信息内容（缺省时使用粘贴板中的内容）
        :return: None
        """
        if not msg:
            raise IndexError
        with open(self.path, 'wb') as f:
            f.write(msg.encode('utf-8'))
