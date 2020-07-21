import sys


def upgrade():
    """更新qs"""
    import os
    if os.system('pip3 install QuickStart-Rhy --upgrade'):
        os.system('pip install QuickStart-Rhy --upgrade')


def upload_pypi():
    """将pypi库上传"""
    import os
    from QuickStart_Rhy import remove, dir_char
    remove('dist')
    if os.system('python3 setup.py sdist'):
        os.system('python setup.py sdist')
    os.system('twine upload dist%s*' % dir_char)


def m3u8_dl(url):
    """下载m3u8"""
    from QuickStart_Rhy.NetTools.m3u8_dl import M3U8DL
    M3U8DL(url, url.split('.')[-2].split('/')[-1]).download()


def download():
    """qs下载引擎，使用--ytb使用youtube-dl下载视频"""
    ytb_flag = '--ytb' in sys.argv
    if ytb_flag:
        sys.argv.remove('--ytb')
    urls = sys.argv[2:]
    if not urls:
        import pyperclip
        urls = pyperclip.paste().split()
    if urls:
        if ytb_flag:
            from youtube_dl import _real_main
        from QuickStart_Rhy.NetTools.normal_dl import normal_dl
        for url in urls:
            if url.endswith('.m3u8'):
                m3u8_dl(url)
            else:
                normal_dl(url) if not ytb_flag else _real_main([url])
    else:
        print("No url found!")


def http():
    """开启http服务"""
    url = ''
    if len(sys.argv) > 2:
        ip, port = sys.argv[2].split(':')
        port = int(port)
        if '-bind' in sys.argv:
            try:
                url = sys.argv[sys.argv.index('-bind') + 1]
                from QuickStart_Rhy.NetTools import formatUrl
                url = formatUrl(url)
            except IndexError:
                print('Usage: qs -ftp ip:port -bind url')
                exit(0)
    else:
        from QuickStart_Rhy.NetTools import get_ip
        ip = get_ip()
        port = 8000
    if not ip:
        exit('get ip failed!')
    from QuickStart_Rhy.NetTools.server import HttpServers
    HttpServers(ip, port, url).start()


def netinfo():
    """通过域名或ip查询ip信息"""
    import json
    import socket
    import requests
    import pyperclip
    import prettytable
    import urllib.parse
    from QuickStart_Rhy import headers

    def print_ip_info(info_ls):
        table = prettytable.PrettyTable(['ip', '运营商', '地址', '经纬'])
        for info in info_ls:
            table.add_row([info['ip'],
                           info['isp'] if 'isp' in info else '未知', info['pos'],
                           str(info['location'])[1:-1].replace("'", '')])
        print(table)

    urls = sys.argv[2:] if len(sys.argv) > 2 else []
    if not urls:
        try:
            urls += pyperclip.paste().strip().split() if not urls else []
        except :
            urls = input('Sorry, but your system is not supported by `pyperclip`\nSo you need input urls manually: ')\
                .strip().split()
    if not urls:
        urls.append('me')
    res_ls = []
    for i in urls:
        try:
            addr = ''
            if i != 'me':
                addr = urllib.parse.urlparse(i).netloc
                addr = socket.getaddrinfo(addr if addr else i, 'http')[0][-1][0]
            res = requests.post('https://v1.alapi.cn/api/ip', data="ip=%s&format=json" % addr,
                                headers={'Content-Type': "application/x-www-form-urlencoded"} if addr else headers)
            res = json.loads(res.text)['data']
            res_ls.append(res)
        except:
            print('[ERROR] Get domain failed:', i)
            continue
    print_ip_info(res_ls)
