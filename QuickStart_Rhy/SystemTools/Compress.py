# coding=utf-8
"""
压缩与解压缩各种文件

Compress and decompress all kinds of files
"""
import io
import os
import sys
import tarfile
import zipfile
import rarfile
import py7zr
from .. import dir_char, user_lang, qs_default_console, qs_warning_string


def get_compress_package_name():
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


def checkIsProtocolFile(protocol, path):
    """
    验证压缩包文件

    Verify compressed package file
    :param protocol: 压缩协议 | compress protocol
    :param path: 文件路径 | File Path
    :return:
    """
    if os.path.exists(path):
        if protocol == tarfile and not tarfile.is_tarfile(path):
            raise TypeError(f"{path} " + ('Not recognized by tar protocol' if user_lang != 'zh' else '无法被tar协议识别'))
        elif protocol == zipfile and not zipfile.is_zipfile(path):
            raise TypeError(f"{path} " + ('Not recognized by zip protocol' if user_lang != 'zh' else '无法被zip协议识别'))
        elif protocol == rarfile and not rarfile.is_rarfile(path):
            raise TypeError(f"{path} " + ('Not recognized by rar protocol' if user_lang != 'zh' else '无法被rar协议识别'))
        elif protocol == py7zr and not py7zr.is_7zfile(path):
            raise TypeError(f"{path} " + ('Not recognized by 7z protocol' if user_lang != 'zh' else '无法被7z协议识别'))
    else:
        raise FileNotFoundError


class _NormalCompressedPackage:
    """
    通用压缩协议类，如果你不懂它是做什么的，请不要调用它

    General compression protocol class, if you do not understand what it does, please do not call it
    """
    def __init__(self, _protocol, path: str, mode='r'):
        """
        通用压缩协议类初始化

        General compression protocol class initialization

        :param _protocol: 压缩协议包 | General compression protocol packages
        :param path: 压缩包路径 | compression package path
        :param mode: 读写模式 | 'r' or 'w', which 'r' means read and 'w' means write
        """
        self._protocol = _protocol
        self.path = path
        if mode not in ('r', 'w'):
            raise ValueError("Requires mode 'r', 'w'")
        if mode == 'r':
            checkIsProtocolFile(_protocol, path)
            if _protocol == zipfile:
                self.src = zipfile.ZipFile(path, 'r')
            elif _protocol == rarfile:
                self.src = rarfile.RarFile(path)
            elif _protocol == py7zr:
                self.src = py7zr.SevenZipFile(path, 'r')
            else:
                self.src = _protocol.open(path, 'r')
            self.mode = True
        elif mode == 'w':
            if _protocol == tarfile:
                self.src = _protocol.open(path, 'x:gz')
            elif _protocol == zipfile:
                self.src = _protocol.ZipFile(path, 'w')
            elif _protocol == rarfile:
                raise NotImplementedError('qs not support to create rar file because `RarFile`')
            elif _protocol == py7zr:
                self.src = _protocol.SevenZipFile(path, 'w')
            self.mode = False

    def add_file(self, path):
        """
        向压缩包添加文件（工作在'w'模式下）

        Add file to the compressed package (works in 'w' mode)

        :param path: 文件路径 | File path
        :return: None
        """
        if self.mode:
            raise io.UnsupportedOperation
        if os.path.exists(path):
            if self._protocol == tarfile:
                self.src.add(path)
            elif self._protocol in [zipfile, py7zr]:
                self.src.write(path)
        else:
            raise FileNotFoundError

    def extract(self):
        """
        解压缩 | extract

        :return: None
        """
        if self.mode:
            if self._protocol in [tarfile, rarfile, py7zr]:
                self.src.extractall()
            elif self._protocol in [zipfile]:
                from pathlib import Path
                for fn in self.src.namelist():
                    path = Path(self.src.extract(fn))
                    try:
                        path.rename(fn.encode('cp437').decode('utf-8'))
                    except:
                        try:
                            path.rename(fn.encode('cp437').decode('gbk'))
                        except Exception as e:
                            qs_default_console.log(qs_warning_string, repr(e))

            else:
                raise NotImplementedError
            self.save()
        else:
            raise io.UnsupportedOperation

    def save(self):
        """
        保存 | Save

        :return: None
        """
        self.src.close()


class Tar(_NormalCompressedPackage):
    def __init__(self, path, mode='r'):
        """
        Tar协议初始化

        Tar protocol initialization.

        :param path: 压缩包路径 | The package path is compressed.
        :param mode: 工作模式 | Working mode ('read' or 'write')
        """
        super().__init__(tarfile, path, mode)

    def add_file(self, path):
        """
        向压缩包添加文件（工作在'write'模式下）

        Add files to the compressed package (works in 'write' mode)

        :param path: 文件路径
        :return: None
        """
        return super().add_file(path)

    def extract(self):
        """
        解压缩

        extract

        :return: None
        """
        return super().extract()

    def save(self):
        """保存 | save"""
        return super().save()


class Zip(_NormalCompressedPackage):
    def __init__(self, path, mode='r'):
        """
        Zip协议初始化

        Zip protocol initialization.

        :param path: 压缩包路径 | The package path is compressed.
        :param mode: 工作模式 | Working mode ('read' or 'write')
        """
        super().__init__(zipfile, path, mode)

    def add_file(self, path):
        """
        向压缩包添加文件（工作在'w'模式下）

        Add files to the compressed package (works in 'write' mode)

        :param path: 文件路径
        :return: None
        """
        return super().add_file(path)

    def extract(self):
        """
        解压缩

        extract

        :return: None
        """
        return super().extract()

    def save(self):
        """保存 | save"""
        return super().save()


class Rar(_NormalCompressedPackage):
    def __init__(self, path, mode='r'):
        """
        Rar协议初始化

        Rar protocol initialization.

        :param path: 压缩包路径 | The package path is compressed.
        :param mode: 工作模式 | Working mode ('read' or 'write')
        """
        super().__init__(rarfile, path, mode)

    def add_file(self, path):
        """
        向压缩包添加文件（工作在'w'模式下）

        Add files to the compressed package (works in 'write' mode)

        :param path: 文件路径
        :return: None
        """
        return super().add_file(path)

    def extract(self):
        """
        解压缩

        extract

        :return: None
        """
        return super().extract()

    def save(self):
        """保存 | save"""
        return super().save()


class SevenZip(_NormalCompressedPackage):
    def __init__(self, path, mode='r'):
        """
        7z协议初始化

        7z protocol initialization.

        :param path: 压缩包路径 | The package path is compressed.
        :param mode: 工作模式 | Working mode ('read' or 'write')
        """
        super().__init__(py7zr, path, mode)

    def add_file(self, path):
        """
        向压缩包添加文件（工作在'w'模式下）

        Add files to the compressed package (works in 'write' mode)

        :param path: 文件路径
        :return: None
        """
        return super().add_file(path)

    def extract(self):
        """
        解压缩

        extract

        :return: None
        """
        return super().extract()

    def save(self):
        """保存 | save"""
        return super().save()
