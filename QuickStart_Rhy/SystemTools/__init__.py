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
    from .. import platform, external_exec

    if platform.startswith("win"):
        print("Not support")
    else:
        if platform.startswith("darwin"):
            external_exec("sudo purge")
        else:
            external_exec("sync")
            external_exec("echo 3 > /proc/sys/vm/drop_caches")


def get_core_num():
    """
    获取核数量

    :return: core num
    """
    from .. import requirePackage

    return requirePackage("psutil").cpu_count()


def file_suffix(file_name):
    """
    获取文件后缀

    :param file_name: 文件名
    :return: 后缀
    """
    return file_name.split(".")[-1]
