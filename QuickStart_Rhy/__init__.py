# coding=utf-8
"""
Docs:
    中文: https://rhythmlian.cn/2020/08/09/QuickStart-Rhy-zh/

    English: https://rhythmlian.cn/2020/02/14/QuickStart-Rhy/
"""
import os
import sys
import json
from rich.console import Console
from rich.prompt import Prompt as qs_default_input

name = 'QuickStart_Rhy'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) '
                  'Version/11.0.2 Safari/604.4.7'}
system = sys.platform
if system.startswith('win'):
    dir_char = '\\'
else:
    dir_char = '/'

user_root = os.path.expanduser('~') + dir_char
if os.path.exists(user_root + '.qsrc'):
    with open(user_root + '.qsrc', 'r', encoding='utf8') as f:
        qs_config = json.loads(f.read(), encoding='utf8')
else:
    import QuickStart_Rhy.firstRun as Init
    qs_config = Init.main(user_root)

user_lang = qs_config['basic_settings']['default_language']
trans_engine = qs_config['basic_settings']['default_translate_engine']['support']
trans_engine = trans_engine[qs_config['basic_settings']['default_translate_engine']['index']]
qs_error_string = f'[bold red][{"ERROR" if user_lang != "zh" else "错误"}]'
qs_warning_string = f'[bold yellow][{"WARNING" if user_lang != "zh" else "警告"}]'
qs_info_string = f'[bold cyan][{"INFO" if user_lang != "zh" else "提示"}]'
qs_default_console = Console()


def cut_string(string: str, length: int) -> list:
    """
    每隔l个字符切分字符串

    :param string: 字符串
    :param length: 切分长度
    :return: 切分后产生的list
    """
    return [string[i: i + length] for i in range(0, len(string), length)]


def table_cell(string: str, length: int) -> list:
    if ' ' not in string and '\n' not in string:
        return cut_string(string, length)
    return [string]


def deal_ctrl_c(signum, frame):
    """
    默认的处理ctrl c的函数

    default function to deal [CTRL C]

    :param signum: signum
    :param frame: frame
    :return: None
    """
    if signum or frame or True:
        exit(0)


def remove(path):
    """
    删除文件或文件夹

    delete file or folder.

    :param path: 路径
    :return: None
    """
    if os.path.exists(path):
        if os.path.isdir(path):
            import shutil
            shutil.rmtree(path)
        else:
            os.remove(path)


def cur_time():
    """
    获取当前时间

    get time of now

    :return: None
    """
    week = {
        'Monday': '周一',
        'Tuesday': '周二',
        'Wednesday': '周三',
        'Thursday': '周四',
        'Friday': '周五',
        'Saturday': '周六',
        'Sunday': '周日'
    }
    import time
    tm = time.strftime('%Y年%m月%d日 %A %H:%M:%S', time.localtime(time.time())).split()
    tm[1] = week[tm[1]]
    qs_default_console.print(qs_info_string, ' '.join(tm))


def u():
    """
    打开命令行参数中的链接

    open urls in argv

    :return: None
    """
    import webbrowser as wb
    from .NetTools import formatUrl
    if sys.argv[2:]:
        for url in sys.argv[2:]:
            url = formatUrl(url)
            wb.open_new_tab(url)
    else:
        import pyperclip
        try:
            url = pyperclip.paste()
        except :
            url = qs_default_input.ask(
                'Sorry, but your system is not supported by `pyperclip`\nSo you need input content manually: '
                if user_lang != 'zh' else '抱歉，但是“pyperclip”不支持你的系统\n，所以你需要手动输入内容:'
                , console=qs_default_console)
        wb.open_new_tab(formatUrl(url))


def open_app():
    """
    Mac OS下的open（不支持其他平台）

    open app (only support Mac OS)

    :return: None
    """
    if system == 'darwin':
        os.system('open -a ' + ' '.join(sys.argv[2:]))
    else:
        qs_default_console.print(qs_error_string, '"-a" is only support Mac OS X')


def open_file(argv=None):
    """
    使用合适应用打开文件

    Open file with appropriate application

    :return: None
    """
    if not argv:
        argv = sys.argv[2:]
    if system == 'darwin':
        os.system('open "' + '" "'.join(argv) + '"')
    elif system == 'linux':
        from subprocess import run
        run(['xdg-open'] + ['"' + i + '"' for i in argv])
    else:
        import webbrowser as wb

        for file in argv:
            if os.path.exists(file):
                path = os.path.abspath(file)
                wb.open('file://%s' % path)


def init():
    import webbrowser as wb
    wb.open('http://login.cup.edu.cn')


def calculate():
    """
    执行算数表达式

    Execute the arithmetic expression.

    :return: None
    """
    try:
        exp = ' '.join(sys.argv[2:])
        qs_default_console.print('%s = %s' % (exp, eval(exp)))
    except:
        qs_default_console.log(qs_error_string, 'Usage: qs cal <exp like "1+1">')
