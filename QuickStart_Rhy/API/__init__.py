from QuickStart_Rhy import dir_char
import json
import os


user_root = os.path.expanduser('~') + dir_char
if os.path.exists(user_root + '.qsrc'):
    with open(user_root + '.qsrc', 'r', encoding='utf8') as f:
        qsconfig = json.loads(f.read(), encoding='utf8')
else:
    with open(user_root + '.qsrc', 'w') as f:
        f.write('{\n'
                '  "rmbg": "GET API KEY: https://www.remove.bg",\n'
                '  "smms": "GET API KEY: https://sm.ms"\n'
                '}')
    qsconfig = {}


def pre_check(funcName: str, ext=True):
    """
    获取用户保存的API KEY

    :param funcName: API KEY在~/.qsrc的名称
    :param ext: 获取失败是否退出程序（默认退出）

    :return: 找到的API KEY
    """
    try:
        api_key = qsconfig[funcName]
        if not api_key:
            exit('You should set %s api key at: %s' % (funcName, user_root + dir_char + '.qsrc'))
    except KeyError:
        if ext:
            exit('You should set %s api key at: %s' % (funcName, user_root + dir_char + '.qsrc'))
        else:
            return False
    else:
        return api_key
