# coding=utf-8
"""
压缩与解压缩各种文件

Compress and decompress all kinds of files
"""
import io
import os
import sys

from .. import (
    user_lang,
    qs_default_console,
    qs_warning_string,
    requirePackage,
)


def get_compress_package_name():
    """
    从命令行参数中，解析并返回压缩包名称

    From the command line arguments, the package name is parsed and returned.

    :return: 压缩包名称，合法的文件列表 | Compressed package name, a list of legitimate files.
    """
    file_names = sys.argv[2:]
    if not file_names:
        exit("No enough parameters")
    if len(file_names) > 1:
        name = "pigeonhole"
    else:
        name = os.path.basename(file_names[0]).split(".")[0]
    ls = []
    for file_name in file_names:
        if os.path.exists(file_name):
            ls.append(file_name)
        else:
            qs_default_console.print(
                qs_warning_string,
                f"{file_name} not found" if user_lang != "zh" else f"{file_name} 未找到",
            )
    return name, ls


def checkIsProtocolFile(protocol, verify_func, path):
    """
    验证压缩包文件

    Verify compressed package file

    :param protocol: 压缩协议 | compress protocol
    :param path: 文件路径 | File Path
    :return:
    """

    protocol_name = {
        "tarfile": "tar",
        "zipfile": "zip",
        "rarfile": "rar",
        "py7zr": "7z",
    }

    if os.path.exists(path):
        if not requirePackage(protocol, verify_func)(path):
            raise TypeError(
                f"{path} "
                + (
                    f"Not recognized by {protocol_name[protocol]} protocol"
                    if user_lang != "zh"
                    else f"无法被{protocol_name[protocol]}协议识别"
                )
            )
    else:
        raise FileNotFoundError


class _NormalCompressedPackage:
    """
    通用压缩协议类，如果你不懂它是做什么的，请不要调用它

    General compression protocol class, if you do not understand what it does, please do not call it
    """

    def __init__(self, protocol, verify_func, obj_name, path: str, mode="r"):
        """
        通用压缩协议类初始化

        General compression protocol class initialization

        :param protocol: 压缩协议包 | General compression protocol packages
        :param verify_func: 验证函数 | Verification function
        :param obj_name: 对象名称 | Object name
        :param path: 压缩包路径 | compression package path
        :param mode: 读写模式 | 'r' or 'w', which 'r' means read and 'w' means write
        """
        self._protocol = protocol
        self.path = path
        if mode not in ("r", "w"):
            raise ValueError("Requires mode 'r', 'w'")
        if mode == "r":
            checkIsProtocolFile(protocol, verify_func, path)
            if protocol != "rarfile":
                self.src = requirePackage(protocol, obj_name)(path, "r")
            else:
                self.src = requirePackage(protocol, obj_name)(path)
            self.mode = True
        elif mode == "w":
            if protocol != "rarfile":
                self.src = requirePackage(protocol, obj_name)(path, "w")
            else:
                raise NotImplementedError(
                    "qs not support to create rar file because `RarFile`"
                )
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
        if not os.path.exists(path):
            raise FileNotFoundError
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if self._protocol == "tarfile":
                        self.src.add(os.path.join(root, file))
                    elif self._protocol in ["zipfile", "py7zr"]:
                        self.src.write(os.path.join(root, file))
        else:
            if self._protocol == "tarfile":
                self.src.add(path)
            elif self._protocol in ["zipfile", "py7zr"]:
                self.src.write(path)

    def extract(self):
        """
        解压缩 | extract

        :return: None
        """
        if self.mode:
            if self._protocol in ["tarfile", "rarfile", "py7zr"]:
                self.src.extractall()
            elif self._protocol == "zipfile":
                from pathlib import Path

                for fn in self.src.namelist():
                    path = Path(self.src.extract(fn))
                    try:
                        path.rename(fn.encode("cp437").decode("utf-8"))
                    except:
                        try:
                            path.rename(fn.encode("cp437").decode("gbk"))
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
    def __init__(self, path, mode="r"):
        """
        Tar协议初始化

        Tar protocol initialization.

        :param path: 压缩包路径 | The package path is compressed.
        :param mode: 工作模式 | Working mode ('read' or 'write')
        """
        super().__init__("tarfile", "is_tarfile", "TarFile", path, mode)

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
    def __init__(self, path, mode="r"):
        """
        Zip协议初始化

        Zip protocol initialization.

        :param path: 压缩包路径 | The package path is compressed.
        :param mode: 工作模式 | Working mode ('read' or 'write')
        """
        super().__init__("zipfile", "is_zipfile", "ZipFile", path, mode)

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
    def __init__(self, path, mode="r"):
        """
        Rar协议初始化

        Rar protocol initialization.

        :param path: 压缩包路径 | The package path is compressed.
        :param mode: 工作模式 | Working mode ('read' or 'write')
        """
        super().__init__("rarfile", "is_rarfile", "RarFile", path, mode)

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
    def __init__(self, path, mode="r"):
        """
        7z协议初始化

        7z protocol initialization.

        :param path: 压缩包路径 | The package path is compressed.
        :param mode: 工作模式 | Working mode ('read' or 'write')
        """
        super().__init__("py7zr", "is_7zfile", "SevenZipFile", path, mode)

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
