# coding=utf-8
"""
调用各种qs的API

Call various QS API
"""
import sys

from . import (
    user_lang,
    platform,
    qs_default_console,
    qs_default_status,
    qs_error_string,
    qs_info_string,
    qs_warning_string,
    requirePackage,
)


def remove_bg():
    """
    删除图片背景

    Delete image background
    """
    path = sys.argv[2]
    from .API.SimpleAPI import rmbg

    with qs_default_status("Dealing.." if user_lang != "zh" else "处理中.."):
        rmbg(path)


def smms():
    """
    上传图片或Markdown中图片到smms

    Upload images or Markdown images to SMMS
    """
    from .API.SimpleAPI import smms

    with qs_default_status("Dealing.." if user_lang != "zh" else "处理中.."):
        smms(sys.argv[2])


def ali_oss():
    """
    阿里云对象存储

    Ali Cloud object storage
    """
    op = sys.argv[2]
    if op not in ["-dl", "-up", "-ls", "-rm"]:
        raise NotImplementedError
    if op != "-ls" and "--bucket" in sys.argv:
        bucket = sys.argv[sys.argv.index("--bucket") + 1]
    elif op == "-ls":
        bucket = None if len(sys.argv) < 4 else sys.argv[3]
    else:
        bucket = None
    files = sys.argv[3:] if op != "-ls" else []

    from .API.AliCloud import AliyunOSS

    ali_api = AliyunOSS()
    func_table = ali_api.get_func_table()
    for file in files:
        func_table[op](file, bucket)
    if not files:
        func_table[op](bucket)


def qiniu():
    """
    七牛云对象存储

    Qiniu cloud object storage
    """
    op = sys.argv[2]
    if op not in ["-dl", "-up", "-ls", "-rm"]:
        raise NotImplementedError
    if op != "-ls" and "--bucket" in sys.argv:
        bucket = sys.argv[sys.argv.index("--bucket") + 1]
    elif op == "-ls":
        bucket = None if len(sys.argv) < 4 else sys.argv[3]
    else:
        bucket = None
    files = sys.argv[3:] if op != "-ls" else []

    from .API.QiniuOSS import QiniuOSS

    qiniu_api = QiniuOSS()
    func_table = qiniu_api.get_func_table()
    for file in files:
        func_table[op](file, bucket)
    if not files:
        func_table[op](bucket)


def txcos():
    """
    腾讯云对象存储

    Tencent Cloud object storage
    """
    op = sys.argv[2]
    if op not in ["-dl", "-up", "-ls", "-rm"]:
        raise IndexError
    if op != "-ls" and "--bucket" in sys.argv:
        bucket = sys.argv[sys.argv.index("--bucket") + 1]
    elif op == "-ls":
        bucket = None if len(sys.argv) < 4 else sys.argv[3]
    else:
        bucket = None
    files = sys.argv[3:] if op != "-ls" else []

    from .API.TencentCloud import TxCOS

    tx_api = TxCOS()
    func_table = tx_api.get_func_table()
    for file in files:
        func_table[op](file, bucket)
    if not files:
        func_table[op](bucket)


def translate(content: str = '', target_lang: str = user_lang):
    """
    qs默认的翻译引擎

    Qs default Translation engine

    :param content: 需要翻译的内容
    """
    from . import trans_engine
    from requests.exceptions import SSLError

    if trans_engine == "default":
        trans_engine = "alapi"

    _translate = requirePackage(f".API.{trans_engine}", "translate")

    output_flag = False if content else True
    if not content:
        content = " ".join(sys.argv[2:])
    if not content:
        try:
            content = requirePackage("pyperclip", "paste")()
        except:
            from . import qs_default_input

            content = qs_default_input.ask(
                "Sorry, but your system is not supported by `pyperclip`\nSo you need input content manually: "
                if user_lang != "zh"
                else "抱歉，但是“pyperclip”不支持你的系统\n，所以你需要手动输入内容:"
            )
    if content:
        retry = 3
        lang = requirePackage("langid", "classify")(content)[0]
        while retry:
            try:
                if not (ret := _translate(
                    content,
                    target_lang="en"
                    if target_lang == user_lang == lang
                    else target_lang,
                )):
                    retry -= 1
                    qs_default_console.print(qs_warning_string, "结果为空" if user_lang != "zh" else "Result is empty")
                    continue
                break
            except SSLError:
                retry -= 1
                qs_default_console.log(
                    qs_warning_string,
                    f"SSL Error, Retrying... \[{3 - retry} / 3]"
                    if user_lang != "zh"
                    else f"SSL错误，重试中... \[{3 - retry} / 3]",
                )
            except Exception as e:
                # qs_default_console.log(qs_error_string, e)
                qs_default_console.print_exception()
                return None

        if output_flag and ret:
            if ret:
                from . import cut_string

                display = "\n".join(
                    [
                        " ".join(
                            cut_string(
                                line, qs_default_console.width, ignore_charset="`"
                            )
                        )
                        for line in ret.split("\n")
                    ]
                )
                qs_default_console.print(display)
            else:
                qs_default_console.log(qs_error_string, "Translate Failed!")
        return ret
    else:
        qs_default_console.log(
            qs_warning_string,
            "No content in your clipboard or command parameters!"
            if user_lang != "zh"
            else "剪贴板或命令参数没有内容!",
        )
        return None


