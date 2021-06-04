# coding=utf-8
"""
利用ipinfo查询ip信息 (需申请API KEY，但定位效果并不好), PR迷之自信

Use IPInfo to query IP information (need to apply API KEY, but the positioning effect is not good),
but Product manager's confidence
"""
from . import pre_check
from .. import requirePackage
ipinfo = requirePackage('ipinfo')


def get_ip_info(ip: str = None):
    """
    利用ipinfo查询ip信息 (需申请API KEY，定位效果并不好, 但PR迷之自信)

    Use IPInfo to query IP information (need to apply API KEY, but the positioning effect is not good),
    but Product manager's confidence

    :param ip: 待查询的ip
    :return: ip信息（dict）
    """
    handler = ipinfo.getHandler(pre_check('ipinfo'))
    res = handler.getDetails(ip)
    return res.all
