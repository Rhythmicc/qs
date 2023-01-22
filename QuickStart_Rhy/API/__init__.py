# coding=utf-8
"""
qs的API模块, 使用前确保配置文件~/.qsrc中已经配置相关的KEY值

Before using the API module of QS, make sure that the relevant key value has been configured in the configuration file ~/.qsrc
"""
from .. import qs_config, user_lang, user_root, qs_default_console, qs_error_string


def pre_check(*keys, ext: bool = True) -> str:
    """
    获取用户保存的API KEY

    Gets the API KEY saved by the user.

    :param funcName: API KEY在~/.qsrc的名称 | API KEY in the name of the .qsrc.
    :param ext: 获取失败是否退出程序 | Get failed whether to exit the program

    :return: 找到的API KEY | API KEY found.
    """
    res = []
    for key in keys:
        try:
            _val = qs_config.apiSelect(key)
            if _val.startswith("GET:"):
                raise KeyError
        except KeyError:
            if ext:
                qs_default_console.print(
                    qs_error_string,
                    'You should set "%s" api key at: %s/.qsrc' % (key, user_root)
                    if user_lang != "zh"
                    else '你需要在qs的配置表 %s/.qsrc 中填入 "%s" 键值' % (user_root, key),
                )
                if _val:
                    from .. import qs_info_string

                    qs_default_console.print(
                        qs_info_string,
                        "How to get it:" if user_lang != "zh" else "如何获取:",
                        _val.split()[-1],
                    )
                exit(-1)
            else:
                _val = None
        res.append(_val)
    return res if len(res) > 1 else res[0]
