import webbrowser as wb
import requests
from requests.exceptions import RequestException
import sys
import os

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
    print('help:')
    print('    qs -u  [url]               :-> open url using default browser')
    print('    qs -a  [app/(file...)]     :-> open app or open file by app(for Mac OS X)')
    print('    qs -f  [file...]           :-> open file by default app')
    print('    qs -dl [urls/""]           :-> download file from url(in clipboard)')
    print('    qs -trans [words]          :-> translate the content of words or in clipboard')
    print('    qs -time                   :-> view current time')
    print('    qs -ftp                    :-> start a simple ftp server')
    print('    qs -top                    :-> cpu and memory monitor')
    print('    qs -weather [address]      :-> check weather (of address)')
    print('    qs -mktar [path]           :-> create gzipped archive for path')
    print('    qs -untar [path]           :-> extract path.tar.*')
    print('    qs -mkzip [path]           :-> make a zip for path')
    print('    qs -unzip [path]           :-> unzip path.zip')
    print('    qs -upload                 :-> upload your pypi library')
    print('    qs -upgrade                :-> update qs')
    print('    qs -pyuninstaller [path]   :-> remove files that pyinstaller create')
    print('NOTE: The program based on: tar, zip, unzip')


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
        os.system('open "' + '" "'.join(sys.argv[2:])+'"')
    else:
        for file in sys.argv[2:]:
            if os.path.exists(file):
                path = os.path.abspath(file)
                wb.open('file://%s' % path)


def init():
    wb.open('http://login.cup.edu.cn')
    return
    root = os.path.expanduser('~') + dir_char
    flag = False
    try:
        with open(root + '.wifirc', 'r') as f:
            user, pwd = f.read().split()
    except:
        import getpass
        user = input('用户:')
        pwd = getpass.getpass('密码:')
        with open(root + '.wifirc', 'w') as f:
            f.write("%s %s" % (user, pwd))
        flag = True
    data = {
        'action': 'login',
        'ac_id': '1',
        'user_ip': get_ip(),
        'nas_ip': '',
        'user_mac': '',
        'url': '',
        'username': user,
        'password': '{MD5}'+pwd,
        'remember': '1'
    }

    html = requests.post('http://login.cup.edu.cn/cgi-bin/srun_portal', data=data, headers=headers)
    if html:
        html = html.text
    else:
        exit('未接入CUP校园网')
    print(html)
    if 'error' in html:
        print('登录失败, 可以进行以下操作:\n\t* 尝试网络缴费后登录\n\t* 重新尝试登录')
        remove(root + '.wifirc')
    else:
        print('登录成功')
        if flag:
            print('(脚本将默认使用当前账户密码登录, 如需更改请编辑或删除"%s"文件)' % (root + '.wifirc'))