def weather():
    """查天气 | Check weather"""
    from .NetTools import headers
    from .ThreadTools import ThreadFunctionWrapper
    import requests

    def get_data(url):
        try:
            ct = requests.get(url, headers)
        except:
            return
        ct.encoding = "utf-8"
        ct = ct.text.split("\n")
        if not platform.startswith("win"):
            res = ct.copy()
        else:
            import re

            for line in range(len(ct)):
                ct[line] = re.sub("\x1b.*?m", "", ct[line])
            res = ct.copy()
        return res

    try:
        loc = sys.argv[2]
    except IndexError:
        loc = ""
    tls = [
        ThreadFunctionWrapper(
            get_data,
            "https://wttr.in/" + (loc if loc else "?lang={}".format(user_lang)),
        ),
        ThreadFunctionWrapper(get_data, "https://v2.wttr.in/" + loc),
    ]
    for i in tls:
        i.start()
    with qs_default_status("Requesting.." if user_lang != "zh" else "请求中.."):
        for i in tls:
            i.join()
    simple = tls[0].get_res()
    table = tls[1].get_res()
    if simple:
        if not loc:
            if user_lang == "zh":
                from .API.alapi import translate

                enLocation = simple[0].split("：")[-1].strip()
                trans_loaction = translate(enLocation)
                qs_default_console.print(
                    "地区：" + trans_loaction if trans_loaction else enLocation
                )
            else:
                qs_default_console.print("Location" + simple[0][simple[0].index(":") :])
        simple = simple[2:7]
        print("\n".join(simple))
    else:
        qs_default_console.log(
            qs_error_string, "Get data failed." if user_lang != "zh" else "错误: 获取数据失败"
        )
    if table:
        qs_default_console.print(table[3][:-1])
        bottom_line = 7
        try:
            while "╂" not in table[bottom_line]:
                bottom_line += 1
        except IndexError:
            qs_default_console.log(
                qs_error_string,
                "Get Weather Data failed!" if user_lang != "zh" else "获取天气数据失败",
            )
            return
        for i in table[7 : bottom_line + 2]:
            print(i[:-1])
        print(
            "└────────────────────────────────────────────────────────────────────────"
        )
        print("\n".join(table[-3 if not loc else -4 :]))
    else:
        print("Error: Get data failed." if user_lang != "zh" else "错误: 获取数据失败")


def largeImage():
    """
    百度图片效果增强

    Baidu picture effect enhancement
    """
    try:
        path = sys.argv[2]
    except IndexError:
        qs_default_console.log(
            qs_error_string, "%s: qs LG <img>" % "Usage" if user_lang != "zh" else "用法"
        )
        return
    else:
        from .API.BaiduCloud import ImageDeal

        aip_cli = ImageDeal()
        with qs_default_status("Dealing.." if user_lang != "zh" else "处理中.."):
            aip_cli.largeImage(path)


