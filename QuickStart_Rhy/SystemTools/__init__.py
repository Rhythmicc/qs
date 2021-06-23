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


def get_core_num():
    """
    获取核数量

    :return: core num
    """
    from .. import requirePackage
    return requirePackage('psutil').cpu_count()
