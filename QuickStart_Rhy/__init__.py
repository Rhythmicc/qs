# coding=utf-8
"""
Docs for different language:
    中文: https://rhythmlian.cn/2020/08/09/QuickStart-Rhy-zh/

    English: https://rhythmlian.cn/2020/02/14/QuickStart-Rhy/
"""
import os
import sys
import time

from QuickProject import QproDefaultStatus as qs_default_status
from QuickProject import external_exec, user_pip, user_root
from QuickProject import QproInfoString as qs_info_string
from QuickProject import QproWarnString as qs_warning_string
from QuickProject import QproErrorString as qs_error_string


from .__cache__ import QsCache
from .__config__ import (
    QsConfig,
    dir_char,
    platform,
    qs_default_console,
    _ask,
    user_lang,
    lang_detector
)

name = "QuickStart_Rhy"
qs_config = QsConfig(os.path.join(user_root, ".qsrc"))
qs_cache = QsCache(os.path.join(user_root, ".qs_cache"))

user_currency = qs_config.basicSelect("default_currency")
trans_engine = qs_config.basicSelect("default_translate_engine")["support"][
    qs_config.basicSelect("default_translate_engine")["index"]
]
force_show_img = qs_config.basicSelect("force_show_img")
qs_console_width = qs_default_console.width

_package_info_ = qs_cache.get("package_info")
_not_update_ = ["io", "tarfile", "zipfile", "shutil"]
if _package_info_ is None:
    _package_info_ = {}

def requirePackage(
    pname: str,
    module: str = "",
    real_name: str = "",
    not_ask: bool = False,
    set_pip: str = user_pip,
    keep_latest: bool = False,
):
    """
    获取本机上的python第三方库

    :param pname: 库名
    :param module: 待引入的模块名，可缺省
    :param real_name: 用于 pip3 install 的名字
    :param not_ask: 不询问
    :param set_pip: pip3的路径
    :param keep_latest: 是否保持最新版本
    :return: 库或模块的地址
    """
    try:
        package_name = pname.split(".")[0] if not real_name else real_name
        if not package_name:  # 引用为自身
            package_name = name
        if package_name not in _not_update_ and (
            keep_latest
            and time.time() - _package_info_.get(package_name, 0) > 3600 * 24 * 7
        ):
            with qs_default_status(f"{lang_detector['updating']} {package_name}"):
                _st, _ct = external_exec(
                    f"{set_pip} install {package_name} -U", without_output=True
                )
                if _st:
                    qs_default_console.print(
                        qs_warning_string,
                        f"{lang_detector['updating']} {package_name} {lang_detector['fail_and_execute_manually']}"
                        f"'{set_pip} install {package_name} -U'",
                    )
                    qs_default_console.print(qs_warning_string, _ct)
            _package_info_[package_name] = time.time()
            qs_cache.set("package_info", _package_info_)
        exec(f"from {pname} import {module}" if module else f"import {pname}")
    except (ModuleNotFoundError, ImportError):
        if not_ask:
            return None
        if package_name == name:
            qs_default_console.print(qs_warning_string, lang_detector['requirePackageWarning'])
        if _ask(
            {
                "type": "confirm",
                "message": f"""Qs {lang_detector['require']} {pname + (' -> ' + module if module else '')}, {lang_detector['confirm_install']}?""",
                "default": True,
            }
        ):
            with qs_default_status(
                f"{lang_detector['Install']} {package_name}"
            ):
                st, _ = external_exec(
                    f"{set_pip} install {package_name} -U",
                    True,
                )
            if st:
                qs_default_console.print(
                    qs_error_string,
                    f"{lang_detector['Install']} {pname + (' -> ' + module if module else '')} {lang_detector['fail_and_execute_manually']}",
                    f"'{set_pip} install {package_name} -U'",
                )
                exit(-1)
            exec(f"from {pname} import {module}" if module else f"import {pname}")
        else:
            return None
    return eval(f"{module if module else pname}")


def cut_string(string: str, length: int, ignore_charset: list = []) -> list:
    """
    每隔l个字符切分字符串

    :param string: 字符串
    :param length: 切分长度
    :param ignore_charset: 忽略的字符集
    :return: 切分后产生的list
    """
    res, cur, cnt = [], "", 0
    for i in string:
        _char_len = 0 if i in ignore_charset else 2 if ord(i) > 255 else 1
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
    tm = time.strftime("%Y-%m-%d %A %H:%M:%S", time.localtime(time.time())).split()
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
                    "message": lang_detector['pyperclip_not_support']
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
            lang_detector['macos_only']
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

    if not os.path.exists(sys.argv[2]):
        return qs_default_console.print(
            qs_error_string,
            "No such file:" if user_lang != "zh" else "未找到文件:",
            sys.argv[2],
        )
    if platform == "darwin":
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
    elif platform.startswith("win"):
        # 检查是否为 powershell
        st, _ = external_exec(
            'powershell -Command "echo $PSVersionTable.PSVersion"', True
        )
        if st:
            return qs_default_console.print(
                qs_error_string,
                "Please use powershell to run this command"
                if user_lang != "zh"
                else "请使用 powershell 运行此命令",
            )
        external_exec(
            'powershell -Command "Set-Clipboard -Path ' + sys.argv[2] + '"', True
        )
    else:
        return qs_default_console.print(
            qs_error_string,
            lang_detector['not_support_current_system']
        )


def tcopy():
    """
    复制文本到粘贴板
    :return:
    """
    requirePackage("pyperclip", "copy")(" ".join(sys.argv[2:]))


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


def swap(file1: str = None, file2: str = None):
    """
    交换两个文件的内容
    """
    index = 2
    if not file1 or not file2:
        file1 = sys.argv[index]
        index += 1
    if not file2:
        file2 = sys.argv[index]

    with open(file1, "rb") as f1:
        data1 = f1.read()
    with open(file2, "rb") as f2:
        data2 = f2.read()

    with open(file1, "wb") as f1:
        f1.write(data2)
    with open(file2, "wb") as f2:
        f2.write(data1)

requirePackage("QuickProject", real_name="Qpro") # 自动更新