def AipNLP():
    """百度NLP | Baidu NLP"""
    from .API.BaiduCloud import AipNLP

    pyperclip = requirePackage("pyperclip")

    pyperclip.paste()
    ct = sys.argv[2:]
    if not ct:
        try:
            ct = [pyperclip.paste()]
        except:
            from . import qs_default_input

            ct = [
                qs_default_input.ask(
                    "Sorry, but your system is not supported by `pyperclip`\nSo you need input content manually: "
                    if user_lang != "zh"
                    else "抱歉，但是“pyperclip”不支持你的系统\n，所以你需要手动输入内容:"
                )
            ]
    NLP = AipNLP()
    for _id, line in enumerate(ct):
        ct[_id] = NLP.get_res(line)
        if _id == 9:
            qs_default_console.print("...")
        elif _id < 9:
            qs_default_console.print(ct[_id])
    try:
        pyperclip.copy("\n".join(ct))
    except:
        pass


def bili_cover():
    """下载Bilibili视频、直播的封面图片（视频链接、视频号均可识别）"""
    from .API.alapi import bili_cover as bc

    pyperclip = requirePackage("pyperclip")

    try:
        url = sys.argv[2]
    except IndexError:
        try:
            url = pyperclip.paste()
        except:
            qs_default_console.log(
                qs_error_string,
                "Sorry, but your system may not be suppported by `pyperclip`"
                if user_lang != "zh"
                else "抱歉，但是“pyperclip”不支持你的系统",
            )
            return
    if not url:
        qs_default_console.log(
            qs_error_string,
            "Usage: qs bcv <url | video code>"
            if user_lang != "zh"
            else "用法: qs bcv <链接 | 视频码>",
        )
        return
    bc(url)


def gbc():
    """查询中国垃圾分类（且仅支持中文查询）"""
    from .API.alapi import garbage_classification

    try:
        with qs_default_status("Requesting data.." if user_lang != "zh" else "请求数据中.."):
            res = garbage_classification(sys.argv[2:])
        qs_default_console.print(res, justify="center")
    except Exception as e:
        qs_default_console.print(qs_error_string, repr(e))
        qs_default_console.print(
            qs_error_string,
            "Usage: qs gbc <garbage...>" if user_lang != "zh" else "用法: qs gbc <垃圾...>",
        )


def short_video_info(son_call=False):
    """
    获取短视频信息 | Get short video information

    :return:
    """
    from .API.alapi import short_video_info
    from .NetTools import get_fileinfo, size_format

    pyperclip = requirePackage("pyperclip")
    import re

    try:
        url = sys.argv[2]
    except IndexError:
        try:
            url = pyperclip.paste()
            url = re.findall("https?://(?:[-\w.]|%[\da-fA-F]{2}|[/])+", url)[0]
        except:
            qs_default_console.print(
                qs_error_string,
                "Sorry, but your system may not be suppported by `pyperclip`"
                if user_lang != "zh"
                else "抱歉，但是“pyperclip”不支持你的系统",
            )
            return
    if not url:
        qs_default_console.print(
            qs_error_string,
            "Usage: qs svi <url/video code>"
            if not son_call
            else "Usage: qs svd <url/video code>",
        )
        return
    output_prefix = {
        "title": "Title " if user_lang != "zh" else "标题",
        "video": "Video " if user_lang != "zh" else "视频",
        "cover": "Cover " if user_lang != "zh" else "封面",
        "source": "Source" if user_lang != "zh" else "来源",
    }

    with qs_default_status("正在获取视频信息"):
        status, res = short_video_info(url.strip("/"))
        if not status:
            qs_default_console.print(qs_info_string, res["title"] + ":" + res["source"])
            return status
        showStatus = "-url" in sys.argv
        qs_default_console.print(
            qs_info_string, "[{}] {}".format(output_prefix["title"], res["title"])
        )
        if res["video_url"]:
            sz = (
                int(get_fileinfo(res["video_url"])[-1].headers["content-length"])
                if not son_call
                else -1
            )
            qs_default_console.print(
                qs_info_string,
                "[{}] {}\n{}".format(
                    output_prefix["video"],
                    size_format(sz, True) if sz > 0 else "--",
                    res["video_url"] if showStatus else "",
                ),
            )
        if showStatus:
            sz = int(get_fileinfo(res["cover_url"])[-1].headers["content-length"])
            qs_default_console.print(
                qs_info_string,
                "[{}] {}\n{}".format(
                    output_prefix["cover"],
                    size_format(sz, True),
                    res["cover_url"] if showStatus else "",
                ),
            )
    if platform == "darwin":
        from .ImageTools.ImagePreview import image_preview

        image_preview(res["cover_url"], True)
    if "source" in res and res["source"]:
        qs_default_console.print(
            qs_info_string, "[{}] {}".format(output_prefix["source"], res["source"])
        )
    return res


