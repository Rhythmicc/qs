# coding=utf-8
"""
调用各种网络工具

Call various network tools
"""
import sys


def upgrade():
    """
    更新qs

    Upgrade qs
    """
    import os
    if os.system('pip3 install QuickStart-Rhy --upgrade'):
        os.system('pip install QuickStart-Rhy --upgrade')


def upload_pypi():
    """
    将pypi库上传

    Upload Pypi Library
    """
    import os
    from . import remove, dir_char
    remove('dist')
    if os.system('python3 setup.py sdist'):
        os.system('python setup.py sdist')
    os.system('twine upload dist%s*' % dir_char)


def m3u8_dl(url):
    """
    下载m3u8

    Download *.m3u8
    """
    from .NetTools.M3u8DL import M3U8DL
    M3U8DL(url, url.split('.')[-2].split('/')[-1]).download()


def download():
    """
    qs下载引擎，使用--video or -v使用youtube-dl下载视频

    Qs download engine, use --video or -v use the default video download engine download
    """
    if any([i in sys.argv for i in ['-h', '-help', '--help']]):
        from . import user_lang
        print('Usage: qs -dl [url...]\n'
              '  [--video] | [-v]  :-> download video (use youtube-dl)\n'
              '  [--proxy] | [-px] :-> use default proxy set in ~/.qsrc'
              if user_lang != 'zh' else
              '使用: qs -dl [链接...]\n'
              '  [--video] | [-v]  :-> 使用youtube-dl下载视频\n'
              '  [--proxy] | ]-px] :-> 使用配置表中的默认代理下载')
        return
    global _real_main
    ytb_flag = '--video' in sys.argv or '-v' in sys.argv
    use_proxy = '--proxy' in sys.argv or '-px' in sys.argv
    if ytb_flag or use_proxy:
        [sys.argv.remove(i) if i in sys.argv else None for i in ['--video', '-v', '--proxy', '-px']]
    urls = sys.argv[2:]
    if not urls:
        import pyperclip
        urls = pyperclip.paste().split()
    if urls:
        if ytb_flag:
            from youtube_dl import _real_main
        from .NetTools.NormalDL import normal_dl
        from . import qs_config
        for url in urls:
            if url.endswith('.m3u8'):
                m3u8_dl(url)
            else:
                if use_proxy:
                    normal_dl(url, set_proxy=qs_config['basic_settings']['default_proxy']) \
                        if not ytb_flag else _real_main([url, '--proxy', qs_config['basic_settings']['default_proxy'],
                                                         '--merge-output-format', 'mp4'])
                else:
                    normal_dl(url) if not ytb_flag else _real_main([url, '--merge-output-format', 'mp4'])
    else:
        print("No url found!")


def http():
    """
    开启http服务

    Turn on the http service.
    """
    url = ''
    if len(sys.argv) > 2:
        ip, port = sys.argv[2].split(':')
        port = int(port)
        if '-bind' in sys.argv:
            try:
                url = sys.argv[sys.argv.index('-bind') + 1]
                from .NetTools import formatUrl
                url = formatUrl(url)
            except IndexError:
                print('Usage: qs -ftp ip:port -bind url')
                exit(0)
    else:
        from .NetTools import get_ip
        ip = get_ip()
        port = 8000
    if not ip:
        exit('get ip failed!')
    from .NetTools.HttpServer import HttpServers
    HttpServers(ip, port, url).start()


def netinfo():
    """
    通过域名或ip查询ip信息

    Query ip information via domain name or ip.
    """
    import socket
    import pyperclip
    import prettytable
    import urllib.parse
    from . import user_lang
    from .API.alapi import ip_info

    def print_ip_info(info_ls):
        table = prettytable.PrettyTable(
            ['ip', '运营商', '地址', '经纬'] if user_lang == 'zh' else ['ip', 'isp', 'pos', 'location']
        )
        for info in info_ls:
            table.add_row([info['ip'],
                           info['isp'].strip() if 'isp' in info else '未知', info['pos'],
                           str(info['location'])[1:-1].replace("'", '')])
        print(table)

    urls = sys.argv[2:] if len(sys.argv) > 2 else []
    if not urls:
        try:
            urls += pyperclip.paste().strip().split() if not urls else []
        except :
            urls = input('Sorry, but your system is not supported by `pyperclip`\nSo you need input content manually: '
                         if user_lang != 'zh' else '抱歉，但是“pyperclip”不支持你的系统\n，所以你需要手动输入内容:')\
                .strip().split()
    if not urls:
        urls.append('me')
    res_ls = []
    for i in urls:
        try:
            addr = ''
            if i != 'me':
                if '://' in i:
                    protocol, domain = i[:i.index('://')], urllib.parse.urlparse(i).netloc
                    addr = socket.getaddrinfo(domain, protocol)[0][-1][0]
                else:  # 无网络协议或直接使用IP地址时默认采用http
                    addr = urllib.parse.urlparse(i).netloc
                    addr = socket.getaddrinfo(addr if addr else i, 'http')[0][-1][0]
            res_ls.append(ip_info(addr))
        except:
            print('[ERROR] Get domain failed:', i)
            continue
    print_ip_info(res_ls)


def wifi():
    """
    扫描附近wifi，选择连接

    Scan nearby wifi and select connection

    :return:
    """
    from . import system, user_lang
    from prettytable import PrettyTable
    if system.lower() != 'darwin':
        from .NetTools.WiFi import WiFi
    else:
        from .NetTools.WiFiDarwin import WiFi
    _wifi = WiFi()
    table = PrettyTable(['id', 'ssid', 'signal', 'lock'] if user_lang != 'zh' else ['序号', '名称', '信号', '加密'])
    connectable_wifi = _wifi.scan()
    if not connectable_wifi:
        print("No available wifi" if user_lang != 'zh' else '没有可用的wifi')
        return

    from PyInquirer import prompt
    from prompt_toolkit.validation import Validator, ValidationError

    class ssidValidator(Validator):
        def validate(self, document):
            document = document.text
            try:
                if int(document) >= len(connectable_wifi):
                    raise IndexError
            except:
                raise ValidationError(message='请输入合法序号' if user_lang == 'zh' else 'Input validate id', cursor_position=len(document))
            return True

    questions = [{
        'type': 'input',
        'name': 'ssid',
        'message': '选择序号以连接:' if user_lang == 'zh' else 'Choose id to connect:',
        'validate': ssidValidator
    }, {
        'type': 'password',
        'name': 'password',
        'message': '输入密码:' if user_lang == 'zh' else 'Input password:'
    }]

    for i, l in enumerate(connectable_wifi):
        table.add_row([i] + l)
    print(table)

    res = prompt(questions)
    if not res:
        return
    ssid = connectable_wifi[int(res['ssid'])]
    password = res['password']
    print('Connect succeed' if user_lang != 'zh' else '连接成功') \
        if _wifi.conn(ssid, password) else print('Connect failed' if user_lang != 'zh' else '连接失败')
