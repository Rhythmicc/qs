# coding=utf-8
"""
命令入口

Command entry
"""
import sys
from .funcList import *
from . import requirePackage


def qs_help(rep:str=""):
    """输出菜单 | Output menu"""
    if not rep or rep not in ['basic', 'system', 'net', 'api', 'image']:
        menu_show([
            ['basic', 'u, a, f, cal, time, pcat..'],
            ['system', 'top, \[mk/un]\[zip/tar/7z]..'],
            ['net', 'http, dl, netinfo, wifi...'],
            ['api', 'trans, smms, rmbg, loli...'],
            ['image', 'stbg, v2gif, v2mp3, v2mp4.']
        ])
        qs_default_console.print(f"\n[bold]{lang_detector['tutorial']}[/]\n", justify="center")
        qs_default_console.print("[bold magenta]qs lesson[/]", justify="center")
    else:
        menu_table(rep)


def main():
    """执行命令 | Execute"""
    debug_flag = "--qs-debug" in sys.argv
    if debug_flag:
        sys.argv.remove("--qs-debug")
    help_flag = '--help' in sys.argv
    if help_flag:
        sys.argv.remove('--help')
    if len(sys.argv) >= 2:
        try:
            func_name = sys.argv[1]
            if func_name not in cmd_table:
                qs_help(func_name)
            else:
                if help_flag:
                    return command_help(func_name)
                func_table = cmd_table[func_name]
                requirePackage(func_table["self"], func_table[func_name][0])()
        except Exception as e:
            from . import qs_default_console

            if debug_flag:
                qs_default_console.print_exception()
            else:
                from . import qs_error_string

                qs_default_console.log(qs_error_string, repr(e))
    else:
        qs_help()


if __name__ == "__main__":
    main()