def short_video_dl():
    """
    下载短视频为mp4格式

    Download short video as mp4

    :return:
    """
    from .NetTools.NormalDL import normal_dl
    from .ImageTools.VideoTools import tomp4
    from . import remove

    res = short_video_info(son_call=True)

    if not res:
        qs_default_console.print(
            qs_error_string, "Download failed" if user_lang != "zh" else "下载失败"
        )
        return

    fileName = res["title"] if res["title"] else "UnknownTitle"
    if "pics" in res and res["pics"]:
        from .ImageTools.ImageTools import topng

        for index, url in enumerate(res["pics"]):
            normal_dl(url, set_name=fileName + str(index + 1))
            topng(fileName + str(index + 1))
            remove(fileName + str(index + 1))
    elif res["video_url"]:
        normal_dl(res["video_url"], set_name=fileName)
        tomp4(fileName)
        remove(fileName)


def acg():
    """
    获取随机acg图片链接（可选择下载）

    Get links to random ACG images (download optional)

    :return:
    """
    import random
    from .API.alapi import acg
    from .API.SimpleAPI import acg2

    qs_default_status("Requesting data.." if user_lang != "zh" else "请求数据中..").start()
    try:
        status, acg_link, width, height = random.choice([acg, acg2])()
        qs_default_console.print(
            qs_info_string, f"{'链接' if user_lang == 'zh' else 'LINK'}: {acg_link}"
        ) if status else qs_default_console.log(qs_error_string, acg_link)
        if status:
            qs_default_console.print(
                qs_info_string,
                "尺寸:" if user_lang == "zh" else "SIZE:",
                width,
                "×",
                height,
            )
            if "--save" in sys.argv[2:]:
                from .NetTools.NormalDL import normal_dl

                # disable download status for Windows
                acg_link = normal_dl(acg_link)
            from .ImageTools.ImagePreview import image_preview

            qs_default_status(
                status="Loading image...\n" if user_lang != "zh" else "加载图片中..\n"
            ).start()
            image_preview(
                open(acg_link) if "--save" in sys.argv[2:] else acg_link,
                "--save" not in sys.argv[2:],
            )
            return
    except Exception as e:
        qs_default_console.print(qs_error_string, repr(e))
    finally:
        qs_default_status.stop()


def bingImg():
    """
    获取bing图片链接（可选择下载）

    Get links to bing images (download optional)

    :return:
    """
    from .API.alapi import bingImg

    qs_default_status("Requesting data.." if user_lang != "zh" else "请求数据中..").start()

    try:
        status, acg_link, cprt = bingImg()
        qs_default_console.print(
            qs_info_string, f"{'链接' if user_lang == 'zh' else 'LINK'}: {acg_link}"
        ) if status else qs_default_console.log(qs_error_string, acg_link)
        if status:
            qs_default_console.print(
                qs_info_string, "版权:" if user_lang == "zh" else "CPRT:", cprt
            )
            if "--save" in sys.argv[2:]:
                from .NetTools.NormalDL import normal_dl

                qs_default_status.stop()
                acg_link = normal_dl(acg_link)
            from .ImageTools.ImagePreview import image_preview

            qs_default_status.update(
                status="Loading image..." if user_lang != "zh" else "加载图片中.."
            )
            image_preview(
                open(acg_link) if "--save" in sys.argv[2:] else acg_link,
                "--save" not in sys.argv[2:],
            )
    except Exception as e:
        qs_default_console.print(qs_error_string, repr(e))
    finally:
        qs_default_status.stop()


def preview_html_images():
    """
    获取网页中图片链接（可在Mac::iTerm中自动预览）

    Get links to pictures in the web page (automatically previewed in Mac::iTerm)

    :return:
    """
    from .API.SimpleAPI import imgs_in_url

    save_flag = "--save" in sys.argv
    if save_flag:
        sys.argv.remove("--save")
    for url in sys.argv[2:]:
        imgs_in_url(url, save_flag)


