# coding=utf-8
"""
Docs for different language:
    中文: https://rhythmlian.cn/2020/08/09/QuickStart-Rhy-zh/

    English: https://rhythmlian.cn/2020/02/14/QuickStart-Rhy/
"""
import os
import sys

from QuickProject import QproDefaultStatus as qs_default_status
from QuickProject import external_exec, user_pip

from .__cache__ import QsCache
from .__config__ import (
    QsConfig,
    dir_char,
    platform,
    qs_default_console,
    _ask,
    user_lang,
)

name = "QuickStart_Rhy"

user_root = os.path.expanduser("~")
qs_config = QsConfig(os.path.join(user_root, ".qsrc"))
qs_cache = QsCache(os.path.join(user_root, ".qs_cache"))

user_currency = qs_config.basicSelect("default_currency")
trans_engine = qs_config.basicSelect("default_translate_engine")["support"][
    qs_config.basicSelect("default_translate_engine")["index"]
]
force_show_img = qs_config.basicSelect("force_show_img")

qs_error_string = f'[bold red][{"ERROR" if user_lang != "zh" else "错误"}]'
qs_warning_string = f'[bold yellow][{"WARNING" if user_lang != "zh" else "警告"}]'
qs_info_string = f'[bold cyan][{"INFO" if user_lang != "zh" else "提示"}]'
qs_console_width = qs_default_console.width


def requirePackage(
    pname: str,
    module: str = "",
    real_name: str = "",
    not_exit: bool = True,
    not_ask: bool = False,
    set_pip: str = user_pip,
):
    """
    获取本机上的python第三方库

    :param pname: 库名
    :param module: 待引入的模块名，可缺省
    :param real_name: 用于 pip3 install 的名字
    :param not_exit: 安装后不退出
    :param not_ask: 不询问
    :param set_pip: pip3的路径
    :return: 库或模块的地址
    """
    try:
        exec(f"from {pname} import {module}" if module else f"import {pname}")
    except (ModuleNotFoundError, ImportError):
        if not_ask:
            return None
        if _ask(
            {
                "type": "confirm",
                "message": f"""Qs require {pname + (' -> ' + module if module else '')}, confirm to install?"""
                if user_lang != "zh"
                else f"""Qs 依赖 {pname + (' -> ' + module if module else '')}，确认安装吗？""",
                "default": True,
            }
        ):
            with qs_default_status(
                f"Installing {pname if not real_name else real_name}"
                if user_lang != "zh"
                else f"正在安装 {pname if not real_name else real_name}"
            ):
                st, _ = external_exec(
                    f"{set_pip} install {pname if not real_name else real_name} -U",
                    True,
                )
            if st:
                qs_default_console.print(
                    qs_error_string,
                    f"Install {pname + (' -> ' + module if module else '')} failed, please install it manually: "
                    if user_lang != "zh"
                    else f"安装 {pname + (' -> ' + module if module else '')} 失败，请手动安装: ",
                    f"'{set_pip} install {pname if not real_name else real_name} -U'",
                )
                exit(-1)
            if not_exit:
                exec(f"from {pname} import {module}" if module else f"import {pname}")
            else:
                qs_default_console.print(
                    qs_info_string,
                    "Install complete! Run again:"
                    if user_lang != "zh"
                    else f"安装完成！再次运行:",
                    " ".join(sys.argv),
                )
                exit(0)
        else:
            exit(-1)
    return eval(f"{module if module else pname}")


def cut_string(string: str, length: int) -> list:
    """
    每隔l个字符切分字符串

    :param string: 字符串
    :param length: 切分长度
    :return: 切分后产生的list
    """
    string = string.strip()
    res, cur, cnt = [], "", 0
    for i in string:
        _char_len = 2 if ord(i) > 255 else 1 if ord(i) > 127 else 1.5
        cnt += _char_len
        if cnt <= length:
            cur += i
        else:
            res.append(cur)
            cur, cnt = i, _char_len
    if cur:
        res.append(cur)
    return res


def _is_in_path(cmd: str):
    """
    判断cmd是否在环境变量中

    :param cmd: 命令
    :return: 是否在环境变量中
    """
    import os

    ls = os.environ["PATH"].split(os.pathsep)
    for prefix in ls:
        if os.path.exists(os.path.join(prefix, cmd)):
            return True
    return False


