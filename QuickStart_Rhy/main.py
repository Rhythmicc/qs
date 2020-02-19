import webbrowser as wb
import requests
from requests.exceptions import RequestException
import threading
import sys
import os
import signal


def deal_ctrl_c(signum, frame):
    if signum or frame or True:
        exit(0)


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) '
                  'Version/11.0.2 Safari/604.4.7'}

system = sys.platform
base_dir = sys.path[0]
color_flag = False
if system.startswith('win'):
    dir_char = '\\'
    color_flag = True
else:
    dir_char = '/'
base_dir += dir_char
arlen = len(sys.argv)


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


def h():
    import colorama

    def color_rep(ss):
        global color_flag
        if color_flag:
            colorama.init()
            color_flag = False
        ss = ss.split(':->')
        return colorama.Fore.LIGHTMAGENTA_EX + ss[0] + colorama.Style.RESET_ALL + \
            ':->' + colorama.Fore.YELLOW + ss[1] + colorama.Style.RESET_ALL

    print('help:')
    print(color_rep('    qs -u  [url]             :-> open url using default browser'))
    print(color_rep('    qs -a  [app/(file...)]   :-> open app or open file by app(for Mac OS X)'))
    print(color_rep('    qs -f  [file...]         :-> open file by default app'))
    print(color_rep('    qs -dl [urls/""]         :-> download file from url(in clipboard)'))
    print(color_rep('    qs -trans [content]      :-> translate the content(in clipboard)'))
    print(color_rep('    qs -time                 :-> view current time'))
    print(color_rep('    qs -ftp                  :-> start a simple ftp server'))
    print(color_rep('    qs -top                  :-> cpu and memory monitor'))
    print(color_rep('    qs -weather [address]    :-> check weather (of address)'))
    print(color_rep('    qs -mktar [path]         :-> create gzipped archive for path'))
    print(color_rep('    qs -untar [path]         :-> extract path.tar.*'))
    print(color_rep('    qs -mkzip [path]         :-> make a zip for path'))
    print(color_rep('    qs -unzip [path]         :-> unzip path.zip'))
    print(color_rep('    qs -upload               :-> upload your pypi library'))
    print(color_rep('    qs -upgrade              :-> update qs'))
    print(color_rep('    qs -pyuninstaller [path] :-> remove files that pyinstaller create'))


def check_one_page(url):
    try:
        response = requests.get(url, headers=headers).status_code
        return response == 200
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


