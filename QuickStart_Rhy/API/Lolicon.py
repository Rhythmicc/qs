from ..NetTools import headers
from .. import user_lang
from . import pre_check
import requests
import json

lolicon_token = pre_check("lolicon_token", ext=False)


def loli_img(keyword: str = ""):
    try:
        res = requests.get(
            "https://api.lolicon.app/setu/",
            headers=headers,
            params={
                "apikey": lolicon_token if lolicon_token else "",
                "r18": "2",
                "keyword": keyword,
                "num": 1,
                "proxy": "disable",
            },
        )
    except Exception as e:
        return False, repr(e), False
    else:
        if res.status_code != requests.codes.ok:
            return (
                False,
                ("Get Data Failed" if user_lang != "zh" else "获取图源数据失败"),
                False,
            )
        data = json.loads(res.text)
        return data["code"] == 0, data["msg"], data["data"]


def magnet2torrent(hash: str):
    try:
        from ..NetTools import get_fileinfo
        from ..NetTools.NormalDL import normal_dl

        infos = get_fileinfo("https://m2t.lolicon.app/m/" + hash)
        normal_dl(infos[0], set_name=f'{infos[-1].headers["torrent-name"]}.torrent')
        return True, "Success"
    except Exception as e:
        return False, repr(e)
