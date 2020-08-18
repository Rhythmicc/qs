# coding=utf-8
import threading
from concurrent.futures import ThreadPoolExecutor, wait


class ThreadFunctionWrapper(threading.Thread):
    def __init__(self, function, *args, **kwargs):
        """
        开辟子线程执行任务（初始化）

        Create child threads to perform tasks (initialization)

        :param function: 函数
        :param args: 参数
        :param kwargs: 参数
        """
        threading.Thread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.res = None

    def run(self):
        """
        执行任务，结果保存在self.res

        Execute the task and save the results in self.res

        :return: None
        """
        self.res = self.function(*self.args, **self.kwargs)

    def get_res(self):
        """
        获取任务执行结果

        Gets the task execution results

        :return: self.res
        """
        return self.res


class FileWriters:
    def __init__(self, filename: str, workers: int, mode: str):
        """
        写文件线程池，为了适配密集io而设计的并行写算法。(采用多个文件指针加速)

        Write file thread pool, a parallel write algorithm designed to accommodate dense IO.
        (Multiple file pointer acceleration)

        :param filename: 文件名
        :param workers: 线程数
        :param mode: 读写模式，如'wb', 'rb+'
        """
        self.workers = workers
        self.handles = [open(filename, mode) for i in range(workers)]
        self.handles_lock = [threading.Lock() for i in range(workers)]
        self.pool = ThreadPoolExecutor(max_workers=workers)
        self.job_q = []
        self.cur_handle = 0

    def wait(self):
        """
        等待完全完成任务

        Wait for the task to complete

        :return:
        """
        wait(self.job_q)

    def _write(self, handle: int, content, index):
        fp = self.handles[handle]
        self.handles_lock[handle].acquire()
        fp.seek(index)
        fp.write(content)
        self.handles_lock[handle].release()

    def new_job(self, content: bytes, index: int):
        """
        写入新的文件块

        Write a new file block

        :param content: 文件内容
        :param index: 起始位置
        :return:
        """
        self.job_q.append(self.pool.submit(self._write, self.cur_handle, content, index))
        self.cur_handle = (self.cur_handle+1) % self.workers

    def __del__(self):
        """
        删除对象，必须等待线程池工作结束

        To delete an object, you must wait for the thread pool to finish working

        :return:
        """
        self.wait()
        self.pool.shutdown()