def kdCheck():
    """
    查国内快递

    Check domestic express

    :return:
    """
    from . import _ask
    from .API.alapi import kdCheck as kdCheckAPI

    with qs_default_status("Requesting data.." if user_lang != "zh" else "请求数据中.."):
        status, code, msg = kdCheckAPI(
            sys.argv[2]
            + (
                ":"
                + _ask(
                    {
                        "type": "input",
                        "message": "顺丰快递需要输入手机后四位",
                    }
                )
                if sys.argv[2][:2].lower() == "sf" and ':' not in sys.argv[2]
                else ""
            )
        )
        if not status:
            qs_default_console.print(qs_error_string, msg)
            return

    from .TuiTools.Table import qs_default_table
    from . import table_cell
    from rich.text import Text

    width = qs_default_console.width // 4 * 3
    tb = qs_default_table(
        [
            {
                "header": "Time" if user_lang != "zh" else "时间",
                "justify": "center",
                "style": "bold cyan",
            },
            {
                "header": "Description" if user_lang != "zh" else "描述",
                "justify": "center",
                "no_wrap": False,
            },
            {"header": "Status" if user_lang != "zh" else "状态", "justify": "center"},
        ],
        (
            [
                ":heavy_exclamation_mark: [bold underline red]Unknown",
                ":airplane: [bold underline yellow]In transit",
                ":delivery_truck: [bold underline green]In delivery",
                ":hearts: [bold underline bold green]Signed receipt",
            ][code]
            if user_lang != "zh"
            else [
                ":heavy_exclamation_mark: [bold underline red]未知",
                ":airplane: [bold underline yellow]运输中",
                ":delivery_truck: [bold underline green]派送中",
                ":hearts: [bold underline magenta]已签收:hearts:",
            ][code]
        )
        + "\n",
    )
    for _id, info in enumerate(msg):
        tb.add_row(
            info["time"],
            Text(table_cell(info["content"], width), justify="full"),
            "[bold green]:heavy_check_mark:" if _id else "[bold yellow]:arrow_left:",
        )
    qs_default_console.print(tb, justify="center")


def loli():
    """
    获取一张"可爱"萝莉图的URL，Mac+iTerm2下可在终端预览

    Get the URL of a "cute" Lori map, which can be previewed on the terminal under MAC + iterm2

    :return:
    """
    from .API.Lolicon import loli_img
    from .ImageTools import ImagePreview
    from .NetTools import NormalDL

    with qs_default_status("Requesting data.." if user_lang != "zh" else "请求数据中.."):
        status, msg, data = loli_img()
        if not status:
            qs_default_console.print(qs_error_string, msg)
            return

    save_flag = "--save" in sys.argv
    proxy = ""

    if "-p" in sys.argv:
        from . import qs_config

        proxy = qs_config.basicSelect("default_proxy")

    for img in data:
        qs_default_console.print(
            f'[bold underline]{img["title"]} [dim]{img["author"]}', justify="center"
        )
        qs_default_console.print(
            qs_info_string,
            "[bold]link" if user_lang != "zh" else "[bold]链接",
            img["url"],
        )
        qs_default_console.print(
            qs_info_string,
            "[bold]size" if user_lang != "zh" else "[bold]尺寸",
            img["width"],
            "x",
            img["height"],
        )
        if save_flag:
            img["url"] = NormalDL.normal_dl(
                img["url"], set_proxy=proxy, set_referer="https://i.pximg.net"
            )
        if platform == "darwin":
            ImagePreview.image_preview(
                open(img["url"]) if save_flag else img["url"],
                not save_flag,
                set_proxy=proxy,
                set_referer="https://i.pximg.net",
            )


def pinyin():
    from .API.alapi import pinyin

    content = " ".join(sys.argv[2:])
    if not content:
        try:
            pyperclip = requirePackage("pyperclip")
            content = pyperclip.paste()
        except:
            from . import qs_default_input

            content = qs_default_input.ask(
                "Sorry, but your system is not supported by `pyperclip`\nSo you need input content manually: "
                if user_lang != "zh"
                else "抱歉，但是“pyperclip”不支持你的系统\n，所以你需要手动输入内容:"
            )
    with qs_default_status("Requesting data.." if user_lang != "zh" else "请求数据中.."):
        status, res = pinyin(content)
    qs_default_console.print(qs_info_string, content)
    qs_default_console.print(qs_info_string if status else qs_error_string, res)


def setu():
    import random

    random.choice([acg, loli])()


