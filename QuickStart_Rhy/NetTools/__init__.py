# coding=utf-8
"""
qs的网络工具库

The network tool library of QS
"""
import socket
import requests
from requests.exceptions import RequestException
from typing import Tuple


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) "
    "Version/11.0.2 Safari/604.4.7"
}


def is_ipv4(ip: str) -> bool:
    """
    判断ip是否为可连接的ipv4

    Determine whether the IP is a connectable IPv4
    :param ip: like 8.8.8.8 etc.
    :return: bool
    """
    try:
        socket.inet_pton(socket.AF_INET, ip)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(ip)
        except socket.error:
            return False
        return ip.count(".") == 3
    except socket.error:  # not a valid ip
        return False
    return True


def is_ipv6(ip: str) -> bool:
    """
    判断ip是否为可连接的ipv6

    Determine whether the IP is a connectable IPv6
    :param ip: like fe80::1862:5a79:a8a0:aae5 etc.
    :return: bool
    """
    try:
        socket.inet_pton(socket.AF_INET6, ip)
    except socket.error:  # not a valid ip
        return False
    return True


def is_ip(ip: str) -> bool:
    """
    判断ip是否为可连接的

    Determine whether the IP is a connectable
    :param ip: like fe80::1862:5a79:a8a0:aae5, 8.8.8.8 etc.
    :return: bool
    """
    if ip == "localhost":
        return True
    return is_ipv4(ip) or is_ipv6(ip)


def is_mac(addr: str) -> bool:
    """
    检查addr是否为mac地址

    Check whether addr is a mac address

    :param addr: string like '80:8f:1d:e2:f2:f5'
    :return: bool
    """
    part = addr.split(":")
    if len(part) != 6:
        return False
    for i in part:
        if len(i) != 2:
            return False
        for j in i:
            if j not in "0123456789abcdefABCDEF":
                return False
    return True


def check_one_page(url: str) -> bool:
    """
    检查url是否可访问

    Check that the URL is accessible

    :param url: url
    :return: True或False
    """
    try:
        response = requests.head(url, headers=headers).status_code
        return response == requests.codes.ok
    except RequestException:
        return False


def formatUrl(try_url: str) -> str:
    """
    为url添加https或http使其能被访问

    Add HTTPS or HTTP to the URL to make it accessible

    :param try_url: 待尝试的url
    :return: 能被成功访问的url
    """
    if try_url.startswith("http://") or try_url.startswith("https://"):
        return try_url
    res_url = try_url
    if not check_one_page(res_url):
        res_url = "https://" + try_url
        if not check_one_page(res_url):
            res_url = "http://" + try_url
    return res_url


def open_url(url: str):
    """
    使用默认浏览器打开url

    Open url using the default browser

    :param url:
    :return:
    """
    import webbrowser as wb

    url = formatUrl(url)
    wb.open_new_tab(url)


def get_ip() -> str:
    """
    获取本机ip

    Get native IP

    :return: ip
    """
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        return ip
    except Exception:
        s.close()
        return socket.gethostbyname(socket.gethostname())


def size_format(sz: int, align: bool = False) -> str:
    """
    格式化文件大小显示

    Format file size display

    :param sz: 整数，表示文件大小
    :param align: 是否对齐
    :return: 文件大小字符串
    """
    if sz >= 1e9:
        return "%.3f GB" % (sz / 1e9) if not align else "%7.3f GB" % (sz / 1e9)
    elif sz >= 1e6:
        return "%.3f MB" % (sz / 1e6) if not align else "%7.3f MB" % (sz / 1e6)
    elif sz >= 1e3:
        return "%.3f KB" % (sz / 1e3) if not align else "%7.3f KB" % (sz / 1e3)
    else:
        return "%.2f B" % sz if not align else "%7.2f B" % sz


def get_ip_info() -> dict:
    """
    通过ip-api获取本机ip信息

    Get native IP information through IP-API

    :return: ip信息的dict，失败返回None
    """
    import json

    res = requests.get("http://ip-api.com/json/", headers=headers)
    if res.status_code == requests.codes.ok:
        return json.loads(res.text)
    else:
        return {}


def get_fileinfo(
    url: str, proxy: str = "", referer: str = ""
) -> Tuple[str, str, requests.Response]:
    """
    获取待下载的文件信息

    Gets information about the file to be downloaded

    :param url: 文件url
    :param proxy: 代理
    :param referer: 绕反爬
    :return: 真实url，文件名，http头部信息 (headers中键值均为小写)
    """
    import re
    import os

    proxies = {"http": "http://" + proxy, "https": "https://" + proxy} if proxy else {}
    if referer:
        headers["referer"] = referer
    try:
        res = requests.head(url, headers=headers, proxies=proxies)
        if res.status_code == 404:
            return url, "", res  # 某些网站会返回404，但是文件还是可以下载的
    except Exception as e:
        return "", repr(e), None
    while res.status_code in [301, 302]:
        url = {i[0]: i[1] for i in res.headers.lower_items()}["location"]
        res = requests.head(url, headers=headers, proxies=proxies)
    res.headers = {i[0]: i[1] for i in res.headers.lower_items()}
    if "content-disposition" in res.headers:
        try:
            filename = re.findall(
                "filename=(.*?);", res.headers["content-disposition"]
            )[0]
        except IndexError:
            from urllib.parse import urlparse

            filename = os.path.basename(urlparse(url).path.strip("/"))
    else:
        from urllib.parse import urlparse

        filename = os.path.basename(urlparse(url).path.strip("/"))
    return url, re.sub(r"^\W+|\W+$", "", filename), res
