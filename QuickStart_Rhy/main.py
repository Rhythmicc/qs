# coding=utf-8
import sys
from QuickStart_Rhy.func_list import *


def qs_help(rep=''):
    """输出菜单 | Output menu"""
    if not rep or rep not in menu_table:
        if user_lang != 'zh':
            print('help:')
            print(color_rep("""
    qs -basic   :-> basic   tools help | -u, -a, -f, -cal, -time
    qs -system  :-> system  tools help | -top, -[mk/un][zip/tar]...
    qs -net     :-> network tools help | -http, -dl, -up[load/grade]
    qs -api     :-> api     tools help | -trans, -smms, -rmbg...
    qs -image   :-> image   tools help | -stbg, -v2gif, -v2mp4..."""))
            print('Docs:\n  · 1: ' + Fore.CYAN + 'https://rhythmlian.cn/2020/02/14/QuickStart-Rhy/' + Style.RESET_ALL)
            print('  · 2: ' + Fore.CYAN + 'https://rhythmicc.github.io/2020/02/14/QuickStart-Rhy/' + Style.RESET_ALL)
        else:
            print("帮助:")
            print(color_rep("""
    qs -basic   :-> 基础工具帮助 | -u, -a, -f, -cal, -time
    qs -system  :-> 系统工具帮助 | -top, -[mk/un][zip/tar]...
    qs -net     :-> 网络工具帮助 | -http, -dl, -up[load/grade]
    qs -api     :-> 扩展工具帮助 | -trans, -smms, -rmbg...
    qs -image   :-> 图像工具帮助 | -stbg, -v2gif, -v2mp4..."""))
            print('文档:\n  · 1: ' + Fore.CYAN + 'https://rhythmlian.cn/2020/02/14/QuickStart-Rhy/' + Style.RESET_ALL)
            print('  · 2: ' + Fore.CYAN + 'https://rhythmicc.github.io/2020/02/14/QuickStart-Rhy/' + Style.RESET_ALL)
    else:
        menu_table[rep]()


cmd_config = {}
for i in basic_funcs:
    if i.startswith('-'):
        cmd_config[i] = basic_funcs
for i in api_funcs:
    if i.startswith('-'):
        cmd_config[i] = api_funcs
for i in net_funcs:
    if i.startswith('-'):
        cmd_config[i] = net_funcs
for i in image_funcs:
    if i.startswith('-'):
        cmd_config[i] = image_funcs
for i in system_funcs:
    if i.startswith('-'):
        cmd_config[i] = system_funcs


def main():
    """执行命令 | Execute"""
    if len(sys.argv) >= 2:
        func_name = sys.argv[1]
        if func_name not in cmd_config:
            qs_help(func_name)
        else:
            func_table = cmd_config[func_name]
            file_name = func_table['self']
            func_name = func_table[func_name]
            if file_name == 'basic':
                exec('from QuickStart_Rhy import %s' % func_name)
            else:
                exec('from QuickStart_Rhy.%s import %s' % (file_name, func_name))
            eval('%s()' % func_name)
    else:
        qs_help()


if __name__ == '__main__':
    main()
