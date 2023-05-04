"""
本模块提供了一些使用numba包的工具，会引导用户安装numba包，如果用户没有安装numba包，会自动跳过使用numba包的功能

This module provides some tools using the numba package, which will guide the user to install the numba package. If the user does not install the numba package, the function using the numba package will be skipped automatically
"""

from .. import requirePackage
jit = requirePackage("numba", "jit")
function_cache = {}

def cut_string(string: str, length: int, ignore_charset: list = []) -> list:
    """
    每隔l个字符切分字符串
    引用numba包会有额外的代价, 但是速度会快很多

    :param string: 字符串
    :param length: 切分长度
    :param ignore_charset: 忽略的字符集
    :return: 切分后产生的list
    """
    if 'cut_string' not in function_cache:
        function_cache['cut_string'] = jit(requirePackage(".", "cut_string"), nopython=True) if jit else requirePackage(".", "cut_string")
    return function_cache['cut_string'](string, length, ignore_charset)
