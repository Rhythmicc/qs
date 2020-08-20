# coding=utf-8
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
    from QuickStart_Rhy import remove, dir_char
    remove('dist')
    if os.system('python3 setup.py sdist'):
        os.system('python setup.py sdist')
    os.system('twine upload dist%s*' % dir_char)


def m3u8_dl(url):
    """
    下载m3u8

    Download *.m3u8
    """
    from QuickStart_Rhy.NetTools.M3u8DL import M3U8DL
    M3U8DL(url, url.split('.')[-2].split('/')[-1]).download()


def download():
    """
    qs下载引擎，使用--video or -v使用youtube-dl下载视频

    Qs download engine, use --video or -v use the default video download engine download
    """
    if any([i in sys.argv for i in ['-h', '-help', '--help']]):
        from QuickStart_Rhy import user_lang
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
        from QuickStart_Rhy.NetTools.NormalDL import normal_dl
        from QuickStart_Rhy import qs_config
        for url in urls:
            if url.endswith('.m3u8'):
                m3u8_dl(url)
            else:
                if use_proxy:
                    normal_dl(url, set_proxy=qs_config['basic_settings']['default_proxy']) \
                        if not ytb_flag else _real_main([url, '--proxy', qs_config['basic_settings']['default_proxy']])
                else:
                    normal_dl(url) if not ytb_flag else _real_main([url])
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
    from QuickStart_Rhy.NetTools.HttpServer import HttpServers
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
    from QuickStart_Rhy import user_lang
    from QuickStart_Rhy.API.alapi import ip_info

    def print_ip_info(info_ls):
        table = prettytable.PrettyTable(['ip', '运营商', '地址', '经纬'])
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
