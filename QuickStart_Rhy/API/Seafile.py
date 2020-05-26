from QuickStart_Rhy.API import pre_check
import pyperclip


class Seafile:
    def __init__(self, path=pre_check('seafile_communicate_path')):
        self.path = path

    def get_msg(self):
        with open(self.path, 'rb') as f:
            pyperclip.copy(f.read().decode('utf-8'))

    def post_msg(self, msg=pyperclip.paste()):
        if not msg:
            raise IndexError
        with open(self.path, 'wb') as f:
            f.write(msg.encode('utf-8'))
