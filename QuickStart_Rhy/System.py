# coding=utf-8
from QuickStart_Rhy import dir_char, system

miss_file = ['.DS_Store']


def top():
    """
    CPU和内存监测

    CPU and memory monitoring

    :return: None
    """
    import time
    import math
    import psutil
    import colorama
    from prettytable import PrettyTable
    from colorama import Style, ansi, Cursor
    from QuickStart_Rhy import cur_time
    from QuickStart_Rhy.TuiTools import Bar
    from QuickStart_Rhy.NetTools.NormalDL import size_format

    def deal():
        print(ansi.clear_screen() + Cursor.POS(0, 0) + Style.RESET_ALL, end='')
        exit(0)

    colorama.init()
    _kernal = psutil.cpu_count()
    _total_mem = psutil.virtual_memory().total
    _cpu_dt = [0] * 40
    _mem_dt = [0] * 40
    _cpu_chart = Bar.RollBar(_cpu_dt, height=10)
    _mem_chart = Bar.RollBar(_mem_dt, height=10)
    charts = [_cpu_chart, _mem_chart]
    window = PrettyTable()
    window.add_row(charts)
    print(ansi.clear_screen())
    try:
        while True:
            _cpu_cur = sum(psutil.cpu_percent(percpu=True)) / _kernal
            _mem_cur = psutil.virtual_memory().used
            _cpu_chart.add(math.ceil(_cpu_cur))
            _mem_chart.add(math.ceil(_mem_cur / _total_mem * 100))
            window.field_names = ['CPU: %.2f%%' % _cpu_cur, 'MEM: %s' % size_format(_mem_cur)]
            print((ansi.clear_screen() if dir_char == '\\' else '') + Cursor.POS(0, 0))
            print(' ' * 39, end='')
            cur_time()
            cur_img = str(window).split('\n')
            for i in cur_img:
                print(' ' * 4, end='')
                print(i)
            time.sleep(1)
    except:
        deal()


def clear_mem():
    """
    清理系统内存

    Clean system memory

    :return: None
    """
    if dir_char == '\\':
        print("Not support")
    else:
        import os
        if system.startswith("darwin"):
            os.system("sudo purge")
        else:
            os.system('sync')
            os.system("echo 3 > /proc/sys/vm/drop_caches")


def mktar():
    """
    创建tar包

    Create a tar packages

    :return: None
    """
    import os
    from QuickStart_Rhy.SystemTools.Compress import get_tar_name, Tar
    tar_name, ls = get_tar_name()
    tar = Tar(tar_name+'.tar.gz', 'write')

    def dfs(cur_p):
        if os.path.isfile(cur_p):
            tar.add_file(cur_p)
            return
        file_ls = os.listdir(cur_p)
        flag_ch = '' if cur_p.endswith(dir_char) else dir_char
        for fp in file_ls:
            fp = cur_p + flag_ch + fp
            dfs(fp)
    for i in ls:
        dfs(i)
    tar.save()


def untar():
    """
    解压tar包

    Unpack the tar packages

    :return: None
    """
    import os
    import sys

    file_names = sys.argv[2:]
    if not file_names:
        exit("No enough parameters")
    from QuickStart_Rhy.SystemTools.Compress import Tar
    from QuickStart_Rhy.NetTools.NormalDL import core_num
    from QuickStart_Rhy.ThreadTools import ThreadPoolExecutor, wait

    pool = ThreadPoolExecutor(max_workers=max(core_num // 2, 4))
    job_q = []

    def run(path):
        if os.path.exists(path):
            try:
                cur_tar = Tar(path)
                cur_tar.extract()
            except Exception as e:
                print('[ERROR] %s' % e)
        else:
            print("No such file or dictionary:%s" % path)

    for file_name in file_names:
        job_q.append(pool.submit(run, file_name))
    wait(job_q)


def mkzip():
    """
    创建ZIP包

    Create a ZIP package

    :return: None
    """
    import os
    from QuickStart_Rhy.SystemTools.Compress import get_tar_name, Zip
    zip_name, ls = get_tar_name()
    z = Zip(zip_name+'.zip', mode='write')

    def dfs(cur_p):
        if os.path.isfile(cur_p):
            z.add_file(cur_p)
            return
        file_ls = os.listdir(cur_p)
        flag_ch = '' if cur_p.endswith(dir_char) else dir_char
        for fp in file_ls:
            fp = cur_p + flag_ch + fp
            dfs(fp)
    for i in ls:
        dfs(i)
    z.save()


def unzip():
    """
    解压ZIP包

    Unpack the ZIP package

    :return: None
    """
    import os
    import sys

    file_names = sys.argv[2:]
    if not file_names:
        exit("No enough parameters")
    from QuickStart_Rhy.SystemTools.Compress import Zip
    from QuickStart_Rhy.NetTools.NormalDL import core_num
    from QuickStart_Rhy.ThreadTools import ThreadPoolExecutor, wait

    pool = ThreadPoolExecutor(max_workers=max(core_num // 2, 4))
    job_q = []

    def run(path):
        if os.path.exists(path):
            try:
                z = Zip(path)
                z.extract()
            except Exception as e:
                print('[ERROR] %s' % e)
        else:
            print("[ERROR] No such file or dictionary:%s" % path)

    for file_name in file_names:
        job_q.append(pool.submit(run, file_name))
    wait(job_q)


def unrar():
    """
    解压RAR包

    Extract RAR package

    :return: None
    """
    import os
    import sys

    file_names = sys.argv[2:]
    if not file_names:
        exit("No enough parameters")
    from QuickStart_Rhy.SystemTools.Compress import RAR
    from QuickStart_Rhy.NetTools.NormalDL import core_num
    from QuickStart_Rhy.ThreadTools import ThreadPoolExecutor, wait

    pool = ThreadPoolExecutor(max_workers=max(core_num // 2, 4))
    job_q = []

    def run(path):
        if os.path.exists(path):
            try:
                z = RAR(path)
                z.extract(os.path.basename(path).split('.')[0])
            except Exception as e:
                print('[ERROR] %s' % e)
        else:
            print("No such file or dictionary:%s" % path)

    for file_name in file_names:
        job_q.append(pool.submit(run, file_name))
    wait(job_q)
