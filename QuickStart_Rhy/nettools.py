# coding=utf-8
"""
调用各种网络工具

Call various network tools
"""
import sys


def upgrade():
    """
    更新qs

    Upgrade qs
    """
    from . import (
        external_exec,
        user_pip,
        qs_default_console,
        qs_info_string,
        qs_default_status,
    )

    with qs_default_status("正在更新"):
        external_exec(f"{user_pip} install QuickStart-Rhy --upgrade", True)
    qs_default_console.print(qs_info_string, "更新完成")


def m3u8_dl(url):
    """
    下载m3u8

    Download *.m3u8
    """
    from .NetTools.M3u8DL import M3U8DL

    M3U8DL(url, url.split(".")[-2].split("/")[-1]).download()


def download():
    """
    qs下载引擎，使用--video or -v使用youtube-dl下载视频

    Qs download engine, use --video or -v use the default video download engine download
    """
    if any([i in sys.argv for i in ["-h", "-help", "--help"]]):
        from . import user_lang, qs_default_console, qs_info_string

        qs_default_console.print(
            qs_info_string,
            'Usage: "qs dl [url...]"\n'
            "  [--video] | [-v]  :-> download video (use youtube-dl)\n"
            "  [--proxy] | [-px] :-> use default proxy set in ~/.qsrc\n"
            "  [--name fileName] :-> Set File Name\n"
            "  [--referer] | [-e] :-> Set Referer\n"
            if user_lang != "zh"
            else '使用: "qs dl [链接...]"\n'
            "  [--video] | [-v]  :-> 使用youtube-dl下载视频\n"
            "  [--proxy] | [-px] :-> 使用配置表中的默认代理下载\n"
            "  [--name fileName] :-> 设置文件名\n"
            "  [--referer] | [-e] :-> 设置Referer\n",
        )
        return
    global _real_main
    ytb_flag = "--video" in sys.argv or "-v" in sys.argv
    use_proxy = "--proxy" in sys.argv or "-px" in sys.argv
    other_args = []
    set_name = None
    set_referer = None
    if "--name" in sys.argv:
        set_name = sys.argv[sys.argv.index("--name") + 1]
    if "--referer" in sys.argv or "-e" in sys.argv:
        set_referer = (
            sys.argv[sys.argv.index("--referer") + 1]
            if "--referer" in sys.argv
            else sys.argv[sys.argv.index("-e") + 1]
        )
        if not set_referer.endswith("/"):
            set_referer += "/"
    if ytb_flag or use_proxy or set_name or set_referer:
        [
            sys.argv.remove(i) if i in sys.argv else None
            for i in [
                "--video",
                "-v",
                "--proxy",
                "-px",
                "--name",
                "--referer",
                "-e",
                set_name,
                set_referer,
            ]
        ]
    nxt_flag = False
    for item in sys.argv[2:]:
        if item.startswith("-") or nxt_flag:
            if nxt_flag:
                nxt_flag = False
            if item.startswith("--"):
                nxt_flag = True
            other_args.append(item)

    [sys.argv.remove(item) for item in other_args]
    urls = sys.argv[2:]
    if not urls:
        from . import requirePackage

        pyperclip = requirePackage("pyperclip")
        urls = pyperclip.paste().split()
    if urls:
        if ytb_flag:
            from . import requirePackage
            from youtube_dl import _real_main

            _real_main = requirePackage("youtube_dl", "_real_main")
        from .NetTools.NormalDL import normal_dl
        from . import qs_config

        for url in urls:
            if url.endswith(".m3u8"):
                m3u8_dl(url)
            else:
                if use_proxy:
                    normal_dl(
                        url,
                        set_name=set_name,
                        set_proxy=qs_config.basicSelect("default_proxy"),
                        set_referer=set_referer,
                    ) if not ytb_flag else _real_main(
                        [
                            url,
                            "--proxy",
                            qs_config.basicSelect("default_proxy"),
                            "--merge-output-format",
                            "mp4",
                        ]
                        + other_args
                    )
                else:
                    normal_dl(
                        url, set_name=set_name, set_referer=set_referer
                    ) if not ytb_flag else _real_main(
                        [url, "--merge-output-format", "mp4"] + other_args
                    )
    else:
        from . import user_lang, qs_default_console, qs_error_string

        qs_default_console.log(
            qs_error_string, "No url found!" if user_lang != "zh" else "无链接输入"
        )


def http():
    """
    开启http服务

    Turn on the http service.
    """
    url = ""
    if len(sys.argv) > 2:
        ip, port = sys.argv[2].split(":")
        port = int(port)
        if "-bind" in sys.argv:
            try:
                url = sys.argv[sys.argv.index("-bind") + 1]
                from .NetTools import formatUrl

                url = formatUrl(url)
            except IndexError:
                print("Usage: qs http ip:port -bind url")
                exit(0)
    else:
        from .NetTools import get_ip

        ip = get_ip()
        port = 8000
    if not ip:
        exit("get ip failed!")
    from .NetTools.HttpServer import HttpServers

    HttpServers(ip, port, url).start()


