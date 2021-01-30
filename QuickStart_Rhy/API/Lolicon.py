from .. import headers, user_lang
from . import pre_check
import requests
import json

lolicon_token = pre_check('lolicon_token', False)


def loli_img(keyword: str = ''):
    try:
        res = requests.get(
            'https://api.lolicon.app/setu/', headers=headers,
            params={
                'apikey': lolicon_token if lolicon_token else '',
                'r18': '2',
                'keyword': keyword,
                'num': 1,
                'proxy': 'disable'
            }
        )
    except Exception as e:
        return False, repr(e), False
    else:
        if res.status_code != requests.codes.ok:
            return False, ("Get Data Failed" if user_lang != 'zh' else "获取图源数据失败"), False
        data = json.loads(res.text)
        return data['code'] == 0, data['msg'], data['data']
