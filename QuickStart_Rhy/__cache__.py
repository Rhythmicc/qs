import os
import time
import pickle
import atexit

class QsCache:
    """
    qs存储在~/.qs_cache的缓存
    """
    def __init__(self, cachePath: str):
        self.path = cachePath
        self.cache_table_path = os.path.join(self.path, 'qs_cache_table')
        if not os.path.exists(cachePath):
            os.mkdir(cachePath)
        if not os.path.exists(self.cache_table_path):
            self.cache_table = {}
        else:
            with open(self.cache_table_path, 'rb') as f:
                self.cache_table = pickle.load(f)
        need_remove = []
        for item in self.cache_table:
            if not os.path.exists(self.cache_table[item]['path']):
                need_remove.append(item)
        for item in need_remove:
            del self.cache_table[item]
        atexit.register(self.exit)

    def get(self, key: str):
        if key not in self.cache_table:
            return None
        self.cache_table[key]['used'] = time.time()
        with open(self.cache_table[key]['path'], "rb") as f:
            return pickle.load(f)

    def set(self, key: str, value, expire_days: int = 0):
        item_path = os.path.join(self.path, key)
        with open(item_path, "wb") as f:
            pickle.dump(value, f)
        
        self.cache_table[key] = {
            'used': time.time(),
            'expire': expire_days * 24 * 60 * 60,
            'path': item_path
        }

    def delete(self, key: str):
        if key in self.cache_table:
            item_path = self.cache_table[key]['path']
            if os.path.exists(item_path):
                os.remove(item_path)
            del self.cache_table[key]
    
    def save_table(self):
        with open(self.cache_table_path, 'wb') as f:
            pickle.dump(self.cache_table, f)

    def exit(self):
        # auto delete item expired
        remove_key = []
        for key in self.cache_table:
            if self.cache_table[key]['expire'] != 0:
                if time.time() - self.cache_table[key]['used'] > self.cache_table[key]['expire']:
                    remove_key.append(key)
        for key in remove_key:
            self.delete(key)
        self.save_table()
