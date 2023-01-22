# coding=utf-8
"""
命令入口

Command entry
"""
import sys
from .funcList import *
from . import requirePackage


def qs_help(rep=""):
    """输出菜单 | Output menu"""
    if not rep or rep not in menu_table:
        if user_lang != "zh":
            color_rep(
                """
    qs basic   :-> basic   tools help | u, a, f, cal, time, pcat..
    qs system  :-> system  tools help | top, \[mk/un]\[zip/tar/7z]..
    qs net     :-> network tools help | http, dl, netinfo, wifi...
    qs api     :-> api     tools help | trans, smms, rmbg, loli...
    qs image   :-> image   tools help | stbg, v2gif, v2mp3, v2mp4.""",
                True,
            )
            qs_default_console.print("\n[bold]Tutorial[/]\n", justify="center")
        else:
            color_rep(
                """
    qs basic   :-> 基础工具帮助 | u, a, f, cal, time, pcat..
    qs system  :-> 系统工具帮助 | top, \[mk/un]\[zip/tar/7z]..
    qs net     :-> 网络工具帮助 | http, dl, netinfo, wifi...
    qs api     :-> 扩展工具帮助 | trans, smms, rmbg, loli...
    qs image   :-> 图像工具帮助 | stbg, v2gif, v2mp3, v2mp4.""",
                True,
            )
            qs_default_console.print("\n[bold]引导[/]\n", justify="center")
        qs_default_console.print("[bold magenta]qs lesson[/]", justify="center")
    else:
        menu_table[rep]()


def main():
    """执行命令 | Execute"""
    debug_flag = "--qs-debug" in sys.argv
    if debug_flag:
        sys.argv.remove("--qs-debug")
    if len(sys.argv) >= 2:
        try:
            func_name = sys.argv[1]

            from .funcList import cmd_table

            if func_name not in cmd_table:
                qs_help(func_name)
            else:
                func_table = cmd_table[func_name]
                file_name = func_table["self"]
                func_name = func_table[func_name]
                requirePackage(
                    "." if file_name == "basic" else f".{file_name}", func_name
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


if __name__ == "__main__":
    main()
