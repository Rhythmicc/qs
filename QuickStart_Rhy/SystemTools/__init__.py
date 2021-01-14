# coding=utf-8
"""
系统工具库

System tool library
"""


def clear_mem():
    """
    清理系统内存

    Clean system memory

    :return: None
    """
    from .. import dir_char, system

    if dir_char == '\\':
        print("Not support")
    else:
        import os
        if system.startswith("darwin"):
            os.system("sudo purge")
        else:
            os.system('sync')
            os.system("echo 3 > /proc/sys/vm/drop_caches")
