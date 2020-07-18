def set_timeout(num):
    """
    定时函数装饰器

    :param num: 时间（秒）
    :return: wrapper
    """
    def wrapper(func):
        def handle(signum, frame):
            raise RuntimeError

        def run(*args, **kwargs):
            import signal
            try:
                signal.signal(signal.SIGALRM, handle)
                signal.alarm(num)
                res = func(*args, **kwargs)
                signal.alarm(0)
                return res
            except RuntimeError:
                return False
        return run
    return wrapper
