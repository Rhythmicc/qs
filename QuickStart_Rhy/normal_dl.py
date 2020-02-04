from concurrent.futures import ThreadPoolExecutor, wait
from threading import Lock
from requests import get, head
import psutil

core_num = psutil.cpu_count()
maxBlockSize = int((psutil.virtual_memory().total >> 6) / core_num)
minBlockSize = 1 << 17


def size_format(sz):
    if sz >= 1e9:
        return '%.3f GB' % (sz / 1e9)
    elif sz >= 1e6:
        return '%.3f MB' % (sz / 1e6)
    elif sz >= 1e3:
        return '%.3f KB' % (sz / 1e3)
    else:
        return '%d B' % sz


def GetBlockSize(sz):
    if sz >= maxBlockSize << 10:
        return maxBlockSize
    elif sz <= minBlockSize << 3:
        return minBlockSize
    else:
        return max(sz >> 10, minBlockSize)


class Downloader:
    def __init__(self, url, nums):
        self.url = url
        self.num = nums
        self.name = url.split('/')[-1]
        self.fileLock = Lock()
        self.cur_sz = 0
        r = head(self.url)
        while r.status_code == 302:
            self.url = r.headers['Location']
            r = head(self.url)
        try:
            self.size = int(r.headers['Content-Length'])
            if self.size < 1e6:
                print('[INFO] FILE SIZE\t{}'.format(size_format(self.size)))
                self.size = -1
            else:
                self.fileBlock = GetBlockSize(self.size)
                print('[INFO] BLOCK SIZE\t{}'.format(size_format(self.size)))
        except KeyError:
            self.size = -1
        if self.size > 0:
            print('[INFO] FILE SIZE\t{}'.format(size_format(self.size)))

    def _dl(self, start):
        _sz = min(start + self.fileBlock, self.size)
        headers = {'Range': 'bytes={}-{}'.format(start, _sz)}
        r = get(self.url, headers=headers, stream=True)
        self.fileLock.acquire()
        with open(self.name, 'rb+') as fp:
            fp.seek(start)
            fp.write(r.content)
        self.cur_sz += _sz - start
        per = self.cur_sz / self.size
        print('[%s] %.2f%%' % ('#'*int(40*per)+' '*int(40-40*per), per*100),
              end='\n' if self.cur_sz == self.size else '\r')
        self.fileLock.release()

    def run(self):
        if self.size > 0:
            with open(self.name, "wb") as fp:
                fp.truncate(self.size)
            pool = ThreadPoolExecutor(max_workers=self.num)
            futures = []
            for i in range(0, self.size, self.fileBlock):
                futures.append(pool.submit(self._dl, i))
            wait(futures)
        else:
            content = get(self.url).content
            with open(self.name, 'wb') as f:
                f.write(content)
        print('[INFO] %s download done!' % self.name)


def normal_dl(url):
    Downloader(url, min(16, core_num * 4)).run()