def exchange():
    from .API.alapi import exchange

    qs_default_status("Requesting data.." if user_lang != "zh" else "请求数据中..").start()
    try:
        status, data = exchange(sys.argv[3], 1)
        qs_default_console.print(
            f"{sys.argv[2]} {sys.argv[3]} ==> {data['exchange']} × {sys.argv[2]} = "
            f"{data['exchange'] * float(sys.argv[2])} {data['currency_to']}\n"
            f"{'Update' if user_lang != 'zh' else '更新时间'}: {data['update_time']}",
            justify="center",
        ) if status else qs_default_console.log(qs_error_string, data)
    except Exception as e:
        qs_default_console.print(qs_error_string, repr(e))
    finally:
        qs_default_status.stop()


def zhihuDaily():
    from .API.alapi import zhihuDaily
    from rich.panel import Panel
    from .ImageTools.ImagePreview import image_preview

    qs_default_status("Requesting data.." if user_lang != "zh" else "请求数据中..").start()
    try:
        status, data = zhihuDaily()
        qs_default_status.stop()
        if not status:
            qs_default_console.log(qs_error_string, data)
            return
        data = data["stories"] + data["top_stories"]
        for item in data:
            res = "[bold cyan]" + ("Author: " if user_lang != "zh" else "作者: ")
            res += "[bold white]" + item["hint"] + "[/bold white]\n"
            res += "[bold cyan]" + ("Link:" if user_lang != "zh" else "链接: ")
            res += "[bold blue]" + item["url"] + "[/bold blue]"
            if "images" in item:
                if platform == "darwin":
                    image_preview(item["images"][0], True)
                else:
                    res += "\n[bold cyan]" + (
                        "Image: \n" if user_lang != "zh" else "图像: \n"
                    )
                    res += "[bold blue]  " + "\n  ".join(item["images"])
            elif "image" in item:
                image_preview(item["image"], True)
            qs_default_console.print(
                Panel(res, title="[b]" + item["title"], width=qs_default_console.width),
                justify="center",
                end="/n/n",
            )
    except Exception as e:
        qs_default_console.print(qs_error_string, repr(e))
    finally:
        qs_default_status.stop()


def wallhaven():
    from .API.SimpleAPI import wallhaven

    url, oneFlag = "", False
    
    if "--url" in sys.argv:
        url = sys.argv[sys.argv.index("--url") + 1]
        sys.argv.remove("--url")
        sys.argv.remove(url)

    oneFlag = "-one" in sys.argv

    res = wallhaven(randomOne=oneFlag) if not url else wallhaven(url, randomOne=oneFlag)
    if not res:
        return

    if "--save" in sys.argv:
        from .NetTools.MultiSingleDL import multi_single_dl

        multi_single_dl([i["url"] for i in res], qps_info=5)
    else:
        if oneFlag:
            res = res[0]
            qs_default_console.print(qs_info_string, "URL:\t", res["url"])
            qs_default_console.print(
                qs_info_string, "SIZE:\t", " × ".join([str(i) for i in res["size"]])
            )
            from .ImageTools.ImagePreview import image_preview

            with qs_default_status("Getting.." if user_lang != "zh" else "获取图片中.."):
                image_preview(res["url"], True)
        else:
            from .TuiTools.Table import qs_default_table

            tb = qs_default_table(
                [
                    {
                        "header": "ID" if user_lang != "zh" else "编号",
                        "justify": "center",
                        "style": "bold",
                    },
                    {"header": "URL", "justify": "center", "style": "bold cyan"},
                    {
                        "header": "Size" if user_lang != "zh" else "尺寸",
                        "justify": "center",
                    },
                ],
                "Wallhaven Anime TopList\n",
            )
            for iid, item in enumerate(res):
                tb.add_row(
                    str(iid), item["url"], " × ".join([str(i) for i in item["size"]])
                )
            qs_default_console.print(tb, justify="center")


def lmgtfy():
    from .API.SimpleAPI import lmgtfy

    pyperclip = requirePackage("pyperclip")

    keyword = " ".join(sys.argv[2:])
    res = lmgtfy(keyword)
    try:
        pyperclip.copy(res)
        qs_default_console.print(
            qs_info_string,
            "The generated link has been copied for you, and teach your friends how to use Google! (Can also Copy "
            "Following link"
            if user_lang != "zh"
            else "已经为您复制生成的链接，快教朋友如何使用Google吧! (也可以复制下面的链接)",
        )
    except:
        qs_default_console.print(
            qs_warning_string,
            "Failed to use clipboard, you can copy the flowing link:"
            if user_lang != "zh"
            else "调用剪切板失败，你可以复制下面的链接:",
        )
    qs_default_console.print(qs_info_string, res)


