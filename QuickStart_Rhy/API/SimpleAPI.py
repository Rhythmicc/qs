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
    api_key = pre_check('rmbg')
    res = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(filePath, 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': api_key},
    )
    if res.status_code == requests.codes.ok:
        img_name = filePath.split(dir_char)[-1].split('.')[0]
        if dir_char in filePath:
            img_root = dir_char.join(filePath.split(dir_char)[:-1]) + dir_char
        else:
            img_root = ''
        with open(img_root + img_name + '_rmbg.png', 'wb') as imgfile:
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
    from ..TuiTools.Table import qs_default_table

    api_key = pre_check('smms')
    res_tb = qs_default_table(['File', 'Status', 'url'] if user_lang != 'zh' else ['文件', '状态', '链接'])

    def post_img(path: str) -> dict:
        try:
            data = {
                'smfile': (path.split('/')[-1], open(path, 'rb')),
                'format': 'json'
            }
        except:
            return {}
        res_json = requests.post('https://sm.ms/api/v2/upload', headers={'Authorization': api_key}, files=data).text
        return json.loads(res_json)

    def get_path(rt, rel):
        return os.path.abspath(rt + rel)

    def format_markdown(path):
        import re
        _user_path = os.path.expanduser('~')
        rt_path = dir_char.join(os.path.abspath(path).split(dir_char)[:-1]) + dir_char
        img_set = {}
        with open(path, 'r') as fp:
            ct = fp.read()
        aims = re.findall('!\[.*?]\((.*?)\)', ct, re.M) + re.findall('<img.*?src="(.*?)".*?>', ct, re.M)
        for aim in aims:
            raw_path = aim
            aim = aim.replace('~', _user_path)
            aim = aim if aim.startswith(dir_char) else get_path(rt_path, aim)
            if aim not in img_set:
                res_dict = post_img(aim)
                if not res_dict:
                    res_tb.add_row(aim.split(dir_char)[-1], 'No File', '')
                    img_set[aim] = False
                else:
                    res_tb.add_row(
                        aim.split(dir_char)[-1], res_dict['success'],
                        res_dict['message'] if not res_dict['success'] else res_dict['data']['url']
                    )
                    if not res_dict['success'] and res_dict['code'] == 'unauthorized':
                        break
                    img_set[aim] = res_dict['data']['url'] if res_dict['success'] else False
            if img_set[aim]:
                ct = ct.replace(raw_path, img_set[aim])
        with open(path, 'w') as fp:
            fp.write(ct)
        qs_default_console.print(res_tb, justify="center")

    try:
        is_md = filePath.endswith('.md')
    except IndexError:
        exit('Usage: qs {*.md} | {picture}')
    else:
        if is_md:
            format_markdown(filePath)
        else:
            res = post_img(filePath)
            if not res:
                res_tb.add_row(filePath.split(dir_char)[-1], 'No File', '')
            else:
                res_tb.add_row(
                    filePath.split(dir_char)[-1], res['success'], '' if not res['success'] else res['data']['url'])
            qs_default_console.print(res_tb, justify="center")


def pasteme(key: str = '100', password: str = '', mode: str = 'get'):
    """
    利用pasteme实现的信息收发

    Use pasteme to send and receive messages

    :param key: 信息编号
    :param password: 获取信息可能需要的密码
    :param mode: 'get' 或 'post'，get时将信息写入key.*文件中，post将剪切板内容上传至pasteme
    :return: None
    """
    from .. import requirePackage
    pyperclip = requirePackage('pyperclip')
    if mode == 'get':
        if password:
            r = requests.get(f'https://api.pasteme.cn/{key},{password}', params={'json': True})
        else:
            r = requests.get(f'https://api.pasteme.cn/{key}', params={'json': True})
        if r.status_code == requests.codes.ok:
            js = json.loads(r.content)
            if js['status'] == 200:
                try:
                    pyperclip.copy(js['content'])
                except:
                    qs_default_console.log(
                        qs_error_string, 'Sorry, but your system may not be suppported by `pyperclip`'
                        if user_lang != 'zh' else
                        '抱歉，但是“pyperclip”不支持你的系统')
                with open("%s.%s" % (key, js['lang']), 'w') as file:
                    file.write(js['content'])
            else:
                qs_default_console.log(qs_error_string,
                                       'Wrong Password' if password else 'Password is required')
        else:
            qs_default_console.log(qs_error_string, 'Unknown error' if user_lang != 'zh' else '未知错误')
    else:
        try:
            ss = pyperclip.paste()
        except:
            from .. import qs_default_input
            path = qs_default_input.ask(
                'Sorry, but your system is not supported by `pyperclip`\nSo you need input content manually: '
                if user_lang != 'zh' else '抱歉，但是“pyperclip”不支持你的系统\n，所以你需要手动输入内容:')
            with open(path, 'r') as file:
                ss = file.read()
        js = {
            'lang': key if key else 'txt',
            'content': ss
        }
        if password:
            js['password'] = password
        r = requests.post('https://api.pasteme.cn',
                          headers={'Content-Type': 'application/json'},
                          json=js)
        if r.status_code == 201:
            qs_default_console.print(json.loads(r.content))
        else:
            qs_default_console.print(qs_error_string, 'post failed' if user_lang != 'zh' else '发送失败')