def translate():
    import pyperclip
    import execjs
    import re
    JS_CODE = """
function a(r, o) {
    for (var t = 0; t < o.length - 2; t += 3) {
        var a = o.charAt(t + 2);
        a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
        a = "+" === o.charAt(t + 1) ? r >>> a: r << a,
        r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
    }
    return r
}
var C = null;
var token = function(r, _gtk) {
    var o = r.length;
    o > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(o / 2) - 5, 10) + r.substring(r.length, r.length - 10));
    var t = void 0,
    t = null !== C ? C: (C = _gtk || "") || "";
    for (var e = t.split("."), h = Number(e[0]) || 0, i = Number(e[1]) || 0, d = [], f = 0, g = 0; g < r.length; g++) {
        var m = r.charCodeAt(g);
        128 > m ? d[f++] = m: (2048 > m ? d[f++] = m >> 6 | 192 : (55296 === (64512 & m) && g + 1 < r.length && 56320 === (64512 & r.charCodeAt(g + 1)) ? (m = 65536 + ((1023 & m) << 10) + (1023 & r.charCodeAt(++g)), d[f++] = m >> 18 | 240, d[f++] = m >> 12 & 63 | 128) : d[f++] = m >> 12 | 224, d[f++] = m >> 6 & 63 | 128), d[f++] = 63 & m | 128)
    }
    for (var S = h,
    u = "+-a^+6",
    l = "+-3^+b+-f",
    s = 0; s < d.length; s++) S += d[s],
    S = a(S, u);
    return S = a(S, l),
    S ^= i,
    0 > S && (S = (2147483647 & S) + 2147483648),
    S %= 1e6,
    S.toString() + "." + (S ^ h)
}
"""

    class Dict:
        def __init__(self):
            self.sess = requests.Session()
            self.headers = {
                'User-Agent':
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/71.0.3578.98 Safari/537.36 '
            }
            self.token = None
            self.gtk = None
            self.javascript = execjs.compile(JS_CODE)
            self.loadMainPage()
            self.loadMainPage()

        def loadMainPage(self):
            url = 'https://fanyi.baidu.com'
            try:
                r = self.sess.get(url, headers=self.headers)
                self.token = re.findall(r"token: '(.*?)',", r.text)[0]
                self.gtk = re.findall(r"window.gtk = '(.*?)';", r.text)[0]
            except Exception as e:
                raise e

        def langdetect(self, query):
            url = 'https://fanyi.baidu.com/langdetect'
            data = {'query': query}
            try:
                r = self.sess.post(url=url, data=data)
            except Exception as e:
                raise e

            json = r.json()
            if 'msg' in json and json['msg'] == 'success':
                return json['lan']
            return None

        def dictionary(self, query, dst='zh', src=None):
            url = 'https://fanyi.baidu.com/v2transapi'
            sign = self.javascript.call('token', query, self.gtk)
            if not src:
                src = self.langdetect(query)
            data = {
                'from': src,
                'to': dst,
                'query': query,
                'simple_means_flag': 3,
                'sign': sign,
                'token': self.token,
            }
            try:
                r = self.sess.post(url=url, data=data)
            except Exception as e:
                raise e
            if r.status_code == 200:
                json = r.json()
                if 'error' in json:
                    raise Exception('baidu sdk error: {}'.format(json['error']))
                return json
            return None

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
    import threading
    import urllib3
    import shutil
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def merge_file(path, ts_ls, name):
        if not path.endswith(dir_char):
            path += dir_char
        with open(name + '.ts', 'wb') as f:
            for ts in ts_ls:
                with open(path + ts, 'rb') as ff:
                    f.write(ff.read())

    class M3U8DL:
        class _monitor(threading.Thread):
            def __init__(self, num, dl_path):
                threading.Thread.__init__(self)
                self.num = num
                self.dl_path = dl_path

            def run(self):
                import time
                rd = "|/-\\"
                pos = 0
                while True:
                    ll = len(os.listdir(self.dl_path))
                    cur = ll / self.num * 100
                    bar = '#' * int(cur / 2) + ' ' * (50 - int(cur / 2))
                    print("[%s][%s][%.2f%%" % (rd[pos % 4], bar, cur), end='\r')
                    if ll == self.num:
                        break
                    time.sleep(0.5)
                    pos += 1

        class _dl(threading.Thread):
            from Crypto.Cipher import AES

            def __init__(self, job_ls, mutex, path='./'):
                threading.Thread.__init__(self)
                self.job_ls = job_ls
                self.mutex = mutex
                self.path = path

            def run(self):
                key = ''
                while self.job_ls:
                    self.mutex.acquire()
                    job = self.job_ls.pop()
                    self.mutex.release()
                    if not job[-1]:
                        uri_pos = job[1].find("URI")
                        quotation_mark_pos = job[1].rfind('"')
                        key_path = job[1][uri_pos:quotation_mark_pos].split('"')[1]
                        key_url = job[0] + key_path
                        res = requests.get(key_url, verify=False)
                        key = res.content
                    else:
                        pd_url = job[0]
                        c_fule_name = job[1]
                        if os.path.exists(os.path.join(self.path, c_fule_name)):
                            continue
                        res = requests.get(pd_url, verify=False)
                        if len(key):
                            cryptor = self.AES.new(key, self.AES.MODE_CBC, key)
                            with open(os.path.join(self.path, c_fule_name + ".mp4"), 'ab') as f:
                                f.write(cryptor.decrypt(res.content))
                        else:
                            with open(os.path.join(self.path, c_fule_name), 'ab') as f:
                                f.write(res.content)
                                f.flush()

        def __init__(self, target, name, thread_num):
            self.target = target
            self.name = name
            self.th_num = thread_num

        def download(self):
            target = self.target
            download_path = os.getcwd() + dir_char + self.name
            if not os.path.exists(download_path):
                os.mkdir(download_path)
            all_content = requests.get(target, verify=False).text
            if "#EXTM3U" not in all_content:
                raise BaseException("非M3U8的链接")
            if "EXT-X-STREAM-INF" in all_content:
                file_line = all_content.split("\n")
                for line in file_line:
                    if '.m3u8' in line:
                        target = target.rsplit("/", 1)[0] + "/" + line
                        all_content = requests.get(target, verify=False).text
            file_line = all_content.split("\n")
            rt = target.rsplit("/", 1)[0] + "/"
            tmp = []
            for index, line in enumerate(file_line):
                if "#EXT-X-KEY" in line:
                    tmp.append((rt, line, 0))
                if "EXTINF" in line:
                    tmp.append((rt + file_line[index + 1], file_line[index + 1].rsplit("/", 1)[-1], 1))
            file_line = tmp[::-1]
            mutex = threading.Lock()
            tls = [self._monitor(len(file_line), download_path)]
            tls[0].start()
            for i in range(self.th_num):
                tls.append(self._dl(file_line, mutex, download_path))
                tls[-1].start()
            for i in tls:
                i.join()
            print("Download completed!")
            merge_file(download_path, tmp, self.name)
            shutil.rmtree(download_path)
    M3U8DL(url, url.split('.')[-2].split('/')[-1], 16).download()


