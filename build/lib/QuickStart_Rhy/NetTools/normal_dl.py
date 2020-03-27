from QuickStart_Rhy.NetTools import size_format, get_fileinfo
from concurrent.futures import ThreadPoolExecutor, wait
from threading import Lock
from requests import get
import psutil
import signal
import time
import os

core_num = psutil.cpu_count()
maxBlockSize = int((psutil.virtual_memory().total >> 6) / core_num)
minBlockSize = 1 << 17


def GetBlockSize(sz):
    if sz >= maxBlockSize << 10:
        return maxBlockSize
    elif sz <= minBlockSize << 3:
        return minBlockSize
    else:
        return max(sz >> 10, minBlockSize)


class Downloader:
    def __init__(self, url: str, num: int):
        signal.signal(signal.SIGINT, self.kill_self)
        self.has_ctrl = False
        self.url = url
        self.num = num
        self.name = os.path.basename(url)
        self.fileLock = Lock()
        self.cur_sz = 0
        self.url, self.name, r = get_fileinfo(url)
        if not self.url:
            print('[ERROR] Connection Error!')
            exit(0)
        try:
            self.size = int(r.headers['Content-Length'])
            if self.size < 1e6:
                print('[INFO] FILE SIZE\t{}'.format(size_format(self.size)))
                self.size = -1
            else:
                self.fileBlock = GetBlockSize(self.size)
        except KeyError:
            self.size = -1
        if self.size > 0:
            self.pool = ThreadPoolExecutor(max_workers=self.num)
            self.futures = []
            if os.path.exists(self.name + '.qs_dl'):
                self.ctn_file = open(self.name + '.qs_dl', 'r+')
                self.ctn = [int(i) for i in self.ctn_file.read().strip().split()]
            else:
                self.ctn_file = open(self.name + '.qs_dl', 'w')
                self.ctn = []
            print('[INFO] FILE SIZE\t{}'.format(size_format(self.size)))
            print('[INFO] BLOCK SIZE\t{}'.format(size_format(self.fileBlock)))

    def kill_self(self, a, b):
        if not self.has_ctrl:
            print('\n[INFO] GET Ctrl C! PLEASE PUSH AGAIN TO CONFIRM!')
            self.has_ctrl = True
        if self.size > 0:
            self.ctn_file.close()
        exit(0)

    def _dl(self, start):
        try:
            _sz = min(start + self.fileBlock, self.size)
            headers = {'Range': 'bytes={}-{}'.format(start, _sz)}
            tm = time.perf_counter()
            r = get(self.url, headers=headers, stream=True)
            with open(self.name, 'rb+') as fp:
                fp.seek(start)
                fp.write(r.content)
            tm = time.perf_counter() - tm
            speed = size_format((self.fileBlock * self.num / tm), align=True)
        except:
            self.futures.append(self.pool.submit(self._dl, start))
        else:
            self.fileLock.acquire()
            self.cur_sz += _sz - start
            per = self.cur_sz / self.size
            print('\r[%s] %.2f%% | %s/s' % ('#' * int(40 * per) + ' ' * int(40 - 40 * per), per * 100, speed),
                  end='\n' if self.cur_sz == self.size else '')
            self.ctn_file.write('%d\n' % start)
            self.fileLock.release()

    def run(self):
        if self.size > 0:
            with open(self.name, "rb+" if self.ctn else "wb") as fp:
                fp.truncate(self.size)
            for i in range(0, self.size, self.fileBlock):
                if self.ctn:
                    if i in self.ctn:
                        self.cur_sz += min(i + self.fileBlock, self.size) - i
                    else:
                        self.futures.append(self.pool.submit(self._dl, i))
                else:
                    self.futures.append(self.pool.submit(self._dl, i))
            wait(self.futures)
            self.ctn_file.close()
            os.remove(self.name + '.qs_dl')
        else:
            content = get(self.url).content
            with open(self.name, 'wb') as f:
                f.write(content)
        print('[INFO] %s download done!' % self.name)


def normal_dl(url):
    Downloader(url, min(16, core_num * 4)).run()
