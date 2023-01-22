# coding=utf-8
from . import *
from .. import user_currency
import json
from urllib.parse import quote
import requests

__common_token__ = "hUxPTdnybk1XLUEFtzkj"
alapi_token = pre_check("alapi_token", ext=False)
if not alapi_token:
    from .. import qs_default_console, qs_error_string, qs_warning_string, _ask

    qs_default_console.print(
        qs_error_string, "This function require alapi token!\n这个功能需要alapi token\n"
    )
    if _ask(
        {
            "type": "confirm",
            "message": "To get alapi token?\n是否前往获取alapi token?",
            "default": True,
        }
    ):
        from .. import open_url
        from .. import qs_config

        try:
            open_url(["https://www.alapi.cn/"])
        except Exception as e:
            qs_default_console.print(
                qs_error_string,
                "Failed to open browser, try url: https://www.alapi.cn/",
            )
        finally:
            alapi_token = _ask(
                {
                    "type": "input",
                    "message": "Input alapi token | 输入alapi token:",
                }
            )
            qs_config.apiUpdate("alapi_token", alapi_token)
    elif _ask(
        {
            "type": "confirm",
            "message": "Use common but limited token?\n是否愿意使用公共但是受限的token?",
            "default": True,
        }
    ):
        alapi_token = __common_token__
        qs_config.apiUpdate("alapi_token", alapi_token)
        qs_default_console.print(
            qs_warning_string,
            "Tokens with restricted applications may not be able to use the functions provided by alapi normally, "
            "and you can try again multiple times."
            if user_lang != "zh"
            else "应用受限的token可能无法正常使用alapi提供的功能，可多次重新尝试。",
        )
    else:
        exit()

if not pre_check("__ban_warning", ext=False) and alapi_token == __common_token__:
    from .. import qs_default_console, qs_warning_string

    qs_default_console.print(
        qs_warning_string,
        "Using common but limited token." if user_lang != "zh" else "正在使用公共但受限的token",
    )
    qs_default_console.print(
        qs_warning_string,
        "If you do not want this, try to apply one:"
        if user_lang != "zh"
        else "如果您不想这样, 可以来申请一个自己的:",
        "https://www.alapi.cn/",
    )

v2_url = "https://v2.alapi.cn/api/"


def translate(text: str, from_lang: str = "auto", to_lang: str = user_lang):
    """
    获取翻译结果

    Get the translation results.

    :param text: 待翻译内容 | Content to be translated.
    :param from_lang: 语种来源 | Source language
    :param to_lang: 翻译成的语种 | Translated into the language
    :return: 翻译的文本 | Translated text
    """
    global alapi_token
    try:
        request_info = (
            "q={}&from={}&to={}".format(quote(text, "utf-8"), from_lang, to_lang)
            if from_lang
            else "q={}&to={}".format(quote(text, "utf-8"), to_lang)
        )
        res = requests.post(
            v2_url + "fanyi",
            data=request_info,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "token": alapi_token,
            }
            if alapi_token
            else {"Content-Type": "application/x-www-form-urlencoded"},
        )
        if res.status_code == requests.codes.ok:
            res = json.loads(res.text)
            if res["code"] != 200:
                return "[ERROR] {}".format(res["msg"])
            return res["data"]["dst"]
        return "[ERROR] 未知错误 | Unknown Error"
    except Exception as unknown_error:
        return f"[ERROR] {repr(unknown_error)}"


def bili_cover(url: str):
    """
    获取BiliBili视频封面

    Get the BiliBili video cover

    :param url: BiliBili视频链接或视频号 | BiliBili video link or video number
    :return:
    """
    import re
    from ..NetTools.NormalDL import normal_dl
    from .. import qs_default_console, qs_error_string, qs_info_string
    from ..ImageTools.ImagePreview import image_preview

    try:
        res = requests.post(
            v2_url + "bilibili/cover",
            data="c=" + url,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "token": alapi_token,
            },
        )
    except Exception as e:
        return qs_default_console.print(qs_error_string, repr(e))
    if res.status_code == requests.codes.ok:
        res = json.loads(res.text)
        if res["code"] != 200 or res["msg"] != "success":
            qs_default_console.log(
                qs_error_string,
                ("Get cover with: %s failed:" if user_lang != "zh" else "下载封面: %s 失败: ")
                % url,
            )
            return
        res = res["data"]
        res["description"] = res["description"].replace("<br />", "\n\t")
        res["description"] = res["description"].replace("&nbsp;", " ")
        res["description"] = re.sub("<.*?>", "", res["description"]).strip()  # 忽略HTML标签
        qs_default_console.print(
            qs_info_string,
            "TITLE:" if user_lang != "zh" else "标题:",
            "%s" % res["title"],
        )
        qs_default_console.print(
            qs_info_string, "" if user_lang != "zh" else "简介:", end="\n\t"
        )
        qs_default_console.print(res["description"], end="\n\n")
        normal_dl(res["cover"], res["title"] + "." + res["cover"].split(".")[-1])
        image_preview(res["title"] + "." + res["cover"].split(".")[-1])
    else:
        qs_default_console.log(
            qs_error_string,
            f"Get cover with: {url} failed" if user_lang != "zh" else f"下载封面: {url} 失败",
        )


