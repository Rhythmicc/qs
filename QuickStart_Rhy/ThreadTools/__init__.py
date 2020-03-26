import threading


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
