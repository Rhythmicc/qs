import requests
from requests.exceptions import RequestException
from QuickStart_Rhy import headers


def check_one_page(url):
    """
    检查url是否可访问

    :param url: url
    :return: True或False
    """
    try:
        response = requests.head(url, headers=headers).status_code
        return response == requests.codes.ok
    except RequestException:
        return False


def formatUrl(try_url):
    """
    为url添加https或http使其能被访问

    :param try_url: 待尝试的url
    :return: 能被成功访问的url
    """
    if try_url.startswith('http://') or try_url.startswith('https://'):
        return try_url
    res_url = try_url
    if not check_one_page(res_url):
        res_url = 'https://' + try_url
        if not check_one_page(res_url):
            res_url = 'http://' + try_url
    return res_url


def get_ip():
    """
    获取本机ip

    :return: ip
    """
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        return ip
    except Exception:
        s.close()
        return socket.gethostbyname(socket.gethostname())


def size_format(sz, align=False):
    """
    格式化文件大小显示

    :param sz: 整数，表示文件大小
    :param align: 是否对齐
    :return: 文件大小字符串
    """
    if sz >= 1e9:
        return '%.3f GB' % (sz / 1e9) if not align else '%7.3f GB' % (sz / 1e9)
    elif sz >= 1e6:
        return '%.3f MB' % (sz / 1e6) if not align else '%7.3f MB' % (sz / 1e6)
    elif sz >= 1e3:
        return '%.3f KB' % (sz / 1e3) if not align else '%7.3f KB' % (sz / 1e3)
    else:
        return '%.2f B' % sz if not align else '%7.2f B' % sz


def get_ip_info():
    """
    通过ip-api获取本机ip信息

    :return: ip信息的dict，失败返回None
    """
    import json
    res = requests.get('http://ip-api.com/json/', headers=headers)
    if res.status_code == requests.codes.ok:
        return json.loads(res.text)
    else:
        return None


def get_fileinfo(url):
    """
    获取待下载的文件信息

    :param url: 文件url
    :return: 真实url，文件名，http头部信息
    """
    import re
    import os
    try:
        res = requests.head(url, headers=headers)
    except:
        return False, False, False
    while res.status_code == 302 or res.status_code == 301:
        url = res.headers['Location']
        res = requests.head(url, headers=headers)
    if 'Content-Disposition' in res.headers:
        try:
            filename = re.findall('filename=(.*?);', res.headers['Content-Disposition'])[0]
        except IndexError:
            from urllib.parse import urlparse
            filename = os.path.basename(urlparse(url).path.strip('/'))
    else:
        from urllib.parse import urlparse
        filename = os.path.basename(urlparse(url).path.strip('/'))
    return url, re.sub(r"^\W+|\W+$", "", filename), res