def ip_info(ip: str):
    """
    获取ip的运营商、地理位置等数据

    Get IP operator, geographic location and other data

    :param ip: ipv4, ipv6, empty means current machine
    :return: data dict {ip, isp, pos | ERROR MESSAGE, location | ERROR code}
    """
    try:
        res = requests.get(
            v2_url + ("ip?ip=%s&format=json" % ip if ip else "ip"),
            headers={"token": alapi_token},
        )
        res = json.loads(res.text)
        if res["code"] != 200:
            return {
                "ip": ip,
                "isp": "",
                "pos": res["msg"],
                "location": "{code, %s}" % res["code"],
            }
        return res["data"]
    except Exception as e:
        return {
            "ip": ip,
            "isp": "",
            "pos": "Network Error" if user_lang != "zh" else "网络错误",
            "location": "{code, %s}" % repr(e),
        }


def garbage_classification(query_ls: list):
    """
    查询中国垃圾分类

    Search Chinese garbage classification

    :param query_ls: 待查询的垃圾列表 | garbage list
    :return: 查询结果的字符串表格 | string table
    """
    from .. import qs_default_console, cut_string

    width = qs_default_console.width // 5 * 2 - 1

    def fmt_string(string, pre_num):
        return "\n" * pre_num + " ".join(cut_string(string, width))

    from ..TuiTools.Table import qs_default_table
    from rich.text import Text
    import math

    table = qs_default_table(
        [
            {"header": "名称", "justify": "center", "style": "bold cyan"},
            {"header": "分类", "justify": "center"},
            {"header": "解释", "justify": "center"},
            {"header": "提示", "justify": "center"},
        ],
        "[bold underline] 查询结果\n",
    )
    first_flag = True
    for query_el in query_ls:
        if first_flag:
            first_flag = False
        else:
            table.add_row(Text("-", style="none"), Text("-", style="none"), "-", "-")
        res = requests.post(
            v2_url + "garbage",
            data="name={}".format(quote(query_el, "utf-8")),
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "token": alapi_token,
            }
            if alapi_token
            else {"Content-Type": "application/x-www-form-urlencoded"},
        )
        if res.status_code == requests.codes.ok:
            res = json.loads(res.text)
            if res["code"] != 200:
                table.add_row(
                    fmt_string(query_el, 0), "", "", fmt_string(res["msg"], 0)
                )
                continue
            try:
                res = res["data"][0]
                half_rows = [
                    math.ceil(len(query_el) / width / 2),
                    1,
                    math.ceil(len(res["explain"]) / width / 2),
                    math.ceil(len(res["tip"]) / width / 2),
                ]
                max_row = max(half_rows)
                half_rows = [max_row - i for i in half_rows]
                table.add_row(
                    fmt_string(query_el, half_rows[0]),
                    fmt_string(
                        [
                            "[bold green]可回收",
                            "[bold red]有害",
                            "[bold yellow]厨余(湿)",
                            "[bold blue]其他(干)",
                        ][int(res["type"]) - 1],
                        half_rows[1],
                    ),
                    Text(fmt_string(res["explain"], half_rows[2]), justify="full"),
                    Text(fmt_string(res["tip"], half_rows[3]), justify="full"),
                )
            except IndexError:
                table.add_row(fmt_string(query_el, 0), "Unknown", "未知垃圾", "未知垃圾")
        else:
            table.add_row(fmt_string(query_el, 0), "Unknown", "None", "Request Error")
    return table


def short_video_info(url: str):
    """
    解析多平台短视频，并返回视频信息与下载直链

    Parse multi - platform short video and return video information with download straight link

    :param url: 短视频分享链接 | Short video sharing link
    :return:
    """
    try:
        res = requests.post(
            v2_url + "video/url",
            data="url={}".format(quote(url, "utf-8")),
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "token": alapi_token,
            }
            if alapi_token
            else {"Content-Type": "application/x-www-form-urlencoded"},
        )
        res = json.loads(res.text)
        if res["code"] != 200:
            return False, {
                "title": res["msg"],
                "cover_url": "None",
                "video_url": "None",
                "source": str(res["code"]),
            }
        return True, res["data"]
    except Exception as e:
        return False, {
            "title": "网络错误" if user_lang == "zh" else "Network Error",
            "cover_url": "None",
            "video_url": "None",
            "source": "Unknown",
        }


