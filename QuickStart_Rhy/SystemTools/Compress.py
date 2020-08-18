# coding=utf-8
import io
import os
import sys
import tarfile
import zipfile
import rarfile
from QuickStart_Rhy import dir_char


def get_tar_name():
    """
    从命令行参数中，解析并返回压缩包名称

    From the command line arguments, the package name is parsed and returned.

    :return: 压缩包名称，合法的文件列表 | Compressed package name, a list of legitimate files.
    """
    file_names = sys.argv[2:]
    if not file_names:
        exit('No enough parameters')
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


class Tar:
    def __init__(self, path, mode='read'):
        """
        Tar协议初始化

        Tar protocol initialization.

        :param path: 压缩包路径 | The package path is compressed.
        :param mode: 工作模式 | Working mode ('read' or 'write')
        """
        if mode == 'read':
            if os.path.exists(path):
                if not tarfile.is_tarfile(path):
                    raise TypeError("%s not a tar file" % path)
                self.src = tarfile.open(path, 'r')
                self.mode = True
            else:
                raise FileNotFoundError
        elif mode == 'write':
            self.src = tarfile.open(path, 'x:gz')
            self.mode = False

    def add_file(self, path):
        """
        向压缩包添加文件（工作在'write'模式下）

        Add files to the compressed package (works in 'write' mode)

        :param path: 文件路径
        :return: None
        """
        if self.mode:
            raise io.UnsupportedOperation
        if os.path.exists(path):
            self.src.add(path)
        else:
            raise FileNotFoundError

    def extract(self):
        """
        解压缩

        extract

        :return: None
        """
        if self.mode:
            self.src.extractall()
            self.save()
        else:
            raise io.UnsupportedOperation

    def save(self):
        """保存 | save"""
        self.src.close()


class Zip:
    def __init__(self, path, mode='read'):
        """
        ZIP协议初始化

        :param path: 压缩包路径
        :param mode: 工作模式（'read' 或 'write'）
        """
        if mode == 'read':
            if os.path.exists(path):
                self.src = zipfile.ZipFile(path, 'r')
                self.mode = True
            else:
                raise FileNotFoundError
        elif mode == 'write':
            if os.path.exists(path):
                raise io.UnsupportedOperation('File exists!')
            self.src = zipfile.ZipFile(path, 'w')
            self.mode = False

    def add_file(self, path):
        """
        向压缩包添加文件（工作在'write'模式下）

        :param path: 文件路径
        :return: None
        """
        if self.mode:
            raise io.UnsupportedOperation('not writeable')
        if os.path.exists(path):
            self.src.write(path)
        else:
            raise FileNotFoundError

    def extract(self):
        """
        解压缩

        :return: None
        """
        if self.mode:
            self.src.extractall()
            self.save()
        else:
            raise io.UnsupportedOperation('not readable')

    def save(self):
        """保存"""
        self.src.close()


class RAR:
    def __init__(self, path, mode='read'):
        """
        RAR协议初始化

        :param path: 压缩包路径
        :param mode: 工作模式（'read' 或 'write'）
        """
        if mode == 'read':
            if os.path.exists(path):
                path = os.path.abspath(path)
                self.src = rarfile.RarFile(path, 'r')
                self.mode = True
            else:
                raise FileNotFoundError
        elif mode == 'write':
            raise NotImplementedError("qs not support to create rar file because `RarFile`")

    def add_file(self, path: str):
        """
        请勿调用 | Please do not call

        向压缩包添加文件（工作在'write'模式下）

        :param path: 文件路径
        :return: None
        """
        raise io.UnsupportedOperation('not writeable')

    def extract(self, dir_name):
        """
        解压缩

        :return: None
        """
        if self.mode:
            if not (os.path.exists(dir_name) and os.path.isdir(dir_name)):
                os.mkdir(dir_name)
            os.chdir(dir_name)
            self.src.extractall()
            self.save()
        else:
            raise io.UnsupportedOperation('not readable')

    def save(self):
        """保存"""
        self.src.close()
