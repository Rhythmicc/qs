import requests
from requests.exceptions import RequestException
from QuickStart_Rhy import headers


def check_one_page(url):
    try:
        response = requests.head(url, headers=headers).status_code
        return response == requests.codes.ok
    except RequestException:
        return False


def formatUrl(try_url):
    if try_url.startswith('http://') or try_url.startswith('https://'):
        return try_url
    res_url = try_url
    if not check_one_page(res_url):
        res_url = 'https://' + try_url
        if not check_one_page(res_url):
            res_url = 'http://' + try_url
    return res_url


def get_ip():
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
    if sz >= 1e9:
        return '%.3f GB' % (sz / 1e9) if not align else '%7.3f GB' % (sz / 1e9)
    elif sz >= 1e6:
        return '%.3f MB' % (sz / 1e6) if not align else '%7.3f MB' % (sz / 1e6)
    elif sz >= 1e3:
        return '%.3f KB' % (sz / 1e3) if not align else '%7.3f KB' % (sz / 1e3)
    else:
        return '%.2f B' % sz if not align else '%7.2f B' % sz


def get_ip_info():
    import json
    res = requests.get('http://ip-api.com/json/', headers=headers)
    if res.status_code == requests.codes.ok:
        return json.loads(res.text)
    else:
        return None


def get_fileinfo(url):
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
