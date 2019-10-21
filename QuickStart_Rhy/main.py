import webbrowser as wb
import requests
from requests.exceptions import RequestException
import sys
import os
import time

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
    print('    qs -u  [url]               :-> open url using default browser')
    print('    qs -a  [app/(file...)]     :-> open app or open file by app(for Mac OS X)')
    print('    qs -f  [file...]           :-> open file by default app')
    print('    qs -dl [urls/""]           :-> download file from url(in clipboard)')
    print('    qs -trans                  :-> translate the content in clipboard')
    print('    qs -time                   :-> view current time')
    print('    qs -ftp                    :-> start a simple ftp server')
    print('    qs -weather [-(all)detail] :-> check weather (view detail)')
    print('    qs -mktar [path]           :-> create gzipped archive for path')
    print('    qs -untar [path]           :-> extract path.tar.*')
    print('    qs -mkzip [path]           :-> make a zip for path')
    print('    qs -unzip [path]           :-> unzip path.zip')
    print('    qs -upload                 :-> upload your pypi library')
    print('    qs -upgrade                :-> update qs')
    print('    qs -pyuninstaller [path]   :-> remove files that pyinstaller create')
    print('NOTE: The program based on: npm, tar, zip, unzip, yddict, curl')


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
        os.system('open ' + ' '.join(sys.argv[2:]))
    else:
        for file in sys.argv[2:]:
            if os.path.exists(file):
                path = os.path.abspath(file)
                wb.open('file://%s' % path)


def init():
    root = os.path.expanduser('~') + dir_char
    flag = False
    try:
        with open(root+'.wifirc', 'r') as f:
            user, pwd = f.read().split()
    except:
        import getpass
        user = input('用户:')
        pwd = getpass.getpass('密码:')
        with open(root+'.wifirc', 'w') as f:
            f.write("%s %s" % (user, pwd))
        flag = True
    data = {
        'action': 'login',
        'ac_id': '1',
        'username': user,
        'password': pwd,
        'save_me': '1'
    }
    html = requests.post('http://login.cup.edu.cn/srun_portal_pc.php', data=data, headers=headers)
    if html:
        html = html.text
    else:
        exit('未接入CUP校园网')
    if '登录成功' not in html:
        print('登录失败, 可以进行以下操作:\n\t* 尝试网络缴费后登录\n\t* 重新尝试登录')
        remove(root+'.wifirc')
    else:
        print('登录成功')
        if flag:
            print('(脚本将默认使用当前账户密码登录, 如需更改请编辑或删除"%s"文件)' % (root + '.wifirc'))


def translate():
    import pyperclip
    content = pyperclip.paste()
    if content:
        content.replace('\n', ' ')
        os.system('yd %s' % content)
    else:
        print("No content in your clipboard!")


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
    tm = time.strftime('%Y-%m-%d %A %H:%M:%S', time.localtime(time.time())).split()
    ls = tm[0].split('-')
    tm[0] = ls[0] + '年' + ls[1] + '月' + ls[2] + '日'
    tm[1] = week[tm[1]]
    print(' '.join(tm))


def download():
    urls = sys.argv[2:]
    if not urls:
        import pyperclip
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


def weather():
    if dir_char == '/':
        res = requests.get('https://wttr.in/?lang=zh', headers).text.split('\n')
        if not res:
            exit('Network error!')
    else:
        os.system('curl -s wttr.in/?lang=zh > tmp')
        with open('tmp', 'r', encoding='utf-8') as f:
            res = f.readlines()
        remove('tmp')
    location = res[0].split('：')[-1]
    res = res[2:]
    cur_time()
    print('地区:%s' % location)
    if arlen > 2 and sys.argv[2].endswith('detail'):
        if sys.argv[2].startswith('-all'):
            print('\n'.join(res[:-1]))
        else:
            print('\n'.join(res[5:15]))
    else:
        print('\n'.join(res[:5]))


def ftp():
    import socket
    ip = socket.gethostbyname(socket.gethostname())
    print('starting ftp simple server: address http://%s:8000/' % ip)
    if os.system('python3 -m http.server'):
        os.system('python -m http.server')


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
    '-u': u,
    '-a': open_app,
    '-f': open_file,
    '-i': init,
    '-trans': translate,
    '-ftp': ftp,
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