def imgs_in_url(url: str, save: bool = False):
    """
    提取url中的img标签链接

    Extract img tag links from url

    :param url:
    :param save:
    :return:
    """
    from .. import headers
    html = requests.get(url, headers=headers)
    if html.status_code != requests.codes.ok:
        qs_default_console.log(qs_error_string, 'Network Error' if user_lang != 'zh' else '网络错误')
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
        for j in ['.png', '.jpg', 'jpeg']:
            if j in aim:
                imgs.append(i)
                break
    for url in imgs:
        if not url.startswith('http') or url.endswith('svg'):
            continue
        url = url.replace('&#46;', '.')
        qs_default_console.log(
            qs_info_string, 'Link:' if user_lang != 'zh' else '链接:', url[:100] + ('' if len(url) <= 100 else '...'))
        if save:
            normal_dl(url)
        if system == 'darwin':
            try:
                image_preview(url, True)
            except Exception as e:
                qs_default_console.log(qs_error_string, repr(e))


def acg2():
    """
    随机获取一张acg图片链接

    Get a random link to an ACG image

    :return: 请求状态, 链接或报错, 宽度, 高度 | status, url or error, width, height
    """
    try:
        res = requests.get('https://api.luvying.com/acgimg?return=json')
    except Exception as e:
        return False, repr(e), None, None
    else:
        import json
        res = json.loads(res.text)
        return res['code'] == '200', (res['acgurl'] if res['code'] == '200' else 'Error'), res['width'], res['height']


def photo():
    """
    随机返回一张写真

    Randomly return a photo

    :return: 请求状态, 图片链接(报错), 文件名 | status, url, file name
    """
    try:
        from ..NetTools import get_fileinfo
        url, name, res = get_fileinfo('https://www.onexiaolaji.cn/RandomPicture/api')
    except Exception as e:
        return False, repr(e), None
    else:
        return res.status_code == requests.codes.ok, url, name


def wallhaven(set_search_url: str = pre_check('wallhaven_aim_url', False), randomOne: bool = False):
    """
    获取wallhaven toplist或指定图片列表

    Get wallhaven toplist or specified picture list

    :param set_search_url: 用于搜索的URL
    :param randomOne: 随机抽一张返回
    :return: 包含链接的列表 | [link1, link2, ...]
    """
    from .. import qs_default_console, qs_error_string
    from . import headers
    import requests
    import re

    if not set_search_url:
        set_search_url = 'https://wallhaven.cc/search?categories=010&purity=011&topRange=1M&sorting=toplist&order=desc'

    urlTemplate = 'https://w.wallhaven.cc/full/{}/wallhaven-{}'
    html = requests.get(set_search_url, headers=headers)
    if html.status_code != requests.codes.ok:
        qs_default_console.print(qs_error_string, f'Http Status: {html.status_code}')
        return None
    html = re.findall('<section.*?>(.*?)</section', html.text, re.S)[0]
    lis = re.findall('<li>(.*?)</li', html, re.S)
    res = []
    for i in lis:
        url, size = re.findall('<img.*?data-src="(.*?)".*?<span.*?class="wall-res".*?>(.*?)<', i, re.S)[0]
        url = url.split('/')[-2:]
        if '<span class="png">' in i:
            url[-1] = url[-1].replace('.jpg', '.png')
        res.append({'url': urlTemplate.format(*url), 'size': [int(i) for i in re.findall('\d+\.?\d*', size)]})
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
    supportLs = [
        'https://moedog.org/tools/google/?q='
    ]
    return random.choice(supportLs) + base64.b64encode(bytes(keyword, 'utf-8')).decode('utf-8')
