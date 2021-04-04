"""
CPU和内存监测, 但是很丑, 只工作在啥他妈都不支持的Windows命令行中

CPU and memory monitoring, but very ugly, only works in the Windows command line which does not support fuck anything
"""


def top():
    """
    CPU和内存监测

    CPU and memory monitoring

    :return: None
    """
    import time
    import math
    import colorama
    from colorama import Style, ansi, Cursor
    from .. import cur_time, dir_char, requirePackage
    from ..TuiTools import Bar
    from ..NetTools.NormalDL import size_format
    psutil = requirePackage('psutil')
    PrettyTable = requirePackage('prettytable', 'PrettyTable')

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
            cur_img = '    '.join(str(window).split('\n') + [' '])
            print(cur_img)
            time.sleep(1)
    except:
        deal()
