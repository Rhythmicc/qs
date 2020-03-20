from QuickStart_Rhy.basic import dir_char


def top():
    import time
    import math
    import psutil
    import colorama
    from prettytable import PrettyTable
    from colorama import Style, ansi, Cursor
    from QuickStart_Rhy.basic import cur_time
    from QuickStart_Rhy.TuiTools import ChartBar
    from QuickStart_Rhy.NetTools.normal_dl import size_format

    def deal():
        print(ansi.clear_screen() + Cursor.POS(0, 0) + Style.RESET_ALL, end='')
        exit(0)

    colorama.init()
    _kernal = psutil.cpu_count()
    _total_mem = psutil.virtual_memory().total
    _cpu_dt = [0] * 40
    _mem_dt = [0] * 40
    _cpu_chart = ChartBar.RollBar(_cpu_dt, height=10)
    _mem_chart = ChartBar.RollBar(_mem_dt, height=10)
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
    from QuickStart_Rhy.SystemTools.Compress import get_tar_name
    tar_name, ls = get_tar_name()
    os.system('tar -czf %s.tar.gz %s' % (tar_name, ' '.join(ls)))


def untar():
    import os
    import sys
    import threading

    file_names = sys.argv[2:]
    if not file_names:
        exit("No enough parameters")

    class _untar(threading.Thread):
        def __init__(self, path):
            threading.Thread.__init__(self)
            self.path = path

        def run(self):
            if os.path.exists(self.path):
                if self.path.endswith('.tar'):
                    os.system('tar -xf %s' % self.path)
                elif self.path.endswith('.gz'):
                    os.system('tar -xzf %s' % self.path)
                elif self.path.endswith('.bz2'):
                    os.system('tar -xjf %s' % self.path)
                else:
                    os.system('tar -xf %s' % self.path)
            else:
                print("No such file or dictionary:%s" % self.path)

    for file_name in file_names:
        t = _untar(file_name)
        t.start()
        t.join()


def mkzip():
    import os
    from QuickStart_Rhy.SystemTools.Compress import get_tar_name
    zip_name, ls = get_tar_name()
    os.system('zip -r -9 %s.zip %s' % (zip_name, ' '.join(ls)))


def unzip():
    import os
    import sys
    import threading

    file_names = sys.argv[2:]
    if not file_names:
        exit("No enough parameters")

    class _unzip(threading.Thread):
        def __init__(self, path):
            threading.Thread.__init__(self)
            self.path = path

        def run(self):
            if os.path.exists(file_name):
                os.system('unzip %s' % file_name)
            else:
                print("No such file or dictionary:%s" % file_name)

    for file_name in file_names:
        t = _unzip(file_name)
        t.start()
        t.join()
