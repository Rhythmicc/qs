# coding=utf-8
"""
qs的普通文件下载器！干翻迅雷，并且支持设置代理，设置referer，好看的命令行交互，啥j8文件都能下；(仅支持http[s]协议)

QS ordinary file downloader! Dry out Thunder, and support to set the proxy, set the Referer,
good-looking command line interaction, and it can download fuck any files; (only supports HTTP[S])

Author: RhythmLian (https://rhythmlian.cn)
"""
from . import size_format, get_fileinfo
from concurrent.futures import ThreadPoolExecutor, wait
from ..ThreadTools import FileWriters
from ..SystemTools import get_core_num
from .. import user_lang, qs_default_console, qs_error_string, qs_info_string, qs_warning_string, headers
from threading import Lock
from requests import get
import signal
import queue
import time
import sys
import os

core_num = get_core_num()
maxBlockSize = int(5e6)
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
    from ..TuiTools.Bar import DataTransformBar

    def __init__(self, url: str, num: int, name: str = '', proxy: str = '',
                 referer: str = '', output_error: bool = False, failed2exit: bool = False, disableStatus: bool = False):
        """
        qs普通文件下载引擎

        Qs general file download engine

        :param url: 文件url
        :param num: 线程数量
        """
        signal.signal(signal.SIGINT, self._kill_self)
        info_flag = True
        self.url, self.num, self.output_error, self.proxies = url, num, output_error, {}
        self.enabled = True
        if not disableStatus:
            with qs_default_console.status('Getting file info..' if user_lang != 'zh' else '获取文件信息中..'):
                self.url, self.name, r = get_fileinfo(url, proxy, referer)
        else:
            self.url, self.name, r = get_fileinfo(url, proxy, referer)
        if not (self.url and self.name and r):
            info_flag = False
            qs_default_console.print(qs_error_string if failed2exit else qs_warning_string,
                                     'Get File information failed, please check network!'
                                     if user_lang != 'zh' else '获取文件信息失败，请检查网络!')
            if failed2exit:
                self.enabled = False
                return
        if self.name and '.' not in self.name:
            self.name = self.name = os.path.basename(url)
        if name:
            self.name = name
        if proxy:
            self.proxies = {
                'http': 'http://'+proxy,
                'https': 'https://'+proxy
            }
        self.headers = headers
        if referer:
            self.headers['Referer'] = referer
        if not self.url:
            qs_default_console.print(qs_error_string, self.name)
            raise Exception('Connection Error!' if user_lang != 'zh' else '连接失败!')
        try:
            if not info_flag:
                raise KeyError
            self.size = int(r.headers['content-length'])
            self.main_progress = Downloader.DataTransformBar()
            self.dl_id = self.main_progress.add_task('Download', filename=self.name, start=False)
            self.main_progress.update(self.dl_id, total=self.size)
            if self.size < 5e6:
                qs_default_console.print(qs_info_string, 'FILE SIZE' if user_lang != 'zh' else '文件大小'
                                         , size_format(self.size))
                self.size = -self.size
            else:
                self.fileBlock = GetBlockSize(self.size)
        except KeyError:
            self.size = -1
            self.main_progress = Downloader.DataTransformBar(False)
            self.dl_id = self.main_progress.add_task('Download', filename=self.name, start=False)
        if self.size > 0:
            self.pool = ThreadPoolExecutor(max_workers=self.num)
            self.futures, self.fileLock = [], Lock()
            self.job_queue = queue.Queue()
            if os.path.exists(self.name + '.qs_dl'):
                self.ctn_file = open(self.name + '.qs_dl', 'r+')
                self.ctn = [int(i) for i in self.ctn_file.read().strip().split()]
            else:
                self.ctn_file = open(self.name + '.qs_dl', 'w')
                self.ctn = []
            self.writers = FileWriters(self.name, max(2, int(core_num / 2)), "rb+" if self.ctn else "wb")
            qs_default_console.print(qs_info_string, 'FILE  SIZE' if user_lang != 'zh' else '文件大小'
                                     , size_format(self.size, align=True))
            qs_default_console.print(qs_info_string, 'THRAED NUM' if user_lang != 'zh' else '线程数量'
                                     , '%7d' % num)

    def _kill_self(self, signum, frame):
        """
        终止下载任务，保存断点

        Terminate the download and save the breakpoint

        :param signum: 信号
        :param frame: frame
        :return: None
        """
        if self.size > 0:
            self.main_progress.stop_task(self.dl_id)
            self.main_progress.stop()
            qs_default_console.print(qs_info_string,
                                     'Get Ctrl-C, exiting...' if user_lang != 'zh' else '捕获Ctrl-C, 正在退出...')
            self.ctn_file.close()
            self.pool.shutdown(wait=False)
            self.writers.wait()
            qs_default_console.print(qs_info_string, 'Deal Done!' if user_lang != 'zh' else '处理完成!')
        os._exit(0)

    def _dl(self, start):
        """
        执行文件块下载任务

        Perform the file block download task

        :param start: 文件块起始偏移量
        :return: None
        """
        try:
            _sz = min(start + self.fileBlock, self.size - 1)
            _headers = self.headers.copy()
            _headers['Range'] = 'bytes={}-{}'.format(start, _sz)
            _content = b''
            for chunk in get(self.url, headers=_headers, timeout=50, proxies=self.proxies).iter_content(65536):
                _content += chunk
                self.main_progress.advance(self.dl_id, sys.getsizeof(chunk))
            self.writers.new_job(_content, start)
        except Exception as e:
            if self.output_error:
                qs_default_console.print(qs_error_string, repr(e))
            self.job_queue.put(start)
        else:
            self.fileLock.acquire()
            self.ctn.append(start)
            self.ctn_file.write('%d\n' % start)
            self.fileLock.release()

    def _single_dl(self):
        """
        无法并行下载或无需并行下载时采用串行下载

        Parallel downloads are not possible or serial downloads are not required

        :return: None
        """
        r = get(self.url, stream=True, proxies=self.proxies, headers=self.headers)
        flag = self.size != -1

        if flag:
            self.main_progress.start_task(self.dl_id)
        else:
            self.main_progress.update(self.dl_id, total=-1)
        with open(self.name, 'wb') as f:
            for chunk in r.iter_content(32768):
                f.write(chunk)
                self.main_progress.advance(self.dl_id, sys.getsizeof(chunk))

    def run(self):
        """
        规划下载任务并开始下载

        qs可以有效应对网络问题对下载任务造成的影响，如：
          1.下载过程中切换代理

          2.链路异常
        并确保下载任务顺利完成

        :return: None
        """
        if not self.enabled:
            return
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
                    qs_default_console.print(qs_warning_string, 'Exists File Block Lost, Retrying after 0.5 sec'
                                             if user_lang != 'zh' else '存在文件块丢失，0.5秒后重试')
                    time.sleep(0.5)
                retry_cnt += 1
            self.writers.wait()
            self.ctn_file.close()
            os.remove(self.name + '.qs_dl')
        else:
            self._single_dl()
        self.main_progress.stop()
        qs_default_console.print(qs_info_string, self.name, 'download done!' if user_lang != 'zh' else '下载完成!')
        return self.name


def normal_dl(url, set_name: str = '', set_proxy: str = '', set_referer: str = '',
              thread_num: int = min(16, core_num * 4), output_error: bool = False, failed2exit: bool = False,
              disableStatus: bool = False):
    """
    自动规划下载线程数量并开始并行下载

    Automatically schedule the number of download threads and begin parallel downloads

    :param disableStatus:
    :param url: 文件url
    :param set_name: 设置文件名（默认采用url所指向的资源名）
    :param set_proxy: 设置代理（默认无代理）
    :param set_referer: 设置referer
    :param thread_num: 线程数
    :param output_error: 输出报错信息
    :param failed2exit: 获取文件信息失败则不下载，否则qs将继续尝试下载
    :return: file name
    """
    return Downloader(
        url=url, num=thread_num, name=set_name, proxy=set_proxy,
        referer=set_referer, output_error=output_error, failed2exit=failed2exit, disableStatus=disableStatus
    ).run()
