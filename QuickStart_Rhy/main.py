import webbrowser as wb
import requests
import shutil
from requests.exceptions import RequestException
import sys
import os
import time
import pyperclip

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) '
                  'Version/11.0.2 Safari/604.4.7'}

system = sys.platform
base_dir = sys.path[0]
if system.startswith('win'):
    dir_char = '\\'
else:
    dir_char = '/'
base_dir += dir_char
arlen = len(sys.argv)


def h():
    print('help:')
    print('    qs -u  [url]             :-> open url using default browser')
    print('    qs -a  [app/(file...)]   :-> open app or open file by app(for Mac OS X)')
    print('    qs -f  [file...]         :-> open file by default app')
    print('    qs -dl [urls/""]         :-> download file from url(in clipboard)')
    print('    qs -t                    :-> translate the content in clipboard')
    print('    qs -time                 :-> view current time')
    print('    qs -mktar [path]         :-> create gzipped archive for path')
    print('    qs -untar [path]         :-> extract path.tar.*')
    print('    qs -mkzip [path]         :-> make a zip for path')
    print('    qs -unzip [path]         :-> unzip path.zip')
    print('    qs -upload               :-> upload your pypi library')
    print('    qs -pyuninstaller [path] :-> remove files that pyinstaller create')


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
            shutil.rmtree(path)
        else:
            os.remove(path)


def setup_dep():
    status = os.system('npm install yddict -g')
    return status


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


def open_app():
    if system == 'darwin':
        os.system('open -a ' + ' '.join(sys.argv[2:]))
    else:
        print('"-a" is only support Mac OS X')


def open_file():
    if dir_char == '/':
        if system == 'darwin':
            os.system('open ' + ' '.join(sys.argv[2:]))
        else:
            for file in sys.argv[2:]:
                if os.path.exists(file):
                    path = os.path.abspath(file)
                    wb.open('file://%s' % path)
    else:
        for file in sys.argv[2:]:
            if os.path.exists(file):
                os.system(file)


def translate():
    content = pyperclip.paste()
    if content:
        content.replace('\n', ' ')
        os.system('yd %s' % content)
    else:
        print("No content in your clipboard!")


def download():
    urls = sys.argv[2:]
    if not urls:
        urls = pyperclip.paste().split()
    for url in urls:
        package = requests.get(url, headers).content
        if package:
            file_name = url.split('/')[-1]
            with open(file_name, 'wb') as f:
                f.write(package)
        else:
            print('Download "%s" failed!' % url)
    else:
        print("No url found!")


def mktar():
    tar_name, ls = get_tar_name()
    os.system('tar -czf %s.tar.gz %s' % (tar_name, ' '.join(ls)))


def untar():
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


def mkzip():
    zip_name, ls = get_tar_name()
    os.system('zip -r -9 %s.zip %s' % (zip_name, ' '.join(ls)))


def unzip():
    if arlen == 2:
        exit("No enough parameters")
    file_names = sys.argv[2:]
    for file_name in file_names:
        if os.path.exists(file_name):
            os.system('unzip %s' % file_name)
        else:
            print("No such file or dictionary:%s" % file_name)


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


def main():
    if arlen >= 2:
        if sys.argv[1] == '-u':
            for url in sys.argv[2:]:
                url = formatUrl(url)
                wb.open_new_tab(url)
        elif sys.argv[1] == '-a':
            open_app()
        elif sys.argv[1] == '-f':
            open_file()
        elif sys.argv[1] == '-i':
            wb.open_new_tab('http://login.cup.edu.cn')
        elif sys.argv[1] == '-t':
            translate()
        elif sys.argv[1] == '-time':
            print(time.strftime('%Z %Y-%m-%d %A %H:%M:%S', time.localtime(time.time())))
        elif sys.argv[1] == '-dl':
            download()
        elif sys.argv[1] == '-mktar':
            mktar()
        elif sys.argv[1] == '-untar':
            untar()
        elif sys.argv[1] == '-mkzip':
            mkzip()
        elif sys.argv[1] == '-unzip':
            unzip()
        elif sys.argv[1] == '-upload':
            upload_pypi()
        elif sys.argv[1] == '-pyuninstaller':
            rm_pyinstaller()
        else:
            h()
    else:
        h()


if __name__ == '__main__':
    main()