def download():
    urls = sys.argv[2:]
    if not urls:
        import pyperclip
        urls = pyperclip.paste().split()
    if urls:
        for url in urls:
            if url.endswith('.m3u8'):
                m3u8_dl(url)
            else:
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
    def request_data(url):
        ct = requests.get(url, headers)
        ct.encoding = 'utf-8'
        ct = ct.text.split('\n')
        if dir_char == '/':
            return ct
        else:
            import re
            for line in range(len(ct)):
                ct[line] = re.sub('\x1b.*?m', '', ct[line])
            return ct

    try:
        loc = sys.argv[2]
    except IndexError:
        loc = ''
    if loc:
        simple = request_data('https://wttr.in/' + loc)
        table = request_data('https://v2.wttr.in/' + loc)
    else:
        simple = request_data('https://wttr.in/?lang=zh')
        table = request_data('https://v2.wttr.in/')
        print('地区：' + simple[0].split('：')[-1])
    simple = simple[2:7]
    print('\n'.join(simple))
    print(table[3][:-1])
    bottom_line = 7
    while '╂' not in table[bottom_line]:
        bottom_line += 1
    for i in table[7:bottom_line + 2]:
        print(i[:-1])
    print('└────────────────────────────────────────────────────────────────────────')
    print('\n'.join(table[-3 if not loc else -4:]))


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
        httpd.serve_forever()


def top():
    import psutil
    import matplotlib.pyplot as plt
    import numpy as np
    import signal

    def deal_ctrl_c(signum, frame):
        exit(0)

    def close(event):
        if event.key in 'qQ':
            exit(0)

    signal.signal(signal.SIGINT, deal_ctrl_c)
    cpu_x = np.arange(1, psutil.cpu_count() + 1)
    len_x = len(cpu_x)
    mem_x = np.arange(1, 11)
    mem_y = np.array([0] * 10)
    mem_p = 9
    mem_lim = psutil.virtual_memory().total / 1024 ** 3
    fig = plt.figure(figsize=(6, 4))
    fig.canvas.mpl_connect('key_press_event', close)
    while True:
        plt.clf()
        cpu_per = psutil.cpu_percent(percpu=True)
        mem_cur = psutil.virtual_memory().used / 1024 ** 3
        cpu_graph = plt.subplot(2, 1, 1)
        cpu_graph.set_title('cpu: %.2f%%' % (sum(cpu_per) / len_x))
        cpu_graph.set_ylabel('percent')
        cpu_graph.set_ylim((0, 100))
        cpu_graph.set_xticks([])
        plt.bar(cpu_x, cpu_per)
        plt.grid(axis="y", linestyle='-.')
        plt.tight_layout()
        mem_graph = plt.subplot(2, 1, 2)
        mem_graph.set_title('memory: %.2fG' % mem_cur)
        mem_graph.set_ylabel('G')
        mem_graph.set_ylim((0, mem_lim))
        mem_graph.set_xticks([])
        mem_y[mem_p] = mem_cur
        mem_p = mem_p - 1 if mem_p else 9
        plt.plot(mem_x, mem_y)
        plt.pause(1)


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
