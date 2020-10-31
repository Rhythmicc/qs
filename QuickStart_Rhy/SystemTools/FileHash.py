import hashlib
import os

BlockSize = 8096


def hashWrapper(algorithm):
    def Wrapper(func):
        def wrapper(filePath: str) -> str:
            global cal
            if not os.path.exists(filePath):
                return 'No such file: ' + filePath
            if not os.path.isfile(filePath):
                return 'Not a file: ' + filePath
            cal = func()
            with open(filePath, 'rb') as f:
                while True:
                    data = f.read(BlockSize)
                    if not data:
                        break
                    cal.update(data)
            return cal.hexdigest()
        return wrapper
    return Wrapper


@hashWrapper('md5')
def md5():
    return hashlib.md5()


@hashWrapper('sha1')
def sha1():
    return hashlib.sha1()


@hashWrapper('sha256')
def sha256():
    return hashlib.sha256()


@hashWrapper('sha512')
def sha512():
    return hashlib.sha512()
