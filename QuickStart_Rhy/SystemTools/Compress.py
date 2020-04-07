import io
import os
import sys
import tarfile
import zipfile
from QuickStart_Rhy import dir_char


def get_tar_name():
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
        if mode == 'read':
            if os.path.exists(path):
                self.src = tarfile.open(path, 'r')
                self.mode = True
            else:
                raise FileNotFoundError
        elif mode == 'write':
            self.src = tarfile.open(path, 'x:gz')
            self.mode = False

    def add_file(self, path):
        if self.mode:
            raise io.UnsupportedOperation
        if os.path.exists(path):
            self.src.add(path)
        else:
            raise FileNotFoundError

    def extract(self):
        if self.mode:
            self.src.extractall()
        else:
            raise io.UnsupportedOperation

    def save(self):
        self.src.close()


class Zip:
    def __init__(self, path, mode='read'):
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
        if self.mode:
            raise io.UnsupportedOperation('not writeable')
        if os.path.exists(path):
            self.src.write(path)
        else:
            raise FileNotFoundError

    def extract(self):
        if self.mode:
            self.src.extractall()
        else:
            raise io.UnsupportedOperation('not readable')

    def save(self):
        self.src.close()
