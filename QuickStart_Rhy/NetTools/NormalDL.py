# coding=utf-8
"""
qs的普通文件下载器！除了迅雷比不过，俺自信比其他的下载器快得多，并且支持设置代理，好看的命令行交互，啥j8文件都能下；(仅支持http[s]协议)

QS ordinary file downloader! Except Xunlei, I'm confident that it's much faster than other downloaders,
and supports setting proxy, nice command line interaction, and it can download fuck any files; (only supports HTTP[S])

Author: RhythmLian (https://rhythmlian.cn)
"""
from . import size_format, get_fileinfo
from concurrent.futures import ThreadPoolExecutor, wait
from ..ThreadTools import FileWriters
from .. import user_lang
from threading import Lock
from requests import get
import psutil
import signal
import queue
import time
import os

core_num = psutil.cpu_count()
maxBlockSize = int(1.5e6)
minBlockSize = int(5e5)


def GetBlockSize(sz):
    """
    自动规划块大小

    Automatically program the block size

    :param sz: 文件大小
    :return: 块大小
    """
    if sz >= maxBlockSize << 10:
        return maxBlockSize
    elif sz <= minBlockSize << 3:
        return minBlockSize
    else:
        return max(sz >> 9, minBlockSize)


class Downloader:
    from rich.console import Console
    from rich.progress import (
        BarColumn,
        DownloadColumn,
        TextColumn,
        TransferSpeedColumn,
        TimeRemainingColumn,
        Progress,
    )

    info_string = '[bold cyan][INFO]' if user_lang != 'zh' else '[bold cyan][信息]'
    warn_string = '[bold yellow][WARNING]' if user_lang != 'zh' else '[bold yellow][警告]'
    erro_string = '[bold red][ERROR]' if user_lang != 'zh' else '[bold red][错误]'
    proxies = {}
    console = Console()

    def __init__(self, url: str, num: int, set_name: str = '', proxy: str = '', output_error: bool = False):
        """
        qs普通文件下载引擎

        Qs general file download engine

        :param url: 文件url
        :param num: 线程数量
        """
        signal.signal(signal.SIGINT, self._kill_self)
        self.has_ctrl = False
        self.url = url
        self.num = num
        self.fileLock = Lock()
        self.url, self.name, r = get_fileinfo(url, proxy)
        if not (self.url and self.name and r):
            Downloader.console.log(Downloader.warn_string, 'Get File information failed, please check network!'
                                   if user_lang != 'zh' else '获取文件信息失败，请检查网络!')
        if set_name:
            self.name = set_name
        if self.name and '.' not in self.name:
            self.name = self.name = os.path.basename(url)
        if proxy:
            Downloader.proxies = {
                'http': 'http://'+proxy,
                'https': 'https://'+proxy
            }
        self.output_error = output_error
        if not self.url:
            Downloader.console.log(Downloader.erro_string, 'Connection Error!' if user_lang != 'zh' else '连接失败!')
            exit(0)
        try:
            self.size = int(r.headers['content-length'])
            self.main_progress = Downloader.Progress(
                Downloader.TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
                Downloader.BarColumn(bar_width=None),
                "[progress.percentage]{task.percentage:>3.1f}%",
                "•",
                Downloader.DownloadColumn(),
                "•",
                Downloader.TransferSpeedColumn(),
                "•",
                Downloader.TimeRemainingColumn(),
                console=Downloader.console
            )
            self.dl_id = self.main_progress.add_task('Download', filename=self.name, start=False)
            self.main_progress.update(self.dl_id, total=self.size)
            if self.size < 5e6:
                Downloader.console.log(Downloader.info_string, 'FILE SIZE' if user_lang != 'zh' else '文件大小'
                                       , size_format(self.size))
                self.size = -self.size
            else:
                self.fileBlock = GetBlockSize(self.size)
        except KeyError:
            self.size = -1
            self.main_progress = Downloader.Progress(
                Downloader.TextColumn(
                    "[bold blue]{task.fields[filename]} [red]" +
                    ('Unknow size' if user_lang != 'zh' else '未知大小'),
                    justify="right"
                ),
                Downloader.BarColumn(bar_width=None),
                Downloader.DownloadColumn(),
                console=Downloader.console
            )
            self.dl_id = self.main_progress.add_task('Download', filename=self.name, start=False)
        if self.size > 0:
            self.pool = ThreadPoolExecutor(max_workers=self.num)
            self.futures = []
            self.job_queue = queue.Queue()
            if os.path.exists(self.name + '.qs_dl'):
                self.ctn_file = open(self.name + '.qs_dl', 'r+')
                self.ctn = [int(i) for i in self.ctn_file.read().strip().split()]
            else:
                self.ctn_file = open(self.name + '.qs_dl', 'w')
                self.ctn = []
            self.writers = FileWriters(self.name, max(2, int(core_num / 2)), "rb+" if self.ctn else "wb")
            Downloader.console.log(Downloader.info_string, 'FILE SIZE' if user_lang != 'zh' else '文件大小'
                                   , size_format(self.size, align=True))
            Downloader.console.log(Downloader.info_string, 'BLOCK SIZE' if user_lang != 'zh' else '块大小'
                                   , size_format(self.fileBlock, align=True))

    def _kill_self(self, signum, frame):
        """
        终止下载任务，保存断点

        Terminate the download and save the breakpoint

        :param signum: 信号
        :param frame: frame
        :return: None
        """
        if self.size > 0:
            Downloader.console.print('')
            Downloader.console.log(Downloader.info_string,
                                   'Get Ctrl-C, exiting...' if user_lang != 'zh' else '捕获Ctrl-C, 正在退出...')
            self.ctn_file.close()
            self.pool.shutdown(wait=False)
            self.writers.wait()
            Downloader.console.log(Downloader.info_string, 'Deal Done!' if user_lang != 'zh' else '处理完成!')
        os._exit(0)

    def _dl(self, start):
        """
        执行文件块下载任务

        Perform the file block download task

        :param start: 文件块起始偏移量
        :return: None
        """
        try:
            _sz = min(start + self.fileBlock, self.size)
            headers = {'Range': 'bytes={}-{}'.format(start, _sz)}
            r = get(self.url, headers=headers, timeout=50, proxies=Downloader.proxies)
            self.writers.new_job(r.content, start)
        except Exception as e:
            msg = repr(e)
            if self.output_error:
                Downloader.console.log(Downloader.erro_string, msg[:msg.index('(')])
            self.job_queue.put(start)
        else:
            self.fileLock.acquire()
            self.ctn.append(start)
            self.ctn_file.write('%d\n' % start)
            self.fileLock.release()
            self.main_progress.advance(self.dl_id, _sz - start)

    def _single_dl(self):
        """
        无法并行下载或无需并行下载时采用串行下载

        Parallel downloads are not possible or serial downloads are not required

        :return: None
        """
        r = get(self.url, stream=True, proxies=Downloader.proxies)
        flag = self.size != -1

        if flag:
            self.main_progress.start_task(self.dl_id)
        else:
            self.main_progress.update(self.dl_id, total=-1)
        with open(self.name, 'wb') as f:
            for chunk in r.iter_content(32768):
                f.write(chunk)
                self.main_progress.advance(self.dl_id, 32768)

    def run(self):
        """
        规划下载任务并开始下载

        qs可以有效应对网络问题对下载任务造成的影响，如：
          1.下载过程中切换代理

          2.链路异常
        并确保下载任务顺利完成

        :return: None
        """
        self.main_progress.start()
        if self.size > 0:
            self.main_progress.start_task(self.dl_id)
            if not self.ctn:
                with open(self.name, "wb") as fp:
                    fp.truncate(self.size)
            self.main_progress.advance(self.dl_id, self.fileBlock*len(self.ctn))
            for i in range(0, self.size, self.fileBlock):
                if self.ctn and i in self.ctn:
                    continue
                else:
                    self.job_queue.put(i)
            retry_cnt = 0
            while not self.job_queue.empty():
                self.futures.clear()
                while not self.job_queue.empty():
                    cur = self.job_queue.get()
                    if cur not in self.ctn:
                        self.futures.append(self.pool.submit(self._dl, cur))
                wait(self.futures)
                if not self.job_queue.empty() and retry_cnt > 2:
                    Downloader.console.log(Downloader.warn_string, 'Exists File Block Lost, Retrying after 0.5 sec'
                                           if user_lang != 'zh' else '存在文件块丢失，0.5秒后重试')
                    time.sleep(0.5)
                retry_cnt += 1
            self.writers.wait()
            self.ctn_file.close()
            os.remove(self.name + '.qs_dl')
        else:
            self._single_dl()
        self.main_progress.stop()
        Downloader.console.log(Downloader.info_string, self.name, 'download done!' if user_lang != 'zh' else '下载完成!')


def normal_dl(url, set_name: str = '', set_proxy: str = '', output_error: bool = False):
    """
    自动规划下载线程数量并开始并行下载

    Automatically schedule the number of download threads and begin parallel downloads

    :param url: 文件url
    :param set_name: 设置文件名（默认采用url所指向的资源名）
    :param set_proxy: 设置代理（默认无代理）
    :param output_error: 输出报错信息
    :return: None
    """
    Downloader(url, min(16, core_num * 4), set_name, set_proxy, output_error).run()


if __name__ == '__main__':
    import sys
    normal_dl(sys.argv[1])
