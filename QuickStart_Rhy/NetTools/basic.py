import requests
from requests.exceptions import RequestException
from QuickStart_Rhy.basic import headers


def check_one_page(url):
    try:
        response = requests.get(url, headers=headers).status_code
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