def table_cell(string: str, length: int) -> str:
    return "\n".join(cut_string(string, length))


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
        "Monday": "周一",
        "Tuesday": "周二",
        "Wednesday": "周三",
        "Thursday": "周四",
        "Friday": "周五",
        "Saturday": "周六",
        "Sunday": "周日",
    }
    import time

    tm = time.strftime("%Y年%m月%d日 %A %H:%M:%S", time.localtime(time.time())).split()
    tm[1] = week[tm[1]]
    qs_default_console.print(qs_info_string, " ".join(tm))


def open_url(argv: list = None):
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
        pyperclip = requirePackage("pyperclip")
        try:
            url = pyperclip.paste()
        except:
            url = _ask(
                {
                    "type": "input",
                    "message": "Sorry, but your system is not supported by `pyperclip`\n  So you need input content manually: "
                    if user_lang != "zh"
                    else "抱歉，但是“pyperclip”不支持你的系统\n  所以你需要手动输入内容:",
                }
            )
        wb.open_new_tab(formatUrl(url))


def open_app():
    """
    Mac OS下的open（不支持其他平台）

    open app (only support Mac OS)

    :return: None
    """
    if platform == "darwin":
        external_exec('open -a "' + '" "'.join(sys.argv[2:]) + '"')
    else:
        return qs_default_console.print(
            qs_error_string,
            '"copy" is only support Mac OS X'
            if user_lang != "zh"
            else '"copy" 只支持Mac OS X',
        )


def open_file(*argv):
    """
    使用合适应用打开文件

    Open file with appropriate application

    :return: None
    """
    if not argv:
        argv = sys.argv[2:]
    if platform == "darwin":
        external_exec('open "' + '" "'.join(argv) + '"')
    elif platform == "linux":
        external_exec('xdg-open "' + '" "'.join(argv) + '"')
    else:
        for file in argv:
            os.startfile(os.path.abspath(file))


def calculate():
    """
    执行算数表达式

    Execute the arithmetic expression.

    :return: None
    """
    try:
        exp = " ".join(sys.argv[2:])
        qs_default_console.print("%s = %s" % (exp, eval(exp)))
    except Exception as e:
        qs_default_console.print(qs_info_string, 'Usage: qs cal <exp like "1+1">')
        qs_default_console.print(qs_error_string, repr(e))


def pcat():
    """
    输出粘贴板中内容

    Output the contents of the clipboard
    :return: None
    """
    print(requirePackage("pyperclip", "paste")())


def fcopy():
    """
    获取文件内容并复制进粘贴板

    Get the content of the file and copy it into the pasteboard
    :return:
    """
    if not os.path.exists(sys.argv[2]):
        return qs_default_console.print(
            qs_error_string,
            "No such file:" if user_lang != "zh" else "未找到文件:",
            sys.argv[2],
        )
    with open(sys.argv[2], "r") as f:
        requirePackage("pyperclip").copy(f.read())


def copy():
    """
    复制文件到粘贴板
    :return:
    """

    def which(command):
        return False if external_exec("which %s" % command, True)[0] else True

    if platform != "darwin":
        return qs_default_console.print(
            qs_error_string,
            '"copy" is only support Mac OS X'
            if user_lang != "zh"
            else '"copy" 只支持Mac OS X',
        )

    if not os.path.exists(sys.argv[2]):
        return qs_default_console.print(
            qs_error_string,
            "No such file:" if user_lang != "zh" else "未找到文件:",
            sys.argv[2],
        )
    # 检查 pbadd 是否在 PATH 中
    if not which("pbadd"):
        from QuickStart_Rhy.NetTools.NormalDL import normal_dl

        normal_dl(
            "https://cos.rhythmlian.cn/ImgBed/86438ea0f489a2c75ff7263eda630005",
            set_name="pbadd",
        )
        external_exec("chmod +x pbadd")
        external_exec("mv pbadd /usr/local/bin/")
    external_exec("pbadd " + sys.argv[2], True)


def get_user_lang():
    print(user_lang)