def netinfo():
    """
    通过域名或ip查询ip信息

    Query ip information via domain name or ip.
    """
    import socket
    import urllib.parse
    from . import user_lang, qs_default_console, qs_error_string, requirePackage

    from .API.alapi import ip_info

    def print_ip_info(info_ls):
        from .TuiTools.Table import qs_default_table

        table = qs_default_table(
            [
                {"header": "ip", "justify": "center", "style": "bold magenta"},
                {"header": "运营商", "justify": "center"},
                {"header": "地址", "justify": "center"},
                {"header": "经纬", "justify": "center"},
            ]
            if user_lang == "zh"
            else [
                {"header": "ip", "justify": "center", "style": "bold magenta"},
                {"header": "isp", "justify": "center"},
                {"header": "pos", "justify": "center"},
                {"header": "location", "justify": "center"},
            ],
            "NetInfo Results\n",
        )
        for info in info_ls:
            table.add_row(
                info["ip"],
                info["isp"].strip() if "isp" in info else "未知",
                info["pos"],
                str(info["location"])[1:-1].replace("'", ""),
            )
        qs_default_console.print(table, justify="center")

    urls = sys.argv[2:] if len(sys.argv) > 2 else []
    if not urls:
        try:
            urls += (
                requirePackage("pyperclip").paste().strip().split() if not urls else []
            )
        except:
            from rich.prompt import Prompt

            urls = (
                Prompt.ask(
                    "Sorry, but your system is not supported by `pyperclip`\nSo you need input content manually: "
                    if user_lang != "zh"
                    else "抱歉，但是“pyperclip”不支持你的系统\n，所以你需要手动输入内容:"
                )
                .strip()
                .split()
            )
    if not urls:
        urls.append("me")
    res_ls = []
    for i in urls:
        try:
            addr = ""
            if i != "me":
                if "://" in i:
                    protocol, domain = (
                        i[: i.index("://")],
                        urllib.parse.urlparse(i).netloc,
                    )
                    addr = socket.getaddrinfo(domain, protocol)[0][-1][0]
                else:  # 无网络协议或直接使用IP地址时默认采用http
                    addr = urllib.parse.urlparse(i).netloc
                    addr = socket.getaddrinfo(addr if addr else i, "http")[0][-1][0]
            res_ls.append(ip_info(addr))
        except:
            qs_default_console.print(qs_error_string, "Get domain failed:", i)
            continue
    print_ip_info(res_ls)


def wifi():
    """
    扫描附近wifi，选择连接

    Scan nearby wifi and select connection

    :return:
    """
    from . import (
        platform,
        user_lang,
        qs_default_console,
        qs_error_string,
        qs_info_string,
    )
    from .TuiTools.Table import qs_default_table

    if platform.lower() != "darwin":
        from .NetTools.WiFi import WiFi
    else:
        from .NetTools.WiFiDarwin import WiFi
    _wifi = WiFi()
    table = qs_default_table(
        ["id", "ssid", "signal", "lock"]
        if user_lang != "zh"
        else ["序号", "名称", "信号", "加密"],
        title="Wi-Fi",
    )
    connectable_wifi = _wifi.scan()
    if not connectable_wifi:
        qs_default_console.print(
            qs_error_string, "No available wifi" if user_lang != "zh" else "没有可用的wifi"
        )
        return

    from .__config__ import prompt
    from prompt_toolkit.validation import Validator, ValidationError

    class ssidValidator(Validator):
        def validate(self, document):
            document = document.text
            try:
                if int(document) >= len(connectable_wifi):
                    raise IndexError
            except:
                raise ValidationError(
                    message="请输入合法序号" if user_lang == "zh" else "Input validate id",
                    cursor_position=len(document),
                )
            return True

    questions = [
        {
            "type": "input",
            "name": "ssid",
            "message": "选择序号以连接:" if user_lang == "zh" else "Choose id to connect:",
            "default": "0",
            "validate": ssidValidator,
        },
        {
            "type": "password",
            "name": "password",
            "message": "输入密码:" if user_lang == "zh" else "Input password:",
        },
    ]

    for i, l in enumerate(connectable_wifi):
        table.add_row(*([str(i)] + [str(j) for j in l]))
    qs_default_console.print(table, justify="center")

    res = prompt(questions)
    if not res:
        return
    ssid = connectable_wifi[int(res["ssid"])]
    password = res["password"]
    qs_default_console.print(
        qs_info_string, "Connect succeed" if user_lang != "zh" else "连接成功"
    ) if _wifi.conn(ssid, password) else qs_default_console.print(
        qs_error_string, "Connect failed" if user_lang != "zh" else "连接失败"
    )
