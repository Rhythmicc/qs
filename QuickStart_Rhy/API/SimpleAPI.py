# coding=utf-8
"""
一些可以轻易实现的API

Some APIs that can be easily implemented
"""
from . import *
from .. import qs_default_console, qs_error_string, qs_info_string
import json
import requests


def rmbg(filePath: str):
    """
    删除图片背景

    Delete image background

    :param filePath: 图片的路径
    :return: None
    """
    api_key = pre_check("rmbg")
    res = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": open(filePath, "rb")},
        data={"size": "auto"},
        headers={"X-Api-Key": api_key},
    )
    if res.status_code == requests.codes.ok:
        import os

        img_name = os.path.basename(filePath).split(".")[0]
        img_root = os.path.dirname(os.path.abspath(filePath))

        with open(os.path.join(img_root, img_name + "_rmbg.png"), "wb") as imgfile:
            imgfile.write(res.content)
    else:
        qs_default_console.log(qs_error_string, res.status_code, res.text)


def smms(filePath: str):
    """
    上传图片或Markdown中所有的图片到smms中

    Upload images or all images from Markdown to SMMS

    :param filePath: 图片或Markdown文件的路径
    :return: None
    """
    import os
    from .. import user_root
    from ..TuiTools.Table import qs_default_table

    api_key = pre_check("smms")
    res_tb = qs_default_table(
        ["File", "Status", "url"] if user_lang != "zh" else ["文件", "状态", "链接"]
    )

    def post_img(path: str) -> dict:
        try:
            data = {"smfile": (path.split("/")[-1], open(path, "rb")), "format": "json"}
        except:
            return {}
        res_json = requests.post(
            "https://sm.ms/api/v2/upload",
            headers={"Authorization": api_key},
            files=data,
        ).text
        return json.loads(res_json)

    def get_path(rt, rel):
        return os.path.abspath(os.path.join(rt, rel))

    def format_markdown(path):
        import re

        rt_path = os.path.dirname(os.path.abspath(path))
        img_set = {}
        with open(path, "r") as fp:
            ct = fp.read()
        aims = re.findall("!\[.*?]\((.*?)\)", ct, re.M) + re.findall(
            '<img.*?src="(.*?)".*?>', ct, re.M
        )
        for aim in aims:
            raw_path = aim
            aim = get_path(rt_path, aim.replace("~", user_root))
            if aim not in img_set:
                res_dict = post_img(aim)
                if not res_dict:
                    res_tb.add_row(os.path.basename(aim), "No File", "")
                    img_set[aim] = False
                else:
                    res_tb.add_row(
                        os.path.basename(aim),
                        res_dict["success"],
                        res_dict["message"]
                        if not res_dict["success"]
                        else res_dict["data"]["url"],
                    )
                    if not res_dict["success"] and res_dict["code"] == "unauthorized":
                        break
                    img_set[aim] = (
                        res_dict["data"]["url"] if res_dict["success"] else False
                    )
            if img_set[aim]:
                ct = ct.replace(raw_path, img_set[aim])
        with open(path, "w") as fp:
            fp.write(ct)
        qs_default_console.print(res_tb, justify="center")

    try:
        is_md = filePath.endswith(".md")
    except IndexError:
        exit("Usage: qs {*.md} | {picture}")
    else:
        if is_md:
            format_markdown(filePath)
        else:
            res = post_img(filePath)
            if not res:
                res_tb.add_row(os.path.basename(filePath), "No File", "")
            else:
                res_tb.add_row(
                    os.path.basename(filePath),
                    res["success"],
                    "" if not res["success"] else res["data"]["url"],
                )
            qs_default_console.print(res_tb, justify="center")


def imgs_in_url(url: str, save: bool = False):
    """
    提取url中的img标签链接

    Extract img tag links from url

    :param url:
    :param save:
    :return:
    """
    from ..NetTools import headers

    html = requests.get(url, headers=headers)
    if html.status_code != requests.codes.ok:
        qs_default_console.log(
            qs_error_string, "Network Error" if user_lang != "zh" else "网络错误"
        )
        return
    import re
    from ..ImageTools.ImagePreview import image_preview

    normal_dl = None
    if save:
        from ..NetTools.NormalDL import normal_dl

    imgs = re.findall('<img.*?src="(.*?)".*?>', html.text)
    a_ls = re.findall('<a.*?href="(.*?)".*?>', html.text)
    for i in a_ls:
        aim = i.lower()
        for j in [".png", ".jpg", "jpeg"]:
            if j in aim:
                imgs.append(i)
                break
    for url in imgs:
        if not url.startswith("http") or url.endswith("svg"):
            continue
        url = url.replace("&#46;", ".")
        qs_default_console.log(
            qs_info_string,
            "Link:" if user_lang != "zh" else "链接:",
            url[:100] + ("" if len(url) <= 100 else "..."),
        )
        if save:
            file_name = normal_dl(url)
        else:
            file_name = url
        image_preview(file_name, True)


