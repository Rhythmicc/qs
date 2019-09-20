import webbrowser as wb
import requests
import shutil
from requests.exceptions import RequestException
import sys
import os
import pyperclip

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7'}

system = sys.platform
base_dir = sys.path[0]
if system.startswith('win'):
    dir_char = '\\'
else:
    dir_char = '/'
base_dir += dir_char


def h():
    print('help:')
    print('    qs -u [url]              :-> open url using safari')
    print('    qs -a [app/(file...)]    :-> open app or open file by app')
    print('    qs -f [file...]          :-> open file by default app')
    print('    qs -t                    :-> translate the content in clipboard')
    print('    qs -mktar [path]         :-> create gzipped archive for path')
    print('    qs -untar [path]         :-> extract path.tar.*')
    print('    qs -mkzip [path]         :-> make a zip for path')
    print('    qs -unzip [path]         :-> unzip path.zip')
    print('    qs -pyuninstaller [path] :-> remove files that pyinstaller create')


def check_one_page(url):
    try:
        response = requests.get(url, headers=headers).status_code
        return response == 200
    except RequestException:
        return False


def formatUrl(Url):
    tUrl = Url
    res = check_one_page(tUrl)
    if not res:
        tUrl = 'https://' + Url
        res = check_one_page(tUrl)
        if not res:
            tUrl = 'http://' + Url
            res = check_one_page(tUrl)
            if not res:
                tUrl = None
    else:
        tUrl = None
    return tUrl


def remove(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def setup_xdg_open():
    status = os.system('yum install xdg-open')
    return status


def a():
    if dir_char == '/':
        if system == 'darwin':
            os.system('open -a ' + ' '.join(sys.argv[2:]))
        else:
            status = os.system('xdg-open %s' % sys.argv[2])
            if status:
                print('No xdg-open! Auto setuping...')
                status = setup_xdg_open()
                if status:
                    exit('setup xdg-open failed')
                os.system('xdg-open %s' % sys.argv[2])
    else:
        print('-a is only support Mac OS X / Linux')


def f():
    if dir_char == '/':
        if system == 'darwin':
            os.system('open ' + ' '.join(sys.argv[2:]))
        else:
            status = os.system('xdg-open ' + ' '.join(sys.argv[2:]))
            if status:
                print('No xdg-open! Auto setuping...')
                status = setup_xdg_open()
                if status:
                    exit('setup xdg-open failed')
                os.system('xdg-open ' + ' '.join(sys.argv[2:]))
    else:
        os.system(sys.argv[2])


def t():
    content = pyperclip.paste()
    if content:
        content.replace('\n', ' ')
        os.system('clear')
        status = os.system('yd %s' % content)
        if status:
            print('Auto install "yddict"')
            status = os.system('npm install yddict -g')
            if status:
                exit('install command "yd" failed!')
            os.system('yd %s' % content)
    else:
        print("No content in your clipboard!")


def main():
    arlen = len(sys.argv)
    if arlen >= 2:
        if sys.argv[1] == '-u':
            for url in sys.argv[2:]:
                url = formatUrl(url)
                if url:
                    wb.open_new_tab(url)
        elif sys.argv[1] == '-a':
            a()
        elif sys.argv[1] == '-f':
            f()
        elif sys.argv[1] == '-i':
            wb.open_new_tab('http://login.cup.edu.cn')
        elif sys.argv[1] == '-t':
            t()
        elif sys.argv[1] == '-mktar':
            if arlen == 2:
                exit("No enough parameters")
            file_names = sys.argv[2:]
            for file_name in file_names:
                if os.path.exists(file_name):
                    os.system('touch %s.tar.gz' % file_name)
                    os.system('tar -czf %s.tar.gz %s' % (file_name, file_name))
                else:
                    print("No such file or dictionary:%s" % file_name)
        elif sys.argv[1] == '-untar':
            if arlen == 2:
                exit("No enough parameters")
            file_names = sys.argv[2:]
            for file_name in file_names:
                if os.path.exists(file_name):
                    if file_name.endswith('.tar'):
                        os.system('tar -xf %s' % file_name)
                    elif file_name.endswith('.gz'):
                        os.system('tar -xzf %s' % file_name)
                    elif file_name.endswith('.bz2'):
                        os.system('tar -xjf %s' % file_name)
                else:
                    print("No such file or dictionary:%s" % file_name)
        elif sys.argv[1] == '-mkzip':
            if arlen == 2:
                exit("No enough parameters")
            file_names = sys.argv[2:]
            for file_name in file_names:
                zip_name = file_name.split('.')[0]
                if os.path.exists(file_name):
                    os.system('zip -r -9 %s.zip %s' % (zip_name, file_name))
                else:
                    print("No such file or dictionary:%s" % file_name)
        elif sys.argv[1] == '-unzip':
            if arlen == 2:
                exit("No enough parameters")
            file_names = sys.argv[2:]
            for file_name in file_names:
                if os.path.exists(file_name):
                    os.system('unzip %s' % file_name)
                else:
                    print("No such file or dictionary:%s" % file_name)
        elif sys.argv[1] == '-pyuninstaller':
            file_name = sys.argv[2]
            remove('build')
            remove('__pycache__')
            remove('%s.spec' % file_name)
            remove('dist')
        else:
            h()
    else:
        h()