def acg():
    """
    随机获取一张acg图片链接

    Get a random link to an ACG image

    :return: acg image link
    """
    try:
        res = requests.post(
            v2_url + "acg",
            data="format=json",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "token": alapi_token,
            }
            if alapi_token
            else {"Content-Type": "application/x-www-form-urlencoded"},
        )
        res = json.loads(res.text)
        if res["code"] != 200:
            return False, res["msg"], 0, 0
        return True, res["data"]["url"], res["data"]["width"], res["data"]["height"]
    except Exception as e:
        return False, repr(e), 0, 0


def bingImg():
    """
    随机获取一张bing图片链接

    Get a link to a bing picture at random

    :return: image link
    """
    try:
        res = requests.post(
            v2_url + "bing",
            data="format=json",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "token": alapi_token,
            }
            if alapi_token
            else {"Content-Type": "application/x-www-form-urlencoded"},
        )
        res = json.loads(res.text)
        if res["code"] != 200:
            return False, res["msg"], ""
        return True, res["data"]["url"], res["data"]["copyright"]
    except Exception as e:
        return False, repr(e), ""


def kdCheck(kd_number: str):
    """
    查询中国快递

    Inquire about China Express

    :param kd_number: 快递单号 | courier number
    :return: bool, list
    """
    try:
        res = requests.post(
            v2_url + "kd",
            data="number=%s" % kd_number,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "token": alapi_token,
            },
        )
        res = json.loads(res.text)
        if res["code"] != 200:
            return False, 0, res["msg"]
        return (
            True,
            int(res["data"]["state"]),
            res["data"]["info"],
        )
    except Exception as e:
        return False, 0, repr(e)


def pinyin(zh_str: str):
    """
    查询中文的拼音

    Query Chinese pinyin

    :param zh_str: Chinese | 中文
    :return:
    """
    try:
        res = requests.post(
            v2_url + "pinyin",
            data=f'word={quote(zh_str, "utf-8")}&tone=1&abbr=0',
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "token": alapi_token,
            },
        )
        res = json.loads(res.text)
        if res["code"] != 200:
            return False, res["msg"]
        return True, res["data"]["pinyin"]
    except Exception as e:
        return False, repr(e)


def exchange(fr, number, to=user_currency):
    """
    查询<number> <fr> 对应 多少 <to>

    Query <number> <fr> corresponding <number?> <to>

    :param to: 待查询的币种
    :param number: 待查询的货币数量
    :param fr: 目标币种
    :return:
    """

    try:
        res = requests.get(
            v2_url + "exchange",
            params={"money": number, "from": fr, "to": to},
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "token": alapi_token,
            },
        )
        res = json.loads(res.text)
        if res["code"] != 200:
            return False, res["msg"]
        return True, res["data"]
    except Exception as e:
        return False, repr(e)


def zhihuDaily():
    """
    获取知乎日报

    Get Zhihu Daily

    :return:
    """
    try:
        res = requests.get(
            v2_url + "zhihu",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "token": alapi_token,
            },
        )
        res = json.loads(res.text)
        if res["code"] != 200:
            return False, res["msg"]
        return True, res["data"]
    except Exception as e:
        return False, repr(e)


def daily60s():
    """
    获取每日60秒早报

    Get the daily 60-second morning report

    :return:
    """
    try:
        res = requests.get(
            v2_url + "zaobao?format=json", headers={"token": alapi_token}
        )
        res = json.loads(res.text)

        if res["code"] != 200:
            return False, res["msg"]
        return True, res["data"]
    except Exception as e:
        return False, repr(e)


def doutu(keyword: str):
    """
    获取keyword的表情包

    :param keyword: 关键词
    :return: 图片链接
    """
    try:
        res = requests.post(
            v2_url + "doutu",
            params={"keyword": keyword},
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "token": alapi_token,
            },
        )
        res = json.loads(res.text)
        if res["code"] != 200:
            return False, res["msg"]
        return True, res["data"]
    except Exception as e:
        return False, repr(e)


def joke():
    """
    获取随机笑话

    :return: title, content
    """
    try:
        res = requests.get(v2_url + "joke/random", headers={"token": alapi_token})
        res = json.loads(res.text)
        if res["code"] != 200:
            return False, res["msg"]
        return True, res["data"]
    except Exception as e:
        return False, repr(e)
