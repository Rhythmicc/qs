# coding=utf-8
"""
Docs:
    中文: https://rhythmlian.cn/2020/08/09/QuickStart-Rhy-zh/

    English: https://rhythmlian.cn/2020/02/14/QuickStart-Rhy/
"""
import os
import sys
from .__config__ import QsConfig, dir_char, system
from .NetTools import headers
from rich.console import Console
from rich.prompt import Prompt as qs_default_input

name = 'QuickStart_Rhy'

user_root = os.path.expanduser('~') + dir_char
qs_config = QsConfig(user_root + '.qsrc', os.path.exists(user_root + '.qsrc'))

user_lang = qs_config.basicSelect('default_language')
user_currency = qs_config.basicSelect('default_currency')
trans_engine = qs_config.basicSelect('default_translate_engine')['support']\
[qs_config.basicSelect('default_translate_engine')['index']]

qs_error_string = f'[bold red][{"ERROR" if user_lang != "zh" else "错误"}]'
qs_warning_string = f'[bold yellow][{"WARNING" if user_lang != "zh" else "警告"}]'
qs_info_string = f'[bold cyan][{"INFO" if user_lang != "zh" else "提示"}]'
qs_default_console = Console()


def requirePackage(pname: str, module: str = "", real_name: str = "", not_exit: bool = True):
    """
    获取本机上的python第三方库

    :param pname: 库名
    :param module: 待引入的模块名，可缺省
    :param real_name: 用于 pip3 install 的名字
    :param not_exit: 安装后不退出
    :return: 库或模块的地址
    """
    try:
        exec(f'from {pname} import {module}' if module else f"import {pname}")
    except:
        from PyInquirer import prompt

        confirm = prompt({
            'type': 'confirm',
            'name': 'install',
            'message': f"""Qs require {pname + (' -> ' + module if module else '')}, confirm to install?  
  Qs 依赖 {pname + (' -> ' + module if module else '')}, 是否确认安装?""",
            'default': True})['install']
        if confirm:
            os.system(f'pip3 install {pname if not real_name else real_name}')
            qs_default_console.print(qs_info_string, f'just run again: "{" ".join(sys.argv)}"')
            if not_exit:
                exec(f'from {pname} import {module}' if module else f"import {pname}")
            else:
                exit(0)
        else:
            exit(-1)
    finally:
        return eval(f'{module if module else pname}')


def cut_string(string: str, length: int) -> list:
    """
    每隔l个字符切分字符串

    :param string: 字符串
    :param length: 切分长度
    :return: 切分后产生的list
    """
    string = string.strip().replace('\n', ' ')
    res, cur, cnt = [], '', 0
    for i in string:
        cnt += 2 if ord(i) > 255 else 1
        if cnt <= length:
            cur += i
        else:
            res.append(cur)
            cur, cnt = i, 2 if ord(i) > 255 else 1
    if cur:
        res.append(cur)
    return res


def table_cell(string: str, length: int) -> str:
    return ' '.join(cut_string(string, length))


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


def u(argv: list = None):
    """
    打开命令行参数中的链接

    open urls in argv

    :return: None
    """
    import webbrowser as wb
    from .NetTools import formatUrl
    if not argv:
        argv = sys.argv[2:]
    if argv:
        for url in argv:
            url = formatUrl(url)
            wb.open_new_tab(url)
    else:
        pyperclip = requirePackage('pyperclip')
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
        run(['xdg-open'] + [i for i in argv])
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
    except Exception as e:
        qs_default_console.print(qs_info_string, 'Usage: qs cal <exp like "1+1">')
        qs_default_console.print(qs_error_string, repr(e))


def pcat():
    """
    输出粘贴板中内容

    Output the contents of the clipboard
    :return: None
    """
    print(requirePackage('pyperclip', 'paste')())


def fcopy():
    """
    获取文件内容并复制进粘贴板

    Get the content of the file and copy it into the pasteboard
    :return:
    """
    if not os.path.exists(sys.argv[2]):
        return qs_default_console.print(qs_error_string, "No such file:" if user_lang != 'zh' else '未找到文件:', sys.argv[2])
    with open(sys.argv[2], 'r') as f:
        requirePackage('pyperclip').copy(f.read())
