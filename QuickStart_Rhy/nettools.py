import sys
import signal
from QuickStart_Rhy.NetTools.basic import get_ip
from QuickStart_Rhy.basic import deal_ctrl_c


def upgrade():
    import os
    if os.system('pip3 install QuickStart-Rhy --upgrade'):
        os.system('pip install QuickStart-Rhy --upgrade')


def upload_pypi():
    import os
    from QuickStart_Rhy.basic import remove, dir_char
    remove('dist')
    if os.system('python3 setup.py sdist bdist_wheel'):
        os.system('python setup.py sdist bdist_wheel')
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


def ftp():
    ip = get_ip()
    if not ip:
        exit('get ip failed!')
    print('starting ftp simple server: address http://%s:8000/' % ip)
    import http.server
    Handler = http.server.SimpleHTTPRequestHandler
    import socketserver
    host = (ip, 8000)
    with socketserver.TCPServer(host, Handler) as httpd:
        signal.signal(signal.SIGINT, deal_ctrl_c)
        httpd.serve_forever()
