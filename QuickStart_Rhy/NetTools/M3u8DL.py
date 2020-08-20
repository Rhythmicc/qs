# coding=utf-8
import urllib3
from concurrent.futures import ThreadPoolExecutor, wait
import requests
import os
from QuickStart_Rhy import dir_char, remove, headers
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
        if proxy:
            M3U8DL.proxies = {
                'http': 'http://'+proxy,
                'https': 'https://'+proxy
            }

    def _dl_one(self, job):
        """
        下载一个ts文件

        Download a TS file

        :param job: 任务信息
        :return: None
        """
        if job[-1]:
            pd_url = job[0]
            c_fule_name = job[1]
            if not os.path.exists(os.path.join(self.path, c_fule_name)):
                res = requests.get(pd_url, verify=False, proxies=M3U8DL.proxies)
                with open(os.path.join(self.path, c_fule_name), 'ab') as f:
                    f.write(res.content)
                    f.flush()
        self._cur += 1
        perc = self._cur / self._all
        leng = int(perc * 40)
        perc *= 100
        print('[%s] %.2f%%' % ('#' * leng + ' ' * (40 - leng), perc),
              end='\n' if self._cur == self._all else '\r')

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
        all_content = requests.get(target, verify=False, headers=headers, proxies=M3U8DL.proxies).text
        if "#EXTM3U" not in all_content:
            raise BaseException("非M3U8的链接")
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
        pool = ThreadPoolExecutor(16)
        work = [pool.submit(self._dl_one, job) for job in file_line]
        wait(work)
        print("Download completed!")
        merge_file(download_path, tmp, self.name)
        remove(download_path)