def remove(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            import shutil
            shutil.rmtree(path)
        else:
            os.remove(path)


def get_tar_name():
    if arlen == 2:
        exit("No enough parameters")
    file_names = sys.argv[2:]
    if len(file_names) > 1:
        tar_name = 'pigeonhole'
    else:
        ls = file_names[0].split(dir_char)
        while not ls[-1]:
            ls.pop()
        tar_name = ls[-1].split('.')[0]
    ls = []
    for file_name in file_names:
        if os.path.exists(file_name):
            ls.append(file_name)
        else:
            print("No such file or dictionary:%s" % file_name)
    return tar_name, ls


def u():
    for url in sys.argv[2:]:
        url = formatUrl(url)
        wb.open_new_tab(url)


def open_app():
    if system == 'darwin':
        os.system('open -a ' + ' '.join(sys.argv[2:]))
    else:
        print('"-a" is only support Mac OS X')


def open_file():
    if system == 'darwin':
        os.system('open "' + '" "'.join(sys.argv[2:]) + '"')
    else:
        for file in sys.argv[2:]:
            if os.path.exists(file):
                path = os.path.abspath(file)
                wb.open('file://%s' % path)


def init():
    wb.open('http://login.cup.edu.cn')


def translate():
    import pyperclip
    from QuickStart_Rhy.Dict import Dict

    content = ' '.join(sys.argv[2:])
    if not content:
        content = pyperclip.paste()
    if content:
        content.replace('\n', ' ')
        translator = Dict()
        ret = translator.dictionary(content)
        print(ret['trans_result']['data'][0]['dst'])
    else:
        print("No content in your clipboard or command parameters!")


def cur_time():
    week = {
        'Monday': '周一',
        'Tuesday': '周二',
        'Wednesday': '周三',
        'Thursday': '周四',
        'Friday': '`周五',
        'Saturday': '周六',
        'Sunday': '周日'
    }
    import time
    tm = time.strftime('%Y-%m-%d %A %H:%M:%S', time.localtime(time.time())).split()
    ls = tm[0].split('-')
    tm[0] = ls[0] + '年' + ls[1] + '月' + ls[2] + '日'
    tm[1] = week[tm[1]]
    print(' '.join(tm))


def m3u8_dl(url):
    from QuickStart_Rhy.m3u8_dl import M3U8DL
    M3U8DL(url, url.split('.')[-2].split('/')[-1]).download()


def download():
    urls = sys.argv[2:]
    if not urls:
        import pyperclip
        urls = pyperclip.paste().split()
    if urls:
        from QuickStart_Rhy.normal_dl import normal_dl
        for url in urls:
            if url.endswith('.m3u8'):
                m3u8_dl(url)
            else:
                normal_dl(url)
    else:
        print("No url found!")


def weather():
    class pull_data(threading.Thread):
        def __init__(self, url):
            threading.Thread.__init__(self)
            self.url = url
            self.ret = []

        def run(self):
            try:
                ct = requests.get(self.url, headers)
            except:
                return
            ct.encoding = 'utf-8'
            ct = ct.text.split('\n')
            if dir_char == '/':
                self.ret = ct.copy()
            else:
                import re
                for line in range(len(ct)):
                    ct[line] = re.sub('\x1b.*?m', '', ct[line])
                self.ret = ct.copy()

        def get_ret(self):
            return self.ret

    try:
        loc = sys.argv[2]
    except IndexError:
        loc = ''
    tls = [pull_data('https://wttr.in/' + (loc if loc else '?lang=zh')), pull_data('https://v2.wttr.in/' + loc)]
    for i in tls:
        i.start()
        i.join()
    simple = tls[0].get_ret()
    table = tls[1].get_ret()
    if simple:
        if not loc:
            from QuickStart_Rhy.Dict import Dict
            translator = Dict()
            print('地区：' + translator.dictionary(simple[0].split('：')[-1])['trans_result']['data'][0]['dst'])
        simple = simple[2:7]
        print('\n'.join(simple))
    else:
        print('Error: Get data failed.')
    if table:
        print(table[3][:-1])
        bottom_line = 7
        while '╂' not in table[bottom_line]:
            bottom_line += 1
        for i in table[7:bottom_line + 2]:
            print(i[:-1])
        print('└────────────────────────────────────────────────────────────────────────')
        print('\n'.join(table[-3 if not loc else -4:]))
    else:
        print('Error: Get detail failed.')


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


def top():
    import colorama
    import psutil
    import time
    import math
    from prettytable import PrettyTable
    from colorama import Style, ansi, Cursor
    from QuickStart_Rhy import ChartBar
    from QuickStart_Rhy.normal_dl import size_format

    def deal():
        print(ansi.clear_screen() + Cursor.POS(0, 0) + Style.RESET_ALL, end='')
        exit(0)

    colorama.init()
    _kernal = psutil.cpu_count()
    _total_mem = psutil.virtual_memory().total
    _cpu_dt = [0] * 40
    _mem_dt = [0] * 40
    _cpu_chart = ChartBar.RollBar(_cpu_dt, height=10)
    _mem_chart = ChartBar.RollBar(_mem_dt, height=10)
    charts = [_cpu_chart, _mem_chart]
    window = PrettyTable()
    window.add_row(charts)
    print(ansi.clear_screen())
    try:
        while True:
            _cpu_cur = sum(psutil.cpu_percent(percpu=True)) / _kernal
            _mem_cur = psutil.virtual_memory().used
            _cpu_chart.add(math.ceil(_cpu_cur))
            _mem_chart.add(math.ceil(_mem_cur / _total_mem * 100))
            window.field_names = ['CPU: %.2f%%' % _cpu_cur, 'MEM: %s' % size_format(_mem_cur)]
            print((ansi.clear_screen() if dir_char == '\\' else '') + Cursor.POS(0, 0))
            print(' ' * 39, end='')
            cur_time()
            cur_img = str(window).split('\n')
            for i in cur_img:
                print(' ' * 4, end='')
                print(i)
            time.sleep(1)
    except:
        deal()


def mktar():
    tar_name, ls = get_tar_name()
    os.system('tar -czf %s.tar.gz %s' % (tar_name, ' '.join(ls)))


def untar():
    if arlen == 2:
        exit("No enough parameters")
    file_names = sys.argv[2:]

    class _untar(threading.Thread):
        def __init__(self, path):
            threading.Thread.__init__(self)
            self.path = path

        def run(self):
            if os.path.exists(self.path):
                if self.path.endswith('.tar'):
                    os.system('tar -xf %s' % self.path)
                elif self.path.endswith('.gz'):
                    os.system('tar -xzf %s' % self.path)
                elif self.path.endswith('.bz2'):
                    os.system('tar -xjf %s' % self.path)
                else:
                    os.system('tar -xf %s' % self.path)
            else:
                print("No such file or dictionary:%s" % self.path)

    for file_name in file_names:
        t = _untar(file_name)
        t.start()
        t.join()


def mkzip():
    zip_name, ls = get_tar_name()
    os.system('zip -r -9 %s.zip %s' % (zip_name, ' '.join(ls)))


def unzip():
    if arlen == 2:
        exit("No enough parameters")
    file_names = sys.argv[2:]

    class _unzip(threading.Thread):
        def __init__(self, path):
            threading.Thread.__init__(self)
            self.path = path

        def run(self):
            if os.path.exists(file_name):
                os.system('unzip %s' % file_name)
            else:
                print("No such file or dictionary:%s" % file_name)

    for file_name in file_names:
        t = _unzip(file_name)
        t.start()
        t.join()


def upgrade():
    if os.system('pip3 install QuickStart-Rhy --upgrade'):
        os.system('pip install QuickStart-Rhy --upgrade')


def upload_pypi():
    remove('dist')
    if os.system('python3 setup.py sdist bdist_wheel'):
        os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist%s*' % dir_char)


def rm_pyinstaller():
    file_name = sys.argv[2]
    remove('build')
    remove('__pycache__')
    remove('%s.spec' % file_name)
    remove('dist')


cmd_config = {
    '-h': h,
    '-u': u,
    '-a': open_app,
    '-f': open_file,
    '-i': init,
    '-trans': translate,
    '-ftp': ftp,
    '-top': top,
    '-time': cur_time,
    '-weather': weather,
    '-dl': download,
    '-mktar': mktar,
    '-untar': untar,
    '-mkzip': mkzip,
    '-unzip': unzip,
    '-upgrade': upgrade,
    '-upload': upload_pypi,
    '-pyuninstaller': rm_pyinstaller
}


def main():
    if arlen >= 2:
        try:
            cmd_config[sys.argv[1]]()
        except KeyError:
            h()
    else:
        h()


if __name__ == '__main__':
    main()
