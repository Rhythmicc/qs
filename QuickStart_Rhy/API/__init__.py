# coding=utf-8
"""
qs的API模块, 使用前确保配置文件~/.qsrc中已经配置相关的KEY值

Before using the API module of QS, make sure that the relevant key value has been configured in the configuration file ~/.qsrc
"""
from .. import qs_config, user_lang, user_root, dir_char, system, headers


def pre_check(funcName: str, ext: bool = True) -> str:
    """
    获取用户保存的API KEY

    Gets the API KEY saved by the user.

    :param funcName: API KEY在~/.qsrc的名称 | API KEY in the name of the .qsrc.
    :param ext: 获取失败是否退出程序 | Get failed whether to exit the program

    :return: 找到的API KEY | API KEY found.
    """
    try:
        api_key = qs_config.apiSelect(funcName)
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
