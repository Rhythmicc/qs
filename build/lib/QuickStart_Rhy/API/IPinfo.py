from QuickStart_Rhy.API import pre_check
import ipinfo


def get_ip_info(ip: str = None):
    handler = ipinfo.getHandler(pre_check('ipinfo'))
    res = handler.getDetails(ip)
    return res.all