def daily60s():
    from .API.alapi import daily60s

    status, res = daily60s()
    if not status:
        return qs_default_console.print(qs_error_string, res)

    from rich.padding import Padding
    import signal
    import time

    cur_index = 0

    with qs_default_status("showing" if user_lang != "zh" else "展示中"):

        def dealSignal(*argv):
            for index in range(cur_index + 1, len(res["news"])):
                qs_default_console.print(
                    Padding(
                        res["news"][index], (0, int(0.2 * qs_default_console.width))
                    )
                )
                qs_default_console.print()
            qs_default_console.print("-" * qs_default_console.width)
            qs_default_console.print(res["weiyu"] + "\n", justify="center")

            if "--save" in sys.argv:
                import os
                from .NetTools.NormalDL import normal_dl

                name = normal_dl(res["image"], set_name="news.png")
                qs_default_console.print(
                    "Preview" if user_lang != "zh" else "预览", justify="center"
                )
                from .ImageTools.ImagePreview import image_preview

                qs_default_status.update(
                    status="loading image.." if user_lang != "zh" else "加载图片中.."
                )
                image_preview(open(name))
            exit(0)

        signal.signal(signal.SIGINT, dealSignal)
        qs_default_console.print(
            "[bold magenta underline]每天60秒读懂世界[/bold magenta underline]",
            justify="center",
        )
        qs_default_console.print(res["date"], justify="center")
        qs_default_console.print("-" * qs_default_console.width)
        len_ls = [len(i) for i in res["news"]]
        total_len = sum(len_ls)
        len_ls = [i / total_len * 60 for i in len_ls]
        len_ls[-1] = 0

        for index, item in enumerate(res["news"]):
            qs_default_console.print(
                Padding(item, (0, int(0.2 * qs_default_console.width)))
            )
            qs_default_console.print()
            cur_index = index
            time.sleep(len_ls[index])
    dealSignal()


def m2t():
    """
    磁力链接转种子文件

    Magnet link to Torrent file
    :return:
    """
    import re

    if "-f" in sys.argv:
        file_path = sys.argv[sys.argv.index("-f") + 1]
        with open(file_path, "r") as f:
            contents = f.read()
    elif "-u" in sys.argv:
        contents = sys.argv[sys.argv.index("-u") + 1]
    else:
        contents = requirePackage("pyperclip", "paste")()
    urls = re.findall("magnet:\?xt=urn:btih:(.*)", contents)
    if len(urls) > 1:
        from . import _ask

        url = _ask(
            {
                "type": "list",
                "message": "Select hash code | 选择哈希码:",
                "choices": urls,
            }
        )
    else:
        url = urls[0]
    from .API.Lolicon import magnet2torrent

    magnet2torrent(url)


def d2m():
    """
    番号搜索并复制磁力链

    :return:
    """
    global url
    try:
        designation = sys.argv[2]
    except IndexError:
        return qs_default_console.print(qs_error_string, "qs d2m <designation>")

    from . import _ask
    from .API.SimpleAPI import Designation2magnet

    copy = requirePackage("pyperclip", "copy", not_ask=True)
    PyperclipException = requirePackage("pyperclip", "PyperclipException")
    copied = False

    searcher = Designation2magnet(designation)
    infos = searcher.search_designation()

    choices = [f"[{n + 1}] " + i[1] + ": " + i[-1] for n, i in enumerate(infos)]
    try:
        url = searcher.get_magnet(
            infos[
                choices.index(
                    _ask(
                        {
                            "type": "list",
                            "message": "Select | 选择",
                            "choices": choices,
                        }
                    )
                )
            ][0]
        )
        if copy:
            copy(url)
            copied = True
        else:
            raise PyperclipException
    except KeyError:
        return
    except PyperclipException:
        qs_default_console.print(qs_info_string, url)

    if copied:
        qs_default_console.print(
            qs_info_string,
            "magnet url copied to clipboard" if user_lang != "zh" else "磁力链接已拷贝至粘贴板",
        )


