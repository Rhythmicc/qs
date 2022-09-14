from . import size_format, get_fileinfo
from concurrent.futures import ThreadPoolExecutor, wait
from ..SystemTools import get_core_num
from ..TuiTools.Bar import NormalProgressBar
from .. import user_lang, qs_default_console, qs_error_string, qs_info_string, qs_warning_string, headers, dir_char
from threading import Lock
from requests import get
import queue
import time
import os

core_num = min(get_core_num() * 4, 16)


class MultiSingleDL:
    def __init__(self, urls: list, rt_dir: str, proxy: str = '', referer: str = '', failed2exit: bool = False, save_to_mem: bool = False):
        self.proxy = proxy
        self.referer = referer
        self.proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        } if proxy else {}
        self.headers = headers
        if referer:
            self.headers['Referer'] = referer
        self.rt_dir = rt_dir if rt_dir.endswith(dir_char) else rt_dir + dir_char
        self.failed2exit = failed2exit
        self.save_to_mem = save_to_mem
        self.status_dict = {}
        self.infos = {}
        self.urls = set(urls)
        self.task_num = len(self.urls)
        if self.save_to_mem:
            self.content_ls = [b''] * self.task_num
        self.cur_task_num = 0
        self.qps = None
        self.qps_counter = 0
        self.max_retry = 3
        self.job_queue = queue.Queue()
        self.task_num_lock = Lock()
        self.pool = ThreadPoolExecutor(max_workers=core_num)
        self.status = qs_default_console.status('获取文件信息中...')
        self.progress, self.task_id = NormalProgressBar('多文件下载', self.task_num)

    def _info(self, url):
        real_url, name, r = get_fileinfo(url, self.proxy, self.referer)

        info_flag = True
        if not (url and name and r):
            info_flag = False
            qs_default_console.print(qs_error_string if self.failed2exit else qs_warning_string, url, ':',
                                     'Get File information failed, please check network!'
                                     if user_lang != 'zh' else '获取文件信息失败，请检查网络!')
            if self.failed2exit:
                self.enabled = False
                return

        self.infos[url] = {
            'url': real_url,
            'name': os.path.basename(url) if name and '.' not in name else name,
            'size': -1 if not info_flag else int(r.headers['content-length']) if 'content-length' in r.headers else -1
        }

        self.task_num_lock.acquire()
        self.cur_task_num += 1
        self.status.update(f'获取文件信息中... {self.cur_task_num} / {self.task_num}')
        self.task_num_lock.release()

    def _dl(self, url, filename, job_id, retry=0):
        try:
            r = get(self.infos[url]['url'], stream=True, proxies=self.proxies, headers=self.headers)
            if not self.save_to_mem:
                with open(self.rt_dir + filename, 'wb') as f:
                    for chunk in r.iter_content(32768):
                        f.write(chunk)
            else:
                for chunk in r.iter_content(32768):
                    self.content_ls[job_id] += chunk
            if self.qps:
                self.task_num_lock.acquire()
                self.qps_counter += 1
                if self.qps_counter >= self.qps:
                    self.qps_counter = 0
                self.task_num_lock.release()
                if self.qps_counter == 0:
                    time.sleep(1 / core_num)
            self.progress.advance(self.task_id, 1)
        except Exception as e:
            if retry < self.max_retry:
                qs_default_console.print(qs_warning_string, f'"{url}": {repr(e)},',
                                         'retrying...' if user_lang != 'zh' else '正在重试...')
                self.job_queue.put({
                    'url': url,
                    'filename': filename,
                    'job_id': job_id,
                    'retry': retry + 1
                })
            else:
                qs_default_console.print(qs_error_string, f'"{url}":', 'Download failed!' if user_lang != 'zh' else '下载失败！')
                self.status_dict[url] = 'failed'
                self.progress.advance(self.task_id, 1)

    def run(self, name_map: dict = None, qps: int = None, without_output: bool = False):
        self.qps = qps
        self.status.start()
        wait([self.pool.submit(self._info, item) for item in self.urls])

        total = sum([self.infos[i]['size'] for i in self.infos])
        failed_num = [self.infos[i]['size'] for i in self.infos].count(-1)
        if not without_output:
            qs_default_console.print(qs_info_string, f'获取文件信息完毕! 文件总大小: {size_format(total)} | 未获取到详细信息条数为: {failed_num}')
        self.status.stop()

        for _id, item in enumerate(self.urls):
            self.job_queue.put({
                'url': item,
                'filename': self.infos[item]['name'],
                'job_id': _id
            } if not name_map else {
                'url': item,
                'filename': name_map[item],
                'job_id': _id
            })

        self.progress.start()
        wait_list = []
        while not self.job_queue.empty():
            while not self.job_queue.empty():
                job = self.job_queue.get()
                wait_list.append(self.pool.submit(self._dl, **job))
            wait(wait_list)
        self.progress.stop()
        return [self.rt_dir + self.infos[i]['name'] for i in self.infos] if not name_map else [self.rt_dir + name_map[i] for i in self.infos]

    def get_content_ls(self):
        return self.content_ls


def multi_single_dl(urls: list, rt_dir: str = './', proxy: str = '', referer: str = '',
                    failed2exit: bool = False, name_map: dict = None, qps: int = 0, without_output: bool = False):
    """
    并行多个小文件下载

    :param urls: 小文件的URL
    :param rt_dir: 文件下载目录
    :param proxy: 代理
    :param referer: referer
    :param failed2exit: 信息获取失败立即退出
    :param name_map: 文件命名映射{URL: filename}
    :param qps: 限制每秒请求次数
    :param without_output: 不输出信息
    :return: 下载好的文件路径列表
    """
    return MultiSingleDL(urls=urls, rt_dir=rt_dir, proxy=proxy, referer=referer, failed2exit=failed2exit).run(
        name_map=name_map, qps=qps, without_output=without_output
    )


def multi_single_dl_content_ls(urls: list, rt_dir: str = './', proxy: str = '', referer: str = '',
                               failed2exit: bool = False, qps: int = 0, without_output: bool = False):
    """
    并行多个小文件下载

    :param urls: 小文件的URL
    :param rt_dir: 文件下载目录
    :param proxy: 代理
    :param referer: referer
    :param failed2exit: 信息获取失败立即退出
    :param qps: 限制每秒请求次数
    :param without_output: 不输出信息
    :return: 存储在内存中的文件内容列表
    """
    dl = MultiSingleDL(urls=urls, rt_dir=rt_dir, proxy=proxy, referer=referer, failed2exit=failed2exit, save_to_mem=True)
    dl.run(qps=qps, without_output=without_output)
    return dl.get_content_ls()
