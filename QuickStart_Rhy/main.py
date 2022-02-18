# coding=utf-8
"""
命令入口

Command entry
"""
import sys
from .funcList import *
from . import requirePackage


def qs_help(rep=''):
    """输出菜单 | Output menu"""
    if not rep or rep not in menu_table:
        if user_lang != 'zh':
            color_rep("""
    qs basic   :-> basic   tools help | u, a, f, cal, time, pcat..
    qs system  :-> system  tools help | top, \[mk/un]\[zip/tar/7z]..
    qs net     :-> network tools help | http, dl, netinfo, wifi...
    qs api     :-> api     tools help | trans, smms, rmbg, loli...
    qs image   :-> image   tools help | stbg, v2gif, v2mp3, v2mp4.""", True)
            qs_default_console.print('\n[underline]Tutorial[/underline]\n', justify='center')
            qs_default_console.print('[bold magenta]qs lesson[/bold magenta]', justify='center')
            qs_default_console.print('\n[underline]Docs\n', justify='center')
            qs_default_console.print('C D N : https://rhythmlian.cn/2020/02/14/QuickStart-Rhy/ _ _ _', justify='center')
            qs_default_console.print('Github: https://rhythmicc.github.io/2020/02/14/QuickStart-Rhy/', justify='center')
            qs_default_console.print('\n[underline]TG Group:\n', justify='center')
            qs_default_console.print('https://t.me/joinchat/G2mpk7-S85eM7sb7', justify='center')
        else:
            color_rep("""
    qs basic   :-> 基础工具帮助 | u, a, f, cal, time, pcat..
    qs system  :-> 系统工具帮助 | top, \[mk/un]\[zip/tar/7z]..
    qs net     :-> 网络工具帮助 | http, dl, netinfo, wifi...
    qs api     :-> 扩展工具帮助 | trans, smms, rmbg, loli...
    qs image   :-> 图像工具帮助 | stbg, v2gif, v2mp3, v2mp4.""", True)
            qs_default_console.print('\n[underline]引导[/underline]\n', justify='center')
            qs_default_console.print('[bold magenta]qs lesson[/bold magenta]', justify='center')
            qs_default_console.print('\n[underline]文档[/underline]\n', justify='center')
            qs_default_console.print('C D N : https://rhythmlian.cn/2020/08/09/QuickStart-Rhy-zh/ _ _ _', justify='center')
            qs_default_console.print('Github: https://rhythmicc.github.io/2020/08/09/QuickStart-Rhy-zh/', justify='center')
            qs_default_console.print('\n[underline]TG群[/underline]\n', justify='center')
            qs_default_console.print('https://t.me/joinchat/G2mpk7-S85eM7sb7', justify='center')
    else:
        menu_table[rep]()


def main():
    """执行命令 | Execute"""
    debug_flag = '--qs-debug' in sys.argv
    if debug_flag:
        sys.argv.remove('--qs-debug')
    if len(sys.argv) >= 2:
        try:
            func_name = sys.argv[1]
            cmd_config = {j: i for i in [basic_funcs, api_funcs, net_funcs, image_funcs, system_funcs] for j in i}
            cmd_config.pop('self')
            if func_name not in cmd_config:
                qs_help(func_name)
            else:
                func_table = cmd_config[func_name]
                file_name = func_table['self']
                func_name = func_table[func_name]
                (
                    requirePackage('QuickStart_Rhy', func_name)
                    if file_name == 'basic' else
                    requirePackage(f'QuickStart_Rhy.{file_name}', func_name)
                )()
        except Exception as e:
            from . import qs_default_console
            if debug_flag:
                qs_default_console.print_exception()
            else:
                from . import qs_error_string
                qs_default_console.log(qs_error_string, repr(e))
    else:
        qs_help()


if __name__ == '__main__':
    main()
