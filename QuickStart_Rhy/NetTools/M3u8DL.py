# coding=utf-8
"""
m3u8文件的下载器

The downloader of m3u8 file
"""
import urllib3
from concurrent.futures import ThreadPoolExecutor, wait
import requests
import os
import queue
from .. import dir_char, remove, headers, user_lang, qs_default_console, qs_error_string, qs_info_string
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def merge_file(path, ts_ls, name):
    """
    将全部ts文件合并

    Merge all TS files

    :param path: 文件夹路径
    :param ts_ls: ts文件路径列表
    :param name: 合并后的ts文件名
    :return:
    """
    if not path.endswith(dir_char):
        path += dir_char
    with open(name + '.ts', 'wb') as f:
        for ts in ts_ls:
            with open(path + ts, 'rb') as ff:
                f.write(ff.read())


class M3U8DL:
    from rich.progress import Progress, TimeRemainingColumn, TextColumn, BarColumn

    proxies = {}

    def __init__(self, target, name, proxy: str = ''):
        """
        初始化M3U8下载引擎

        Initialize the M3U8 download engine

        :param target: 目标url
        :param name: 文件名
        """
        self.path = ''
        self._cur = 0
        self._all = 0
        self.target = target
        self.name = name
        self.job_queue = queue.Queue()
        if proxy:
            M3U8DL.proxies = {
                'http': 'http://'+proxy,
                'https': 'https://'+proxy
            }
        self.main_progress = M3U8DL.Progress(
            M3U8DL.TextColumn("[bold blue]{task.fields[taskName]}", justify="right"),
            M3U8DL.BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            M3U8DL.TimeRemainingColumn(),
            console=qs_default_console
        )
        self.dl_id = self.main_progress.add_task("Download", taskName='Downloading' if user_lang != 'zh' else '下载中')

    def _dl_one(self, job):
        """
        下载一个ts文件

        Download a TS file

        :param job: 任务信息
        :return: None
        """
        try:
            if job[-1]:
                pd_url = job[0]
                c_fule_name = job[1]
                if not os.path.exists(os.path.join(self.path, c_fule_name)):
                    res = requests.get(pd_url, verify=False, proxies=M3U8DL.proxies)
                    with open(os.path.join(self.path, c_fule_name), 'ab') as f:
                        f.write(res.content)
                        f.flush()
            self.main_progress.advance(self.dl_id, 1)
        except Exception as e:
            qs_default_console.log(qs_error_string, repr(e))
            self.job_queue.put(job)

    def download(self):
        """
        下载

        :return: None
        """
        target = self.target
        download_path = os.getcwd() + dir_char + self.name
        self.path = download_path
        if not os.path.exists(download_path):
            os.mkdir(download_path)
        try:
            all_content = requests.get(target, verify=False, headers=headers, proxies=M3U8DL.proxies).text
        except Exception as e:
            qs_default_console.log(qs_error_string, repr(e))
            return
        if "#EXTM3U" not in all_content:
            raise Exception("Not M3U8 Link" if user_lang != 'zh' else "非M3U8的链接")
        if "EXT-X-STREAM-INF" in all_content:
            file_line = all_content.split("\n")
            for line in file_line:
                if '.m3u8' in line:
                    target = target.rsplit("/", 1)[0] + "/" + line
                    all_content = requests.get(target, verify=False, headers=headers, proxies=M3U8DL.proxies).text
        file_line = all_content.split("\n")
        _rt = target.rsplit("/", 1)[0] + "/"
        tmp = []
        for index, line in enumerate(file_line):
            if "#EXT-X-KEY" in line:
                tmp.append((_rt, line, 0))
            if "EXTINF" in line:
                tmp.append((_rt + file_line[index + 1], file_line[index + 1].rsplit("/", 1)[-1], 1))
        file_line = tmp[::-1]
        self._all = len(file_line)
        tmp = [jb[1] for jb in file_line]

        self.main_progress.update(self.dl_id, total=len(file_line))
        for i in file_line:
            self.job_queue.put(i)
        pool = ThreadPoolExecutor(16)
        self.main_progress.start()
        self.main_progress.start_task(self.dl_id)
        while not self.job_queue.empty():
            cur_work = []
            while not self.job_queue.empty():
                cur_work.append(pool.submit(self._dl_one, self.job_queue.get()))
            wait(cur_work)
        self.main_progress.stop()

        qs_default_console.print(qs_info_string, "Download completed! Start merge.."
                                 if user_lang != 'zh' else '下载完成! 开始合并..')
        merge_file(download_path, tmp, self.name)
        remove(download_path)
