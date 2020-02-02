from concurrent.futures import ThreadPoolExecutor, wait
from threading import Lock
from requests import get, head


class Downloader:
    def __init__(self, url, nums, file):
        self.url = url
        self.num = nums
        self.name = file
        self.fileLock = Lock()
        r = head(self.url)
        while r.status_code == 302:
            self.url = r.headers['Location']
            r = head(self.url)
        try:
            self.size = int(r.headers['Content-Length'])
        except KeyError:
            self.size = -1
        print('FILE SIZE：{} bytes'.format(self.size if self.size > 0 else 'Unknown'))

    def down(self, start, end):
        headers = {'Range': 'bytes={}-{}'.format(start, end)}
        r = get(self.url, headers=headers, stream=True)
        self.fileLock.acquire()
        with open(self.name, "rb+") as fp:
            fp.seek(start)
            fp.write(r.content)
            self.fileLock.release()

    def run(self):
        if self.size > 0:
            fp = open(self.name, "wb")
            fp.truncate(self.size)
            fp.close()
            part = self.size // self.num
            pool = ThreadPoolExecutor(max_workers=self.num)
            futures = []
            for i in range(self.num):
                start = part * i
                if i == self.num - 1:
                    end = self.size
                else:
                    end = start + part - 1
                futures.append(pool.submit(self.down, start, end))
            wait(futures)
        else:
            content = get(self.url).content
            with open(self.name, 'wb') as f:
                f.write(content)
        print('%s download done!' % self.name)


def normal_dl(url, thread_num=16):
    Downloader(url, thread_num, url.split('/')[-1]).run()
