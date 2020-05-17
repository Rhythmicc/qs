import sys


def upgrade():
    import os
    if os.system('pip3 install QuickStart-Rhy --upgrade'):
        os.system('pip install QuickStart-Rhy --upgrade')


def upload_pypi():
    import os
    from QuickStart_Rhy import remove, dir_char
    remove('dist')
    if os.system('python3 setup.py sdist'):
        os.system('python setup.py sdist')
    os.system('twine upload dist%s*' % dir_char)


def m3u8_dl(url):
    from QuickStart_Rhy.NetTools.m3u8_dl import M3U8DL
    M3U8DL(url, url.split('.')[-2].split('/')[-1]).download()


def download():
    urls = sys.argv[2:]
    if not urls:
        import pyperclip
        urls = pyperclip.paste().split()
    if urls:
        from QuickStart_Rhy.NetTools.normal_dl import normal_dl
        for url in urls:
            if url.endswith('.m3u8'):
                m3u8_dl(url)
            else:
                normal_dl(url)
    else:
        print("No url found!")


def http():
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
