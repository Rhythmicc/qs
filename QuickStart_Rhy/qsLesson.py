# coding=utf-8
"""
命令交互，查看qs的各种菜单和文档

Command interaction, view various menus and documents of QS
"""
from . import user_lang, open_url, _ask


def onlineDocuments():
    import webbrowser as wb

    wb.open(
        "https://rhythmlian.cn/"
        + (
            "2020/02/14/QuickStart-Rhy/"
            if user_lang != "zh"
            else "2020/08/09/QuickStart-Rhy-zh/"
        )
    )


def lesson():
    try:
        res = _ask(
            {
                "type": "list",
                "message": "Welcome using qs, choose and get help:"
                if user_lang != "zh"
                else "欢迎使用qs, 选择以下选项获得帮助:",
                "choices": [
                    "1. basic tools" if user_lang != "zh" else "1. 基础工具",
                    "2. system tools" if user_lang != "zh" else "2. 系统工具",
                    "3. network tools" if user_lang != "zh" else "3. 网络工具",
                    "4. api tools" if user_lang != "zh" else "4. 扩展工具",
                    "5. image tools" if user_lang != "zh" else "5. 图像工具",
                    "6. online Docs" if user_lang != "zh" else "6. 在线文档",
                    "7. join TG group" if user_lang != "zh" else "7. 加入TG群",
                ],
            }
        )
    except KeyboardInterrupt:
        from . import qs_default_console, qs_error_string

        return qs_default_console.print(
            qs_error_string, "User Cancel" if user_lang != "zh" else "用户取消"
        )

    if res[0] == "7":
        return open_url(["https://t.me/joinchat/G2mpk7-S85eM7sb7"])
    else:
        from .funcList import menu_table

        {
            "1": menu_table["basic"],
            "2": menu_table["system"],
            "3": menu_table["net"],
            "4": menu_table["api"],
            "5": menu_table["image"],
            "6": onlineDocuments,
        }[res[0]]()
