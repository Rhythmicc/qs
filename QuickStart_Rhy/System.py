from QuickStart_Rhy import dir_char


def top():
    import time
    import math
    import psutil
    import colorama
    from prettytable import PrettyTable
    from colorama import Style, ansi, Cursor
    from QuickStart_Rhy import cur_time
    from QuickStart_Rhy.TuiTools import Bar
    from QuickStart_Rhy.NetTools.normal_dl import size_format

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


def mktar():
    import os
    from QuickStart_Rhy.SystemTools.Compress import get_tar_name, Tar
    tar_name, ls = get_tar_name()
    tar = Tar(tar_name+'.tar.gz', 'write')

    def dfs(cur_p):
        if os.path.isfile(cur_p):
            tar.add_file(cur_p)
            return
        file_ls = os.listdir(cur_p)
        flag = cur_p.endswith(dir_char)
        for fp in file_ls:
            fp = cur_p + ('' if flag else dir_char) + fp
            dfs(fp)
    for i in ls:
        dfs(i)
    tar.save()


def untar():
    import os
    import sys

    file_names = sys.argv[2:]
    if not file_names:
        exit("No enough parameters")
    from QuickStart_Rhy.SystemTools.Compress import Tar
    from QuickStart_Rhy.NetTools.normal_dl import core_num
    from QuickStart_Rhy.ThreadTools import ThreadPoolExecutor, wait

    pool = ThreadPoolExecutor(max_workers=max(core_num // 2, 4))
    job_q = []

    def run(path):
        if os.path.exists(path):
            cur_tar = Tar(path)
            cur_tar.extract()
            del cur_tar
        else:
            print("No such file or dictionary:%s" % path)

    for file_name in file_names:
        job_q.append(pool.submit(run, file_name))
    wait(job_q)


def mkzip():
    import os
    from QuickStart_Rhy.SystemTools.Compress import get_tar_name, Zip
    zip_name, ls = get_tar_name()
    z = Zip(zip_name+'.zip', mode='write')

    def dfs(cur_p):
        if os.path.isfile(cur_p):
            z.add_file(cur_p)
            return
        file_ls = os.listdir(cur_p)
        flag = cur_p.endswith(dir_char)
        for fp in file_ls:
            fp = cur_p + ('' if flag else dir_char) + fp
            dfs(fp)
    for i in ls:
        dfs(i)
    z.save()


def unzip():
    import os
    import sys

    file_names = sys.argv[2:]
    if not file_names:
        exit("No enough parameters")
    from QuickStart_Rhy.SystemTools.Compress import Zip
    from QuickStart_Rhy.NetTools.normal_dl import core_num
    from QuickStart_Rhy.ThreadTools import ThreadPoolExecutor, wait

    pool = ThreadPoolExecutor(max_workers=max(core_num // 2, 4))
    job_q = []

    def run(path):
        if os.path.exists(path):
            try:
                z = Zip(path)
                z.extract()
            except:
                print('[ERROR] %s extract failed!' % path)
        else:
            print("No such file or dictionary:%s" % path)

    for file_name in file_names:
        job_q.append(pool.submit(run, file_name))
    wait(job_q)
