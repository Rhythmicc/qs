# coding=utf-8
from QuickStart_Rhy import *


def pre_check(funcName: str, ext: bool = True) -> str:
    """
    获取用户保存的API KEY

    Gets the API KEY saved by the user.

    :param funcName: API KEY在~/.qsrc的名称 | API KEY in the name of the .qsrc.
    :param ext: 获取失败是否退出程序 | Get failed whether to exit the program

    :return: 找到的API KEY | API KEY found.
    """
    try:
        api_key = qs_config['API_settings'][funcName]
        if api_key.startswith("GET:"):
            raise KeyError
    except KeyError:
        if ext:
            exit('You should set %s api key at: %s.qsrc' % (funcName, user_root)
                 if user_lang != 'zh' else '你需要在qs的配置表 %s.qsrc 中填入设%s键值' % (user_root, funcName))
        else:
            return ''
    else:
        return api_key