def play_music(*argv, using_afplay: bool = False):
    if not argv:
        argv = sys.argv[2:]

    if not using_afplay:
        AS = requirePackage("pydub", "AudioSegment")
        play = requirePackage("pydub.playback", "play")

    for music in argv:
        try:
            play(AS.from_file(music)) if not using_afplay else external_exec(
                f"afplay {os.path.abspath(music)}"
            )
        except:
            pass


def qs_print(*argv):
    """
    打印文件

    :return:
    """
    if not argv:
        argv = sys.argv[2:]
    if platform.startswith("win"):
        win32api = requirePackage("pywin32", "win32api")
        win32print = requirePackage("pywin32", "win32print")
        for file in argv:
            win32api.ShellExecute(
                0, "print", file, '/d:"%s"' % win32print.GetDefaultPrinter(), ".", 0
            )
    else:
        for file in argv:
            external_exec(f"lp {file}")


def sas():
    """
    设置音源

    Set audio source

    :return: None
    """
    if platform != "darwin":
        qs_default_console.print(
            qs_error_string,
            "Not support your system" if user_lang != "zh" else "不支持你的系统",
        )
        return
    if not _is_in_path("SwitchAudioSource"):
        if _ask(
            {
                "type": "confirm",
                "message": "Install SwitchAudioSource?"
                if user_lang != "zh"
                else "安装 SwitchAudioSource？",
                "default": True,
            }
        ):
            with qs_default_status(
                "Installing SwitchAudioSource..."
                if user_lang != "zh"
                else "正在安装 SwitchAudioSource..."
            ):
                retries = 3
                while retries:
                    external_exec("brew install SwitchAudioSource")
                    if _is_in_path("SwitchAudioSource"):
                        break
                    retries -= 1
                if not retries:
                    qs_default_console.print(
                        qs_error_string,
                        "Install failed" if user_lang != "zh" else "安装失败",
                    )
                    return
    import json

    current = json.loads(external_exec("SwitchAudioSource -c -f json", True)[1])
    devices = [
        json.loads(i)
        for i in external_exec("SwitchAudioSource -a -f json", True)[1].splitlines()
    ]
    devices = {
        i["id"]: {
            "uid": i["uid"],
            "type": "🔈" if i["type"] == "output" else "🎤",
            "name": i["name"],
        }
        for i in devices
    }
    if not devices:
        qs_default_console.print(
            qs_error_string, "No device found" if user_lang != "zh" else "未找到设备"
        )
        return
    from .TuiTools.Table import qs_default_table

    table = qs_default_table(
        ["ID", "Name", "Type", "Current"]
        if user_lang != "zh"
        else ["ID", "名称", "类型", "当前设备"]
    )
    for i in devices:
        table.add_row(i, devices[i]["name"], devices[i]["type"]) if devices[i][
            "uid"
        ] != current["uid"] else table.add_row(
            i, devices[i]["name"], devices[i]["type"], "[bold green]⬅[/]"
        )
    qs_default_console.print(table, justify="center")

    default = qs_cache.get("audio_source")
    uids = {val["uid"]: key for key, val in devices.items()}
    question = {
        "type": "input",
        "message": "Input device ID" if user_lang != "zh" else "输入设备 ID",
        "validate": lambda x: x in [str(i) for i in devices],
    }
    if default:
        _default = default.copy()
        for item in default:
            if item not in uids:
                _default.pop(item)
        if _default:
            if len(_default) > 1:
                _default.pop(current["uid"])
            question["default"] = uids[max(_default, key=_default.get)]
    else:
        default = {}
    if not (select := _ask(question)):
        return
    uid = devices[select]["uid"]
    default[uid] = default.get(uid, 0) + 1

    external_exec("SwitchAudioSource -i %s" % select, True)
    qs_cache.set("audio_source", default)
    qs_default_console.print(qs_info_string, "Done" if user_lang != "zh" else "完成")


def swap():
    """
    交换两个文件的内容
    """

    file1 = sys.argv[2]
    file2 = sys.argv[3]

    with open(file1, "r") as f1:
        data1 = f1.read()
    with open(file2, "r") as f2:
        data2 = f2.read()

    with open(file1, "w") as f1:
        f1.write(data2)
    with open(file2, "w") as f2:
        f2.write(data1)
