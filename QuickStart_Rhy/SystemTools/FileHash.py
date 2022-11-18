"""
计算各种文件哈希值

Calculate the hash value of various files
"""
import hashlib
import os

BlockSize = 8096


def hashWrapper(algorithm):
    """
    计算文件哈希值(通用)

    :param algorithm: 算法名 [md5, sha1, sha256, sha512]
    :return:
    """

    def Wrapper(func):
        def wrapper(filePath: str) -> str:
            global cal
            if not os.path.exists(filePath):
                return "No such file: " + filePath
            if not os.path.isfile(filePath):
                return "Not a file: " + filePath
            cal = func()
            with open(filePath, "rb") as f:
                while True:
                    data = f.read(BlockSize)
                    if not data:
                        break
                    cal.update(data)
            return cal.hexdigest()

        return wrapper

    return Wrapper


@hashWrapper("md5")
def md5():
    return hashlib.md5()


@hashWrapper("sha1")
def sha1():
    return hashlib.sha1()


@hashWrapper("sha256")
def sha256():
    return hashlib.sha256()


@hashWrapper("sha512")
def sha512():
    return hashlib.sha512()
