from QuickStart_Rhy.API import pre_check
import ipinfo


def get_ip_info(ip: str = None):
    """
    利用ipinfo查询ip信息（需申请API KEY，但定位效果并不好）

    :param ip: 待查询的ip
    :return: ip信息（dict）
    """
    handler = ipinfo.getHandler(pre_check('ipinfo'))
    res = handler.getDetails(ip)
    return res.all
