from .__config__ import dir_char


class QsCache:
    """
    qs存储在~/.qs_cache的缓存
    """
    import os
    import pickle

    def __init__(self, cachePath: str):
        self.path = cachePath + dir_char
        if not QsCache.os.path.exists(cachePath):
            QsCache.os.mkdir(cachePath)

    def get(self, key: str):
        if not QsCache.os.path.exists(self.path + key):
            return None
        with open(self.path + key, 'rb') as f:
            return QsCache.pickle.loads(f.read())

    def set(self, key: str, value):
        with open(self.path + key, 'wb') as f:
            QsCache.pickle.dump(value, f)

    def delete(self, key: str):
        if QsCache.os.path.exists(self.path + key):
            QsCache.os.remove(self.path + key)