def acg2():
    """
    随机获取一张acg图片链接

    Get a random link to an ACG image

    :return: 请求状态, 链接或报错, 宽度, 高度 | status, url or error, width, height
    """
    try:
        res = requests.get("https://api.luvying.com/acgimg?return=json")
    except Exception as e:
        return False, repr(e), None, None
    else:
        import json

        res = json.loads(res.text)
        return (
            res["code"] == "200",
            (res["acgurl"] if res["code"] == "200" else "Error"),
            res["width"],
            res["height"],
        )


def wallhaven(
    set_search_url: str = pre_check("wallhaven_aim_url", ext=False),
    randomOne: bool = False,
):
    """
    获取wallhaven toplist或指定图片列表

    Get wallhaven toplist or specified picture list

    :param set_search_url: 用于搜索的URL
    :param randomOne: 随机抽一张返回
    :return: 包含链接的列表 | [link1, link2, ...]
    """
    from .. import qs_default_console, qs_error_string
    from ..NetTools import headers
    import requests
    import re

    if not set_search_url:
        set_search_url = "https://wallhaven.cc/search?categories=010&purity=011&topRange=1M&sorting=toplist&order=desc"

    urlTemplate = "https://w.wallhaven.cc/full/{}/wallhaven-{}"
    html = requests.get(set_search_url, headers=headers)
    if html.status_code != requests.codes.ok:
        qs_default_console.print(qs_error_string, f"Http Status: {html.status_code}")
        return None
    html = re.findall("<section.*?>(.*?)</section", html.text, re.S)[0]
    lis = re.findall("<li>(.*?)</li", html, re.S)
    res = []
    for i in lis:
        url, size = re.findall(
            '<img.*?data-src="(.*?)".*?<span.*?class="wall-res".*?>(.*?)<', i, re.S
        )[0]
        url = url.split("/")[-2:]
        if '<span class="png">' in i:
            url[-1] = url[-1].replace(".jpg", ".png")
        res.append(
            {
                "url": urlTemplate.format(*url),
                "size": [int(i) for i in re.findall("\d+\.?\d*", size)],
            }
        )
    if randomOne:
        import random

        return [random.choice(res)]
    return res


def lmgtfy(keyword: str):
    """
    让我帮你Google一下

    Let me google that for you

    :param keyword: 关键词
    :return: 目标链接 | http link
    """
    import random
    import base64

    supportLs = ["https://moedog.org/tools/google/?q="]
    return random.choice(supportLs) + base64.b64encode(bytes(keyword, "utf-8")).decode(
        "utf-8"
    )


class Designation2magnet:
    import re

    def __init__(self, description):
        self.rt_url = "https://18mag.net"
        self.cover_url = "https://www5.javmost.com/search/{designation}/"
        self.description = description

    def search_designation(self):
        """
        番号搜索

        :return:
        """
        infos = [
            Designation2magnet.re.findall(
                '<a.*?href="(.*?)".*?>(.*?)<.*?td-size.*?>(.*?)<',
                item,
                Designation2magnet.re.S,
            )
            for item in Designation2magnet.re.findall(
                "<tr>(.*?)</tr>",
                requests.get(self.rt_url + "/search?q={}".format(self.description))
                .text.replace("<b>", "")
                .replace("</b>", ""),
                Designation2magnet.re.S,
            )
        ]
        if [] in infos:
            return [
                (i[0][0], i[0][1].strip(), i[0][2]) for i in infos[: infos.index([])]
            ]
        else:
            return [(i[0][0], i[0][1].strip(), i[0][2]) for i in infos]

    def get_magnet(self, info: str):
        """
        将选定的信息转为磁力链

        :param info:
        :return:
        """
        return (
            "magnet:?xt=urn:btih:"
            + Designation2magnet.re.findall(
                "种子特征码.*?<dd>(.*?)<",
                requests.get(self.rt_url + info).text,
                Designation2magnet.re.S,
            )[0]
        )
