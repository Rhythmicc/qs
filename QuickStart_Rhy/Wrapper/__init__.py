# coding=utf-8
"""
qs用到的函数装饰器, 在使用它们前, 请确保你理解注释描述的内容

Before using function decorators used by QS, please make sure that you understand the content described by the annotation.
"""


def set_timeout(num: int):
    """
    定时函数装饰器

    Timing function decorator

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


def mkCompressPackageWrap(func):
    """
    创建压缩文件的通用函数装饰器, 被装饰的函数将被传递压缩文件名, 你需要返回:
        QuickStart_Rhy.SystemTools.Compress._NormalCompressedPackage
    的子类对象, 并将读写状态设为 写 状态

    General function decorator for creating compressed files, the decorated function will be passed the compressed file
    name, which you need to return:
        QuickStart_Rhy.SystemTools.Compress._NormalCompressedPackage
    's sub object, and set read-write mode as write

    :param func: func(filePath: str = '') -> QuickStart_Rhy.SystemTools.Compress._NormalCompressedPackage
    :return: 装饰器 | wrapper
    """
    def wrapper():
        import os
        from .. import dir_char
        from ..SystemTools.Compress import get_compress_package_name
        packages_name, ls = get_compress_package_name()
        packages = func(packages_name)

        def dfs(cur_p):
            if os.path.isfile(cur_p):
                packages.add_file(cur_p)
                return
            file_ls = os.listdir(cur_p)
            flag_ch = '' if cur_p.endswith(dir_char) else dir_char
            for fp in file_ls:
                fp = cur_p + flag_ch + fp
                dfs(fp)

        for i in ls:
            dfs(i)
        packages.save()
    return wrapper


def unCompressPackageWrap(func):
    """
    解压缩文件的通用函数装饰器, 被装饰的函数将被传递压缩文件名, 你需要返回:
        QuickStart_Rhy.SystemTools.Compress._NormalCompressedPackage
    的子类对象, 并将读写状态设为 读 状态

    General function decorator for extracting compressed files, the decorated function will be passed the compressed file
    name, which you need to return:
        QuickStart_Rhy.SystemTools.Compress._NormalCompressedPackage
    's sub object, and set read-write mode as read

    :param func: func(filePath: str = '') -> QuickStart_Rhy.SystemTools.Compress._NormalCompressedPackage
    :return: 装饰器 | wrapper
    """
    def wrapper():
        import os
        import sys

        file_names = sys.argv[2:]
        if not file_names:
            exit("No enough parameters")
        from .. import qs_default_console, qs_error_string
        from ..NetTools.NormalDL import core_num
        from ..ThreadTools import ThreadPoolExecutor, wait
        pool = ThreadPoolExecutor(max_workers=max(core_num // 2, 4))
        job_q = []

        def run(path):
            if os.path.exists(path):
                try:
                    cur_tar = func(path)
                    cur_tar.extract()
                except Exception as e:
                    qs_default_console.log(qs_error_string, repr(e))
            else:
                qs_default_console.log(qs_error_string, "No such file or dictionary: %s" % path)

        for file_name in file_names:
            job_q.append(pool.submit(run, file_name))
        wait(job_q)
    return wrapper


def HashWrapper(algorithm: str):
    """
    文件哈希值计算(通用函数)

    :param algorithm: 算法名称 [md5, sha1, sha256, sha512]
    :return:
    """
    def Wrapper(func):
        def _wrapper():
            import sys, os
            from .. import qs_default_console, qs_info_string, user_lang

            ls = sys.argv[2:]
            if not ls:
                qs_default_console.print(qs_info_string, 'Usage: qs %s file1 file2 ...' % algorithm)
                return

            exec('from QuickStart_Rhy.SystemTools.FileHash import %s' % algorithm)
            for file in ls:
                qs_default_console.print(
                    qs_info_string, 'Calculate:' if user_lang != 'zh' else '计算:', os.path.basename(file)
                )
                exec(f'qs_default_console.print(qs_info_string, "{algorithm}" + ":", {algorithm}("{file}"))')
        return _wrapper
    return Wrapper