def doutu():
    """
    获取关键词的随机十张表情包
    :return:
    """
    try:
        keyword = sys.argv[2]
    except IndexError:
        return qs_default_console.print(qs_error_string, "qs doutu <keyword>")

    from .API.alapi import doutu
    from .ImageTools.ImagePreview import image_preview

    status, urls = doutu(keyword)
    if not status:
        qs_default_console.print(qs_error_string, urls)
    else:
        import random

        urls = random.choices(urls, k=10)

        for item in urls:
            qs_default_console.print(qs_info_string, item)
            image_preview(item, is_url=True)


def joke():
    """
    获取段子
    :return:
    """
    import re
    from .API.alapi import joke
    from rich.panel import Panel

    status, ct = joke()
    if not status:
        qs_default_console.print(qs_error_string, ct)
        return
    content = re.sub("&(.*?);", "", ct["content"])
    qs_default_console.print(
        Panel(
            content,
            title="[b magenta]" + ct["title"],
            title_align="center",
            width=qs_default_console.width,
            subtitle=ct["time"],
        )
    )


def gpt():
    """
    ChatGPT-3.5
    :return:
    """
    translate_text = "--translate" in sys.argv
    if translate_text:
        from commonmark.blocks import Parser
        from commonmark.render.rst import ReStructuredTextRenderer

        parser = Parser()
        sys.argv.remove("--translate")

        class TranslateRenderer(ReStructuredTextRenderer):
            def __init__(self):
                super().__init__()

            def text(self, node, entering):
                self.out(translate(node.literal))

            def link(self, node, entering):
                if entering:
                    self.out("[")
                else:
                    self.out("](%s)" % node.destination)

            def image(self, node, entering):
                if entering:
                    self.out("![")
                else:
                    self.out(f"]({node.destination})")

            def code(self, node, entering):
                self.out("`")
                self.out(node.literal)
                self.out("`")

            def code_block(self, node, entering):
                directive = "```"
                language_name = None

                info_words = node.info.split() if node.info else []
                if len(info_words) > 0 and len(info_words[0]) > 0:
                    language_name = info_words[0]

                if language_name:
                    directive += language_name

                self.cr()
                self.out(directive)
                self.cr()
                self.out(node.literal)
                self.out("```")
                self.cr()

            def heading(self, node, entering):
                if entering:
                    self.cr()
                    self.out("#" * node.level)
                    self.out(" ")
                else:
                    self.cr()

        render = TranslateRenderer()

    from rich.markdown import Markdown
    from rich.live import Live
    from .API.ChatGPT import chatGPT, API_KEY, ALAPI
    from . import _ask
    from .NumbaTools import cut_string

    qs_default_console.print(
        qs_info_string, "Type 'exit' to exit" if user_lang != "zh" else "输入 'exit' 退出"
    )

    if not translate_text:
        qs_default_console.print(
            qs_info_string,
            "Add '--translate' to enable auto translate"
            if user_lang != "zh"
            else "添加 '--translate' 以启用自动翻译",
        )

    record = ""

    while (
        prompt := _ask(
            {
                "type": "input",
                "message": "Input Question" if user_lang != "zh" else "输入问题",
            }
        )
    ) != "exit":
        if translate_text:
            prompt = translate(prompt, target_lang="en")
            qs_default_console.print("EN:", prompt)

        with qs_default_status("Thinking..." if user_lang != "zh" else "思考中..."):
            response = chatGPT(prompt)

        qs_default_console.print(
            "[bold green]" + ("Answer" if user_lang != "zh" else "回答") + "[/]\n",
            justify="center",
        )
        prefix = "" if prompt not in ["继续", "continue"] else record

        with Live(
            "",
            console=qs_default_console,
            auto_refresh=False,
            vertical_overflow="visible",
        ) as live:
            total_res = prefix
            for res in response:
                if API_KEY or ALAPI:
                    if ALAPI:  # ALAPI 优先启用
                        total_res = prefix + res
                    elif API_KEY:
                        total_res += res
                else:
                    total_res = prefix + res["message"]
                display = "\n".join(
                    [
                        " ".join(
                            cut_string(
                                line, qs_default_console.width, ignore_charset="`"
                            )
                        )
                        for line in total_res.split("\n")
                    ]
                )
                live.update(Markdown(display, justify="full"), refresh=True)
            record = total_res
            if (
                translate_text
                and requirePackage("langid", "classify")(total_res)[0] != user_lang
            ):
                live.update(
                    Markdown(render.render(parser.parse(total_res)), justify="full"),
                    refresh=True,
                )
