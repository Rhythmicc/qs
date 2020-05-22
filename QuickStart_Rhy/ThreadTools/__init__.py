import threading
from concurrent.futures import ThreadPoolExecutor, wait


class ThreadFunctionWrapper(threading.Thread):
    def __init__(self, function, *args, **kwargs):
        threading.Thread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.res = None

    def run(self):
        self.res = self.function(*self.args, **self.kwargs)

    def get_res(self):
        return self.res


class FileWriters:
    def __init__(self, filename, workers, mode):
        self.workers = workers
        self.handles = [open(filename, mode) for i in range(workers)]
        self.handles_lock = [threading.Lock() for i in range(workers)]
        self.pool = ThreadPoolExecutor(max_workers=workers)
        self.job_q = []
        self.cur_handle = 0

    def wait(self):
        wait(self.job_q)

    def _write(self, handle: int, content, index):
        fp = self.handles[handle]
        self.handles_lock[handle].acquire()
        fp.seek(index)
        fp.write(content)
        self.handles_lock[handle].release()

    def new_job(self, content, index):
        self.job_q.append(self.pool.submit(self._write, self.cur_handle, content, index))
        self.cur_handle = (self.cur_handle+1) % self.workers

    def __del__(self):
        self.wait()
        self.pool.shutdown()
