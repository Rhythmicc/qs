import threading
import urllib3
import shutil
import requests
import os
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

dir_char = '\\' if sys.platform.startswith('win') else '/'


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
